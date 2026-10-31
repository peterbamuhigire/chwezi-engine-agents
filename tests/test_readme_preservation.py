#!/usr/bin/env python3
"""Seeded-failure tests for scripts/check_readme_preservation.py (README kaizen, 31 October 2026).

Every test builds a small temporary git repository: an old README on ``main`` and a new one on
``change``. The cases that must fail (a lost command, a lost link, a broken anchor, a moved page whose
links do not resolve) sit next to the cases that must pass (a table moved to a docs page, a renamed
heading that keeps its anchor). Nothing here touches the package's own repository.
"""

from __future__ import annotations

import importlib.util
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_readme_preservation", PACKAGE / "scripts" / "check_readme_preservation.py")
assert SPEC and SPEC.loader
P = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = P
SPEC.loader.exec_module(P)

FENCE = "```"
# The check scans every tracked text file for the README file name followed by a hash and an anchor, so the
# fixtures below build such links from pieces and this file never contains one.
README_FILE = "README" + ".md"


def link(prefix: str, anchor: str, text: str = "x") -> str:
    """A Markdown link to ANCHOR in the README file reached through PREFIX (a folder path or empty)."""
    return f"[{text}]({prefix}{README_FILE}#{anchor})"


OLD_README = f"""# Demo

Intro with [skill a](skills/a/SKILL.md) and [the site](https://example.org/x).

## Install

{FENCE}sh
# install the dependencies
python3 scripts/run.py --flag
npm ci
{FENCE}

Run `git status --short` often.

## Details

See the [guide](docs/guide.md).
"""

Files = dict  # path -> text, bytes, or None (delete in the new revision)


def git(root: Path, *args: str) -> str:
    done = subprocess.run(
        ["git", "-c", "user.name=Tester", "-c", "user.email=tester@example.invalid", "-c", "commit.gpgsign=false", *args],
        cwd=root, check=True, capture_output=True,
    )
    return done.stdout.decode("utf-8", errors="replace").strip()


class PreservationCase(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="readme-preserve-")).resolve()
        self.repo = self.tmp / "demo"
        self.repo.mkdir()
        git(self.repo, "init", "-q")
        git(self.repo, "symbolic-ref", "HEAD", "refs/heads/main")

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, files: Files) -> None:
        for name, content in files.items():
            path = self.repo / name
            if content is None:
                path.unlink()
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content if isinstance(content, bytes) else content.encode("utf-8"))

    def build(self, new: Files, old: Files | None = None) -> None:
        """Commit OLD on main (the old README by default), then NEW on the branch ``change``."""
        self.write(old if old is not None else {"README.md": OLD_README})
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "-m", "old")
        git(self.repo, "checkout", "-q", "-b", "change")
        self.write(new)
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-q", "--allow-empty", "-m", "new")

    def run_check(self, *extra: str, new: str = "change") -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = P.main([str(self.repo), "main", new, *extra])
        return code, out.getvalue(), err.getvalue()

    def readme(self, old: str, new: str) -> str:
        """The old README with one text replacement applied; the fixture must contain the text."""
        self.assertIn(old, OLD_README, "fixture drift: the replacement target is not in the old README")
        return OLD_README.replace(old, new)


