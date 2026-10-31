#!/usr/bin/env python3
"""Tests for scripts/readme_metrics.py (README kaizen, 31 October 2026).

Each measure has an exact-value case, and the limits have a case on each side of every boundary, so a
change to a threshold, a comparison or a counting rule fails a test. Fixtures are short Markdown strings.
"""

from __future__ import annotations

import importlib.util
import io
import json
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("readme_metrics", PACKAGE / "scripts" / "readme_metrics.py")
assert SPEC and SPEC.loader
M = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = M
SPEC.loader.exec_module(M)

FENCE = "```"
GOOD = (
    "# Demo\n\nThis tool measures a README. It is small.\n\n"
    "- [One](#one)\n- [Two](#two)\n- [Three](#three)\n- [Four](#four)\n\n"
    f"{FENCE}sh\nrun it\n{FENCE}\n\n## One\n\nShort text here.\n\n## Two\n\nMore short text.\n\n## Three\n\nEnd.\n\n## Four\n\nDone.\n"
)
PASSING = {"toc": 1, "first_cmd": 10, "longest_sec": 100, "long_lines": 0, "max_line": 100, "sent_len": 10.0}


class SyllableTests(unittest.TestCase):
    def test_counts_vowel_groups_and_drops_a_silent_final_e(self) -> None:
        for word, expected in [("cat", 1), ("the", 1), ("table", 2), ("make", 1), ("tree", 1), ("beautiful", 3), ("rhythm", 1)]:
            with self.subTest(word=word):
                self.assertEqual(M.syllables(word), expected)

    def test_a_token_without_letters_has_none(self) -> None:
        self.assertEqual(M.syllables(""), 0)
        self.assertEqual(M.syllables("123"), 0)


class CountTests(unittest.TestCase):
    def test_words_skip_code_fences_and_headings_but_count_bullets_and_tables(self) -> None:
        text = f"# Title words\n\nOne two three.\n\n{FENCE}sh\nignored words here\n{FENCE}\n\n- item four five\n\n| a | b c |\n|---|---|\n"
        self.assertEqual(M.measure_text(text)["words"], 3 + 3 + 3)

    def test_h2_counts_only_level_two_headings_outside_fences(self) -> None:
        text = f"# T\n## One\n### Sub\n{FENCE}\n## fenced\n{FENCE}\n## Two\n#### Deep\n"
        self.assertEqual(M.measure_text(text)["h2"], 2)

    def test_first_cmd_is_the_line_of_the_first_fence_of_any_kind(self) -> None:
        self.assertEqual(M.measure_text(f"a\nb\n{FENCE}text\nx\n{FENCE}\n{FENCE}sh\ny\n{FENCE}\n")["first_cmd"], 3)
        self.assertEqual(M.measure_text(f"a\n   {FENCE}\nx\n   {FENCE}\n")["first_cmd"], 2)

    def test_first_cmd_is_zero_without_a_code_block(self) -> None:
        self.assertEqual(M.measure_text("# T\n\nNo code here.\n")["first_cmd"], 0)

    def test_longest_section_includes_its_h3_content(self) -> None:
        text = "Intro one two.\n## A\nalpha beta gamma delta\n### Sub\nepsilon zeta\n## B\none\n"
        self.assertEqual(M.measure_text(text)["longest_sec"], 6)

    def test_the_text_before_the_first_h2_is_a_section_of_its_own(self) -> None:
        text = "Intro a b c d e f g.\n## A\nx\n"
        self.assertEqual(M.measure_text(text)["longest_sec"], 8)

    def test_a_300_character_line_is_not_long_and_a_301_character_line_is(self) -> None:
        self.assertEqual(M.measure_text("x" * 300 + "\n")["long_lines"], 0)
        self.assertEqual(M.measure_text("x" * 301 + "\n")["long_lines"], 1)

    def test_long_lines_and_max_line_ignore_code_fences_and_include_tables_and_headings(self) -> None:
        text = f"{FENCE}\n{'y' * 900}\n{FENCE}\n| {'t' * 400} |\n## {'h' * 350}\n"
        got = M.measure_text(text)
        self.assertEqual(got["long_lines"], 2)
        self.assertEqual(got["max_line"], 404)  # "| " + 400 + " |"

    def test_bullets_cover_the_four_list_markers_and_indentation(self) -> None:
        text = "- a\n* b\n+ c\n1. d\n2) e\n   - nested\nnot a bullet\n"
        self.assertEqual(M.measure_text(text)["bullets"], 6)

    def test_table_rows_include_the_separator_row(self) -> None:
        self.assertEqual(M.measure_text("| a | b |\n|---|---|\n| c | d |\n")["tables"], 3)

    def test_windows_line_endings_give_the_same_measures(self) -> None:
        self.assertEqual(M.measure_text(GOOD.replace("\n", "\r\n")), M.measure_text(GOOD))


