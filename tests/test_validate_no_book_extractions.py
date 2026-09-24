"""Normal, failure and false-positive checks for the book-extraction guard."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate-no-book-extractions.py"


def write(path: Path, text: str = "content\n") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class BookExtractionGuardTests(unittest.TestCase):
    def run_validator(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(VALIDATOR), *args],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

    def test_domain_topics_and_provenance_notes_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            engine = Path(directory) / "engine"
            write(engine / "skills/industry/food-processing/references/juice-extraction.md")
            write(engine / "skills/languages/python/references/pdf-extraction.md")
            write(engine / "skills/ops/references/agent-operations-runbook-summary.md")
            write(engine / "docs/updates/2026-09-20-book-informed-implementation-notes.md")
            result = self.run_validator("--root", str(engine))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS: book-extraction check", result.stdout)

    def test_banned_folders_and_book_digests_fail(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            engine = Path(directory) / "engine"
            write(engine / "book-extractions/some-title-extraction.md")
            write(engine / "docs/book-study/chapter-1.md")
            write(engine / "research/wave1-ifrs-book-extraction.md")
            write(engine / "skills/x/references/clean-code-book-notes.md")
            result = self.run_validator("--root", str(engine))
        self.assertEqual(result.returncode, 1)
        self.assertIn("engine/book-extractions: banned book-extraction folder", result.stderr)
        self.assertIn("engine/docs/book-study: banned book-extraction folder", result.stderr)
        self.assertIn("wave1-ifrs-book-extraction.md: book digest file name", result.stderr)
        self.assertIn("clean-code-book-notes.md: book digest file name", result.stderr)

    def test_extraction_outside_skill_folders_needs_allowlist(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            engine = Path(directory) / "engine"
            write(engine / "docs/ore-extraction.md")
            blocked = self.run_validator("--root", str(engine))
            allowlist = Path(directory) / "allow.txt"
            allowlist.write_text("engine/docs/ore-extraction.md  # mining process topic\n", encoding="utf-8")
            allowed = self.run_validator("--root", str(engine), "--allowlist", str(allowlist))
        self.assertEqual(blocked.returncode, 1)
        self.assertIn("not allowlisted", blocked.stderr)
        self.assertEqual(allowed.returncode, 0, allowed.stderr)

    def test_missing_root_is_not_assessed_not_pass(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = self.run_validator("--root", str(Path(directory) / "absent"))
        self.assertEqual(result.returncode, 3)
        self.assertIn("NOT_ASSESSED", result.stdout)
        self.assertNotIn("PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
