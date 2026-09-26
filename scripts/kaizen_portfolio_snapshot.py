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


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=root, capture_output=True, check=False,
        text=True, encoding="utf-8", errors="replace",
    )
    if result.returncode:
        raise RuntimeError(f"git {' '.join(args)} failed in {root}: {result.stderr.strip()}")
    return result.stdout.strip()


def file_sha(path: Path) -> str | None:
    return sha256(path.read_bytes()) if path.is_file() else None


def collect_engine(root: Path, name: str) -> tuple[dict, list[dict]]:
    if not root.is_dir():
        raise FileNotFoundError(root)
    status = git(root, "status", "--porcelain=v1", "--untracked-files=all")
    dirty = []
    for line in sorted(status.splitlines()):
        if not line:
            continue
        rel = line[3:]
        path = root / rel
        dirty.append({
            "status": line[:2].strip(),
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
    print(json.dumps({"engines": len(engines), "raw_skill_file_total": len(skills), "coordination_skill_file_total": len(coordination_skills), "output_dir": str(out)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
