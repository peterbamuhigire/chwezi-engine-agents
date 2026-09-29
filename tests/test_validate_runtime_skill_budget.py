#!/usr/bin/env python3
"""Unit tests for the aggregate runtime skill metadata validator."""

from __future__ import annotations

import importlib.util
import json
import subprocess
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
lexical_routing = sys.modules["lexical_routing"]


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


def _write_skill(root: Path, engine: str, name: str, description: str) -> None:
    folder = root / engine / "skills" / name
    folder.mkdir(parents=True)
    text = "---\n" + f"name: {name}\n" + f"description: {description}\n" + "---\n\n" + f"# {name}\n"
    (folder / "SKILL.md").write_text(text, encoding="utf-8")


DUPLICATE = "Use when reconciling supplier invoices against purchase orders and goods received notes in procurement ledgers."
REGISTER = (
    "schema_version: 1\n"
    "pairs:\n"
    "  - skills: [engine-a/invoice-matching, engine-b/invoice-matching]\n"
    "    disposition: canonical_owner\n"
    "    owner: engine-a/invoice-matching\n"
    "    reason: shared doctrine\n"
    "    decided_by: test\n"
    "    decided_on: 2026-09-29\n"
    "    review_after: 2026-12-29\n"
    "    follow_up: none\n"
)


class CollisionGateTests(unittest.TestCase):
    """M10-03-T01: union collision scan with an ownership register."""

    def _run(self, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), "--collisions", *args], capture_output=True, text=True)

    def _engines(self, root: Path) -> None:
        _write_skill(root, "engine-a", "invoice-matching", DUPLICATE)
        _write_skill(root, "engine-b", "invoice-matching", DUPLICATE)
        _write_skill(root, "engine-a", "kitchen-rota", "Use when planning restaurant kitchen shift rotas and staff breaks.")
        _write_skill(root, "engine-b", "tax-returns", "Use when filing annual corporate income tax returns with statutory schedules.")

    def test_undeclared_duplicate_description_pair_exits_1(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._engines(root)
            result = self._run("--root", str(root / "engine-a"), "--root", str(root / "engine-b"))
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("undeclared-collision", result.stdout)

    def test_declared_pair_exits_0(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._engines(root)
            register = root / "ownership.yaml"
            register.write_text(REGISTER, encoding="utf-8")
            result = self._run("--root", str(root / "engine-a"), "--root", str(root / "engine-b"), "--ownership", str(register), "--format", "json")
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["undeclared_pairs_ge_error"], 0)
            self.assertEqual(payload["cross_engine_pairs_ge_error"], 1)

    def test_fix_differentiate_pair_still_colliding_fails(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._engines(root)
            register = root / "ownership.yaml"
            register.write_text(REGISTER.replace("canonical_owner", "fix_differentiate"), encoding="utf-8")
            result = self._run("--root", str(root / "engine-a"), "--root", str(root / "engine-b"), "--ownership", str(register))
            self.assertEqual(result.returncode, 1)
            self.assertIn("undifferentiated-collision", result.stdout)

    def test_block_scalar_description_is_read(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory) / "engine-a" / "skills" / "folded"
            folder.mkdir(parents=True)
            text = "---\nname: folded\ndescription: >-\n  Use when reconciling supplier\n  invoices.\n---\n"
            (folder / "SKILL.md").write_text(text, encoding="utf-8")
            docs, issues = lexical_routing.discover_engine("engine-a", Path(directory) / "engine-a")
            self.assertEqual(issues, [])
            self.assertEqual(docs[0].description, "Use when reconciling supplier invoices.")

    def test_missing_sibling_engine_is_not_assessed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._engines(root)
            result = self._run("--root", str(root / "engine-a"), "--root", str(root / "engine-missing"))
            self.assertEqual(result.returncode, 3, result.stdout + result.stderr)
            self.assertIn("NOT_ASSESSED", result.stdout)

    def test_private_engine_path_is_refused(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            private = Path(directory) / "political-essay-skills"
            private.mkdir()
            result = self._run("--root", str(private))
            self.assertEqual(result.returncode, 2)
            self.assertIn("REFUSED", result.stderr)
            with self.assertRaises(lexical_routing.PrivateEngineError):
                lexical_routing.discover_engine("x", private)

    def test_catalogue_never_lists_the_private_engine(self) -> None:
        catalog = Path(__file__).resolve().parents[1] / "catalog" / "engines.yaml"
        engines = lexical_routing.load_catalog_engines(catalog, Path("/workspace"))
        self.assertFalse(any("political-essay" in str(root) for _engine, root in engines))

    def test_british_spelling_is_folded(self) -> None:
        self.assertEqual(lexical_routing.tokenize("colour optimise organisation"), lexical_routing.tokenize("color optimize organization"))

    def test_fixture_lint_detects_slug_and_copy(self) -> None:
        self.assertTrue(lexical_routing.lint_prompt("Write the 02 business case", "02-business-case", "x"))
        self.assertTrue(lexical_routing.lint_prompt("Write the business case now", "02-business-case", "x"))
        self.assertEqual(lexical_routing.lint_prompt("Justify the ERP spend to the board", "02-business-case", "Use when writing a business case"), [])


if __name__ == "__main__":
    unittest.main()
