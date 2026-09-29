#!/usr/bin/env python3
"""Tests for scripts/generate_engine_tour.py (M10-12-T06/T10) against a synthetic fixture workspace.

Two runs are byte-identical; --check passes on a fresh tour, fails on a dangling path and on a
manifest gate command missing from the tour; --check-links resolves links and engine routes."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SCRIPT = PACKAGE / "scripts" / "generate_engine_tour.py"
FIXTURE = PACKAGE / "tests" / "fixtures" / "engine-workspace"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), *args], capture_output=True, text=True, check=False)


def digest(folder: Path) -> dict[str, str]:
    return {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(folder.iterdir())}


class TourTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="engine-tour-"))
        self.workspace = self.tmp / "ws"
        shutil.copytree(FIXTURE, self.workspace)
        self.out = self.tmp / "tours"
        self.base = ["--workspace-root", str(self.workspace), "--engine", "demo-engine", "--out-dir", str(self.out)]

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_generation_is_deterministic_and_within_contract(self) -> None:
        first = run(*self.base)
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        hashes = digest(self.out)
        self.assertEqual(sorted(hashes), ["demo-engine.json", "demo-engine.md"])
        second = run(*self.base)
        self.assertEqual(second.returncode, 0)
        self.assertEqual(digest(self.out), hashes)
        tour = json.loads((self.out / "demo-engine.json").read_text(encoding="utf-8"))
        self.assertTrue(7 <= len(tour["steps"]) <= 12)
        self.assertNotIn("generated_at", json.dumps(tour))
        titles = [step["title"] for step in tour["steps"]]
        self.assertEqual(titles[:3], ["Purpose", "Router", "Engine contract"])
        gates = next(step for step in tour["steps"] if step["title"] == "Gates")
        self.assertIn("python -X utf8 scripts/check.py", gates["data"]["commands"])
        hubs = next(step for step in tour["steps"] if step["title"] == "Hub skills")
        self.assertEqual(hubs["data"]["hubs"][0]["skill"], "skills/core/beta-skill")
        adding = next(step for step in tour["steps"] if step["title"] == "Adding a skill")
        self.assertEqual(adding["data"]["status"], "NOT_ASSESSED")

    def test_check_passes_then_fails_on_dangling_path_and_missing_gate(self) -> None:
        self.assertEqual(run(*self.base).returncode, 0)
        ok = run(*self.base, "--check")
        self.assertEqual(ok.returncode, 0, ok.stdout)
        path = self.out / "demo-engine.json"
        tour = json.loads(path.read_text(encoding="utf-8"))
        tour["steps"][0]["paths"].append({"engine": "demo-engine", "path": "NO_SUCH_FILE.md"})
        path.write_text(json.dumps(tour), encoding="utf-8")
        dangling = run(*self.base, "--check")
        self.assertEqual(dangling.returncode, 1)
        self.assertIn("dangling path", dangling.stdout)
        self.assertEqual(run(*self.base).returncode, 0)
        tour = json.loads(path.read_text(encoding="utf-8"))
        for step in tour["steps"]:
            if step["title"] == "Gates":
                step["data"]["commands"] = []
        path.write_text(json.dumps(tour), encoding="utf-8")
        missing = run(*self.base, "--check")
        self.assertEqual(missing.returncode, 1)
        self.assertIn("gate command missing", missing.stdout)

    def test_absent_engine_is_not_assessed(self) -> None:
        result = run("--workspace-root", str(self.workspace), "--engine", "absent-engine", "--out-dir", str(self.out))
        self.assertEqual(result.returncode, 3)

    def test_check_links(self) -> None:
        doc = self.workspace / "demo-engine" / "MAP.md"
        doc.write_text("See [the router](AGENTS.md) and `demo-engine:skills/core/alpha-skill/`.\n", encoding="utf-8")
        catalog = self.tmp / "engines.yaml"
        catalog.write_text("engines:\n  - {id: demo-engine, path: demo-engine, router: AGENTS.md}\n", encoding="utf-8")
        good = run("--workspace-root", str(self.workspace), "--catalog", str(catalog), "--check-links", str(doc))
        self.assertEqual(good.returncode, 0, good.stdout)
        doc.write_text("See `demo-engine:skills/core/missing-skill/` and [x](missing.md).\n", encoding="utf-8")
        bad = run("--workspace-root", str(self.workspace), "--catalog", str(catalog), "--check-links", str(doc))
        self.assertEqual(bad.returncode, 1)
        self.assertIn("unresolved route", bad.stdout)
        self.assertIn("broken link", bad.stdout)


if __name__ == "__main__":
    unittest.main()
