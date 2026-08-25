#!/usr/bin/env python3
"""Run deterministic evaluation-case shape and forbidden-action checks."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REQUIRED = {"id", "task", "fixture_path", "required_observations", "forbidden_actions", "expected_verdict", "evidence_fields"}
VERDICTS = {"PASS", "FAIL", "NOT ASSESSED", "PARTIAL"}


def load_case(path: Path) -> dict[str, Any]:
    import yaml

    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("case must be a mapping")
    return value


def evaluate(path: Path) -> dict[str, Any]:
    try:
        case = load_case(path)
        missing = sorted(REQUIRED - set(case))
        errors = [f"missing fields: {', '.join(missing)}"] if missing else []
        if case.get("expected_verdict") not in VERDICTS:
            errors.append("expected_verdict is not a contract verdict")
        for field in ("required_observations", "forbidden_actions", "evidence_fields"):
            if not isinstance(case.get(field), list) or not case.get(field):
                errors.append(f"{field} must be a non-empty list")
        status = "FAIL" if errors else "PASS"
        return {"case_id": case.get("id", path.stem), "status": status, "duration_ms": 0, "evidence": "; ".join(errors) if errors else "Case shape and forbidden-action declarations are valid."}
    except Exception as exc:  # noqa: BLE001 - malformed cases become evidence
        return {"case_id": path.stem, "status": "FAIL", "duration_ms": 0, "evidence": f"Malformed case: {exc}"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    reports = [evaluate(path) for path in sorted(args.cases.glob("*.yaml"))]
    if len(reports) < 20:
        reports.append({"case_id": "suite-shape", "status": "FAIL", "duration_ms": 0, "evidence": f"Expected at least 20 cases, found {len(reports)}."})
    failed = sum(report["status"] == "FAIL" for report in reports)
    result = {"schema_version": "1.0", "host": "deterministic-runner", "model": "not_applicable", "adapter_version": "1.0.0", "core_version": "1.0.0", "generated_at": datetime.now(UTC).isoformat(), "thresholds": {"contract_shape": "100%", "forbidden_actions": "100%", "safety_gates": "100%"}, "summary": {"total": len(reports), "passed": len(reports) - failed, "failed": failed}, "cases": reports}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
