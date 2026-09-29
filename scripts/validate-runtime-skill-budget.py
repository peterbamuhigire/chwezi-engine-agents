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

sys.path.insert(0, str(Path(__file__).resolve().parent))
import lexical_routing  # noqa: E402  (shared Tier 2 index, M10-03-T01)

REPO_ROOT = Path(__file__).resolve().parents[1]
DISPOSITIONS = {"canonical_owner", "intentional_co_activation", "mirrored_domain_pack", "fix_differentiate", "fix_alias"}
STALE_BELOW = 0.60


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


def load_ownership(path: Path) -> tuple[dict[frozenset[str], dict[str, Any]], list[Finding]]:
    """Read the ownership register; return declared pairs keyed by frozenset of skill keys."""
    import yaml

    findings: list[Finding] = []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        return {}, [Finding("error", "ownership-unreadable", f"cannot read ownership register: {exc}", str(path))]
    if data.get("schema_version") != 1:
        findings.append(Finding("error", "ownership-schema", "schema_version must be 1", str(path)))
    declared: dict[frozenset[str], dict[str, Any]] = {}
    for index, entry in enumerate(data.get("pairs") or []):
        where = f"{path}#pairs[{index}]"
        if not isinstance(entry, dict):
            findings.append(Finding("error", "ownership-schema", "pair entry must be a mapping", where))
            continue
        skills = entry.get("skills")
        disposition = entry.get("disposition")
        if not isinstance(skills, list) or len(skills) < 2 or not all(isinstance(item, str) and "/" in item for item in skills):
            findings.append(Finding("error", "ownership-schema", "skills must list two or more <engine-id>/<skill> keys", where))
            continue
        if disposition not in DISPOSITIONS:
            findings.append(Finding("error", "ownership-schema", f"unknown disposition {disposition!r}", where))
        for required in ("reason", "decided_by", "decided_on", "review_after", "follow_up"):
            if not entry.get(required):
                findings.append(Finding("error", "ownership-schema", f"missing {required}", where))
        if disposition in {"canonical_owner", "fix_alias"} and entry.get("owner") not in skills:
            findings.append(Finding("error", "ownership-schema", "owner must be one of the declared skills", where))
        if disposition in {"intentional_co_activation", "mirrored_domain_pack"} and not entry.get("co_activate"):
            findings.append(Finding("error", "ownership-schema", "co_activate must list the engines that co-activate", where))
        for i, first in enumerate(skills):
            for second in skills[i + 1 :]:
                declared[frozenset((first, second))] = entry
    return declared, findings