class LinkTests(PreservationCase):
    def test_an_unchanged_readme_is_ok(self) -> None:
        self.build({})
        code, out, _ = self.run_check()
        self.assertEqual(code, 0, out)
        self.assertIn("RESULT: OK", out)

    def test_a_lost_relative_link_fails_and_is_named(self) -> None:
        self.build({"README.md": self.readme("Intro with [skill a](skills/a/SKILL.md) and", "Intro with")})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("LOST link target: skills/a/SKILL.md", out)

    def test_a_table_moved_to_a_docs_page_is_not_flagged(self) -> None:
        new_readme = self.readme("[skill a](skills/a/SKILL.md) and [the site](https://example.org/x)", "[the catalogue](docs/catalogue.md)")
        page = "# Catalogue\n\n| Skill |\n|---|\n| [a](../skills/a/SKILL.md) |\n\nSource: https://example.org/x\n"
        self.build({"README.md": new_readme, "docs/catalogue.md": page})
        code, out, _ = self.run_check()
        self.assertEqual(code, 0, out)
        self.assertIn("moved to docs 2; LOST 0", out)

    def test_a_page_two_folders_deep_resolves_its_own_parents(self) -> None:
        new_readme = self.readme("[skill a](skills/a/SKILL.md)", "[catalogue](docs/ref/catalogue.md)")
        page = "# Catalogue\n\n[a](../../skills/a/SKILL.md)\n"
        self.build({"README.md": new_readme, "docs/ref/catalogue.md": page})
        code, out, _ = self.run_check()
        self.assertEqual(code, 0, out)

    def test_a_moved_link_that_does_not_resolve_to_the_same_file_is_lost(self) -> None:
        # In docs/catalogue.md the target skills/a/SKILL.md means docs/skills/a/SKILL.md, not the README's file.
        new_readme = self.readme("[skill a](skills/a/SKILL.md)", "[catalogue](docs/catalogue.md)")
        self.build({"README.md": new_readme, "docs/catalogue.md": "# Catalogue\n\n[a](skills/a/SKILL.md)\n"})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("LOST link target: skills/a/SKILL.md", out)

    def test_a_link_dropped_while_an_unchanged_page_holds_it_is_still_lost(self) -> None:
        old = {"README.md": OLD_README, "docs/catalogue.md": "# Catalogue\n\n[a](../skills/a/SKILL.md)\n"}
        self.build({"README.md": self.readme("[skill a](skills/a/SKILL.md)", "skill a")}, old=old)
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("LOST link target: skills/a/SKILL.md", out)

    def test_a_lost_url_fails_and_a_moved_url_does_not(self) -> None:
        dropped = self.readme(" and [the site](https://example.org/x)", "")
        self.build({"README.md": dropped})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("LOST link target: https://example.org/x", out)

    def test_a_url_moved_to_a_changed_docs_page_is_not_lost(self) -> None:
        dropped = self.readme(" and [the site](https://example.org/x)", "")
        self.build({"README.md": dropped, "docs/sources.md": "# Sources\n\n- https://example.org/x\n"})
        code, out, _ = self.run_check()
        self.assertEqual(code, 0, out)

    def test_a_fragment_does_not_change_the_target(self) -> None:
        self.build({"README.md": self.readme("(docs/guide.md)", "(docs/guide.md#top)")})
        self.assertEqual(self.run_check()[0], 0)

    def test_dot_slash_and_trailing_slash_are_the_same_target(self) -> None:
        old = {"README.md": OLD_README + "\n[one](./docs/one.md) and [two](docs/adapters/)\n"}
        new = {"README.md": OLD_README + "\n[one](docs/one.md) and [two](docs/adapters)\n"}
        self.build(new, old=old)
        code, out, _ = self.run_check()
        self.assertEqual(code, 0, out)

    def test_a_lost_reference_style_link_fails(self) -> None:
        old = {"README.md": OLD_README + "\nSee [the spec][spec].\n\n[spec]: docs/spec.md\n"}
        new = {"README.md": OLD_README + "\nSee the spec.\n"}
        self.build(new, old=old)
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("LOST link target: docs/spec.md", out)

    def test_a_footnote_definition_is_not_a_link(self) -> None:
        old = {"README.md": OLD_README + "\nA claim.[^note]\n\n[^note]: Detail text here.\n"}
        new = {"README.md": OLD_README + "\nA claim.\n"}
        self.build(new, old=old)
        self.assertEqual(self.run_check()[0], 0)

    def test_relative_links_on_a_moved_page_resolve_from_that_page(self) -> None:
        old = {"README.md": OLD_README + "\n[tour](docs/tours/a.md)\n"}
        new = {"README.md": OLD_README + "\n[tours](docs/index.md)\n", "docs/index.md": "# Index\n\n[tour](tours/a.md)\n"}
        self.build(new, old=old)
        code, out, _ = self.run_check()
        self.assertEqual(code, 0, out)


