#!/usr/bin/env python3
"""The routing ratchet: floors are raised, never lowered without a ledger row (M10-03-T11)."""

from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("routing_baseline", ROOT / "scripts" / "validate-routing-baseline.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)
BASELINE = json.loads((ROOT / "evals" / "routing" / "baseline.json").read_text(encoding="utf-8"))
LEDGER = (ROOT / "evals" / "routing" / "rejected-changes.md").read_text(encoding="utf-8")


def test_checked_in_baseline_passes():
    assert MODULE.validate(BASELINE, LEDGER) == []


def test_lowering_a_floor_without_a_ledger_row_fails():
    data = copy.deepcopy(BASELINE)
    engine = next(iter(data["engines"].values()))
    lowered = engine["floor"] - 5
    engine["floor"] = lowered
    engine["floor_history"].append({"date": "2099-01-01", "floor": lowered, "reason": "quietly lowered"})
    errors = MODULE.validate(data, LEDGER)
    assert any("without ledger_ref" in error for error in errors)


def test_lowering_with_an_unknown_ledger_row_fails():
    data = copy.deepcopy(BASELINE)
    engine = next(iter(data["engines"].values()))
    lowered = engine["floor"] - 5
    engine["floor"] = lowered
    engine["p_at_1"] = lowered
    engine["floor_history"].append({"date": "2099-01-01", "floor": lowered, "reason": "x", "ledger_ref": "RC-9999", "approved_by": "Peter Bamuhigire"})
    errors = MODULE.validate(data, LEDGER)
    assert any("not found in rejected-changes.md" in error for error in errors)


def test_lowering_with_a_ledger_row_and_approval_passes():
    data = copy.deepcopy(BASELINE)
    engine = next(iter(data["engines"].values()))
    lowered = engine["floor"] - 5
    engine["floor"] = lowered
    engine["floor_history"].append({"date": "2099-01-01", "floor": lowered, "reason": "x", "ledger_ref": "RC-TEST", "approved_by": "Peter Bamuhigire"})
    assert MODULE.validate(data, LEDGER + "\n| RC-TEST | seeded row |\n") == []


def test_editing_the_floor_without_history_fails():
    data = copy.deepcopy(BASELINE)
    engine = next(iter(data["engines"].values()))
    engine["floor"] = engine["floor"] - 1
    assert any("must equal the last floor_history entry" in error for error in MODULE.validate(data, LEDGER))


def test_undeclared_pairs_must_be_zero():
    data = copy.deepcopy(BASELINE)
    data["portfolio"]["undeclared_pairs_ge_075"] = 1
    assert "portfolio: undeclared_pairs_ge_075 must be 0" in MODULE.validate(data, LEDGER)
