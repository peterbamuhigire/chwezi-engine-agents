#!/usr/bin/env python3
"""Run deterministic evaluation-case shape and forbidden-action checks."""

from __future__ import annotations

import argparse
import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REQUIRED = {"id", "task", "fixture_path", "required_observations", "forbidden_actions", "expected_verdict", "evidence_fields"}
# Optional route-oracle keys (M10-03-T09/T10). Any other extra key is tolerated as before.
RUN_MODES = {"lexical", "behavioural"}
LAST_RUN = {"PASS", "FAIL", "NOT_ASSESSED"}
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


def oracle_shape_errors(case: dict[str, Any]) -> list[str]:
    """Shape of the optional route-oracle keys: expected_primary, must_co_activate, run_mode, last_run, known_defect."""
    errors: list[str] = []
    primary = case.get("expected_primary")
    if primary is not None and (not isinstance(primary, str) or "/" not in primary.strip("/")):
        errors.append("expected_primary must be <engine-id>/<skill>")
    co_activate = case.get("must_co_activate")
    if co_activate is not None and (not isinstance(co_activate, list) or not all(isinstance(item, str) and item for item in co_activate)):
        errors.append("must_co_activate must be a list of engine ids")
    if case.get("run_mode") is not None and case.get("run_mode") not in RUN_MODES:
        errors.append(f"run_mode must be one of {sorted(RUN_MODES)}")
    if case.get("last_run") is not None and case.get("last_run") not in LAST_RUN:
        errors.append(f"last_run must be one of {sorted(LAST_RUN)}")
    if case.get("run_mode") == "behavioural" and case.get("last_run") == "PASS" and not case.get("last_run_evidence"):
        errors.append("a behavioural PASS needs last_run_evidence")
    if case.get("known_defect") is not None and not isinstance(case.get("known_defect"), str):
        errors.append("known_defect must name the owning phase, for example M10-11")
    return errors