class CommandTests(PreservationCase):
    def test_a_lost_fenced_command_fails_and_is_named(self) -> None:
        self.build({"README.md": self.readme("npm ci\n", "")})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("LOST command: npm ci", out)

    def test_a_command_moved_to_a_changed_docs_page_is_not_lost(self) -> None:
        new_readme = self.readme("npm ci\n", "")
        self.build({"README.md": new_readme, "docs/setup.md": f"# Setup\n\n{FENCE}sh\nnpm ci\n{FENCE}\n"})
        code, out, _ = self.run_check()
        self.assertEqual(code, 0, out)
        self.assertIn("moved to docs 1; LOST 0", out)

    def test_a_removed_comment_line_in_a_fence_is_not_a_lost_command(self) -> None:
        self.build({"README.md": self.readme("# install the dependencies\n", "")})
        self.assertEqual(self.run_check()[0], 0)

    def test_a_lost_inline_command_fails(self) -> None:
        self.build({"README.md": self.readme("Run `git status --short` often.", "Run it often.")})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("LOST command: git status --short", out)

    def test_inline_code_that_is_not_a_command_is_ignored(self) -> None:
        old = {"README.md": OLD_README + "\nSee `docs/guide.md` and `python3` and `some words in code`.\n"}
        self.build({"README.md": OLD_README}, old=old)
        self.assertEqual(self.run_check()[0], 0)

    def test_white_space_inside_a_command_does_not_matter(self) -> None:
        self.build({"README.md": self.readme("npm ci", "npm    ci")})
        self.assertEqual(self.run_check()[0], 0)

    def test_python_replaced_by_python3_is_reported_as_lost(self) -> None:
        # A deliberate replacement is still reported; the record must explain it.
        self.build({"README.md": self.readme("python3 scripts/run.py", "python scripts/run.py")})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("LOST command: python3 scripts/run.py --flag", out)

    def test_an_indented_fenced_command_is_read(self) -> None:
        old = {"README.md": OLD_README + f"\n1. Do it:\n\n   {FENCE}sh\n   bash scripts/do-it.sh\n   {FENCE}\n"}
        self.build({"README.md": OLD_README}, old=old)
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("LOST command: bash scripts/do-it.sh", out)


