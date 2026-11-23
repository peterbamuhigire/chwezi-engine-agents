"""Evaluate public synthetic routing requests separately from independent task outcomes."""

import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts/lib"))
from retrieval_metrics import BM25, reciprocal_rank


def evaluate(fixture):
    owners = fixture["owners"]
    observations = []
    for q in fixture["queries"]:
        permitted = [key for key in q["permitted"] if key in owners]

        def tokens(s):
            return re.findall(r"[a-z0-9]+", s.lower())

        ranked = []
        if permitted:
            index = BM25().fit(
                [{"description": tokens(owners[key])} for key in permitted]
            )
            scores = zip(index.scores(tokens(q["request"])), permitted)
            ranked = [key for score, key in sorted(scores, reverse=True) if score > 0]
        expected = q["owner"]
        execution = "NOT_ASSESSED"
        if "observed_output" in q:
            execution = (
                "PASS" if q["observed_output"] == q["expected_output"] else "FAIL"
            )
        observations.append(
            {
                "id": q["id"],
                "family": q["family"],
                "ranked": ranked,
                "label_source": q["label_source"],
                "split": q["split"],
                "route_match": (ranked[0] if ranked else None) == expected,
                "reciprocal_rank": reciprocal_rank(ranked, [expected])
                if expected
                else None,
                "execution": execution,
            }
        )
    families = {row["family"] for row in observations}
    return {
        "rows": observations,
        "request_count": len(observations),
        "family_count": len(families),
        "route_matches": sum(r["route_match"] for r in observations),
        "abstentions": sum(not r["ranked"] for r in observations),
        "task_passed": sum(r["execution"] == "PASS" for r in observations),
        "task_assessed": sum(r["execution"] in ("PASS", "FAIL") for r in observations),
        "rank_control": reciprocal_rank(["X", "Y"], ["Y"]),
    }


if __name__ == "__main__":
    print(
        json.dumps(
            evaluate(
                json.loads(Path(__file__).with_name("ai-route-cases.json").read_bytes())
            ),
            indent=2,
        )
    )
