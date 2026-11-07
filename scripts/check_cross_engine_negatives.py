#!/usr/bin/env python3
"""Evaluate declared cross-engine negative fixtures in the public lexical union.

This is a check, not a runtime router or proof of model behaviour. It reads the
existing Dev nested-negative and Research top-level-negative fixture formats.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict
import hashlib
import json
from pathlib import Path

import yaml

from lexical_routing import LexicalIndex, discover_engine, load_catalog_engines, refuse_private

ROOT = Path(__file__).resolve().parents[1]


def cross_cases(engine: str, data: dict) -> tuple[list[dict], int]:
    if not isinstance(data, dict):
        raise ValueError("fixture root must be an object")
    rows = []
    for index, item in enumerate(data.get("negatives", [])):
        rows.append((item, item.get("skill"), f"negative-{index}"))
    for index, fixture in enumerate(data.get("fixtures", [])):
        for negative_index, item in enumerate(fixture.get("negatives", [])):
            rows.append((item, fixture.get("expect"), f"fixture-{index}-negative-{negative_index}"))
    cases = []
    local_cases = 0
    for item, skill, fallback_id in rows:
        owner = item.get("owner")
        prompt = item.get("prompt", item.get("task"))
        if (not isinstance(owner, str) or not owner.strip()
                or not isinstance(skill, str) or not skill
                or not isinstance(prompt, str) or not prompt.strip()):
            raise ValueError(f"malformed negative case {fallback_id}; owner, skill and prompt are required")
        if "/" not in owner:
            local_cases += 1  # Single-engine checks retain ownership of these cases.
            continue
        cases.append({"id": str(item.get("id", fallback_id)), "skill": f"{engine}/{skill}",
                      "owner": owner, "prompt": prompt})
    return cases, local_cases


def evaluate(case: dict, index: LexicalIndex) -> dict:
    ranked = index.rank(case["prompt"])
    scores = dict(ranked)
    order = [key for key, _ in ranked]
    owner, skill = case["owner"], case["skill"]
    missing = [key for key in (owner, skill) if key not in scores]
    if missing:
        return {**case, "status": "NOT_ASSESSED", "reason": "missing active skill: " + ", ".join(missing)}
    passed = scores[owner] > 0 and scores[owner] > scores[skill]
    return {**case, "status": "PASS" if passed else "FAIL",
            "owner_rank": order.index(owner) + 1, "skill_rank": order.index(skill) + 1,
            "tied_scores": scores[owner] == scores[skill],
            "owner_score": scores[owner], "skill_score": scores[skill],
            "reason": "owner must score strictly above the competing skill; a tie does not pass"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, required=True)
    parser.add_argument("--fixture", action="append", required=True, metavar="ENGINE_ID=PATH")
    args = parser.parse_args()
    try:
        engines = load_catalog_engines(ROOT / "catalog/engines.yaml", args.workspace_root)
        engine_ids = {engine for engine, _ in engines}
        docs, issues, roots = [], [], []
        for engine, root in engines:
            refuse_private(root.resolve())
            roots.append({"engine": engine, "root": str(root.resolve())})
            if not root.is_dir():
                issues.append({"code": "missing-engine", "path": str(root)})
                continue
            found, errors = discover_engine(engine, root)
            docs.extend(found)
            issues.extend(asdict(error) for error in errors)
        cases, inputs, skipped_local, case_keys = [], [], 0, set()
        for spec in args.fixture:
            engine, separator, filename = spec.partition("=")
            if not separator or engine not in engine_ids:
                raise ValueError("--fixture requires a catalogue engine ID and explicit file path")
            path = Path(filename).resolve()
            payload = path.read_bytes()
            inputs.append({"engine": engine, "path": str(path), "sha256": hashlib.sha256(payload).hexdigest()})
            cross, local = cross_cases(engine, yaml.safe_load(payload.decode("utf-8-sig")))
            skipped_local += local
            for case in cross:
                key = (str(path), case["id"])
                if key in case_keys:
                    raise ValueError(f"duplicate case {key}")
                case_keys.add(key)
                cases.append({**case, "fixture": str(path)})
        index = LexicalIndex(docs)
        results = [evaluate(case, index) for case in cases]
        report = {"scope": "public catalogue lexical proxy; not live routing", "roots": roots,
                  "fixture_scope": "Only the explicitly supplied files; local negatives belong to their native checks",
                  "skipped_local_negatives": skipped_local,
                  "catalog_sha256": hashlib.sha256((ROOT / "catalog/engines.yaml").read_bytes()).hexdigest(),
                  "effective_corpus_sha256": hashlib.sha256(json.dumps(
                      [asdict(doc) for doc in docs], sort_keys=True).encode()).hexdigest(),
                  "inputs": inputs, "active_documents": len(docs), "issues": issues,
                  "total_cross_engine_cases": len(results),
                  "summary": {state: sum(row["status"] == state for row in results)
                              for state in ("PASS", "FAIL", "NOT_ASSESSED")}, "results": results}
        print(json.dumps(report, indent=2))
        return 0 if results and not issues and all(r["status"] == "PASS" for r in results) else 1
    except (OSError, ValueError, TypeError, AttributeError, yaml.YAMLError) as exc:
        print(json.dumps({"status": "NOT_ASSESSED", "error": str(exc)}))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
