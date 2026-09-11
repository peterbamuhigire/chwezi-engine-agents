#!/usr/bin/env python3
"""Validate lifecycle and invocation metadata for exposed skill roots."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

FRONTMATTER = re.compile(r"^\ufeff?---\r?\n(.*?)\r?\n---", re.DOTALL)
LIFECYCLES = {"promoted", "experimental", "deprecated", "reference-only"}
INVOCATIONS = {"implicit", "explicit", "both"}


def inspect_root(root: Path) -> list[str]:
    findings: list[str] = []
    if not root.is_dir():
        return [f"root does not exist: {root}"]

    for path in sorted(root.rglob("SKILL.md")):
        if any(part.startswith(".") for part in path.relative_to(root).parts):
            continue
        text = path.read_text(encoding="utf-8")
        match = FRONTMATTER.match(text)
        if not match:
            findings.append(f"{path}: missing or malformed frontmatter")
            continue
        try:
            frontmatter = yaml.safe_load(match.group(1)) or {}
        except yaml.YAMLError as exc:
            findings.append(f"{path}: invalid YAML: {exc}")
            continue
        metadata = frontmatter.get("metadata") or {}
        if not isinstance(metadata, dict):
            findings.append(f"{path}: metadata must be a mapping")
            continue

        lifecycle = metadata.get("lifecycle", "promoted")
        if lifecycle not in LIFECYCLES:
            findings.append(f"{path}: unsupported lifecycle {lifecycle!r}")
        elif lifecycle != "promoted":
            findings.append(f"{path}: {lifecycle!r} skill is exposed through a promoted runtime root")

        invocation = metadata.get("invocation", "implicit")
        if invocation not in INVOCATIONS:
            findings.append(f"{path}: unsupported invocation {invocation!r}")
        elif invocation == "explicit":
            description = str(frontmatter.get("description", "")).lower()
            if "explicit" not in description and "direct user" not in description:
                findings.append(f"{path}: explicit invocation is not stated in the description")

    for alias in sorted(root.rglob("ALIAS.md")):
        if (alias.parent / "SKILL.md").exists():
            findings.append(f"{alias.parent}: SKILL.md and ALIAS.md cannot both be exposed")

    return findings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", action="append", required=True, help="Exact exposed skill root; repeatable")
    args = parser.parse_args()
    findings: list[str] = []
    for value in args.root:
        findings.extend(inspect_root(Path(value).resolve()))
    if findings:
        for finding in findings:
            print(f"[FAIL] {finding}")
        print(f"skill-lifecycle: findings={len(findings)}")
        return 1
    print(f"skill-lifecycle: roots={len(args.root)} findings=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