class AnchorTests(PreservationCase):
    def test_a_broken_in_page_link_fails(self) -> None:
        self.build({"README.md": OLD_README + "\nJump to [nowhere](#no-such-heading).\n"})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("BROKEN in-page link #no-such-heading", out)

    def test_a_valid_in_page_link_passes(self) -> None:
        self.build({"README.md": OLD_README + "\nJump to [install](#install).\n"})
        self.assertEqual(self.run_check()[0], 0)

    def test_a_heading_linked_from_a_docs_page_must_survive(self) -> None:
        docs = {"README.md": OLD_README, "docs/index.md": f"See the {link('../', 'details', 'details')}.\n"}
        self.build({"README.md": self.readme("## Details", "## More")}, old=docs)
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("BROKEN anchor #details linked from ['docs/index.md']", out)

    def test_a_link_added_by_the_branch_to_a_missing_heading_fails(self) -> None:
        self.build({"docs/index.md": f"See the {link('../', 'no-such-part', 'part')}.\n"})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("BROKEN anchor #no-such-part linked from ['docs/index.md']", out)

    def test_a_link_removed_together_with_its_heading_passes(self) -> None:
        old = {"README.md": OLD_README, "docs/index.md": f"See the {link('../', 'details', 'details')}.\n"}
        self.build({"README.md": self.readme("## Details", "## More"), "docs/index.md": "No link now.\n"}, old=old)
        code, out, _ = self.run_check()
        self.assertEqual(code, 0, out)

    def test_a_renamed_heading_that_keeps_its_anchor_passes(self) -> None:
        docs = {"README.md": OLD_README, "docs/index.md": f"See the {link('../', 'details', 'details')}.\n"}
        self.build({"README.md": self.readme("## Details", "## `Details`")}, old=docs)
        self.assertEqual(self.run_check()[0], 0)

    def test_the_link_is_resolved_against_the_folder_of_the_linking_file(self) -> None:
        # docs/adapters/README.md is another README: its anchors are not this README's anchors.
        old = {"README.md": OLD_README, "docs/index.md": link("adapters/", "gone") + "\n", "docs/adapters/README.md": "# A\n"}
        self.build({"README.md": OLD_README}, old=old)
        code, out, _ = self.run_check()
        self.assertEqual(code, 0, out)
        self.assertIn("anchors: 0 README anchor links", out)

    def test_a_link_two_folders_up_from_a_nested_page_reaches_the_readme(self) -> None:
        old = {"README.md": OLD_README, "docs/deep/page.md": link("../../", "gone") + "\n"}
        self.build({"README.md": OLD_README}, old=old)
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("BROKEN anchor #gone linked from ['docs/deep/page.md']", out)

    def test_every_linking_file_is_read_not_only_the_first(self) -> None:
        old = {
            "README.md": OLD_README,
            "docs/a.md": link("../", "gone-a") + "\n",
            "docs/b.md": link("../", "gone-b") + "\n",
            "scripts/c.py": f"# {README_FILE}#gone-c\n",
        }
        self.build({"README.md": OLD_README}, old=old)
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        for anchor, source in (("gone-a", "docs/a.md"), ("gone-b", "docs/b.md"), ("gone-c", "scripts/c.py")):
            self.assertIn(f"BROKEN anchor #{anchor} linked from ['{source}']", out)

    def test_a_script_that_names_a_missing_anchor_fails(self) -> None:
        old = {"README.md": OLD_README, "scripts/tool.py": f"# see {README_FILE}#gone for the table\n"}
        self.build({"README.md": OLD_README}, old=old)
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("BROKEN anchor #gone linked from ['scripts/tool.py']", out)

    def test_a_script_that_names_an_existing_anchor_passes(self) -> None:
        old = {"README.md": OLD_README, "scripts/tool.py": f"# see {README_FILE}#details for the table\n"}
        self.build({"README.md": OLD_README}, old=old)
        self.assertEqual(self.run_check()[0], 0)

    def test_a_link_shown_in_inline_code_or_a_code_fence_is_an_example_not_a_link(self) -> None:
        example = link("../", "gone")
        page = f"Write it as `{example}`.\n\n{FENCE}md\n{example}\n{FENCE}\n"
        self.build({"README.md": OLD_README}, old={"README.md": OLD_README, "docs/howto.md": page})
        code, out, _ = self.run_check()
        self.assertEqual(code, 0, out)
        self.assertIn("anchors: 0 README anchor links", out)

    def test_a_real_link_next_to_a_code_example_still_counts(self) -> None:
        example = link("../", "example-only")
        page = f"Write it as `{example}` or see {link('../', 'gone')}.\n"
        self.build({"README.md": OLD_README}, old={"README.md": OLD_README, "docs/howto.md": page})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("BROKEN anchor #gone linked from ['docs/howto.md']", out)
        self.assertNotIn("#example-only", out)

    def test_a_plain_text_mention_in_markdown_is_not_a_link(self) -> None:
        old = {"README.md": OLD_README, "docs/note.md": f"The anchor `{README_FILE}#gone` is an example.\n"}
        self.build({"README.md": OLD_README}, old=old)
        self.assertEqual(self.run_check()[0], 0)

    def test_repeated_headings_get_numbered_anchors(self) -> None:
        readme = OLD_README + "\n## Install\n\nSecond.\n\n[a](#install-1) [b](#install-2)\n"
        self.build({"README.md": readme}, old={"README.md": OLD_README})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("BROKEN in-page link #install-2", out)
        self.assertNotIn("BROKEN in-page link #install-1", out)

    def test_a_heading_inside_a_code_fence_is_not_an_anchor(self) -> None:
        readme = OLD_README + f"\n{FENCE}md\n## Ghost\n{FENCE}\n\n[g](#ghost)\n"
        self.build({"README.md": readme})
        code, out, _ = self.run_check()
        self.assertEqual(code, 1)
        self.assertIn("BROKEN in-page link #ghost", out)

    def test_punctuation_and_link_text_in_headings_follow_the_github_rule(self) -> None:
        readme = OLD_README + "\n## Tools & scripts (v2)\n\n## [Linked](x.md) title\n\n[a](#tools--scripts-v2) [b](#linked-title)\n"
        self.build({"README.md": readme})
        code, out, _ = self.run_check()
        self.assertEqual(code, 0, out)

    def test_a_removed_heading_nobody_links_is_a_note_not_a_failure(self) -> None:
        self.build({"README.md": self.readme("## Details\n\nSee the [guide](docs/guide.md).\n", "See the [guide](docs/guide.md).\n")})
        code, out, _ = self.run_check()
        self.assertEqual(code, 0, out)
        self.assertIn("note: 1 heading anchor(s) of the old README are gone", out)
        self.assertIn("#details", out)

    def test_an_abbreviated_commit_hash_works_as_a_revision(self) -> None:
        docs = {"README.md": OLD_README, "docs/index.md": link("../", "gone") + "\n"}
        self.build({"README.md": OLD_README}, old=docs)
        short = git(self.repo, "rev-parse", "--short", "change")
        code, out, _ = self.run_check(new=short)
        self.assertEqual(code, 1)
        self.assertIn("BROKEN anchor #gone", out)