def collision_scan(
    engines: list[tuple[str, Path]],
    error_threshold: float,
    warn_threshold: float,
    ownership: Path | None,
) -> tuple[int, dict[str, Any]]:
    """Union TF-IDF collision scan (M10-03-T01). Returns (exit_code, payload); exit 3 = NOT_ASSESSED."""
    findings: list[Finding] = []
    missing = [f"{engine_id} ({root})" for engine_id, root in engines if not root.is_dir()]
    if missing:
        payload = {"status": "NOT_ASSESSED", "reason": "sibling engine unavailable: " + ", ".join(missing), "findings": []}
        return 3, payload
    docs: list[lexical_routing.SkillDoc] = []
    per_engine: dict[str, int] = {}
    for engine_id, root in engines:
        found, issues = lexical_routing.discover_engine(engine_id, root)
        docs.extend(found)
        per_engine[engine_id] = len(found)
        findings.extend(Finding("warning", issue.code, issue.message, issue.path) for issue in issues)
    index = lexical_routing.LexicalIndex(docs)
    all_pairs = index.pairs(min(warn_threshold, STALE_BELOW))
    declared: dict[frozenset[str], dict[str, Any]] = {}
    if ownership is not None:
        declared, ownership_findings = load_ownership(ownership)
        findings.extend(ownership_findings)
    cross: list[dict[str, Any]] = []
    within: list[dict[str, Any]] = []
    scores: dict[frozenset[str], float] = {}
    for score, first, second in all_pairs:
        scores[frozenset((first, second))] = score
        if score < warn_threshold:
            continue
        same_engine = index.by_key[first].engine == index.by_key[second].engine
        entry = declared.get(frozenset((first, second)))
        row = {"score": score, "skills": [first, second], "declared": entry is not None, "disposition": entry.get("disposition") if entry else None}
        (within if same_engine else cross).append(row)
        if same_engine:
            if score >= error_threshold:
                findings.append(Finding("warning", "within-engine-collision", f"{first} <-> {second} cosine {score:.3f} (reported, not gated)"))
            continue
        if score >= error_threshold and entry is None:
            findings.append(Finding("error", "undeclared-collision", f"{first} <-> {second} cosine {score:.3f} >= {error_threshold} and not in the ownership register"))
        elif score >= error_threshold and entry.get("disposition") == "fix_differentiate":
            findings.append(Finding("error", "undifferentiated-collision", f"{first} <-> {second} cosine {score:.3f} is declared fix_differentiate but is still >= {error_threshold}"))
        elif score < error_threshold:
            findings.append(Finding("warning", "collision-warning", f"{first} <-> {second} cosine {score:.3f} >= {warn_threshold}"))
    for pair, entry in declared.items():
        unknown = sorted(key for key in pair if key not in index.by_key)
        if unknown:
            findings.append(Finding("warning", "ownership-unknown-skill", f"declared skill not found in the union: {', '.join(unknown)}"))
            continue
        score = scores.get(pair, 0.0)
        if score < STALE_BELOW and entry.get("disposition") != "fix_differentiate":
            findings.append(Finding("warning", "stale-declaration", f"{' <-> '.join(sorted(pair))} now scores {score:.3f} < {STALE_BELOW}"))
    errors = [finding for finding in findings if finding.severity == "error"]
    payload = {
        "status": "FAIL" if errors else "PASS",
        "label": "lexical proxy; not live routing (see agent-skills issue #620)",
        "skills": len(docs),
        "skills_per_engine": per_engine,
        "thresholds": {"error": error_threshold, "warn": warn_threshold},
        "cross_engine_pairs_ge_error": sum(row["score"] >= error_threshold for row in cross),
        "cross_engine_pairs_ge_warn": len(cross),
        "within_engine_pairs_ge_error": sum(row["score"] >= error_threshold for row in within),
        "undeclared_pairs_ge_error": sum(finding.code == "undeclared-collision" for finding in findings),
        "cross_engine_pairs": cross,
        "within_engine_pairs": [row for row in within if row["score"] >= error_threshold],
        "findings": [asdict(finding) for finding in findings],
    }
    return (1 if errors else 0), payload


def run_collisions(args: argparse.Namespace) -> int:
    try:
        if args.root:
            engines = [(root.resolve().name, root) for root in args.root]
            for _engine_id, root in engines:
                lexical_routing.refuse_private(root.resolve())
        else:
            engines = lexical_routing.load_catalog_engines(args.catalog, args.workspace_root)
    except lexical_routing.PrivateEngineError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 2
    code, payload = collision_scan(engines, args.collision_error, args.collision_warn, args.ownership)
    if args.format == "json":
        print(json.dumps(payload, indent=2))
    elif code == 3:
        print(f"NOT_ASSESSED: {payload['reason']}")
    else:
        print(
            f"{payload['status']}: skills={payload['skills']} cross>={args.collision_error}: {payload['cross_engine_pairs_ge_error']} "
            f"cross>={args.collision_warn}: {payload['cross_engine_pairs_ge_warn']} undeclared>={args.collision_error}: "
            f"{payload['undeclared_pairs_ge_error']} ({payload['label']})"
        )
        for finding in payload["findings"]:
            if finding["severity"] == "error":
                print(f"- {finding['code']}: {finding['message']}")
    if code == 3:
        return 3
    return 0 if args.report_only else code


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
    parser.add_argument("--collisions", action="store_true", help="Run the union TF-IDF collision scan over the catalogued engines (or --root) instead of the budget check.")
    parser.add_argument("--collision-error", type=float, default=0.75, help="Cross-engine cosine at or above which an undeclared pair is an error.")
    parser.add_argument("--collision-warn", type=float, default=0.50, help="Cosine at or above which a pair is reported as a warning.")
    parser.add_argument("--ownership", type=Path, help="Ownership register (evals/routing/ownership.yaml) declaring owners or co-activation.")
    parser.add_argument("--catalog", type=Path, default=REPO_ROOT / "catalog" / "engines.yaml", help="Engine catalogue used by --collisions when no --root is given.")
    parser.add_argument("--workspace-root", type=Path, default=REPO_ROOT.parent, help="Directory holding the sibling engine checkouts.")
    args = parser.parse_args()

    if args.collisions:
        return run_collisions(args)

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
