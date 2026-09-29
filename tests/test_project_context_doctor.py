#!/usr/bin/env python3
"""Seeded-fixture tests for scripts/project_context_doctor.py (M10-12-T02).

Each finding code is produced by exactly one seeded fixture; the valid fixture exits 0; the
doctor writes nothing (file hashes before and after are unchanged)."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

PACKAGE = Path(__file__).resolve().parents[1]
SCRIPT = PACKAGE / "scripts" / "project_context_doctor.py"
FIXTURES = PACKAGE / "tests" / "fixtures" / "project-context"
SPEC = importlib.util.spec_from_file_location("project_context_doctor", SCRIPT)
assert SPEC and SPEC.loader
DOCTOR = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = DOCTOR
SPEC.loader.exec_module(DOCTOR)

SEEDED = {
    "schema-marker-missing": ("project/schema-marker-missing", 1),
    "field-missing": ("project/field-missing", 1),
    "schema-invalid": ("project/schema-invalid", 1),
    "pointer-outside-workspace": ("project/pointer-outside-workspace", 1),
    "pointer-missing-target": ("project/pointer-missing-target", 0),
    "stale-pointer-target": ("project/stale-pointer-target", 0),
    "duplicated-content": ("project/duplicated-content", 0),
    "visual-choice-present": ("project/visual-choice-present", 0),
    "review-overdue": ("project/review-overdue", 0),
}
FIXED_TIME = time.mktime((2026, 1, 1, 12, 0, 0, 0, 0, -1))


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*")) if path.is_file()
    }


class DoctorFixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # Copy to a temporary folder outside Git and pin modification times, so staleness is
        # decided by the fixture dates and not by the checkout time.
        cls.tmp = Path(tempfile.mkdtemp(prefix="project-context-"))
        cls.root = cls.tmp / "project-context"
        shutil.copytree(FIXTURES, cls.root)
        for path in cls.root.rglob("*"):
            os.utime(path, (FIXED_TIME, FIXED_TIME))
        cls.workspace = cls.root / "workspace"

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def run_case(self, name: str) -> tuple[int, dict]:
        import datetime as dt

        return DOCTOR.run(self.root / name / "PROJECT.md", self.workspace.resolve(), dt.date(2026, 9, 29))

    def test_valid_fixture_exits_zero_with_no_findings(self) -> None:
        code, report = self.run_case("valid")
        self.assertEqual(code, 0, report)
        self.assertEqual(report["status"], "PASS")
        self.assertEqual(report["findings"], [])

    def test_each_code_comes_from_exactly_one_fixture(self) -> None:
        produced: dict[str, list[str]] = {}
        for name, (expected, exit_code) in SEEDED.items():
            code, report = self.run_case(name)
            codes = sorted({item["code"] for item in report["findings"]})
            self.assertEqual(codes, [expected], f"{name}: {codes}")
            self.assertEqual(code, exit_code, f"{name}: exit {code}")
            produced.setdefault(expected, []).append(name)
        self.assertEqual(sorted(produced), sorted(code for code, _ in SEEDED.values()))
        self.assertTrue(all(len(names) == 1 for names in produced.values()), produced)

    def test_findings_use_ar09_fields(self) -> None:
        _, report = self.run_case("visual-choice-present")
        item = report["findings"][0]
        for key in ("code", "severity", "message", "subject", "evidence", "supported_fixes", "next_action"):
            self.assertIn(key, item)
        self.assertIn("Inter", item["evidence"]["banned_faces_named"])
        self.assertIn("#1a6b5c", item["evidence"]["hex_colours"])

    def test_omitted_pointer_declared_absent_is_a_mention(self) -> None:
        text = (self.root / "valid" / "PROJECT.md").read_text(encoding="utf-8")
        text = text.replace("brand_brief: demo-site/docs/brand-brief.md\n", "")
        text = text.replace("  absent: []\n", "  absent:\n    - Brand brief (not yet written)\n")
        case = self.root / "absent-brand-brief"
        case.mkdir(exist_ok=True)
        (case / "PROJECT.md").write_text(text, encoding="utf-8")
        code, report = self.run_case("absent-brand-brief")
        self.assertEqual(code, 0)
        self.assertEqual([(f["code"], f["severity"], f["evidence"]["declared_absent"]) for f in report["findings"]],
                         [("project/field-missing", "mention", True)])

    def test_absent_repository_folder_is_not_assessed(self) -> None:
        text = (self.root / "valid" / "PROJECT.md").read_text(encoding="utf-8")
        text = text.replace("website_repository: demo-site\n", "website_repository: not-on-this-machine\n")
        case = self.root / "absent-repository"
        case.mkdir(exist_ok=True)
        (case / "PROJECT.md").write_text(text, encoding="utf-8")
        code, report = self.run_case("absent-repository")
        self.assertEqual(code, 3)
        self.assertEqual(report["status"], "NOT_ASSESSED")

    def test_doctor_performs_no_write(self) -> None:
        before = tree_hashes(self.root)
        for name in ["valid", *SEEDED]:
            self.run_case(name)
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT), "--project", str(self.root / "valid" / "PROJECT.md"),
             "--workspace-root", str(self.workspace), "--json", "--today", "2026-09-29"],
            capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "PASS")
        self.assertEqual(tree_hashes(self.root), before)


class TemplateSchemaTests(unittest.TestCase):
    def run_validator(self, instance: Path) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(PACKAGE / "scripts" / "validate-contracts.py"),
             "--schema", str(PACKAGE / "schemas" / "project-context.schema.json"), "--instance", str(instance)],
            capture_output=True, text=True, check=False,
        )

    def test_template_front_matter_validates(self) -> None:
        result = self.run_validator(PACKAGE / "templates" / "project-context" / "PROJECT.md")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unknown_field_fails(self) -> None:
        result = self.run_validator(FIXTURES / "schema-invalid" / "PROJECT.md")
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("favourite_colour_scheme", result.stdout)


if __name__ == "__main__":
    unittest.main()
