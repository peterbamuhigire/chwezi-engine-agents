#!/usr/bin/env python3
"""Tests for scripts/skill_graph.py (M10-12-T08): a fixture with a seeded retired-alias mention and
a seeded cross-engine collision detects both; two runs are byte-identical; the shrink guard
refuses a graph that loses more than 20 % of its edges; the private engine is refused."""

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
SCRIPT = PACKAGE / "scripts" / "skill_graph.py"
FIXTURE = PACKAGE / "tests" / "fixtures" / "graph-workspace"


def run(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), *args], capture_output=True, text=True, check=False)


class SkillGraphTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="skill-graph-"))
        self.base = ["--workspace-root", str(FIXTURE), "--engine", "engine-a", "--engine", "engine-b"]

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def build(self, name: str) -> Path:
        out = self.tmp / name
        result = run(*self.base, "--out", str(out))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return out

    def test_detects_seeded_retired_alias_and_cross_engine_collision(self) -> None:
        out = self.build("a")
        report = json.loads((out / "skill-graph-report.json").read_text(encoding="utf-8"))
        self.assertEqual([hit["slug"] for hit in report["retired_alias_mentions"]], ["old-invoice-skill"])
        self.assertEqual(report["retired_alias_mentions"][0]["at"], "engine-a/skills/core/ledger-posting/SKILL.md:8")
        self.assertEqual([hit["reference"] for hit in report["missing_skill_paths"]], ["skills/core/missing-skill"])
        graph = json.loads((out / "skill-graph.json").read_text(encoding="utf-8"))
        similar = graph["edge_types"].index("similar_trigger")
        pairs = [(graph["nodes"][a], graph["nodes"][b]) for a, b, t in graph["edges"] if t == similar]
        self.assertEqual(pairs, [("skill:engine-a/skills/core/invoice-layout", "skill:engine-b/skills/docs/printable-invoices")])
        self.assertEqual(graph["provenance"]["similar_trigger"], "AMBIGUOUS")

    def test_two_runs_are_byte_identical(self) -> None:
        first, second = self.build("a"), self.build("b")
        for name in ("skill-graph.json", "skill-graph-report.json"):
            self.assertEqual(hashlib.sha256((first / name).read_bytes()).hexdigest(),
                             hashlib.sha256((second / name).read_bytes()).hexdigest(), name)

    def test_shrink_guard(self) -> None:
        out = self.build("a")
        graph_path = out / "skill-graph.json"
        graph = json.loads(graph_path.read_text(encoding="utf-8"))
        graph["edges"] = graph["edges"] * 3  # pretend the previous graph was three times larger
        graph_path.write_text(json.dumps(graph), encoding="utf-8")
        refused = run(*self.base, "--out", str(out))
        self.assertEqual(refused.returncode, 2)
        self.assertIn("shrink guard", refused.stdout)
        allowed = run(*self.base, "--out", str(out), "--allow-shrink")
        self.assertEqual(allowed.returncode, 0)

    def test_private_engine_refused(self) -> None:
        result = run("--workspace-root", str(FIXTURE), "--engine", "political-essay-skills", "--out", str(self.tmp / "p"))
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.tmp / "p").exists())


if __name__ == "__main__":
    unittest.main()
