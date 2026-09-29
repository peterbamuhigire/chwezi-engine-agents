#!/usr/bin/env python3
"""Validate the Tier 2 routing ratchet in evals/routing/baseline.json (M10-03-T11).

Rule: a floor is raised, never lowered. `floor_history` is append-only and each engine's (and the
portfolio's) current `floor` must equal the last history entry. A floor below max(floor_history) is
an error unless that last entry carries `ledger_ref` (a row id present in
evals/routing/rejected-changes.md) and `approved_by`; the exception is then recorded in the history.

Figures are a lexical proxy, not live routing (see agent-skills issue #620).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASELINE = REPO_ROOT / "evals" / "routing" / "baseline.json"
DEFAULT_LEDGER = REPO_ROOT / "evals" / "routing" / "rejected-changes.md"
ENGINE_FIELDS = ("p_at_1", "p_at_3", "owned_negatives", "coverage", "floor", "floor_history")
PORTFOLIO_FIELDS = ("undeclared_pairs_ge_075", "oracle_primary_at_1", "floor", "floor_history")


def check_ratchet(label: str, block: dict[str, Any], ledger_text: str) -> list[str]:
    errors: list[str] = []
    history = block.get("floor_history")
    floor = block.get("floor")
    if not isinstance(history, list) or not history:
        return [f"{label}: floor_history must be a non-empty list"]
    if not isinstance(floor, (int, float)):
        return [f"{label}: floor must be a number"]
    floors = []
    for index, entry in enumerate(history):
        if not isinstance(entry, dict) or not isinstance(entry.get("floor"), (int, float)) or not entry.get("date") or not entry.get("reason"):
            errors.append(f"{label}: floor_history[{index}] needs date, floor and reason")
            continue
        floors.append(entry["floor"])
    if errors:
        return errors
    dates = [entry["date"] for entry in history]
    if dates != sorted(dates):
        errors.append(f"{label}: floor_history is append-only; dates must not go backwards")
    if floor != history[-1]["floor"]:
        errors.append(f"{label}: floor {floor} must equal the last floor_history entry ({history[-1]['floor']})")
    # Every drop, current or historical, needs a ledger row and an approver.
    for index in range(1, len(history)):
        if history[index]["floor"] < max(floors[:index]):
            entry = history[index]
            ref = entry.get("ledger_ref")
            if not ref or not entry.get("approved_by"):
                errors.append(f"{label}: floor lowered to {entry['floor']} below {max(floors[:index])} without ledger_ref and approved_by")
            elif str(ref) not in ledger_text:
                errors.append(f"{label}: ledger_ref {ref!r} not found in rejected-changes.md")
    if isinstance(block.get("p_at_1"), (int, float)) and block["p_at_1"] < floor:
        errors.append(f"{label}: recorded p_at_1 {block['p_at_1']} is below its own floor {floor}")
    if isinstance(block.get("oracle_primary_at_1"), (int, float)) and block["oracle_primary_at_1"] < floor:
        errors.append(f"{label}: recorded oracle_primary_at_1 {block['oracle_primary_at_1']} is below its own floor {floor}")
    return errors


def validate(baseline: dict[str, Any], ledger_text: str) -> list[str]:
    errors: list[str] = []
    if baseline.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    engines = baseline.get("engines")
    if not isinstance(engines, dict) or not engines:
        errors.append("engines must be a non-empty mapping")
        engines = {}
    for engine_id, block in engines.items():
        missing = [field for field in ENGINE_FIELDS if field not in block]
        if missing:
            errors.append(f"{engine_id}: missing {', '.join(missing)}")
            continue
        errors.extend(check_ratchet(engine_id, block, ledger_text))
    portfolio = baseline.get("portfolio")
    if not isinstance(portfolio, dict):
        errors.append("portfolio block is required")
    else:
        missing = [field for field in PORTFOLIO_FIELDS if field not in portfolio]
        if missing:
            errors.append(f"portfolio: missing {', '.join(missing)}")
        else:
            if portfolio["undeclared_pairs_ge_075"] != 0:
                errors.append("portfolio: undeclared_pairs_ge_075 must be 0")
            errors.extend(check_ratchet("portfolio", portfolio, ledger_text))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    args = parser.parse_args()
    if not args.baseline.is_file():
        print(f"NOT_ASSESSED: baseline missing: {args.baseline}")
        return 3
    baseline = json.loads(args.baseline.read_text(encoding="utf-8"))
    ledger_text = args.ledger.read_text(encoding="utf-8") if args.ledger.is_file() else ""
    errors = validate(baseline, ledger_text)
    if errors:
        print("FAIL: routing baseline ratchet")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"PASS: routing baseline ratchet ({len(baseline['engines'])} engines + portfolio; lexical proxy, not live routing)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