def route_oracles(case_paths: list[Path], workspace_root: Path) -> dict[str, Any]:
    """Execute expected_primary / must_co_activate lexically over the union (a lexical proxy, not live routing)."""
    import sys

    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    import lexical_routing

    engines = lexical_routing.load_catalog_engines(REPO_ROOT / "catalog" / "engines.yaml", workspace_root)
    # The coordinator package's own skills compete in the same runtime when it is installed.
    engines.append(("chwezi-engine-agents", REPO_ROOT / "skills"))
    label = "lexical proxy; not live routing (see agent-skills issue #620)"
    missing = [engine_id for engine_id, root in engines if not root.is_dir()]
    if missing:
        return {"status": "NOT_ASSESSED", "label": label, "reason": "sibling engine unavailable: " + ", ".join(missing)}
    docs = []
    for engine_id, root in engines:
        docs.extend(lexical_routing.discover_engine(engine_id, root)[0])
    index = lexical_routing.LexicalIndex(docs)
    results: list[dict[str, Any]] = []
    for path in case_paths:
        case = load_case(path)
        primary = case.get("expected_primary")
        if not primary:
            continue
        ranking = index.rank(str(case["task"]))
        keys = [key for key, _score in ranking]
        top5_engines = [index.by_key[key].engine for key in keys[:5]]
        expected_engine = primary.split("/", 1)[0]
        rank = keys.index(primary) + 1 if primary in index.by_key else None
        co_activate = list(case.get("must_co_activate") or [])
        results.append(
            {
                "case_id": case.get("id", path.stem),
                "run_mode": case.get("run_mode", "lexical"),
                "known_defect": case.get("known_defect"),
                "expected_primary": primary,
                "expected_engine": expected_engine,
                "rank": rank,
                "primary_at_1": rank == 1,
                "engine_at_1": index.by_key[keys[0]].engine == expected_engine,
                "tie_at_1": rank == 1 and len(ranking) > 1 and abs(ranking[0][1] - ranking[1][1]) < 1e-9,
                "must_co_activate": co_activate,
                "co_activate_at_5": all(engine in top5_engines for engine in co_activate) if co_activate else None,
                "top3": [[key, round(score, 3)] for key, score in ranking[:3]],
                "error": None if primary in index.by_key else "expected_primary is not in the union",
                # T05 lint applies to acceptance prompts: they must not name or copy the expected skill.
                "lint": lexical_routing.lint_prompt(str(case["task"]), primary.split("/", 1)[1], index.by_key[primary].description if primary in index.by_key else "")
                if case.get("run_mode") == "behavioural"
                else [],
            }
        )

    def rate(rows: list[dict[str, Any]], field: str) -> dict[str, Any]:
        hits = sum(bool(row[field]) for row in rows)
        return {"hits": hits, "total": len(rows), "pct": round(100 * hits / len(rows), 1) if rows else None}

    # Route oracles (run_mode lexical) carry the primary@1 metric; acceptance prompts (run_mode
    # behavioural) are recorded separately because their gate is the M10-05 behavioural run.
    acceptance = [row for row in results if row["run_mode"] == "behavioural"]
    oracles = [row for row in results if row["run_mode"] != "behavioural"]
    gated = [row for row in oracles if not row["known_defect"]]
    per_engine: dict[str, Any] = {}
    for engine in sorted({row["expected_engine"] for row in gated}):
        rows = [row for row in gated if row["expected_engine"] == engine]
        per_engine[engine] = {"primary_at_1": rate(rows, "primary_at_1"), "engine_at_1": rate(rows, "engine_at_1")}
    co_rows = [row for row in gated if row["co_activate_at_5"] is not None]
    return {
        "status": "ASSESSED",
        "label": label,
        "skills": len(docs),
        "oracles": len(oracles),
        "known_defects": [row["case_id"] for row in oracles if row["known_defect"]],
        "known_defect_primary_at_1": rate([row for row in oracles if row["known_defect"]], "primary_at_1"),
        "primary_at_1": rate(gated, "primary_at_1"),
        "engine_at_1": rate(gated, "engine_at_1"),
        "must_co_activate_at_5": rate(co_rows, "co_activate_at_5"),
        "ties_at_1": [row["case_id"] for row in results if row["tie_at_1"]],
        "per_engine": per_engine,
        "acceptance_prompts": {
            "cases": len(acceptance),
            "lexical_primary_at_1": rate(acceptance, "primary_at_1"),
            "lexical_engine_at_1": rate(acceptance, "engine_at_1"),
            "behavioural": "NOT_ASSESSED (zero-spend rule; behavioural run assigned to M10-05)",
            "lint_findings": {row["case_id"]: row["lint"] for row in acceptance if row["lint"]},
        },
        "errors": {row["case_id"]: row["error"] for row in results if row["error"]},
        "results": results,
    }


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
        errors.extend(oracle_shape_errors(case))
        status = "FAIL" if errors else "PASS"
        return {"case_id": case.get("id", path.stem), "status": status, "duration_ms": 0, "evidence": "; ".join(errors) if errors else "Case shape, forbidden-action declarations and fixture presence are valid."}
    except Exception as exc:  # noqa: BLE001 - malformed cases become evidence
        return {"case_id": path.stem, "status": "FAIL", "duration_ms": 0, "evidence": f"Malformed case: {exc}"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", type=Path, default=REPO_ROOT / "evals" / "cases")
    parser.add_argument("--out", type=Path, default=REPO_ROOT / "evals" / "reports" / "latest.json")
    parser.add_argument("--min-cases", type=int, default=MIN_CASES)
    parser.add_argument("--route-oracles", action="store_true", help="Also execute expected_primary/must_co_activate lexically over the union of catalogued engines.")
    parser.add_argument("--workspace-root", type=Path, default=REPO_ROOT.parent, help="Directory holding the sibling engine checkouts (for --route-oracles).")
    parser.add_argument("--min-oracle-primary", type=float, default=None, help="Fail when oracle primary@1 (known defects excluded) falls below this percentage.")
    args = parser.parse_args()
    case_paths = sorted(args.cases.glob("*.yaml"))
    reports = [evaluate(path) for path in case_paths]
    if len(reports) < args.min_cases:
        reports.append({"case_id": "suite-shape", "status": "FAIL", "duration_ms": 0, "evidence": f"Expected at least {args.min_cases} cases, found {len(reports)}."})
    failed = sum(report["status"] == "FAIL" for report in reports)
    result = {"schema_version": "1.0", "host": "deterministic-runner", "model": "not_applicable", "adapter_version": "1.0.0", "core_version": "1.0.0", "generated_at": datetime.now(UTC).astimezone().isoformat(), "thresholds": {"contract_shape": "100%", "forbidden_actions": "100%", "safety_gates": "100%"}, "summary": {"total": len(reports), "passed": len(reports) - failed, "failed": failed}, "cases": reports}
    oracle_failed = False
    oracle_not_assessed = False
    if args.route_oracles:
        oracles = route_oracles(case_paths, args.workspace_root)
        result["route_oracles"] = oracles
        if oracles["status"] == "NOT_ASSESSED":
            oracle_not_assessed = True
            print(f"route-oracles: NOT_ASSESSED ({oracles['reason']})")
        else:
            summary = {key: oracles[key] for key in ("oracles", "primary_at_1", "engine_at_1", "must_co_activate_at_5", "acceptance_prompts")}
            summary["known_defects"] = len(oracles["known_defects"])
            print(f"route-oracles ({oracles['label']}): {json.dumps(summary, sort_keys=True)}")
            if oracles["errors"] or oracles["acceptance_prompts"]["lint_findings"]:
                print(f"route-oracles: errors {oracles['errors']} lint {oracles['acceptance_prompts']['lint_findings']}")
                oracle_failed = True
            pct = oracles["primary_at_1"]["pct"]
            if args.min_oracle_primary is not None and (pct is None or pct < args.min_oracle_primary):
                print(f"route-oracles: primary@1 {pct}% is below the floor {args.min_oracle_primary}%")
                oracle_failed = True
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], sort_keys=True))
    if failed or oracle_failed:
        return 1
    return 3 if oracle_not_assessed else 0


if __name__ == "__main__":
    raise SystemExit(main())
