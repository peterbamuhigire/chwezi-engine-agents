#!/usr/bin/env python3
"""Tests for scripts/skill_usage_scan.py (M10-12-T11) on synthetic transcripts.

Counts come only from tool calls inside the window; no prompt, response or tool-result text
reaches any output; the private engine is dropped; an output path inside the workspace or a Git
repository is refused; Codex is parsed only in the recognised shape."""

from __future__ import annotations

import csv
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SCRIPT = PACKAGE / "scripts" / "skill_usage_scan.py"
FIXTURE = PACKAGE / "tests" / "fixtures" / "usage-scan"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), *args], capture_output=True, text=True, check=False)


class UsageScanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="usage-scan-"))
        self.out = self.tmp / "out"
        self.base = ["--transcripts", str(FIXTURE / "transcripts"), "--inventory", str(FIXTURE / "inventory.jsonl"),
                     "--since", "2026-08-01", "--until", "2026-09-30", "--workspace-root", str(PACKAGE.parent)]

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def rows(self) -> dict[str, dict]:
        with (self.out / "skill-usage.csv").open(encoding="utf-8") as handle:
            return {row["skill_path"].split("/")[2]: row for row in csv.DictReader(handle)}

    def test_counts_tool_calls_in_window_only(self) -> None:
        result = run(*self.base, "--out", str(self.out))
        self.assertEqual(result.returncode, 0, result.stderr)
        rows = self.rows()
        self.assertEqual(rows["alpha-skill"]["extracted_reads"], "2")
        self.assertEqual(rows["beta-skill"]["inferred_reads"], "1")
        self.assertEqual(rows["gamma-skill"]["total_reads"], "0")      # July read is outside the window
        self.assertEqual(rows["delta-orphan"]["total_reads"], "0")     # private transcript folder skipped
        summary = json.loads((self.out / "skill-usage-summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["totals"]["private_engine_paths_dropped"], 1)
        self.assertEqual(summary["totals"]["never_read"], 2)
        self.assertEqual(summary["sources"]["codex"], "NOT_REQUESTED")

    def test_no_transcript_text_in_outputs(self) -> None:
        self.assertEqual(run(*self.base, "--out", str(self.out)).returncode, 0)
        blob = "".join(p.read_text(encoding="utf-8") for p in self.out.iterdir())
        for secret in ("PRIVATE-PROMPT-TEXT", "PRIVATE-RESPONSE-TEXT", "PRIVATE-TOOL-RESULT"):
            self.assertNotIn(secret, blob)

    def test_codex_recognised_shape_is_parsed(self) -> None:
        result = run(*self.base, "--codex-root", str(FIXTURE / "codex"), "--out", str(self.out))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.rows()["gamma-skill"]["inferred_reads"], "1")
        summary = json.loads((self.out / "skill-usage-summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["sources"]["codex"], "PARSED")

    def test_unrecognised_codex_is_not_assessed(self) -> None:
        odd = self.tmp / "codex-odd"
        odd.mkdir()
        (odd / "x.jsonl").write_text('{"kind": "unknown"}\n', encoding="utf-8")
        self.assertEqual(run(*self.base, "--codex-root", str(odd), "--out", str(self.out)).returncode, 0)
        summary = json.loads((self.out / "skill-usage-summary.json").read_text(encoding="utf-8"))
        self.assertEqual(summary["sources"]["codex"], "NOT_ASSESSED")

    def test_refuses_output_inside_repository(self) -> None:
        inside = PACKAGE / "tmp-usage-scan-refusal"
        result = run(*self.base, "--out", str(inside))
        self.assertEqual(result.returncode, 1)
        self.assertIn("REFUSED", result.stderr)
        self.assertFalse(inside.exists())


if __name__ == "__main__":
    unittest.main()
