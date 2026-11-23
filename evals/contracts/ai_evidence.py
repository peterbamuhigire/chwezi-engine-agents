"""Validate a versioned AI evidence reference in a legacy-compatible handoff."""

import hashlib
import json
from pathlib import Path


def inspect_evidence(root, reference, expected):
    identity = {
        key: expected.get(key)
        for key in ("producer", "consumer", "case_id", "criterion")
    }

    def outcome(status, reason):
        return {**identity, "status": status, "next_action": reason}

    if not isinstance(reference, dict) or reference.get("format") != "ai-evidence/1":
        return outcome(
            "NOT_ASSESSED",
            "Request the versioned evidence reference from the producer.",
        )
    if not isinstance(reference.get("path"), str) or not reference["path"]:
        return outcome("BLOCKED", "Supply the project-relative evidence path.")
    base = Path(root).resolve()
    path = (base / reference["path"]).resolve()
    if path == base or not path.is_relative_to(base) or not path.is_file():
        return outcome(
            "BLOCKED", "Return a readable evidence file within the allowed checkout."
        )
    raw = path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != reference.get("sha256"):
        return outcome(
            "BLOCKED", "Reconcile the digest against the producer's accepted revision."
        )
    try:
        document = json.loads(raw)
    except (ValueError, UnicodeError):
        return outcome("BLOCKED", "Return a valid JSON evidence record.")
    if not isinstance(document, dict):
        return outcome("BLOCKED", "Return a JSON object for this criterion.")
    for key in (*identity, "input_revision", "output_revision"):
        if not expected.get(key) or document.get(key) != expected[key]:
            return outcome(
                "BLOCKED",
                "Re-run the expected " + key + " and bind the resulting evidence.",
            )
    if not document.get("limitations") or not document.get("next_action"):
        return outcome(
            "BLOCKED", "State the limits of the measurement and its next action."
        )
    if (
        "observed" not in document
        or document["observed"] is None
        or expected.get("expected_outcome") is None
        or type(document["observed"]) is not type(expected["expected_outcome"])
        or document["observed"] != expected["expected_outcome"]
    ):
        return outcome(
            "BLOCKED", "Inspect the measured result and rerun the acceptance case."
        )
    return outcome("ACCEPTED", document["next_action"])


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("handoff", type=Path)
    parser.add_argument(
        "expectation",
        type=Path,
        help="Independent reviewer expectation for the referenced example",
    )
    args = parser.parse_args()
    handoff = json.loads(args.handoff.read_bytes())
    expected = json.loads(args.expectation.read_bytes())
    refs = [
        item
        for item in handoff.get("evidence", [])
        if isinstance(item, dict) and item.get("format") == "ai-evidence/1"
    ]
    if len(refs) != 1:
        parser.exit(2, "Expected one versioned evidence reference in this handoff.\n")
    result = inspect_evidence(args.handoff.parent, refs[0], expected)
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["status"] == "ACCEPTED" else 1)
