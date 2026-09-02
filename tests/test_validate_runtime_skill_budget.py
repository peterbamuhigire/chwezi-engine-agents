#!/usr/bin/env python3
"""Unit tests for the aggregate runtime skill metadata validator."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate-runtime-skill-budget.py"
SPEC = importlib.util.spec_from_file_location("runtime_budget", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class RuntimeBudgetTests(unittest.TestCase):
    def test_folded_description_is_normalised(self) -> None:
        parsed = MODULE.parse_frontmatter("---\nname: example\ndescription: >-\n  Use when routing example work.\n  Keep details in references.\n---\n")
        self.assertEqual(parsed, ("example", "Use when routing example work. Keep details in references."))

    def test_duplicate_names_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("one", "two"):
                path = root / name
                path.mkdir()
                (path / "SKILL.md").write_text("---\nname: duplicate\ndescription: Use when testing.\n---\n", encoding="utf-8")
            records, findings = MODULE.discover([root], {".git"})
            findings = MODULE.evaluate(records, findings, 10, 350, 10_000, 10_000)
            self.assertTrue(any(finding.code == "duplicate-name" for finding in findings))

    def test_budget_failure_is_reported(self) -> None:
        record = MODULE.SkillRecord("example", "Use when testing.", "example/SKILL.md")
        findings = MODULE.evaluate([record], [], 0, 350, 10_000, 10_000)
        self.assertTrue(any(finding.code == "skill-count" for finding in findings))

    def test_configured_plugins_select_latest_cache(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "config.toml"
            cache = root / "cache"
            plugin = cache / "market" / "example"
            for version in ("old", "latest"):
                skill = plugin / version / "skills" / "example"
                skill.mkdir(parents=True)
                (skill / "SKILL.md").write_text("---\nname: example\ndescription: Use when testing.\n---\n", encoding="utf-8")
            config.write_text('[plugins."example@market"]\nenabled = true\n', encoding="utf-8")
            roots, findings = MODULE.configured_plugin_roots(config, cache)
            self.assertEqual(findings, [])
            self.assertEqual(roots, [plugin / "latest"])


if __name__ == "__main__":
    unittest.main()
