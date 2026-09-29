#!/usr/bin/env python3
"""Deterministic engine tours for the Chwezi portfolio (M10-12-T06, UA-09).

For each catalogued engine plus this coordination package, writes
``docs/engine-tours/<engine-id>.json`` and ``.md``: seven to twelve fixed-order steps, each citing
one to five existing paths. Sentences come from fixed templates filled with data; no model is
involved. JSON uses sorted keys and carries no timestamp; ``generated_from_commit`` is the only
revision field.

Steps (in order; a step with no data is omitted, except step 9, which reports NOT_ASSESSED):
 1 Purpose (README)            6 Gates (manifest validation commands and catalogue validators)
 2 Router (AGENTS.md, bridge)  7 Routing evidence (fixture files and case counts)
 3 Engine contract (manifest)  8 Hooks (hooks/hooks.json events)
 4 Skill layout                9 Adding a skill (skill-writing skill or CONTRIBUTING.md)
 5 Hub skills (T05 fan-in)    10 Cross-cutting engines (orchestrator handoff table)

Modes:
  (default)            generate tours for --engine/--all into --out-dir
  --check              read-only: fail on a dangling path or a manifest/catalogue gate command
                       missing from the tour; a changed engine HEAD alone is a ``stale`` warning
  --check-links FILE   read-only: every relative Markdown link and every ``engine-id:path`` route
                       in FILE resolves on disk

Exit codes: 0 clean; 1 findings or bad input; 3 NOT_ASSESSED (a named engine is absent).
The step discipline (fan-in for hub selection, depth to step order, 5-15 step contract) is adapted
from Egonex-AI/Understand-Anything (MIT, https://github.com/Egonex-AI/Understand-Anything, commit
b05cc3b20990afca537b4fc0a49b4d7fbdc65bb0); no code is copied.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path, PurePosixPath

import yaml

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
COORDINATION = "chwezi-engine-agents"
DEFAULT_OUT = PACKAGE_ROOT / "docs" / "engine-tours"
ORCHESTRATOR = "core/instructions/engine-orchestrator.md"
PRIVATE = ("political-essay-skills",)
SKILL_WRITING_NAMES = ("skill-writing", "skill-authoring", "writing-skills")
MIN_STEPS, MAX_STEPS = 7, 12
CROSS_CUTTING = (
    ("chwezi-accounting-doctrine", "finance, accounting, tax or statutory work"),
    ("design-system-skills", "any change to how an output looks"),
    ("digital-research-skills", "current, uncertain or source-sensitive claims"),
)


def load_module(name: str):
    spec = importlib.util.spec_from_file_location(name, PACKAGE_ROOT / "scripts" / f"{name}.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


FANIN = load_module("skill_fanin")


def load_yaml(path: Path):
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    except (OSError, yaml.YAMLError):
        return None


def one_line(text: str) -> str:
    return " ".join(str(text).split())


def catalog_entries(catalog: Path) -> list[dict]:
    data = load_yaml(catalog) or {}
    return [entry for entry in data.get("engines", []) if isinstance(entry, dict)]


def head_commit(root: Path) -> str:
    """HEAD of the repository whose top level is ``root``; otherwise 'not-a-git-checkout'."""
    try:
        top = subprocess.run(["git", "-C", str(root), "rev-parse", "--show-toplevel"], capture_output=True,
                             text=True, timeout=20, check=False).stdout.strip()
        if not top or Path(top).resolve() != root.resolve():
            return "not-a-git-checkout"
        return subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True,
                              timeout=20, check=False).stdout.strip() or "not-a-git-checkout"
    except (OSError, subprocess.SubprocessError):
        return "not-a-git-checkout"


def plural(count: int, noun: str) -> str:
    return f"{count} {noun}" + ("" if count == 1 else "s")


def readme_title(root: Path) -> str | None:
    try:
        for line in (root / "README.md").read_text(encoding="utf-8-sig").splitlines():
            if line.startswith("# "):
                return one_line(line[2:])
    except OSError:
        return None
    return None


def ref(folder: str, path: str) -> dict:
    return {"engine": folder, "path": path}


def command_paths(command: str, root: Path, folder: str) -> list[dict]:
    refs = []
    for token in re.split(r"\s+", command.replace("\\", "/")):
        token = token.strip("'\"")
        if token.startswith("./"):
            token = token[2:]
        if re.search(r"\.(py|ps1|sh|js|mjs)$", token) and (root / token).is_file():
            refs.append(ref(folder, token))
    return refs


def fixture_cases(path: Path) -> int:
    data = load_yaml(path)
    if isinstance(data, dict):
        for key in ("fixtures", "cases"):
            if isinstance(data.get(key), list):
                return len(data[key])
        return 0
    return len(data) if isinstance(data, list) else 0


def hook_events(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return []
    hooks = data.get("hooks") if isinstance(data, dict) else None
    return sorted(hooks) if isinstance(hooks, dict) else []


def handoff_rows(workspace: Path) -> dict[str, str]:
    text = (workspace / COORDINATION / ORCHESTRATOR)
    rows: dict[str, str] = {}
    if not text.is_file():
        return rows
    for line in text.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^\|\s*([^|]+?)\s*\|\s*`([^`]+)`\s*\|", line)
        if match and not match.group(1).startswith("Question"):
            rows[match.group(2)] = match.group(1)
    return rows


# --------------------------------------------------------------------------- tour building

def build_tour(engine_id: str, folder: str, root: Path, workspace: Path, catalog_entry: dict | None,
               fanin_rows: list[dict], handoff: dict[str, str]) -> dict:
    manifest = load_yaml(root / ".skills-engine" / "engine-manifest.yaml")
    manifest = manifest if isinstance(manifest, dict) else {}
    display = one_line(manifest.get("display_name") or readme_title(root) or engine_id)
    steps: list[dict] = []

    def add(title: str, text: str, paths: list[dict], data: dict | None = None) -> None:
        existing = [p for p in paths if (workspace / p["engine"] / p["path"]).exists()]
        unique = []
        for item in existing:
            if item not in unique:
                unique.append(item)
        if not unique:  # never cite a missing path; fall back to the engine's router file
            unique = [ref(folder, ((manifest.get("router") or {}).get("path")) or "AGENTS.md")]
        steps.append({"title": title, "text": text, "paths": unique[:5], "data": data or {}})

    # 1 Purpose
    add("Purpose", f"Start with README.md: it states what {display} is for and what it does not cover.",
        [ref(folder, "README.md")])

    # 2 Router
    router = ((manifest.get("router") or {}).get("path")) or (catalog_entry or {}).get("router") or "AGENTS.md"
    router_paths = [ref(folder, router)]
    catalog_router = (catalog_entry or {}).get("router")
    if catalog_router and catalog_router != router:
        router_paths.append(ref(folder, catalog_router))
    bridge = (root / "CLAUDE.md").is_file()
    if bridge:
        router_paths.append(ref(folder, "CLAUDE.md"))
    add("Router", f"Read {router} before choosing any skill; it is the routing source of truth."
        + (" CLAUDE.md is a bridge that imports it." if bridge else ""), router_paths,
        {"router": router, "catalogue_router": catalog_router or router})

    # 3 Engine contract
    if manifest:
        agent = manifest.get("agent_integration") or {}
        glob = ((manifest.get("skills") or {}).get("discovery_glob")) or "not declared"
        approvals = sorted(agent.get("approval_required_for") or [])
        forbidden = sorted(agent.get("forbidden_operations") or [])
        add("Engine contract",
            f"The engine manifest declares the router ({router}), the discovery glob ({glob}), "
            f"{len(approvals)} approval-gated operations and {len(forbidden)} forbidden operations.",
            [ref(folder, ".skills-engine/engine-manifest.yaml")],
            {"discovery_glob": glob, "approval_required_for": approvals, "forbidden_operations": forbidden})
    else:
        add("Engine contract",
            "This package has no engine manifest; its contract is the catalogue of engines it routes to "
            "and its own router.", [ref(folder, "catalog/engines.yaml"), ref(folder, "AGENTS.md")],
            {"catalogued_engines": len(catalog_entries(workspace / COORDINATION / "catalog" / "engines.yaml"))})

    # 4 Skill layout
    categories = Counter(PurePosixPath(row["skill"]).parent.as_posix() for row in fanin_rows)
    top = sorted(categories.items(), key=lambda item: (-item[1], item[0]))
    layout_paths = [ref(folder, name) for name, _ in top[:4]]
    add("Skill layout",
        f"{plural(len(fanin_rows), 'active SKILL.md file')} in {plural(len(categories), 'folder')}; the largest are "
        + ", ".join(f"{name} ({count})" for name, count in top[:4]) + "." if fanin_rows else
        "No active SKILL.md files were found under the discovery glob.",
        layout_paths or [ref(folder, router)],
        {"active_skills": len(fanin_rows), "folders": dict(sorted(categories.items()))})

    # 5 Hub skills
    hubs = sorted(fanin_rows, key=lambda r: (-r["inbound_skills"], -r["inferred"]["fixtures"], r["skill"]))[:5]
    if hubs:
        add("Hub skills",
            "The skills other skills lean on most (inbound links, mentions and aliases): "
            + ", ".join(f"{PurePosixPath(h['skill']).name} ({h['inbound_skills']})" for h in hubs) + ".",
            [ref(folder, f"{h['skill']}/SKILL.md") for h in hubs],
            {"hubs": [{"skill": h["skill"], "inbound_skills": h["inbound_skills"]} for h in hubs],
             "source": "scripts/skill_fanin.py"})

    # 6 Gates
    commands = []
    for item in manifest.get("validation") or []:
        if isinstance(item, dict) and item.get("command"):
            commands.append(one_line(item["command"]))
    validators = (catalog_entry or {}).get("validators") or []
    if isinstance(validators, str):
        validators = [v.strip() for v in validators.split("|")]
    commands.extend(one_line(v) for v in validators)
    if engine_id == COORDINATION:
        commands.extend(sorted(
            f"python -X utf8 scripts/{p.name}" if p.suffix == ".py" else f"pwsh scripts/{p.name}"
            for p in (root / "scripts").glob("validate-*") if p.suffix in {".py", ".ps1"}))
    commands = list(dict.fromkeys(commands))
    gate_paths: list[dict] = []
    for command in commands:
        gate_paths.extend(p for p in command_paths(command, root, folder) if p not in gate_paths)
    add("Gates", f"Run {'this check' if len(commands) == 1 else f'these {len(commands)} checks'} before claiming the engine is healthy; an unavailable "
        "check is NOT_ASSESSED, never a pass.", gate_paths or [ref(folder, router)], {"commands": commands})

    # 7 Routing evidence
    fixtures = FANIN.fixture_files(root)
    if fixtures:
        counts = {p.relative_to(root).as_posix(): fixture_cases(p) for p in fixtures}
        add("Routing evidence",
            f"Routing fixtures record which skill should win for a realistic request: {sum(counts.values())} "
            f"cases in {plural(len(counts), 'file')}.", [ref(folder, name) for name in counts], {"fixture_cases": counts})

    # 8 Hooks
    events = hook_events(root / "hooks" / "hooks.json")
    if events:
        add("Hooks", f"hooks/hooks.json registers these events: {', '.join(events)}.",
            [ref(folder, "hooks/hooks.json")], {"events": events})

    # 9 Adding a skill
    writing = sorted(row["skill"] for row in fanin_rows if PurePosixPath(row["skill"]).name in SKILL_WRITING_NAMES)
    if writing:
        add("Adding a skill", f"Follow {writing[0]}/SKILL.md before adding or changing a skill.",
            [ref(folder, f"{writing[0]}/SKILL.md")], {"status": "PASS"})
    elif (root / "CONTRIBUTING.md").is_file():
        add("Adding a skill", "Follow CONTRIBUTING.md before adding or changing a skill.",
            [ref(folder, "CONTRIBUTING.md")], {"status": "PASS"})
    else:
        add("Adding a skill", "No skill-writing skill or CONTRIBUTING.md was found: NOT_ASSESSED.",
            [ref(folder, router)], {"status": "NOT_ASSESSED"})

    # 10 Cross-cutting engines
    question = handoff.get(engine_id)
    others = [f"{eid} for {why}" for eid, why in CROSS_CUTTING if eid != engine_id]
    add("Cross-cutting engines",
        (f"In a cross-engine handoff this engine answers: \"{question}\" " if question else "")
        + "Add " + "; ".join(others) + ". They activate alongside this engine, never instead of it.",
        [ref(COORDINATION, ORCHESTRATOR)], {"handoff_question": question or "not listed"})

    return {
        "schema_version": "1.0", "engine_id": engine_id, "folder": folder, "display_name": display,
        "generated_from_commit": head_commit(root), "generator": "scripts/generate_engine_tour.py",
        "steps": [{"number": i + 1, **step} for i, step in enumerate(steps)],
    }


def render_markdown(tour: dict) -> str:
    lines = [
        f"# {tour['display_name']} — engine tour", "",
        f"Generated by `{tour['generator']}` from commit `{tour['generated_from_commit'][:12]}` of "
        f"`{tour['folder']}`. Do not edit by hand; regenerate after engine changes. Paths are "
        "workspace-relative.", "",
    ]
    for step in tour["steps"]:
        lines.append(f"## {step['number']}. {step['title']}")
        lines.append("")
        lines.append(step["text"])
        lines.append("")
        for path in step["paths"]:
            lines.append(f"- `{path['engine']}/{path['path']}`")
        commands = step["data"].get("commands")
        if commands:
            lines.append("")
            lines.append("```text")
            lines.extend(commands)
            lines.append("```")
        lines.append("")
    return "\n".join(lines).rstrip("\n") + "\n"


def engine_list(workspace: Path, catalog: Path, names: list[str], all_engines: bool) -> list[tuple[str, str, dict | None]]:
    entries = catalog_entries(catalog)
    if all_engines:
        chosen = [(str(e["id"]), str(e["path"]), e) for e in entries]
        chosen.append((COORDINATION, COORDINATION, None))
        return chosen
    result = []
    for name in names:
        entry = next((e for e in entries if name in (e.get("id"), e.get("path"))), None)
        if entry:
            result.append((str(entry["id"]), str(entry["path"]), entry))
        else:
            result.append((name, name, None))
    return result


def refuse_private(name: str) -> None:
    if any(marker in name.lower() for marker in PRIVATE):
        raise SystemExit(f"REFUSED: private engine {name}")


def generate(workspace: Path, catalog: Path, targets, out_dir: Path) -> int:
    missing = [folder for _, folder, _ in targets if not (workspace / folder).is_dir()]
    if missing:
        print(f"NOT_ASSESSED: engines absent: {', '.join(missing)}")
        return 3
    folders = [folder for _, folder, _ in targets]
    _, fanin = FANIN.build(workspace, folders, None)
    handoff = handoff_rows(workspace)
    out_dir.mkdir(parents=True, exist_ok=True)
    bad = 0
    for engine_id, folder, entry in targets:
        rows = [r for r in fanin["skills"] if r["engine"] == folder]
        tour = build_tour(engine_id, folder, workspace / folder, workspace, entry, rows, handoff)
        count = len(tour["steps"])
        if not MIN_STEPS <= count <= MAX_STEPS:
            print(f"FAIL: {engine_id} has {count} steps (contract {MIN_STEPS}-{MAX_STEPS})")
            bad += 1
        (out_dir / f"{engine_id}.json").write_text(json.dumps(tour, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
                                                  encoding="utf-8", newline="\n")
        (out_dir / f"{engine_id}.md").write_text(render_markdown(tour), encoding="utf-8", newline="\n")
        print(f"wrote {engine_id}: {count} steps")
    return 1 if bad else 0


def check(workspace: Path, catalog: Path, targets, out_dir: Path) -> int:
    findings, warnings, not_assessed = [], [], []
    for engine_id, folder, entry in targets:
        root = workspace / folder
        path = out_dir / f"{engine_id}.json"
        if not root.is_dir():
            not_assessed.append(folder)
            continue
        if not path.is_file():
            findings.append(f"{engine_id}: tour missing ({path.name})")
            continue
        tour = json.loads(path.read_text(encoding="utf-8"))
        if not MIN_STEPS <= len(tour.get("steps", [])) <= MAX_STEPS:
            findings.append(f"{engine_id}: {len(tour.get('steps', []))} steps outside {MIN_STEPS}-{MAX_STEPS}")
        for step in tour.get("steps", []):
            if not 1 <= len(step.get("paths", [])) <= 5:
                findings.append(f"{engine_id}: step {step.get('number')} cites {len(step.get('paths', []))} paths")
            for item in step.get("paths", []):
                if not (workspace / item["engine"] / item["path"]).exists():
                    findings.append(f"{engine_id}: dangling path {item['engine']}/{item['path']}")
        gates = next((s for s in tour.get("steps", []) if s.get("title") == "Gates"), {"data": {}})
        listed = set(gates["data"].get("commands", []))
        manifest = load_yaml(root / ".skills-engine" / "engine-manifest.yaml") or {}
        required = [one_line(v["command"]) for v in manifest.get("validation") or [] if isinstance(v, dict) and v.get("command")]
        validators = (entry or {}).get("validators") or []
        required += [one_line(v) for v in (validators if isinstance(validators, list) else str(validators).split("|"))]
        for command in required:
            if command not in listed:
                findings.append(f"{engine_id}: gate command missing from tour: {command}")
        head = head_commit(root)
        if head != tour.get("generated_from_commit"):
            warnings.append(f"{engine_id}: stale (tour from {str(tour.get('generated_from_commit'))[:12]}, HEAD {head[:12]})")
    for line in warnings:
        print(f"WARNING stale: {line}")
    for line in findings:
        print(f"FAIL: {line}")
    if findings:
        return 1
    if not_assessed:
        print(f"NOT_ASSESSED: engines absent: {', '.join(not_assessed)}")
        return 3
    print(f"PASS: {len(targets)} tours; dangling paths 0; missing gate commands 0; stale warnings {len(warnings)}")
    return 0


def check_links(workspace: Path, catalog: Path, file: Path) -> int:
    text = file.read_text(encoding="utf-8")
    folders = {str(e["id"]): str(e["path"]) for e in catalog_entries(catalog)}
    folders.update({str(e["path"]): str(e["path"]) for e in catalog_entries(catalog)})
    folders[COORDINATION] = COORDINATION
    problems, checked = [], 0
    for target in re.findall(r"\]\(\s*<?([^)\s>]+)", text):
        target = target.split("#", 1)[0]
        if not target or re.match(r"^[a-z]+:", target):
            continue
        checked += 1
        if not (file.parent / target).exists():
            problems.append(f"broken link: {target}")
    for engine, path in re.findall(r"`([a-z0-9-]+):([^`\s]+)`", text):
        if engine not in folders:
            continue
        checked += 1
        if not (workspace / folders[engine] / path).exists():
            problems.append(f"unresolved route: {engine}:{path}")
    for line in problems:
        print(f"FAIL: {line}")
    if problems:
        return 1
    print(f"PASS: {checked} links and routes resolve in {file.name}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Deterministic engine tours (read-only except the out dir).")
    parser.add_argument("--workspace-root", type=Path, default=PACKAGE_ROOT.parent)
    parser.add_argument("--catalog", type=Path, default=PACKAGE_ROOT / "catalog" / "engines.yaml")
    parser.add_argument("--engine", action="append", default=[])
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--check-links", type=Path)
    args = parser.parse_args(argv)
    workspace = args.workspace_root.resolve()
    if args.check_links:
        return check_links(workspace, args.catalog, args.check_links.resolve())
    if not args.all and not args.engine:
        parser.error("name --engine or --all")
    targets = engine_list(workspace, args.catalog, args.engine, args.all)
    for _, folder, _ in targets:
        refuse_private(folder)
    if args.check:
        return check(workspace, args.catalog, targets, args.out_dir)
    return generate(workspace, args.catalog, targets, args.out_dir)


if __name__ == "__main__":
    raise SystemExit(main())