class RunTests(PreservationCase):
    def test_the_same_revision_twice_still_checks_the_anchors(self) -> None:
        self.build({"README.md": OLD_README + "\n[x](#nowhere)\n"})
        out, err = io.StringIO(), io.StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = P.main([str(self.repo), "change", "change"])
        self.assertEqual(code, 1)
        self.assertIn("BROKEN in-page link #nowhere", out.getvalue())

    def test_an_unknown_revision_is_not_assessed(self) -> None:
        self.build({})
        code, out, err = self.run_check(new="no-such-branch")
        self.assertEqual(code, 3)
        self.assertEqual(out, "")
        self.assertIn("NOT_ASSESSED", err)

    def test_a_folder_that_is_not_a_repository_is_not_assessed(self) -> None:
        plain = self.tmp / "plain"
        plain.mkdir()
        err = io.StringIO()
        with redirect_stdout(io.StringIO()), redirect_stderr(err):
            code = P.main([str(plain), "main", "change"])
        self.assertEqual(code, 3)
        self.assertIn("not a git repository", err.getvalue())

    def test_a_missing_readme_at_a_revision_is_not_assessed(self) -> None:
        self.build({"README.md": None})
        code, _, err = self.run_check()
        self.assertEqual(code, 3)
        self.assertIn("does not exist at 'change'", err)

    def test_bytes_that_are_not_utf8_do_not_crash_the_check(self) -> None:
        old = {"README.md": OLD_README.encode("utf-8") + b"\nCaf\xe9 \xff text.\n"}
        self.build({"README.md": OLD_README.encode("utf-8") + b"\nCaf\xe9 \xff text.\n"}, old=old)
        code, out, _ = self.run_check()
        self.assertEqual(code, 0, out)

    def test_verbose_lists_what_moved_and_the_default_does_not(self) -> None:
        new_readme = self.readme("npm ci\n", "").replace("[skill a](skills/a/SKILL.md)", "[catalogue](docs/catalogue.md)")
        page = f"# Catalogue\n\n[a](../skills/a/SKILL.md)\n\n{FENCE}sh\nnpm ci\n{FENCE}\n"
        self.build({"README.md": new_readme, "docs/catalogue.md": page})
        _, quiet, _ = self.run_check()
        _, loud, _ = self.run_check("--verbose")
        self.assertNotIn("moved link target", quiet)
        self.assertIn("moved link target: skills/a/SKILL.md", loud)
        self.assertIn("moved command: npm ci", loud)

    def test_output_never_names_the_repository_path(self) -> None:
        self.build({"README.md": self.readme("npm ci\n", "") + "\n[x](#nowhere)\n"})
        code, out, err = self.run_check()
        self.assertEqual(code, 1)
        self.assertNotIn(str(self.tmp), out + err)

    def test_the_readme_path_can_be_another_file(self) -> None:
        old = {"README.md": "# Root\n", "docs/README.md": "# Docs\n\n## Part\n"}
        new = {"docs/README.md": "# Docs\n\n## Other\n", "docs/link.md": link("", "part", "p") + "\n"}
        self.build(new, old=old)
        code, out, _ = self.run_check("--readme", "docs/README.md")
        self.assertEqual(code, 1)
        self.assertIn("BROKEN anchor #part linked from ['docs/link.md']", out)


class UnitTests(unittest.TestCase):
    def test_heading_slugs_match_the_github_rule(self) -> None:
        text = "# A\n\n## What the October 2026 kaizen improved\n\n## Q&A: why?\n\n## Dup\n\n## Dup\n\n## Dup\n"
        self.assertEqual(
            P.heading_slugs(text),
            {"a", "what-the-october-2026-kaizen-improved", "qa-why", "dup", "dup-1", "dup-2"},
        )

    def test_link_targets_are_resolved_against_the_holder_folder(self) -> None:
        text = "[a](../x/y.md#z) [b](https://example.org/p) [c](#top) [d](mailto:a@example.org) [e](/abs/path)"
        self.assertEqual(P.link_targets(text, "docs/sub"), {"docs/x/y.md", "https://example.org/p", "/abs/path"})
        self.assertEqual(P.link_targets(text, "docs"), {"x/y.md", "https://example.org/p", "/abs/path"})

    def test_commands_reads_fences_and_command_like_inline_code(self) -> None:
        text = f"{FENCE}sh\n# comment\n// other comment\n\n  sh a.sh  --x\n{FENCE}\n`node -v` `node` `plain words` `./run.sh go`\n"
        self.assertEqual(P.commands(text), {"sh a.sh --x", "node -v", "./run.sh go"})


if __name__ == "__main__":
    unittest.main()
