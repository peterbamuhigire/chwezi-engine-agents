import sys
import tempfile
import unittest
from unittest.mock import Mock, patch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from check_cross_engine_negatives import cross_cases, evaluate, main
from lexical_routing import LexicalIndex, SkillDoc, discover_engine


class CrossEngineNegativeTests(unittest.TestCase):
    def test_both_native_fixture_shapes_preserve_all_cross_engine_cases(self):
        dev = {"fixtures": [{"expect": "build", "negatives": [
            {"task": "Write requirements", "owner": "srs/spec"},
            {"task": "Build locally", "owner": "other"}]}]}
        research = {"negatives": [{"id": "n1", "skill": "research", "prompt": "Write requirements", "owner": "srs/spec"}]}
        cases, skipped = cross_cases("dev", dev)
        self.assertEqual(len(cases), 1)
        self.assertEqual(skipped, 1)
        self.assertEqual(cross_cases("research", research)[0][0]["id"], "n1")
        self.assertEqual(cases[0]["skill"], "dev/build")

    def test_owner_win_competitor_win_tie_and_missing_are_distinct(self):
        index = LexicalIndex([SkillDoc("a", "spec", "requirements approval specification", "a"),
                              SkillDoc("b", "build", "code implementation compilation", "b")])
        case = {"id": "case", "skill": "b/build", "owner": "a/spec", "prompt": "requirements approval"}
        self.assertEqual(evaluate(case, index)["status"], "PASS")
        self.assertEqual(evaluate({**case, "prompt": "code implementation"}, index)["status"], "FAIL")
        self.assertEqual(evaluate({**case, "prompt": "the and"}, index)["status"], "FAIL")
        self.assertEqual(evaluate({**case, "owner": "missing/spec"}, index)["status"], "NOT_ASSESSED")

    def test_malformed_cross_case_fails(self):
        with self.assertRaises(ValueError):
            cross_cases("a", {"negatives": [{"owner": "b/skill", "skill": "test"}]})

    def test_valid_case_cannot_hide_missing_or_malformed_owner(self):
        for owner in (None, "", 3):
            with self.subTest(owner=owner), self.assertRaises(ValueError):
                cross_cases("a", {"negatives": [
                    {"owner": "b/skill", "skill": "test", "prompt": "Valid case"},
                    {"owner": owner, "skill": "test", "prompt": "Unassigned case"}]})

    def test_resolved_private_root_is_rejected_before_discovery(self):
        root = Mock()
        root.resolve.return_value = Path("/private/political-essay-skills")
        with patch("sys.argv", ["check", "--workspace-root", ".", "--fixture", "a=test.json"]), patch(
            "check_cross_engine_negatives.load_catalog_engines", return_value=[("a", root)]
        ), patch("check_cross_engine_negatives.discover_engine") as discover, patch("builtins.print"):
            self.assertEqual(main(), 2)
            discover.assert_not_called()

    def test_private_skill_file_link_is_rejected_before_read(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            public = base / "public"
            private = base / "political-essay-skills"
            public.mkdir()
            private.mkdir()
            target = private / "SKILL.md"
            target.write_text("private fixture", encoding="utf-8")
            try:
                (public / "SKILL.md").symlink_to(target)
            except OSError as exc:
                self.skipTest(f"File symlink unavailable: {exc}")
            with patch("lexical_routing.read_frontmatter") as read:
                docs, issues = discover_engine("public", public)
                self.assertEqual(docs, [])
                self.assertEqual(len(issues), 1)
                read.assert_not_called()


if __name__ == "__main__":
    unittest.main()
