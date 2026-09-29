"""Pass and seeded-failure checks for scripts/validate-rule-markers.py (M10-04-T13)."""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-rule-markers.py"
DESIGN_DOC = ROOT.parent / "design-system-skills" / "doctrine" / "references" / "ai-slop-banned-fonts.md"

MARKDOWN = """# Fixture
<!-- rule:font.ban.hard.inter -->
- **Inter** - banned.
<!-- rule:font.ban.secondary.poppins -->
- **Poppins** - banned.
"""
SIDECAR = {"hardBan": [{"family": "Inter"}], "secondaryBan": [{"family": "Poppins"}]}


class RuleMarkerValidatorTests(unittest.TestCase):
    def run_on(self, markdown: str, sidecar: dict) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            doc = Path(tmp) / "fonts.md"
            doc.write_text(markdown, encoding="utf-8")
            doc.with_suffix(".json").write_text(json.dumps(sidecar), encoding="utf-8")
            return subprocess.run([sys.executable, "-X", "utf8", str(VALIDATOR), str(doc)],
                                  capture_output=True, text=True, check=False)

    def test_clean_fixture_passes(self):
        result = self.run_on(MARKDOWN, SIDECAR)
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_seeded_duplicate_id_fails(self):
        doubled = MARKDOWN + "<!-- rule:font.ban.hard.inter -->\n- **Inter** again.\n"
        result = self.run_on(doubled, SIDECAR)
        self.assertEqual(result.returncode, 1)
        self.assertIn("duplicate marker ID", result.stdout)

    def test_sidecar_family_without_marker_fails(self):
        sidecar = {**SIDECAR, "hardBan": [{"family": "Inter"}, {"family": "Geist"}]}
        result = self.run_on(MARKDOWN, sidecar)
        self.assertEqual(result.returncode, 1)
        self.assertIn("'Geist' has no marker", result.stdout)

    def test_marker_without_sidecar_entry_fails(self):
        extra = MARKDOWN + "<!-- rule:font.ban.hard.comic-sans -->\n- **Comic Sans**.\n"
        result = self.run_on(extra, SIDECAR)
        self.assertEqual(result.returncode, 1)
        self.assertIn("does not resolve", result.stdout)

    def test_bad_id_format_fails(self):
        result = self.run_on(MARKDOWN.replace("font.ban.secondary.poppins", "Font_Poppins"), SIDECAR)
        self.assertEqual(result.returncode, 1)

    @unittest.skipUnless(DESIGN_DOC.is_file(), "design-system-skills sibling checkout not present (NOT_ASSESSED)")
    def test_design_pilot_file_passes(self):
        result = subprocess.run([sys.executable, "-X", "utf8", str(VALIDATOR), str(DESIGN_DOC)],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout)


if __name__ == "__main__":
    unittest.main()