class ContentsListTests(unittest.TestCase):
    @staticmethod
    def doc(links: int, before_third_h2: bool = True) -> str:
        link_block = "\n".join(f"[l{i}](#l{i})" for i in range(links)) + "\n"
        head, tail = ("# T\n\n" + link_block, "") if before_third_h2 else ("# T\n\n", link_block)
        return f"{head}\n## A\n\nx\n\n## B\n\ny\n\n## C\n\nz\n\n{tail}"

    def test_four_in_page_links_before_the_third_h2_make_a_contents_list(self) -> None:
        self.assertEqual(M.measure_text(self.doc(4))["toc"], 1)

    def test_three_links_are_not_enough(self) -> None:
        self.assertEqual(M.measure_text(self.doc(3))["toc"], 0)

    def test_links_after_the_third_h2_do_not_count(self) -> None:
        self.assertEqual(M.measure_text(self.doc(6, before_third_h2=False))["toc"], 0)

    def test_a_short_document_is_read_to_the_end(self) -> None:
        text = "# T\n\n## A\n\n" + " ".join(f"[l{i}](#l{i})" for i in range(4)) + "\n"
        self.assertEqual(M.measure_text(text)["toc"], 1)

    def test_links_between_the_second_and_third_h2_still_count(self) -> None:
        links = " ".join(f"[l{i}](#l{i})" for i in range(4))
        text = f"# T\n\n## A\n\nx\n\n## B\n\n{links}\n\n## C\n\nz\n"
        self.assertEqual(M.measure_text(text)["toc"], 1)

    def test_h2_lines_inside_a_code_fence_do_not_move_the_cut(self) -> None:
        links = " ".join(f"[l{i}](#l{i})" for i in range(4))
        text = f"# T\n\n{FENCE}\n## c1\n## c2\n## c3\n{FENCE}\n{links}\n\n## A\n## B\n## C\n"
        self.assertEqual(M.measure_text(text)["toc"], 1)


class ProseTests(unittest.TestCase):
    def test_mean_sentence_length_is_words_over_sentences(self) -> None:
        self.assertEqual(M.measure_text("One two three four. Five six seven eight nine ten.\n")["sent_len"], 5.0)

    def test_a_fragment_adds_its_words_but_no_sentence(self) -> None:
        # Kept as measured in the baseline: the numerator holds every word, the denominator only real sentences.
        self.assertEqual(M.measure_text("Hello. One two three four.\n")["sent_len"], 5.0)

    def test_a_sentence_may_run_over_several_lines(self) -> None:
        self.assertEqual(M.measure_text("One two three\nfour five six.\n")["sent_len"], 6.0)

    def test_bullets_and_table_cells_are_not_prose(self) -> None:
        base = M.measure_text("One two three four.\n")
        padded = M.measure_text("One two three four.\n\n- " + "word " * 80 + "ends here.\n\n| " + "cell " * 50 + " |\n")
        self.assertEqual((padded["sent_len"], padded["fre"]), (base["sent_len"], base["fre"]))

    def test_inline_code_is_removed_and_a_link_keeps_its_text(self) -> None:
        got = M.measure_text("See `a very long code span here` and [link text](https://example.org/z) now.\n")
        self.assertEqual(got["sent_len"], 5.0)

    def test_lines_that_start_with_a_bracket_tag_or_image_are_not_prose(self) -> None:
        got = M.measure_text("[Link](x.md) starts this line here.\n<p>Html starts this line here.</p>\n![img](a.png) caption words here.\n")
        self.assertEqual((got["sent_len"], got["fre"]), (0, 0))

    def test_reading_ease_of_a_known_sentence(self) -> None:
        # 6 words, 6 syllables: 206.835 - 1.015 * 6 - 84.6 * 1 = 116.145
        self.assertEqual(M.measure_text("The cat sat on the mat.\n")["fre"], 116)

    def test_longer_words_lower_the_reading_ease(self) -> None:
        plain = M.measure_text("The cat sat on the mat.\n")["fre"]
        heavy = M.measure_text("Organisational interoperability necessitates considerable standardisation.\n")["fre"]
        self.assertLess(heavy, plain - 100)

    def test_no_prose_gives_zero_for_both_prose_measures(self) -> None:
        got = M.measure_text("# T\n\n- only a bullet here\n")
        self.assertEqual((got["sent_len"], got["fre"]), (0, 0))


