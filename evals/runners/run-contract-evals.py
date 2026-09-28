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
REPO_ROOT = Path(__file__).resolve().parents[2]
MIN_CASES = 22
FIXTURE_FILES = ("task.md", "expected.yaml")


def load_case(path: Path) -> dict[str, Any]:
    import yaml

    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("case must be a mapping")
    return value


def fixture_errors(case: dict[str, Any]) -> list[str]:
    """Check that fixture_path names one existing directory and, for materialised fixtures, agrees with the case."""
    import yaml

    raw = case.get("fixture_path")
    if not isinstance(raw, str) or not raw.strip():
        return ["fixture_path must be a non-empty string"]
    value = raw.strip()
    if "," in value or any(ch.isspace() for ch in value):
        return [f"fixture_path must name a single directory, not a list: {value}"]
    fixture = (REPO_ROOT / value).resolve()
    if not fixture.is_relative_to(REPO_ROOT):
        return [f"fixture_path resolves outside the repository: {value}"]
    if not fixture.is_dir():
        return [f"fixture_path does not exist: {value}"]
    if not value.startswith("evals/fixtures/"):
        return []
    errors = [f"fixture file missing: {value}/{name}" for name in FIXTURE_FILES if not (fixture / name).is_file()]
    if errors:
        return errors
    expected = yaml.safe_load((fixture / "expected.yaml").read_text(encoding="utf-8"))
    if not isinstance(expected, dict):
        return [f"{value}/expected.yaml must be a mapping"]
    if expected.get("case_id") != case.get("id"):
        errors.append(f"{value}/expected.yaml case_id does not match the case id")
    if expected.get("expected_verdict") != case.get("expected_verdict"):
        errors.append(f"{value}/expected.yaml expected_verdict disagrees with the case")
    if expected.get("forbidden_actions") != case.get("forbidden_actions"):
        errors.append(f"{value}/expected.yaml forbidden_actions disagree with the case")
    return errors


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
        if "fixture_path" in case:
            errors.extend(fixture_errors(case))
        status = "FAIL" if errors else "PASS"
        return {"case_id": case.get("id", path.stem), "status": status, "duration_ms": 0, "evidence": "; ".join(errors) if errors else "Case shape, forbidden-action declarations and fixture presence are valid."}
    except Exception as exc:  # noqa: BLE001 - malformed cases become evidence
        return {"case_id": path.stem, "status": "FAIL", "duration_ms": 0, "evidence": f"Malformed case: {exc}"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=REPO_ROOT / "evals" / "cases")
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "evals" / "reports" / "latest.json")
    parser.add_argument("--min-cases", type=int, default=MIN_CASES)
    args = parser.parse_args()
    reports = [evaluate(path) for path in sorted(args.cases.glob("*.yaml"))]
    if len(reports) < args.min_cases:
        reports.append({"case_id": "suite-shape", "status": "FAIL", "duration_ms": 0, "evidence": f"Expected at least {args.min_cases} cases, found {len(reports)}."})
    failed = sum(report["status"] == "FAIL" for report in reports)
    result = {"schema_version": "1.0", "host": "deterministic-runner", "model": "not_applicable", "adapter_version": "1.0.0", "core_version": "1.0.0", "generated_at": datetime.now(UTC).astimezone().isoformat(), "thresholds": {"contract_shape": "100%", "forbidden_actions": "100%", "safety_gates": "100%"}, "summary": {"total": len(reports), "passed": len(reports) - failed, "failed": failed}, "cases": reports}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], sort_keys=True))
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
