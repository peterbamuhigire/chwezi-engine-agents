#!/usr/bin/env python3
"""Validate `<!-- rule:<id> -->` doctrine markers (M10-04-T13, IM-16 pilot).

A rule marker is an HTML comment that pins one doctrine line to a stable ID, so
later ablation evaluations and machine rules (`rules.json` `doctrine_ref`) can
cite that line. Markers are invisible when the Markdown is rendered.

Checks on the Markdown file:

1. Every marker ID matches ``^[a-z0-9]+(\\.[a-z0-9-]+)+$`` (lower-case, dotted).
2. Every marker ID is unique in the file.
3. A marker is followed by another marker or by a non-blank doctrine line.

When a banned-font JSON sidecar is present (default: the Markdown path with a
``.json`` suffix; override with ``--sidecar``), the check runs both ways:

4. Every family in the sidecar resolves to a marker
   (hardBan -> ``font.ban.hard.<slug>`` or a hardBanFamilyPrefixes marker;
   secondaryBan -> ``font.ban.secondary.<slug>``;
   conditionalPrimaryOnly -> ``font.conditional.<slug>``;
   monospaceBanned -> ``font.ban.mono.<slug>`` or any hard-ban resolution;
   bareSystemStackAlone -> ``font.ban.hard.bare-system-stack``).
5. Every ``font.*`` marker resolves to a sidecar entry. M10-02 registered the
   JSON as the canonical distributed copy (catalog/shared-assets.yaml,
   ``ai-slop-banned-fonts-json``) while the Markdown stays the authored source,
   so neither direction is allowed to drift.

Adapted in paraphrase from pbakaus/impeccable rule markers (Apache-2.0,
https://github.com/pbakaus/impeccable, commit 114ea1d3838fca73b253af45f873b9c4f5f213c8).
No code copied.

Exit codes: 0 PASS, 1 FAIL (findings), 2 usage or read error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

MARKER = re.compile(r"<!--\s*rule:(?P<id>[^\s>]*)\s*-->")
ID_FORMAT = re.compile(r"^[a-z0-9]+(\.[a-z0-9-]+)+$")


def slug(family: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", family.lower()).strip("-")


def read_markers(text: str) -> tuple[list[tuple[int, str]], list[str]]:
    findings: list[str] = []
    markers: list[tuple[int, str]] = []
    lines = text.splitlines()
    for number, line in enumerate(lines, start=1):
        for match in MARKER.finditer(line):
            markers.append((number, match.group("id")))
    seen: dict[str, int] = {}
    for number, rule_id in markers:
        if not ID_FORMAT.match(rule_id):
            findings.append(f"line {number}: marker ID {rule_id!r} does not match the dotted lower-case format")
        if rule_id in seen:
            findings.append(f"line {number}: duplicate marker ID {rule_id!r} (first at line {seen[rule_id]})")
        else:
            seen[rule_id] = number
        following = lines[number:]
        target = next((l for l in following if not MARKER.fullmatch(l.strip())), "")
        if not target.strip():
            findings.append(f"line {number}: marker {rule_id!r} is not followed by a doctrine line")
    return markers, findings


def check_sidecar(ids: set[str], sidecar: dict) -> list[str]:
    findings: list[str] = []
    prefixes = [p.get("prefix", "") for p in sidecar.get("hardBanFamilyPrefixes") or []]
    resolved: set[str] = set()

    def hard(family: str) -> str | None:
        own = f"font.ban.hard.{slug(family)}"
        if own in ids:
            return own
        for prefix in prefixes:
            if prefix and family.startswith(prefix) and f"font.ban.hard.{slug(prefix)}" in ids:
                return f"font.ban.hard.{slug(prefix)}"
        return None

    def need(kind: str, family: str, found: str | None, expected: str) -> None:
        if found:
            resolved.add(found)
        else:
            findings.append(f"sidecar {kind} family {family!r} has no marker (expected {expected})")

    for entry in sidecar.get("hardBan") or []:
        family = entry["family"]
        need("hardBan", family, hard(family), f"font.ban.hard.{slug(family)}")
    for prefix in prefixes:
        rule_id = f"font.ban.hard.{slug(prefix)}"
        need("hardBanFamilyPrefixes", prefix, rule_id if rule_id in ids else None, rule_id)
    for entry in sidecar.get("secondaryBan") or []:
        rule_id = f"font.ban.secondary.{slug(entry['family'])}"
        need("secondaryBan", entry["family"], rule_id if rule_id in ids else None, rule_id)
    for entry in sidecar.get("conditionalPrimaryOnly") or []:
        rule_id = f"font.conditional.{slug(entry['family'])}"
        need("conditionalPrimaryOnly", entry["family"], rule_id if rule_id in ids else None, rule_id)
    for entry in sidecar.get("monospaceBanned") or []:
        family = entry["family"]
        rule_id = f"font.ban.mono.{slug(family)}"
        need("monospaceBanned", family, rule_id if rule_id in ids else hard(family), rule_id)
    if sidecar.get("bareSystemStackAlone"):
        rule_id = "font.ban.hard.bare-system-stack"
        need("bareSystemStackAlone", "(system stack)", rule_id if rule_id in ids else None, rule_id)
    for rule_id in sorted(ids):
        if rule_id.startswith("font.") and rule_id not in resolved:
            findings.append(f"marker {rule_id!r} does not resolve to any sidecar entry")
    return findings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate <!-- rule:<id> --> doctrine markers.")
    parser.add_argument("markdown", type=Path)
    parser.add_argument("--sidecar", type=Path, help="banned-font JSON sidecar (default: <markdown>.json if present)")
    parser.add_argument("--no-sidecar", action="store_true", help="check marker format and uniqueness only")
    args = parser.parse_args(argv)
    try:
        text = args.markdown.read_text(encoding="utf-8")
        sidecar_path = None if args.no_sidecar else (args.sidecar or args.markdown.with_suffix(".json"))
        sidecar = None
        if sidecar_path is not None and (args.sidecar or sidecar_path.is_file()):
            sidecar = json.loads(sidecar_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"could not read input: {error}", file=sys.stderr)
        return 2
    markers, findings = read_markers(text)
    if not markers:
        findings.append("no rule markers found")
    if sidecar is not None:
        findings += check_sidecar({rule_id for _, rule_id in markers}, sidecar)
    for finding in findings:
        print(f"FAIL {args.markdown.name}: {finding}")
    status = "FAIL" if findings else "PASS"
    print(f"{status}: {len(markers)} marker(s); sidecar {'checked' if sidecar is not None else 'not used'}; findings {len(findings)}")
    return 1 if findings else 0


if __name__ == "__main__":
    raise SystemExit(main())
