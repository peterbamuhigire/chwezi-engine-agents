#!/usr/bin/env python3
"""Tests for scripts/skill_fanin.py (M10-12-T05): a fixture engine with one seeded zero-inbound
skill reports exactly that skill; provenance counts are separated; the private engine is refused."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SCRIPT = PACKAGE / "scripts" / "skill_fanin.py"
WORKSPACE = PACKAGE / "tests" / "fixtures" / "engine-workspace"
SPEC = importlib.util.spec_from_file_location("skill_fanin", SCRIPT)
assert SPEC and SPEC.loader
FANIN = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = FANIN
SPEC.loader.exec_module(FANIN)


class FanInTests(unittest.TestCase):
    def setUp(self) -> None:
        code, self.payload = FANIN.build(WORKSPACE.resolve(), ["demo-engine"], None)
        self.assertEqual(code, 0)
        self.rows = {row["skill"].rsplit("/", 1)[-1]: row for row in self.payload["skills"]}

    def test_lists_every_active_skill(self) -> None:
        self.assertEqual(sorted(self.rows), ["alpha-skill", "beta-skill", "delta-orphan", "gamma-skill"])
        self.assertEqual(self.payload["engines"]["demo-engine"]["active_skills"], 4)

    def test_seeded_zero_inbound_skill_is_the_only_one(self) -> None:
        zero = sorted(name for name, row in self.rows.items() if row["zero_inbound"])
        self.assertEqual(zero, ["delta-orphan"])

    def test_provenance_is_separated(self) -> None:
        self.assertEqual(self.rows["beta-skill"]["extracted"]["links"], 1)
        self.assertEqual(self.rows["gamma-skill"]["inferred"]["fixtures"], 1)
        self.assertEqual(self.rows["gamma-skill"]["inferred"]["mentions"], 1)
        self.assertEqual(self.rows["alpha-skill"]["inferred"]["mentions"], 1)
        self.assertEqual(self.rows["delta-orphan"]["extracted"]["router"], "family")

    def test_deterministic(self) -> None:
        _, again = FANIN.build(WORKSPACE.resolve(), ["demo-engine"], None)
        self.assertEqual(again, self.payload)

    def test_private_engine_refused(self) -> None:
        with self.assertRaises(FANIN.PrivateEngineError):
            FANIN.build(WORKSPACE.resolve(), ["political-essay-skills"], None)

    def test_missing_engine_is_not_assessed(self) -> None:
        code, payload = FANIN.build(WORKSPACE.resolve(), ["absent-engine"], None)
        self.assertEqual(code, 3)
        self.assertEqual(payload["status"], "NOT_ASSESSED")


if __name__ == "__main__":
    unittest.main()
