"""Replay public-safe handoffs against an independently pinned producer manifest."""

import argparse
import hashlib
import json
from pathlib import Path

ROUTES = {
    "classifier": {
        "case": "K1",
        "steps": [
            ("srs-skills", "AC-S01"),
            ("chwezi-development-engine", "AC-D01"),
            ("chwezi-dev-engine", "AC-E01"),
        ],
    },
    "coding": {
        "case": "K3",
        "steps": [
            ("srs-skills", "AC-S04"),
            ("chwezi-development-engine", "AC-D07"),
            ("chwezi-dev-engine", "AC-E05"),
        ],
    },
}


def digest_record(record):
    # Git checkouts can use CRLF or LF. Bind the parsed UTF-8 JSON record deterministically.
    canonical = json.dumps(
        record, sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(canonical).hexdigest()


def replay(incoming, pins):
    results = {}
    for route, journey in ROUTES.items():
        steps = []
        for producer, criterion in journey["steps"]:
            path = incoming / (producer + ".json")
            step = {
                "route": route,
                "producer": producer,
                "artifact": path.name,
                "criterion": criterion,
            }
            pin = pins.get(producer, {})
            packet = None
            if path.is_file():
                try:
                    packet = json.loads(path.read_bytes())
                except (ValueError, UnicodeError):
                    pass
            if not path.is_file():
                issue = "missing producer receipt"
            elif not isinstance(packet, dict) or digest_record(packet) != pin.get(
                "canonical_sha256"
            ):
                issue = "receipt digest differs from accepted manifest"
            elif not isinstance(packet.get("receipts"), list) or not isinstance(
                packet.get("cases"), list
            ):
                issue = "malformed producer evidence or case list"
            else:
                proof = next(
                    (
                        x
                        for x in (packet.get("receipts") or [])
                        if isinstance(x, dict) and x.get("criterion_id") == criterion
                    ),
                    None,
                )
                case = next(
                    (
                        c
                        for c in (packet.get("cases") or [])
                        if isinstance(c, dict) and c.get("id") == journey["case"]
                    ),
                    None,
                )
                if (
                    packet.get("tested_revision") != pin.get("revision")
                    or packet.get("producer") != producer
                ):
                    issue = "stale producer identity or revision"
                elif (
                    not proof
                    or proof.get("result") != "PASS"
                    or not proof.get("sha256")
                    or not case
                    or not case.get("outcome")
                ):
                    issue = "missing accepted criterion or case"
                else:
                    issue = None
                    step.update(
                        tested_revision=packet["tested_revision"],
                        evidence_sha256=proof["sha256"],
                        expected_outcome=case["outcome"],
                    )
            step.update(
                status="BLOCKED" if issue else "ACCEPTED",
                next_action="Reconcile " + str(issue) + " with " + producer
                if issue
                else "Use the tested local result.",
            )
            steps.append(step)
        results[route] = {
            "steps": steps,
            "status": "ACCEPTED"
            if all(s["status"] == "ACCEPTED" for s in steps)
            else "BLOCKED",
        }
    return {"journeys": results, "hosted_provider": "NOT_ASSESSED"}


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2]
    p = argparse.ArgumentParser()
    p.add_argument(
        "--incoming",
        type=Path,
        default=root / "docs/plans/ai-engine-kaizen/evidence/incoming",
    )
    p.add_argument(
        "--pins", type=Path, default=Path(__file__).with_name("ai-producer-pins.json")
    )
    args = p.parse_args()
    result = replay(args.incoming, json.loads(args.pins.read_bytes()))
    print(json.dumps(result, indent=2))
    raise SystemExit(
        0 if all(x["status"] == "ACCEPTED" for x in result["journeys"].values()) else 1
    )
