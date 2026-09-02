#!/usr/bin/env python3
"""Validate the skill metadata exposed to an agent runtime.

The normal engine guardrail checks one repository at a time. This validator
checks the assembled runtime catalog, where local engines and plugins compete
for one discovery-context budget.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


DEFAULT_MAX_SKILLS = 200
DEFAULT_MAX_DESCRIPTION_CHARS = 400
DEFAULT_MAX_TOTAL_DESCRIPTION_CHARS = 50_000
DEFAULT_MAX_TOTAL_METADATA_CHARS = 60_000
FRONTMATTER_RE = re.compile(r"^\ufeff?---\r?\n(.*?)\r?\n---\r?\n?", re.DOTALL)


@dataclass(frozen=True)
class SkillRecord:
    name: str
    description: str
    path: str


@dataclass(frozen=True)
class Finding:
    severity: str
    code: str
    message: str
    path: str | None = None


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> tuple[str, str] | None:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return None
    lines = match.group(1).splitlines()
    name: str | None = None
    description: str | None = None
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("name:"):
            name = _unquote(line.split(":", 1)[1])
        if line.startswith("description:"):
            value = line.split(":", 1)[1].strip()
            if value in {">", ">-", ">+", "|", "|-", "|+"}:
                parts: list[str] = []
                index += 1
                while index < len(lines):
                    continuation = lines[index]
                    if continuation and not continuation[0].isspace():
                        index -= 1
                        break
                    parts.append(continuation.strip())
                    index += 1
                separator = "\n" if value.startswith("|") else " "
                description = separator.join(part for part in parts if part)
            else:
                description = _unquote(value)
        index += 1
    if not name or description is None:
        return None
    return name, " ".join(description.split())


def discover(roots: list[Path], excluded_dirs: set[str]) -> tuple[list[SkillRecord], list[Finding]]:
    records: list[SkillRecord] = []
    findings: list[Finding] = []
    seen_paths: set[Path] = set()
    for root in roots:
        root = root.resolve()
        if not root.exists():
            findings.append(Finding("error", "missing-root", f"runtime root does not exist: {root}", str(root)))
            continue
        if not root.is_dir():
            findings.append(Finding("error", "invalid-root", f"runtime root is not a directory: {root}", str(root)))
            continue
        for path in sorted(root.rglob("SKILL.md")):
            if any(part in excluded_dirs for part in path.parts):
                continue
            if path in seen_paths:
                continue
            seen_paths.add(path)
            try:
                parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError) as exc:
                findings.append(Finding("error", "read-error", f"cannot read {path}: {exc}", str(path)))
                continue
            if parsed is None:
                findings.append(Finding("error", "invalid-frontmatter", "missing name or description frontmatter", str(path)))
                continue
            name, description = parsed
            records.append(SkillRecord(name, description, str(path)))
    return records, findings


def configured_plugin_roots(config_path: Path, cache_root: Path) -> tuple[list[Path], list[Finding]]:
    findings: list[Finding] = []
    try:
        import tomllib

        config: dict[str, Any] = tomllib.loads(config_path.read_text(encoding="utf-8"))
    except (ImportError, OSError, UnicodeError, ValueError) as exc:
        return [], [Finding("error", "plugin-config", f"cannot read plugin configuration {config_path}: {exc}", str(config_path))]
    configured = config.get("plugins", {})
    roots: list[Path] = []
    if not isinstance(configured, dict):
        return [], [Finding("error", "plugin-config", "plugins section is not a table", str(config_path))]
    for plugin_id, settings in sorted(configured.items()):
        if not isinstance(settings, dict) or settings.get("enabled") is not True:
            continue
        if not isinstance(plugin_id, str) or "@" not in plugin_id:
            findings.append(Finding("error", "plugin-config", f"invalid enabled plugin identifier: {plugin_id!r}", str(config_path)))
            continue
        plugin_name, marketplace = plugin_id.split("@", 1)
        plugin_dir = cache_root / marketplace / plugin_name
        if not plugin_dir.is_dir():
            findings.append(Finding("error", "plugin-cache", f"enabled plugin cache is missing: {plugin_dir}", str(plugin_dir)))
            continue
        candidates = [child for child in plugin_dir.iterdir() if child.is_dir() and any(child.rglob("SKILL.md"))]
        if any(child.name == "latest" for child in candidates):
            candidates = [child for child in candidates if child.name == "latest"]
        else:
            candidates.sort(key=lambda child: child.stat().st_mtime, reverse=True)
            candidates = candidates[:1]
        if candidates:
            roots.append(candidates[0])
    return roots, findings


def evaluate(
    records: list[SkillRecord],
    findings: list[Finding],
    max_skills: int,
    max_description_chars: int,
    max_total_description_chars: int,
    max_total_metadata_chars: int,
    catalog_records: list[SkillRecord] | None = None,
) -> list[Finding]:
    result = list(findings)
    governed_records = records if catalog_records is None else catalog_records
    if len(governed_records) > max_skills:
        result.append(Finding("error", "skill-count", f"{len(governed_records)} governed skills exceeds runtime cap {max_skills}"))
    by_name: dict[str, list[SkillRecord]] = defaultdict(list)
    for record in records:
        by_name[record.name].append(record)
        if record in governed_records and len(record.description) > max_description_chars:
            result.append(
                Finding(
                    "error",
                    "description-length",
                    f"description is {len(record.description)} characters; max is {max_description_chars}",
                    record.path,
                )
            )
    for name, duplicates in sorted(by_name.items()):
        if len(duplicates) > 1:
            paths = ", ".join(record.path for record in duplicates)
            result.append(Finding("error", "duplicate-name", f"skill name {name!r} appears more than once: {paths}"))
    description_chars = sum(len(record.description) for record in records)
    metadata_chars = sum(len(record.name) + len(record.description) for record in records)
    if description_chars > max_total_description_chars:
        result.append(Finding("error", "description-budget", f"descriptions total {description_chars} characters; max is {max_total_description_chars}"))
    if metadata_chars > max_total_metadata_chars:
        result.append(Finding("error", "metadata-budget", f"skill metadata totals {metadata_chars} characters; max is {max_total_metadata_chars}"))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", action="append", type=Path, help="Exact runtime directory to scan; repeatable.")
    parser.add_argument("--config", type=Path, help="Codex TOML config; enabled plugin roots are discovered from the cache.")
    parser.add_argument("--plugin-cache", type=Path, help="Plugin cache root used with --config.")
    parser.add_argument("--catalog-root", action="append", type=Path, help="Repository-owned catalog root governed by count and per-description limits; repeatable. Defaults to all roots.")
    parser.add_argument("--exclude-dir", action="append", default=[".git", "node_modules", "__pycache__"])
    parser.add_argument("--max-skills", type=int, default=DEFAULT_MAX_SKILLS)
    parser.add_argument("--max-description-chars", type=int, default=DEFAULT_MAX_DESCRIPTION_CHARS)
    parser.add_argument("--max-total-description-chars", type=int, default=DEFAULT_MAX_TOTAL_DESCRIPTION_CHARS)
    parser.add_argument("--max-total-metadata-chars", type=int, default=DEFAULT_MAX_TOTAL_METADATA_CHARS)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--report-only", action="store_true", help="Report findings but return success.")
    args = parser.parse_args()

    roots = list(args.root or [])
    initial_findings: list[Finding] = []
    if bool(args.config) != bool(args.plugin_cache):
        parser.error("--config and --plugin-cache must be supplied together")
    plugin_roots: list[Path] = []
    if args.config and args.plugin_cache:
        plugin_roots, plugin_findings = configured_plugin_roots(args.config, args.plugin_cache)
        roots.extend(plugin_roots)
        initial_findings.extend(plugin_findings)
    if not roots:
        parser.error("at least one --root or a --config/--plugin-cache pair is required")
    records, discovered_findings = discover(roots, set(args.exclude_dir))
    initial_findings.extend(discovered_findings)
    catalog_records = None
    if args.catalog_root:
        catalog_records, catalog_findings = discover(args.catalog_root, set(args.exclude_dir))
        initial_findings.extend(catalog_findings)
    findings = evaluate(records, initial_findings, args.max_skills, args.max_description_chars, args.max_total_description_chars, args.max_total_metadata_chars, catalog_records)
    description_chars = sum(len(record.description) for record in records)
    metadata_chars = sum(len(record.name) + len(record.description) for record in records)
    payload = {
        "status": "FAIL" if findings else "PASS",
        "skills": len(records),
        "governed_skills": len(records if catalog_records is None else catalog_records),
        "plugin_roots": [str(root) for root in plugin_roots],
        "description_chars": description_chars,
        "metadata_chars": metadata_chars,
        "limits": {
            "max_skills": args.max_skills,
            "max_description_chars": args.max_description_chars,
            "max_total_description_chars": args.max_total_description_chars,
            "max_total_metadata_chars": args.max_total_metadata_chars,
        },
        "findings": [asdict(finding) for finding in findings],
    }
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    else:
        print(f"{payload['status']}: skills={len(records)} description_chars={description_chars} metadata_chars={metadata_chars} findings={len(findings)}")
        for finding in findings:
            location = f" [{finding.path}]" if finding.path else ""
            print(f"- {finding.code}: {finding.message}{location}")
    return 2 if findings and not args.report_only else 0


if __name__ == "__main__":
    raise SystemExit(main())
