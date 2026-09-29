#!/usr/bin/env python3
"""Skill fan-in report for the Chwezi portfolio (M10-12-T05, UA-12). Read-only.

For every active SKILL.md of the named engines, count the inbound references by provenance:

EXTRACTED
  links      Markdown links from another skill's files (SKILL.md and its references) that
             resolve into this skill's folder, within or across engines.
  aliases    alias-registry entries (dev ``docs/skill-aliases.yml``) that target the skill.
  router     ``direct`` (the router or catalogue names the skill's path or slug), ``family``
             (it names the parent folder, for example ``skills/ai/*`` or ``01-strategic-vision``),
             ``glob`` (it routes by a discovery pattern such as ``skills/<category>/<skill-name>``)
             or ``none``.
INFERRED
  mentions   exact slug mentions in another skill's SKILL.md or references. A hyphenated slug
             must match a whole hyphenated token; a single-word slug counts only inside
             backticks or a path, so ordinary words are not read as mentions.
  fixtures   routing-fixture expectations (expected / expect / owner keys) naming the skill.

``zero_inbound`` is true when no other skill links to, mentions or aliases the skill. It is a
separate flag from reachability: reachability is not recomputed here. The P01 inventory
(docs/operations/skills-kaizen-evidence/2026-09-26/skill-inventory.jsonl) is the authority and
its classification is copied into each row. The M10-03 fixture adapters were not delivered, so
fixture files are read directly with a generic key walk (labelled ``fixture_reader: direct``).

The private political-essay engine is refused. Fan-in as an importance signal is adapted from
Egonex-AI/Understand-Anything (MIT, https://github.com/Egonex-AI/Understand-Anything, commit
b05cc3b20990afca537b4fc0a49b4d7fbdc65bb0); no code is copied.

Exit codes: 0 report written; 1 bad input; 3 NOT_ASSESSED (a named engine is absent).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath

import yaml

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
COORDINATION = "chwezi-engine-agents"
DEFAULT_INVENTORY = PACKAGE_ROOT / "docs" / "operations" / "skills-kaizen-evidence" / "2026-09-26" / "skill-inventory.jsonl"
PRIVATE = ("political-essay-skills",)
EXCLUDED_DIRS = frozenset({
    ".git", "node_modules", "__pycache__", ".claude", ".agents", ".codex", ".cursor", ".claude-plugin",
    ".codex-plugin", "plugin-cache", "plugins-cache", "archive", "archived", "templates", "_TEMPLATE",
    "projects", "vendor", "dist", "build",
})
ROUTER_FILES = ("AGENTS.md", "CLAUDE.md", "README.md", "SKILL.md", "skill_overview.md", "docs/skill-catalog.md")
FIXTURE_GLOBS = (
    "tests/routing-fixtures.json", "tests/routing-fixtures.yml", "tests/fixtures/routing.json",
    "tests/fixtures/routing-fixtures.json", "tests/skill-engine/routing-fixtures.json", "tests/routing/*.json",
    "scripts/routing_fixtures.yml",
)
FIXTURE_KEYS = {"expected", "expect", "owner", "expected_primary", "expected_skill"}
FRONT_MATTER_RE = re.compile(r"^﻿?---\r?\n.*?\r?\n---\r?\n?", re.DOTALL)
LINK_RE = re.compile(r"\]\(\s*<?([^)\s>#]+)")
TOKEN_RE = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


class PrivateEngineError(ValueError):
    pass


@dataclass
class Skill:
    engine: str
    slug: str
    name: str
    folder: Path          # absolute
    rel: str              # engine-relative folder, POSIX
    links: set[str] = field(default_factory=set)
    mentions: set[str] = field(default_factory=set)
    aliases: set[str] = field(default_factory=set)
    fixtures: int = 0
    router: str = "none"

    @property
    def key(self) -> str:
        return f"{self.engine}/{self.rel}"


def refuse_private(value: str | Path) -> None:
    lowered = str(value).replace("\\", "/").lower()
    if any(marker in lowered for marker in PRIVATE):
        raise PrivateEngineError(f"private engine refused: {value}")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace").replace("\r\n", "\n")
    except OSError:
        return ""


def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    except (OSError, yaml.YAMLError):
        return None


def frontmatter_name(text: str) -> str | None:
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return None
    try:
        data = yaml.safe_load(match.group(0).strip().strip("-"))
    except yaml.YAMLError:
        return None
    return str(data.get("name")) if isinstance(data, dict) and data.get("name") else None


# --------------------------------------------------------------------------- discovery

def catalog_paths(workspace: Path) -> dict[str, Path]:
    data = load_yaml(PACKAGE_ROOT / "catalog" / "engines.yaml") or {}
    paths = {str(entry["path"]): workspace / str(entry["path"]) for entry in data.get("engines", [])}
    paths[COORDINATION] = workspace / COORDINATION
    return paths


def active_skill_files(root: Path) -> list[Path]:
    """Active SKILL.md files: alias-registry active roots when declared, else the manifest glob."""
    roots: list[Path] = []
    aliases = load_yaml(root / "docs" / "skill-aliases.yml")
    if isinstance(aliases, dict):
        policy = aliases.get("active_skill_policy") or {}
        roots = [root / str(item) for item in policy.get("active_roots") or []]
    glob = "skills/**/SKILL.md"
    manifest = load_yaml(root / ".skills-engine" / "engine-manifest.yaml")
    if isinstance(manifest, dict):
        glob = str(((manifest.get("skills") or {}).get("discovery_glob")) or glob)
    found: list[Path] = []
    if roots:
        for base in roots:
            found.extend(base.rglob("SKILL.md"))
    else:
        prefix = glob.split("**", 1)[0].rstrip("/")
        base = root / prefix if prefix else root
        found.extend(base.rglob("SKILL.md") if base.is_dir() else [])
    result = []
    for path in found:
        rel_parts = path.relative_to(root).parts[:-1]
        if not rel_parts:
            continue  # a repository-level router SKILL.md is not a routed skill
        if any(part in EXCLUDED_DIRS or part.startswith(".") for part in rel_parts):
            continue
        result.append(path)
    return sorted(set(result))


def discover(engine: str, root: Path) -> list[Skill]:
    refuse_private(root)
    skills = []
    for path in active_skill_files(root):
        folder = path.parent
        rel = folder.relative_to(root).as_posix()
        name = frontmatter_name(read_text(path)) or folder.name
        skills.append(Skill(engine, folder.name.lower(), name, folder.resolve(), rel))
    return skills


# --------------------------------------------------------------------------- scanning

def norm_key(path: Path | str) -> str:
    return str(path).replace("\\", "/").rstrip("/").lower()


def owner_of(path: Path, folders: dict[str, "Skill"]) -> "Skill | None":
    """Deepest skill folder that contains the path (string walk; Path maths is slow on Windows)."""
    key = norm_key(path)
    while key:
        skill = folders.get(key)
        if skill is not None:
            return skill
        if "/" not in key:
            return None
        key = key.rsplit("/", 1)[0]
    return None


def skill_documents(skill: Skill, folders: dict[str, "Skill"]) -> list[Path]:
    docs = [skill.folder / "SKILL.md"]
    refs = skill.folder / "references"
    if refs.is_dir():
        docs.extend(p for p in sorted(refs.rglob("*.md")) if owner_of(p, folders) is skill)
    return docs


def scan(skills: list[Skill], roots: dict[str, Path]) -> None:
    folders = {norm_key(s.folder): s for s in skills}
    by_slug: dict[str, list[Skill]] = defaultdict(list)
    for skill in skills:
        by_slug[skill.slug].append(skill)
    for source in skills:
        for doc in skill_documents(source, folders):
            text = read_text(doc)
            body = FRONT_MATTER_RE.sub("", text, count=1)
            # EXTRACTED: Markdown links that resolve into another skill's folder.
            for target in LINK_RE.findall(body):
                if re.match(r"^[a-z]+:", target):
                    continue
                resolved = os.path.normpath(os.path.join(str(doc.parent), target))
                owner = owner_of(resolved, folders)
                if owner is not None and owner is not source:
                    owner.links.add(source.key)
            # INFERRED: exact slug mentions.
            tokens = Counter(TOKEN_RE.findall(body.lower()))
            for token in tokens:
                for target in by_slug.get(token, ()):
                    if target is source:
                        continue
                    if "-" in token or re.search(rf"(`{re.escape(token)}`|/{re.escape(token)}(/|\b))", body.lower()):
                        target.mentions.add(source.key)


def scan_aliases(skills: list[Skill], roots: dict[str, Path]) -> None:
    by_rel = {(s.engine, s.rel): s for s in skills}
    for engine, root in roots.items():
        data = load_yaml(root / "docs" / "skill-aliases.yml")
        if not isinstance(data, dict):
            continue
        values: list[str] = []
        for key in ("inactive_skill_aliases", "finance_canonical_duplicates"):
            section = data.get(key) or {}
            if isinstance(section, dict):
                values.extend(str(v) for v in section.values())
        for planned in (data.get("planned_routes") or {}).values():
            if isinstance(planned, dict):
                values.extend(str(v) for v in planned.get("absorb") or [])
        for value in values:
            value = value.strip("/")
            target = by_rel.get((engine, value))
            if target is None:
                slug = PurePosixPath(value).name.lower()
                matches = [s for s in skills if s.engine == engine and s.slug == slug]
                target = matches[0] if len(matches) == 1 else None
            if target is not None:
                target.aliases.add(f"{engine}/docs/skill-aliases.yml")


def scan_router(skills: list[Skill], roots: dict[str, Path]) -> None:
    for engine, root in roots.items():
        manifest = load_yaml(root / ".skills-engine" / "engine-manifest.yaml") or {}
        router = ((manifest.get("router") or {}).get("path")) if isinstance(manifest, dict) else None
        names = list(dict.fromkeys([*(filter(None, [router])), *ROUTER_FILES]))
        text = "\n".join(read_text(root / name) for name in names if (root / name).is_file()).lower()
        glob_route = bool(re.search(r"<category>/<skill[-_ ]?name>|\*\*/skill\.md|<skill[-_ ]?name>/skill\.md", text))
        for skill in (s for s in skills if s.engine == engine):
            rel = skill.rel.lower()
            parent = str(PurePosixPath(rel).parent)
            last = PurePosixPath(parent).name
            if rel in text or f"`{skill.slug}`" in text or f"/{skill.slug}/" in text:
                skill.router = "direct"
            elif parent not in (".", "skills") and (
                re.search(rf"(?<![\w-]){re.escape(parent)}(?![\w-])", text)
                or re.search(rf"[`\s(]{re.escape(last)}/", text)
            ):
                skill.router = "family"
            elif glob_route:
                skill.router = "glob"


def walk_fixture(value, out: list[str]) -> None:
    if isinstance(value, dict):
        for key, item in value.items():
            if key in FIXTURE_KEYS and isinstance(item, str):
                out.append(item)
            elif key in FIXTURE_KEYS and isinstance(item, list):
                out.extend(str(x) for x in item if isinstance(x, str))
            else:
                walk_fixture(item, out)
    elif isinstance(value, list):
        for item in value:
            walk_fixture(item, out)


def fixture_files(root: Path) -> list[Path]:
    found: set[Path] = set()
    for pattern in FIXTURE_GLOBS:
        found.update(p for p in root.glob(pattern) if p.is_file())
    return sorted(found)


def scan_fixtures(skills: list[Skill], roots: dict[str, Path]) -> dict[str, list[str]]:
    used: dict[str, list[str]] = {}
    for engine, root in roots.items():
        names: list[str] = []
        files = fixture_files(root)
        used[engine] = [p.relative_to(root).as_posix() for p in files]
        for path in files:
            data = load_yaml(path)  # YAML is a superset of JSON
            walk_fixture(data, names)
        counts = Counter(PurePosixPath(n.strip().strip("/")).name.lower() for n in names)
        for skill in (s for s in skills if s.engine == engine):
            skill.fixtures = counts.get(skill.slug, 0) + (counts.get(skill.name.lower(), 0) if skill.name.lower() != skill.slug else 0)
    return used


def load_inventory(path: Path | None) -> dict[tuple[str, str], str]:
    if path is None or not path.is_file():
        return {}
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            result[(row["engine"], row["path"])] = row.get("classification", "")
    return result


def build(workspace: Path, engines: list[str], inventory: Path | None) -> tuple[int, dict]:
    known = catalog_paths(workspace)
    roots: dict[str, Path] = {}
    missing = []
    for engine in engines:
        refuse_private(engine)
        root = known.get(engine, workspace / engine)
        if not root.is_dir():
            missing.append(engine)
        else:
            roots[engine] = root.resolve()
    if missing:
        return 3, {"status": "NOT_ASSESSED", "missing_engines": missing}
    skills: list[Skill] = []
    for engine, root in roots.items():
        skills.extend(discover(engine, root))
    scan(skills, roots)
    scan_aliases(skills, roots)
    scan_router(skills, roots)
    fixtures_used = scan_fixtures(skills, roots)
    inventory_rows = load_inventory(inventory)
    rows = []
    for skill in sorted(skills, key=lambda s: (s.engine, s.rel)):
        inbound = skill.links | skill.mentions | skill.aliases
        rows.append({
            "engine": skill.engine, "skill": skill.rel, "name": skill.name,
            "extracted": {"links": len(skill.links), "aliases": len(skill.aliases), "router": skill.router},
            "inferred": {"mentions": len(skill.mentions), "fixtures": skill.fixtures},
            "inbound_skills": len(inbound),
            "cross_engine_inbound": sum(1 for key in inbound if not key.startswith(skill.engine + "/")),
            "zero_inbound": not inbound,
            "p01_classification": inventory_rows.get((skill.engine, f"{skill.rel}/SKILL.md"), "not_in_p01_inventory"),
        })
    per_engine = {}
    for engine in roots:
        engine_rows = [r for r in rows if r["engine"] == engine]
        per_engine[engine] = {
            "active_skills": len(engine_rows),
            "zero_inbound": sum(r["zero_inbound"] for r in engine_rows),
            "router_none": sum(r["extracted"]["router"] == "none" for r in engine_rows),
            "fixture_files": fixtures_used.get(engine, []),
        }
    payload = {
        "schema_version": "1.0", "tool": "skill_fanin", "status": "PASS",
        "fixture_reader": "direct (M10-03 adapters not delivered; generic expected/expect/owner key walk)",
        "reachability_source": "P01 skill-inventory.jsonl (not recomputed)",
        "engines": per_engine, "skills": rows,
    }
    return 0, payload


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only skill fan-in report.")
    parser.add_argument("--workspace-root", type=Path, default=PACKAGE_ROOT.parent)
    parser.add_argument("--engine", action="append", default=[], help="Engine folder (repeatable)")
    parser.add_argument("--all", action="store_true", help="All catalogued engines plus the coordination package")
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--json", action="store_true", help="Print the full JSON report")
    parser.add_argument("--out", type=Path, help="Write the JSON report to this file")
    args = parser.parse_args(argv)
    workspace = args.workspace_root.resolve()
    engines = list(args.engine)
    if args.all:
        engines = sorted(catalog_paths(workspace))
    if not engines:
        parser.error("name --engine or --all")
    try:
        code, payload = build(workspace, engines, args.inventory)
    except PrivateEngineError as exc:
        print(f"REFUSED: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8", newline="\n")
    if args.json:
        sys.stdout.write(text)
    elif code == 0:
        for engine, summary in payload["engines"].items():
            print(f"{engine}: active={summary['active_skills']} zero_inbound={summary['zero_inbound']} router_none={summary['router_none']}")
    else:
        print(f"NOT_ASSESSED: missing engines {payload['missing_engines']}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
