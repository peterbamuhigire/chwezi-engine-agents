#!/usr/bin/env python3
"""Create a deterministic, read-only baseline for the eleven public skill engines.

The snapshot records raw SKILL.md files and repository working-tree state. It
does not infer router reachability or semantic equivalence; those require
engine-specific review before any entrypoint is changed.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path


ENGINE_NAMES = (
    "business-plan-skills",
    "chwezi-accounting-doctrine",
    "chwezi-dev-engine",
    "design-system-skills",
    "digital-research-engine",
    "linux-skills",
    "proposal-skills",
    "social-media-skills",
    "srs-skills",
    "website-skills",
    "windows-admin-engine-skills",
)
EXCLUDED_PARTS = {
    ".claude", ".codex", ".git", "adapters", "archive", "archived",
    "fixtures", "node_modules", "projects", "templates", "tests",
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git(root: Path, *args: str, strip: bool = True) -> str:
    """Run git and return stdout.

    ``strip=False`` keeps leading whitespace, which is significant in
    ``git status --porcelain`` output: a leading space is the empty index
    column, so stripping it shifts the path of the first dirty entry.
    """
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, check=False,
        text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed in {root}: {result.stderr.strip()}")
    return result.stdout.strip() if strip else result.stdout.rstrip("\r\n")


def parse_porcelain(status: str) -> list[tuple[str, str]]:
    """Return (status code, path) pairs from ``git status --porcelain=v1``.

    The first two columns are the index and worktree codes and column three is
    a space, so the path always starts at offset 3. Renames report the new path.
    """
    rows = []
    for line in status.splitlines():
        if len(line) < 4:
            continue
        rel = line[3:]
        if " -> " in rel:
            rel = rel.split(" -> ", 1)[1]
        if len(rel) >= 2 and rel[0] == rel[-1] == '"':
            rel = rel[1:-1]
        rows.append((line[:2].strip(), rel))
    return sorted(rows, key=lambda row: row[1])


def file_sha(path: Path) -> str | None:
    return sha256(path.read_bytes()) if path.is_file() else None


IMPORT_LINE_RE = re.compile(r"^@(\S+)\s*$")
MAX_IMPORT_DEPTH = 5


def router_size(root: Path, router: str = "CLAUDE.md") -> dict:
    """Measure the Claude router and everything it pulls in through ``@`` imports.

    Import lines (``@<path>`` alone on a line) are resolved relative to the
    importing file, recursively to ``MAX_IMPORT_DEPTH``, with a cycle guard.
    Each file counts once. Missing targets are recorded, not followed.
    """
    entry = root / router
    if not entry.is_file():
        return {"router_bytes": None, "router_import_bytes": 0,
                "router_effective_bytes": None, "router_imports": []}
    imports: list[dict] = []
    seen = {entry.resolve()}

    def follow(path: Path, depth: int) -> None:
        if depth >= MAX_IMPORT_DEPTH:
            return
        text = path.read_bytes().decode("utf-8-sig", errors="replace")
        for line in text.splitlines():
            match = IMPORT_LINE_RE.match(line.strip())
            if not match:
                continue
            target = (path.parent / match.group(1)).resolve()
            if target in seen:
                continue
            seen.add(target)
            try:
                rel = target.relative_to(root.resolve()).as_posix()
            except ValueError:
                rel = match.group(1)
            if not target.is_file():
                imports.append({"path": rel, "bytes": None, "missing": True})
                continue
            imports.append({"path": rel, "bytes": target.stat().st_size})
            follow(target, depth + 1)

    follow(entry, 0)
    router_bytes = entry.stat().st_size
    import_bytes = sum(item["bytes"] or 0 for item in imports)
    return {
        "router_bytes": router_bytes,
        "router_import_bytes": import_bytes,
        "router_effective_bytes": router_bytes + import_bytes,
        "router_imports": imports,
    }


def collect_engine(root: Path, name: str) -> tuple[dict, list[dict]]:
    if not root.is_dir():
        raise FileNotFoundError(root)
    status = git(root, "status", "--porcelain=v1", "--untracked-files=all", strip=False)
    dirty = []
    for code, rel in parse_porcelain(status):
        path = root / rel
        dirty.append({
            "status": code,
            "path": rel.replace("\\", "/"),
            "working_sha256": file_sha(path),
        })
    patch = git(root, "diff", "--binary", "HEAD")
    record = {
        "engine": name,
        "path": str(root.resolve()),
        "remote": git(root, "remote", "get-url", "origin"),
        "head": git(root, "rev-parse", "HEAD"),
        "branch": git(root, "branch", "--show-current"),
        "working_tree_clean": not dirty,
        "dirty_files": dirty,
        "tracked_diff_sha256": sha256(patch.encode("utf-8")),
        **router_size(root),
    }
    skill_rows = []
    discovered = []
    for directory, child_dirs, filenames in os.walk(root):
        child_dirs[:] = sorted(
            (child for child in child_dirs if child.casefold() not in {".git", "node_modules"}),
            key=str.casefold,
        )
        if "SKILL.md" in filenames:
            discovered.append(Path(directory) / "SKILL.md")
    for path in sorted(discovered, key=lambda p: p.relative_to(root).as_posix().casefold()):
        rel = path.relative_to(root)
        if any(part.casefold() in EXCLUDED_PARTS for part in rel.parts[:-1]):
            classification = "excluded_candidate"
        else:
            classification = "raw_candidate_reachability_unassessed"
        data = path.read_bytes()
        content = data.decode("utf-8-sig", errors="replace")
        frontmatter = re.match(r"^---\s*\n(.*?)\n---", content, re.S)
        name_match = re.search(r"^name:\s*(.+)", frontmatter.group(1), re.M) if frontmatter else None
        description_match = re.search(r"^description:\s*(.+)", frontmatter.group(1), re.M) if frontmatter else None
        skill_rows.append({
            "engine": name,
            "path": rel.as_posix(),
            "classification": classification,
            "bytes": len(data),
            "lines": len(content.splitlines()),
            "frontmatter_name": name_match.group(1).strip() if name_match else None,
            "description_present": bool(description_match),
            "sha256": sha256(data),
        })
    record["raw_skill_files"] = len(skill_rows)
    record["excluded_candidates"] = sum(row["classification"] == "excluded_candidate" for row in skill_rows)
    record["candidate_files"] = record["raw_skill_files"] - record["excluded_candidates"]
    record["router_reachability"] = "NOT_ASSESSED_BY_THIS_RAW_INVENTORY"
    return record, skill_rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace-root", type=Path, required=True)
    parser.add_argument("--coordination-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--as-of", required=True, help="ISO date captured in the baseline")
    args = parser.parse_args()
    root = args.workspace_root.resolve()
    out = args.output_dir.resolve()
    out.mkdir(parents=True, exist_ok=True)
    engines, skills = [], []
    for name in ENGINE_NAMES:
        record, rows = collect_engine(root / name, name)
        engines.append(record)
        skills.extend(rows)
    coordination, coordination_skills = collect_engine(args.coordination_root.resolve(), "chwezi-engine-agents")
    skills.sort(key=lambda row: (row["engine"].casefold(), row["path"].casefold()))
    coordination_skills.sort(key=lambda row: row["path"].casefold())
    for row in coordination_skills:
        row["scope"] = "coordination"
    baseline = {
        "as_of": args.as_of,
        "workspace_root": str(root),
        "generator": {"file": Path(__file__).name, "sha256": file_sha(Path(__file__).resolve())},
        "scope": "eleven public domain engines; the coordinator is recorded separately",
        "classification_limit": "raw filesystem classification only; router reachability and semantic active counts require engine-specific reconciliation",
        "engines": engines,
        "coordination_repository": coordination,
        "raw_skill_file_total": len(skills),
        "coordination_raw_skill_file_total": len(coordination_skills),
    }
    (out / "baseline.json").write_text(json.dumps(baseline, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    with (out / "skill-inventory.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for row in skills:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    with (out / "coordination-skill-inventory.jsonl").open("w", encoding="utf-8", newline="\n") as handle:
        for row in coordination_skills:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    summary = {"engines": len(engines), "raw_skill_file_total": len(skills), "coordination_skill_file_total": len(coordination_skills), "output_dir": str(out)}
    # Local-only: the machine's global Claude memory size is printed to the
    # console for the operator and never written into the public output files.
    global_router = Path.home() / ".claude" / "CLAUDE.md"
    summary["local_only_global_claude_md_bytes"] = global_router.stat().st_size if global_router.is_file() else None
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
