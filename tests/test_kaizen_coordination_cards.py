"""Normal and failure-path checks for coordination Kaizen references."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-kaizen-cards.py"


class CoordinationCardValidationTests(unittest.TestCase):
    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(VALIDATOR), *args],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_all_coordination_cards_and_readme_pass(self) -> None:
        result = self.run_validator()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Coordination Kaizen card structure valid.", result.stdout)

    def test_incomplete_card_fails_with_actionable_findings(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "incomplete.md"
            path.write_text("# Incomplete card\n", encoding="utf-8")
            result = self.run_validator("--card", str(path), "--profile", "h2")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("missing heading", result.stderr)
        self.assertIn("NOT_ASSESSED", result.stderr)


if __name__ == "__main__":
    unittest.main()