class LimitTests(unittest.TestCase):
    def misses(self, **change: float) -> list[str]:
        return M.limit_misses({**PASSING, **change})

    def test_a_readme_inside_every_limit_has_no_misses(self) -> None:
        self.assertEqual(self.misses(), [])

    def test_each_limit_is_inclusive_at_its_boundary_and_fails_one_step_beyond(self) -> None:
        cases = [
            ("toc", 1, 0), ("first_cmd", 40, 41), ("first_cmd", 1, 0), ("longest_sec", 1500, 1501),
            ("long_lines", 20, 21), ("max_line", 700, 701), ("sent_len", 16.5, 16.6),
        ]
        for name, inside, outside in cases:
            with self.subTest(name=name, inside=inside):
                self.assertEqual(self.misses(**{name: inside}), [])
            with self.subTest(name=name, outside=outside):
                got = self.misses(**{name: outside})
                self.assertEqual(len(got), 1)
                self.assertTrue(got[0].startswith(name + " is"), got)

    def test_the_limits_are_the_documented_set(self) -> None:
        self.assertEqual(set(M.LIMITS), {"toc", "first_cmd", "longest_sec", "long_lines", "max_line", "sent_len"})


class CommandLineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="readme-metrics-")).resolve()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def put(self, folder: str, text: str) -> Path:
        path = self.tmp / folder / "README.md"
        path.parent.mkdir(parents=True)
        path.write_text(text, encoding="utf-8")
        return path

    def run_cli(self, *args: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = M.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def test_a_readme_inside_the_limits_passes_check(self) -> None:
        code, out, _ = self.run_cli("--check", str(self.put("good", GOOD)))
        self.assertEqual(code, 0, out)
        self.assertIn("all met", out)

    def test_a_readme_outside_the_limits_fails_check_and_names_each_miss(self) -> None:
        bad = "# Bad\n\n" + "word " * 200 + "\n"
        code, out, _ = self.run_cli("--check", str(self.put("bad", bad)))
        self.assertEqual(code, 1)
        for name in ("toc", "first_cmd", "max_line", "sent_len"):
            self.assertIn(f"LIMIT bad: {name} is", out)

    def test_without_check_a_missed_limit_still_exits_zero(self) -> None:
        bad = "# Bad\n\n" + "word " * 200 + "\n"
        code, out, _ = self.run_cli(str(self.put("bad", bad)))
        self.assertEqual(code, 0)
        self.assertNotIn("LIMIT", out)

    def test_json_prints_every_measure_for_each_file(self) -> None:
        code, out, _ = self.run_cli("--json", str(self.put("good", GOOD)))
        self.assertEqual(code, 0)
        row = json.loads(out.strip())
        self.assertEqual(row["file"], "good")
        self.assertEqual(set(row) - {"file"}, set(M.MEASURES))
        self.assertEqual(row["h2"], 4)

    def test_the_table_is_labelled_by_the_folder_that_holds_each_file(self) -> None:
        code, out, _ = self.run_cli(str(self.put("alpha", GOOD)), str(self.put("beta", GOOD)))
        self.assertEqual(code, 0)
        labels = [line.split()[0] for line in out.splitlines()[1:]]
        self.assertEqual(labels, ["alpha", "beta"])
        self.assertEqual(out.splitlines()[0].split()[1:], list(M.MEASURES))

    def test_an_unreadable_file_is_not_assessed_and_the_others_are_still_measured(self) -> None:
        code, out, err = self.run_cli(str(self.tmp / "missing" / "README.md"), str(self.put("good", GOOD)))
        self.assertEqual(code, 3)
        self.assertIn("NOT_ASSESSED README.md", err)
        self.assertNotIn(str(self.tmp), err)
        self.assertIn("good", out)

    def test_an_unreadable_file_is_not_a_pass_under_check(self) -> None:
        code, _, _ = self.run_cli("--check", str(self.tmp / "missing" / "README.md"))
        self.assertEqual(code, 3)

    def test_bytes_that_are_not_utf8_are_replaced_not_fatal(self) -> None:
        path = self.tmp / "odd" / "README.md"
        path.parent.mkdir(parents=True)
        path.write_bytes(GOOD.encode("utf-8") + b"\nCaf\xe9 \xff done here.\n")
        code, out, _ = self.run_cli(str(path))
        self.assertEqual(code, 0, out)


if __name__ == "__main__":
    unittest.main()
