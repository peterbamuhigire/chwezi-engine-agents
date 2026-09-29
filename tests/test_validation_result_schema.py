#!/usr/bin/env python3
"""Validation-result schema: optional findings[] stays backwards compatible (M10-07-T05 / AR-09, done in M10-03)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

jsonschema = pytest.importorskip("jsonschema")

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = json.loads((ROOT / "schemas" / "validation-result.schema.json").read_text(encoding="utf-8"))
FIXTURES = ROOT / "tests" / "fixtures"


def errors(name: str) -> list[str]:
    instance = yaml.safe_load((FIXTURES / name).read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(SCHEMA)
    return [error.message for error in validator.iter_errors(instance)]


def test_existing_result_without_findings_still_validates():
    assert errors("valid-validation-result.yaml") == []


def test_existing_invalid_result_still_fails():
    assert errors("invalid-validation-result.yaml")


def test_result_with_findings_validates():
    assert errors("valid-validation-result-with-findings.yaml") == []


def test_unknown_finding_field_fails():
    messages = errors("invalid-validation-result-unknown-finding-field.yaml")
    assert any("auto_fix_applied" in message for message in messages)
