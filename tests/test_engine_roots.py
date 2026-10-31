#!/usr/bin/env python3
"""Tests for scripts/lib/engine_roots.py (pass-2 K1): engines resolve on layouts that differ from
the catalogue (more than one parent folder, former folder names), and anything that cannot be
resolved is reported, never guessed."""

from __future__ import annotations

import importlib.util
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

PACKAGE = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("engine_roots", PACKAGE / "scripts" / "lib" / "engine_roots.py")
assert SPEC and SPEC.loader
ER = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = ER
SPEC.loader.exec_module(ER)

ENTRY = {"id": "chwezi-dev-engine", "repository": "chwezi-dev-engine", "path": "chwezi-dev-engine", "aliases": ["skills-web-dev"]}


class EngineRootsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp(prefix="engine-roots-")).resolve()
        self.a, self.b = self.tmp / "a", self.tmp / "b"
        self.a.mkdir()
        self.b.mkdir()

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_catalogue_path_resolves(self) -> None:
        (self.a / "chwezi-dev-engine").mkdir()
        result = ER.resolve_engine(ENTRY, ER.roots_from([self.a]))
        self.assertTrue(result.found)
        self.assertEqual(result.path, self.a / "chwezi-dev-engine")

    def test_former_folder_name_resolves_through_alias(self) -> None:
        (self.a / "skills-web-dev").mkdir()
        result = ER.resolve_engine(ENTRY, ER.roots_from([self.a]))
        self.assertTrue(result.found)
        self.assertEqual(result.path.name, "skills-web-dev")

    def test_engines_in_a_second_root_are_found(self) -> None:
        (self.b / "skills-web-dev").mkdir()
        result = ER.resolve_engine(ENTRY, ER.roots_from([self.a, self.b]))
        self.assertTrue(result.found)
        self.assertEqual(result.path, self.b / "skills-web-dev")

    def test_first_root_wins_when_both_roots_have_the_engine(self) -> None:
        (self.a / "chwezi-dev-engine").mkdir()
        (self.b / "chwezi-dev-engine").mkdir()
        result = ER.resolve_engine(ENTRY, ER.roots_from([self.b, self.a]))
        self.assertEqual(result.path, self.b / "chwezi-dev-engine")

    def test_stale_copy_under_the_old_name_is_ambiguous_not_guessed(self) -> None:
        (self.a / "chwezi-dev-engine").mkdir()
        (self.a / "skills-web-dev").mkdir()
        result = ER.resolve_engine(ENTRY, ER.roots_from([self.a]))
        self.assertEqual(result.status, "ambiguous")
        self.assertIsNone(result.path)
        self.assertEqual(len(result.candidates), 2)

    def test_link_and_target_are_one_directory(self) -> None:
        target = self.b / "real"
        target.mkdir()
        try:
            (self.a / "chwezi-dev-engine").symlink_to(target, target_is_directory=True)
        except OSError:
            self.skipTest("symbolic links are not available on this host")
        (self.a / "skills-web-dev").symlink_to(target, target_is_directory=True)
        result = ER.resolve_engine(ENTRY, ER.roots_from([self.a]))
        self.assertTrue(result.found, "two names for one real directory are not ambiguity")

    def test_missing_engine_is_reported_without_a_path(self) -> None:
        result = ER.resolve_engine(ENTRY, ER.roots_from([self.a, self.b]))
        self.assertEqual(result.status, "missing")
        self.assertIsNone(result.path)
        self.assertNotIn(str(self.tmp), ER.describe(result))

    def test_a_file_is_not_an_engine(self) -> None:
        (self.a / "chwezi-dev-engine").write_text("not a directory", encoding="utf-8")
        self.assertEqual(ER.resolve_engine(ENTRY, ER.roots_from([self.a])).status, "missing")

    def test_environment_roots_follow_explicit_roots_and_skip_non_directories(self) -> None:
        env = {ER.ENV_VAR: os.pathsep.join([str(self.b), str(self.tmp / "absent")])}
        roots = ER.roots_from([self.a], environ=env)
        self.assertEqual(roots, [self.a, self.b])

    def test_duplicate_roots_are_collapsed(self) -> None:
        self.assertEqual(ER.roots_from([self.a, self.a, str(self.a)]), [self.a])

    def test_candidate_names_are_ordered_and_unique(self) -> None:
        entry = {"id": "x", "repository": "r", "path": "x", "aliases": ["x", "old"]}
        self.assertEqual(ER.candidate_names(entry), ["x", "r", "old"])

    def test_the_shipped_catalogue_resolves_all_eleven_engines_by_former_names(self) -> None:
        catalog = yaml.safe_load((PACKAGE / "catalog" / "engines.yaml").read_text(encoding="utf-8"))
        for entry in catalog["engines"]:
            # Lay each engine out the way this workstation does: a former name where an alias exists.
            name = (entry.get("aliases") or [entry["path"]])[0]
            (self.a / name).mkdir(exist_ok=True)
        resolved = ER.resolve_catalog(catalog, ER.roots_from([self.a]))
        self.assertEqual(len(resolved), 11)
        self.assertEqual([k for k, v in resolved.items() if not v.found], [])
        renamed = {e["id"] for e in catalog["engines"] if e.get("aliases")}
        self.assertEqual(renamed, {"chwezi-sdlc-documentation", "chwezi-dev-engine", "chwezi-design-engine", "digital-research-skills"})

    def test_coordination_package_can_be_added(self) -> None:
        resolved = ER.resolve_catalog({"engines": []}, [], include_coordination=PACKAGE)
        self.assertTrue(resolved[ER.COORDINATION].found)


if __name__ == "__main__":
    unittest.main()
