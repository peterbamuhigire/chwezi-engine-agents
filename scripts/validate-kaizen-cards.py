#!/usr/bin/env python3
"""Validate the coordination Kaizen operation references.

This is a structural check. It does not certify domain judgement, currentness,
provider behaviour, or production integration.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


CARD_SPECS = {
    "h2": {
        "filename": "agentic-h2-readiness-card.md",
        "required_headings": (
            "## Purpose and scope",
            "## Input and provenance contract",
            "## Decision procedure",
            "## Failure, unknown and denied states",
            "## Acceptance oracle",
            "## Synthetic exercise",
            "## Handoff and rollback",
            "## Evidence labels",
        ),
        "required_terms": ("READY_FOR_H2_PILOT", "H3", "NOT_ASSESSED"),
    },
    "horizons": {
        "filename": "three-horizon-ai-adoption-card.md",
        "required_headings": (
            "## Purpose and scope",
            "## Input and provenance contract",
            "## Decision procedure",
            "## Failure, unknown and denied states",
            "## Acceptance oracle",
            "## Synthetic exercise",
            "## Handoff and rollback",
            "## Evidence labels",
        ),
        "required_terms": ("H1", "H2", "H3", "NOT_ASSESSED"),
    },
    "runbook": {
        "filename": "task-runbook-and-integration-evidence.md",
        "required_headings": (
            "## Purpose and scope",
            "## Input and provenance contract",
            "## Decision procedure",
            "## Failure, unknown and denied states",
            "## Acceptance oracle",
            "## Synthetic interoperability and identity case",
            "## Handoff and rollback",
            "## Evidence labels",
        ),
        "required_terms": ("core/contracts/handoff.yaml", "BLOCKED", "NOT_ASSESSED"),
    },
}


def card_issues(path: Path, profile: str) -> list[str]:
    """Return structural issues for one card without making semantic claims."""

    spec = CARD_SPECS[profile]
    if not path.is_file():
        return [f"missing card: {path}"]
    text = path.read_text(encoding="utf-8")
    issues = [f"missing heading {heading!r}" for heading in spec["required_headings"] if heading not in text]
    issues.extend(f"missing required term {term!r}" for term in spec["required_terms"] if term not in text)
    for label in ("Observation", "Inference"):
        if label not in text:
            issues.append(f"missing evidence label {label!r}")
    return issues


def readme_issues(readme: Path) -> list[str]:
    if not readme.is_file():
        return [f"missing README: {readme}"]
    text = readme.read_text(encoding="utf-8")
    return [
        f"README does not link {spec['filename']}"
        for spec in CARD_SPECS.values()
        if spec["filename"] not in text
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--card", type=Path, help="validate one card instead of the default set")
    parser.add_argument("--profile", choices=sorted(CARD_SPECS), help="profile for --card")
    args = parser.parse_args(argv)

    if bool(args.card) != bool(args.profile):
        parser.error("--card and --profile must be supplied together")

    failures: list[str] = []
    if args.card:
        failures.extend(f"{args.profile}: {issue}" for issue in card_issues(args.card, args.profile))
    else:
        operation_dir = args.root / "docs" / "operations"
        for profile, spec in CARD_SPECS.items():
            path = operation_dir / spec["filename"]
            issues = card_issues(path, profile)
            if issues:
                failures.extend(f"{profile}: {issue}" for issue in issues)
            else:
                print(f"PASS {path.relative_to(args.root)}")
        failures.extend(readme_issues(args.root / "README.md"))

    if failures:
        for issue in failures:
            print(f"FAIL {issue}", file=sys.stderr)
        return 1
    if args.card:
        print(f"PASS {args.card}")
    print("Coordination Kaizen card structure valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
