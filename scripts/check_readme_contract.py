#!/usr/bin/env python3
"""Check the README layout contract that ``scripts/validate-portfolio-craft.ps1`` enforces, on any host. Read-only.

Rule ``capabilities-in-lead-h2``: each catalogued engine's ``README.md`` has the heading ``## Capabilities`` or
``## Capability map`` among its first four H2 headings. The PowerShell script is Windows-only and no host
without ``pwsh`` ran it, so a README rewrite on 31 October 2026 removed the heading from ten engines without
any check noticing. This port gives Linux, macOS and CI the same answer.

The port mirrors the PowerShell rule exactly, so the two cannot disagree:

* an H2 is any line that starts with ``## ``, whether or not it sits inside a code fence;
* a heading matches when the whole line equals ``## Capabilities`` or ``## Capability map``, ignoring case
  (PowerShell ``-in`` is case-insensitive) but not trailing spaces;
* line endings (LF or CRLF) and a leading byte-order mark do not matter.

Engines are found through ``scripts/lib/engine_roots.py`` (``--engines-root``, ``CHWEZI_ENGINES_ROOT`` or
``--workspace-root``). Output names engines by catalogue id, never by path.

Exit codes: 0 every checked README passes; 1 at least one README fails or is missing; 3 an engine checkout is
missing or ambiguous and nothing else failed (NOT_ASSESSED, never a pass).
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import engine_roots  # noqa: E402

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
LEAD_H2_COUNT = 4
ACCEPTED = {"## capabilities", "## capability map"}


@dataclass
class Finding:
    engine: str
    rule: str
    detail: str


def lead_h2(text: str, count: int = LEAD_H2_COUNT) -> list[str]:
    """The first ``count`` lines that start with ``## ``, as the PowerShell rule reads them."""
    return [line for line in text.splitlines() if line.startswith("## ")][:count]


def has_capabilities(headings: list[str]) -> bool:
    return any(heading.casefold() in ACCEPTED for heading in headings)


def check_readme(engine: str, readme: Path) -> list[Finding]:
    if not readme.is_file():
        return [Finding(engine, "readme-missing", "README.md not found")]
    headings = lead_h2(readme.read_text(encoding="utf-8-sig", errors="replace"))
    if has_capabilities(headings):
        return []
    found = " | ".join(headings) if headings else "no H2 headings"
    return [Finding(engine, "capabilities-in-lead-h2",
                    f"README must have '## Capability map' or '## Capabilities' within its first {LEAD_H2_COUNT} "
                    f"H2 headings (found: {found})")]


def run(package: Path, roots: list[Path]) -> tuple[list[Finding], list[dict], int]:
    findings: list[Finding] = []
    not_assessed: list[dict] = []
    checked = 0
    catalog = yaml.safe_load((package / "catalog" / "engines.yaml").read_text(encoding="utf-8"))
    for entry in catalog["engines"]:
        resolution = engine_roots.resolve_engine(entry, roots)
        if not resolution.found:
            not_assessed.append({"engine": str(entry["id"]), "reason": engine_roots.describe(resolution)})
            continue
        checked += 1
        findings.extend(check_readme(str(entry["id"]), resolution.path / "README.md"))
    return findings, not_assessed, checked


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--engines-root", type=Path, action="append", default=[],
                        help="folder that holds engine checkouts (repeatable; also CHWEZI_ENGINES_ROOT)")
    parser.add_argument("--workspace-root", type=Path, default=PACKAGE_ROOT.parent)
    parser.add_argument("--package-root", type=Path, default=PACKAGE_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    roots = engine_roots.roots_from(args.engines_root, fallback=args.workspace_root)
    findings, not_assessed, checked = run(args.package_root.resolve(), roots)
    if args.json:
        print(json.dumps({"checked": checked, "findings": [asdict(f) for f in findings], "not_assessed": not_assessed}, indent=2))
    else:
        for f in findings:
            print(f"[{f.rule}] {f.engine}: {f.detail}")
        for item in not_assessed:
            print(f"NOT_ASSESSED {item['engine']}: {item['reason']}")
        print(f"checked {checked} engine READMEs; findings {len(findings)}; not assessed {len(not_assessed)}")
    if findings:
        return 1
    return 3 if not_assessed else 0


if __name__ == "__main__":
    sys.exit(main())
