#!/usr/bin/env python3
"""Tests for the P01 portfolio snapshot: porcelain parsing and router sizes."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "kaizen_portfolio_snapshot.py"
SPEC = importlib.util.spec_from_file_location("kaizen_portfolio_snapshot", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


def run_git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


class PorcelainTests(unittest.TestCase):
    def test_leading_space_of_first_line_is_kept(self) -> None:
        # " M README.md" is a worktree-only change; the path must keep its first letter.
        rows = MODULE.parse_porcelain(" M README.md\n?? catalog/engines.yaml\n")
        self.assertEqual(rows, [("M", "README.md"), ("??", "catalog/engines.yaml")])

    def test_rename_reports_new_path(self) -> None:
        self.assertEqual(MODULE.parse_porcelain("R  old.md -> new.md\n"), [("R", "new.md")])

    def test_first_dirty_path_is_intact_in_real_repository(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            run_git(root, "init", "-q")
            run_git(root, "config", "user.email", "test@example.invalid")
            run_git(root, "config", "user.name", "Test")
            run_git(root, "config", "core.autocrlf", "false")
            run_git(root, "remote", "add", "origin", "https://example.invalid/fixture.git")
            (root / "README.md").write_text("one\n", encoding="utf-8")
            run_git(root, "add", "README.md")
            run_git(root, "commit", "-q", "-m", "init")
            (root / "README.md").write_text("two\n", encoding="utf-8")
            record, _ = MODULE.collect_engine(root, "fixture")
            self.assertEqual([row["path"] for row in record["dirty_files"]], ["README.md"])
            self.assertEqual(record["dirty_files"][0]["status"], "M")


class RouterSizeTests(unittest.TestCase):
    def test_import_is_resolved_and_counted(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "CLAUDE.md").write_bytes(b"# Claude Code repository memory\n\n@AGENTS.md\n")
            (root / "AGENTS.md").write_bytes(b"x" * 100)
            size = MODULE.router_size(root)
            self.assertEqual(size["router_bytes"], 44)
            self.assertEqual(size["router_import_bytes"], 100)
            self.assertEqual(size["router_effective_bytes"], 144)
            self.assertEqual(size["router_imports"], [{"path": "AGENTS.md", "bytes": 100}])

    def test_cycle_is_guarded_and_nested_import_followed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "docs").mkdir()
            (root / "CLAUDE.md").write_bytes(b"@AGENTS.md\n")
            (root / "AGENTS.md").write_bytes(b"@docs/extra.md\n@CLAUDE.md\n")
            (root / "docs" / "extra.md").write_bytes(b"@../AGENTS.md\nbody\n")
            size = MODULE.router_size(root)
            self.assertEqual([item["path"] for item in size["router_imports"]], ["AGENTS.md", "docs/extra.md"])
            self.assertEqual(size["router_effective_bytes"], 11 + 26 + 19)

    def test_missing_router_gives_none(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            size = MODULE.router_size(Path(directory))
            self.assertIsNone(size["router_bytes"])


if __name__ == "__main__":
    unittest.main()
