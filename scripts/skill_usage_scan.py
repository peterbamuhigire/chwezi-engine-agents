#!/usr/bin/env python3
"""Local-only skill usage scan (M10-12-T11, CV-05). Read-only over transcripts.

Counts reads of engine SKILL.md files in Claude Code transcripts (``~/.claude/projects/**/*.jsonl``)
over a named window and maps each path to a skill through the P01 inventory.

EXTRACTED  ``Read`` tool calls on a SKILL.md path; ``Skill`` tool invocations whose name maps to
           exactly one inventoried skill.
INFERRED   shell commands (Bash, PowerShell) that print a SKILL.md (cat, head, tail, sed, less,
           more, type, Get-Content, gc), and Codex ``exec`` cells that do the same.

Privacy: only ``tool_use`` blocks and their input paths or commands are read. No prompt, response
or tool-result text is emitted. Transcript folders of the private political-essay engine are
skipped unread, and any path under ``political-essay-skills`` is dropped before counting. Output
(a per-skill CSV and a summary JSON) must lie outside every Git repository; a path inside the
workspace root is refused unless ``--allow-repo-output``.

Interpretation: zero reads in the window is dead-load evidence for consolidation review, never a
retirement decision. The data covers one machine and one user's sessions.

Codex sessions are parsed only through ``--codex-root`` and only when the recognised shape
(``response_item`` records whose payload is a ``custom_tool_call`` named ``exec``) is present;
otherwise Codex is NOT_ASSESSED.

"Measure before cutting" is adapted from JuliusBrussee/caveman (skill text MIT,
https://github.com/JuliusBrussee/caveman, commit 2fd153c); no BSL code is used or installed.

Exit codes: 0 written; 1 bad input or refused output path; 3 NOT_ASSESSED (no transcripts).
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = PACKAGE_ROOT / "docs" / "operations" / "skills-kaizen-evidence" / "2026-09-26"
DEFAULT_INVENTORIES = (EVIDENCE / "skill-inventory.jsonl", EVIDENCE / "coordination-skill-inventory.jsonl")
PRIVATE = "political-essay-skills"
PRINT_RE = re.compile(r"(?<![\w-])(cat|head|tail|sed|less|more|type|get-content|gc|bat|nl)(?![\w-])", re.I)
SKILL_PATH_RE = re.compile(r"([A-Za-z]:)?[^\s'\"`|;<>()*?]*?/?([A-Za-z0-9_.-]+)/((?:[^\s'\"`|;<>()*?]+/)*?)SKILL\.md", re.I)
SHELL_TOOLS = {"bash", "powershell"}
# Folder renames inside the window: reads under the old folder name count for the current engine.
FOLDER_RENAMES = {"/skills-web-dev/": "/chwezi-dev-engine/"}


def norm(path: str) -> str:
    return path.replace("\\\\", "/").replace("\\", "/")


def load_inventory(paths: list[Path]) -> tuple[dict[tuple[str, str], str], dict[str, list[tuple[str, str]]]]:
    rows: dict[tuple[str, str], str] = {}
    names: dict[str, list[tuple[str, str]]] = {}
    for path in paths:
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            engine = str(row.get("engine") or "chwezi-engine-agents")
            if PRIVATE in engine:
                continue
            key = (engine, str(row["path"]))
            rows[key] = str(row.get("frontmatter_name") or "")
            if row.get("frontmatter_name"):
                names.setdefault(str(row["frontmatter_name"]).lower(), []).append(key)
    return rows, names


class Mapper:
    def __init__(self, inventory: dict[tuple[str, str], str]):
        self.inventory = inventory
        self.engines = sorted({engine for engine, _ in inventory}, key=len, reverse=True)
        self.by_lower = {(e.lower(), p.lower()): (e, p) for e, p in inventory}

    def map_path(self, raw: str, cwd: str | None = None) -> tuple[str, str] | None | str:
        """Return (engine, rel) for an inventoried SKILL.md, 'private' for the private engine, or None.

        A relative path is resolved against the session's working directory (the ``cwd`` field
        of the transcript record); a Git Bash drive prefix (/c/...) is folded to c:/..."""
        path = norm(raw).lower().strip()
        if path.startswith("./"):
            path = path[2:]
        if re.match(r"^/[a-z]/", path):
            path = f"{path[1]}:{path[2:]}"
        if cwd and not re.match(r"^[a-z]:/|^/|^~", path):
            path = norm(cwd).lower().rstrip("/") + "/" + path
        for old, new in FOLDER_RENAMES.items():
            path = path.replace(old, new)
        if PRIVATE in path:
            return "private"
        for engine in self.engines:
            marker = f"/{engine.lower()}/"
            index = path.rfind(marker)
            if index < 0 and path.startswith(engine.lower() + "/"):
                index, marker = -1, engine.lower() + "/"
            if index >= 0 or path.startswith(engine.lower() + "/"):
                rel = path[index + len(marker):] if index >= 0 else path[len(marker):]
                hit = self.by_lower.get((engine.lower(), rel))
                if hit:
                    return hit
        return None


CD_RE = re.compile(r"(?:^|[;&|\n]\s*)(?:cd|set-location|pushd)\s+(?:-literalpath\s+|-path\s+)?([\"']?)([^\s;&|\"']+)\1", re.I)


def command_cwd(command: str, cwd: str | None) -> str | None:
    """The folder a shell command changes into first (cd, Set-Location, pushd), else the session cwd."""
    match = CD_RE.search(command)
    if not match:
        return cwd
    target = norm(match.group(2))
    if re.match(r"^[A-Za-z]:/|^/", target) or cwd is None:
        return target
    return norm(cwd).rstrip("/") + "/" + target


def skill_paths_in(text: str) -> list[str]:
    return [m.group(0) for m in SKILL_PATH_RE.finditer(norm(text))]


def parse_time(value: str | None) -> dt.datetime | None:
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


class Counts:
    def __init__(self) -> None:
        self.extracted: Counter = Counter()
        self.inferred: Counter = Counter()
        self.unmapped = 0
        self.private_dropped = 0
        self.records = 0

    def add(self, mapper: Mapper, raw: str, kind: str, cwd: str | None = None) -> None:
        hit = mapper.map_path(raw, cwd)
        if hit == "private":
            self.private_dropped += 1
        elif hit is None:
            self.unmapped += 1
        else:
            (self.extracted if kind == "extracted" else self.inferred)[hit] += 1


def in_window(stamp: dt.datetime | None, since: dt.datetime, until: dt.datetime) -> bool:
    return stamp is not None and since <= stamp < until


def scan_claude(root: Path, mapper: Mapper, names: dict, since, until, counts: Counts) -> int:
    files = 0
    for path in sorted(root.rglob("*.jsonl")):
        if "political-essay" in str(path).lower():
            continue
        files += 1
        with path.open(encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if '"tool_use"' not in line:
                    continue
                try:
                    record = json.loads(line)
                except ValueError:
                    continue
                if not in_window(parse_time(record.get("timestamp")), since, until):
                    continue
                message = record.get("message")
                content = message.get("content") if isinstance(message, dict) else None
                if not isinstance(content, list):
                    continue
                for block in content:
                    if not isinstance(block, dict) or block.get("type") != "tool_use":
                        continue
                    name = str(block.get("name") or "")
                    data = block.get("input") if isinstance(block.get("input"), dict) else {}
                    counts.records += 1
                    cwd = record.get("cwd") if isinstance(record.get("cwd"), str) else None
                    if name == "Read" and str(data.get("file_path", "")).lower().endswith("skill.md"):
                        counts.add(mapper, str(data["file_path"]), "extracted", cwd)
                    elif name == "Skill" and data.get("skill"):
                        skill = str(data["skill"]).split(":")[-1].lower()
                        keys = names.get(skill, [])
                        if len(keys) == 1:
                            counts.extracted[keys[0]] += 1
                    elif name.lower() in SHELL_TOOLS and isinstance(data.get("command"), str):
                        command = data["command"]
                        if "skill.md" in command.lower() and PRINT_RE.search(command):
                            for raw in skill_paths_in(command):
                                counts.add(mapper, raw, "inferred", command_cwd(command, cwd))
    return files


def scan_codex(root: Path, mapper: Mapper, since, until, counts: Counts) -> tuple[str, int]:
    files, recognised = 0, 0
    for path in sorted(root.rglob("*.jsonl")):
        files += 1
        cwd = None
        with path.open(encoding="utf-8", errors="replace") as handle:
            for line in handle:
                if '"custom_tool_call"' not in line and '"cwd"' not in line:
                    continue
                try:
                    record = json.loads(line)
                except ValueError:
                    continue
                payload = record.get("payload")
                if record.get("type") in {"session_meta", "turn_context"} and isinstance(payload, dict) and isinstance(payload.get("cwd"), str):
                    cwd = payload["cwd"]
                    continue
                if record.get("type") != "response_item" or not isinstance(payload, dict):
                    continue
                if payload.get("type") != "custom_tool_call" or payload.get("name") != "exec" or not isinstance(payload.get("input"), str):
                    continue
                recognised += 1
                if not in_window(parse_time(record.get("timestamp")), since, until):
                    continue
                text = payload["input"]
                if "skill.md" in text.lower() and PRINT_RE.search(text):
                    for raw in skill_paths_in(text):
                        counts.add(mapper, raw, "inferred", command_cwd(text, cwd))
    if files and recognised:
        return "PARSED", files
    return "NOT_ASSESSED", files


def inside_repository(path: Path) -> bool:
    for candidate in [path, *path.parents]:
        if (candidate / ".git").exists():
            return True
    return False


def deciles(values: list[int]) -> dict:
    if not values:
        return {}
    ordered = sorted(values)
    top = ordered[int(0.9 * (len(ordered) - 1))]
    bottom = ordered[int(0.1 * (len(ordered) - 1))]
    return {"top_decile_threshold": top, "bottom_decile_threshold": bottom,
            "skills_at_or_above_top": sum(v >= top for v in values), "skills_at_or_below_bottom": sum(v <= bottom for v in values)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Local-only SKILL.md usage scan (tool calls only).")
    parser.add_argument("--transcripts", type=Path, default=Path.home() / ".claude" / "projects")
    parser.add_argument("--codex-root", type=Path)
    parser.add_argument("--since", required=True, help="ISO date, inclusive")
    parser.add_argument("--until", required=True, help="ISO date, inclusive")
    parser.add_argument("--out", required=True, type=Path, help="Output folder outside every Git repository")
    parser.add_argument("--inventory", type=Path, action="append")
    parser.add_argument("--workspace-root", type=Path, default=Path(r"C:\wamp64\www"))
    parser.add_argument("--allow-repo-output", action="store_true")
    args = parser.parse_args(argv)

    out = args.out.resolve()
    workspace = args.workspace_root.resolve()
    if not args.allow_repo_output:
        within_workspace = out == workspace or workspace in out.parents
        if within_workspace or inside_repository(out):
            print(f"REFUSED: output path {out} is inside the workspace or a Git repository; "
                  "pass --allow-repo-output only for a deliberate, reviewed case", file=sys.stderr)
            return 1
    if not args.transcripts.is_dir():
        print(f"NOT_ASSESSED: transcripts folder absent: {args.transcripts}")
        return 3
    since = dt.datetime.fromisoformat(args.since).replace(tzinfo=dt.timezone.utc)
    until = (dt.datetime.fromisoformat(args.until) + dt.timedelta(days=1)).replace(tzinfo=dt.timezone.utc)
    inventory, names = load_inventory(args.inventory or list(DEFAULT_INVENTORIES))
    if not inventory:
        print("NOT_ASSESSED: P01 inventory unavailable")
        return 3
    mapper = Mapper(inventory)
    counts = Counts()
    claude_files = scan_claude(args.transcripts, mapper, names, since, until, counts)
    codex_status, codex_files = ("NOT_REQUESTED", 0)
    if args.codex_root:
        codex_status, codex_files = scan_codex(args.codex_root, mapper, since, until, counts) if args.codex_root.is_dir() else ("NOT_ASSESSED", 0)

    rows = []
    for key in sorted(inventory):
        extracted, inferred = counts.extracted.get(key, 0), counts.inferred.get(key, 0)
        rows.append({"engine": key[0], "skill_path": key[1], "extracted_reads": extracted,
                     "inferred_reads": inferred, "total_reads": extracted + inferred})
    per_engine: dict[str, dict] = {}
    for row in rows:
        entry = per_engine.setdefault(row["engine"], {"skills": 0, "never_read": 0, "reads": 0})
        entry["skills"] += 1
        entry["reads"] += row["total_reads"]
        entry["never_read"] += row["total_reads"] == 0
    summary = {
        "schema_version": "1.0", "tool": "skill_usage_scan",
        "window": {"since": args.since, "until": args.until},
        "sources": {"claude_transcript_files": claude_files, "tool_use_blocks_in_window": counts.records,
                    "codex": codex_status, "codex_files": codex_files},
        "totals": {"skills": len(rows), "extracted_reads": sum(counts.extracted.values()),
                   "inferred_reads": sum(counts.inferred.values()), "unmapped_skill_md_reads": counts.unmapped,
                   "private_engine_paths_dropped": counts.private_dropped,
                   "never_read": sum(r["total_reads"] == 0 for r in rows)},
        "per_engine": dict(sorted(per_engine.items())),
        "deciles": deciles([r["total_reads"] for r in rows]),
        "interpretation": "Zero reads is dead-load evidence for consolidation review, never a retirement decision; one machine, one user.",
    }
    out.mkdir(parents=True, exist_ok=True)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=["engine", "skill_path", "extracted_reads", "inferred_reads", "total_reads"], lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    (out / "skill-usage.csv").write_text(buffer.getvalue(), encoding="utf-8", newline="\n")
    (out / "skill-usage-summary.json").write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary["totals"], sort_keys=True))
    print(f"codex: {codex_status}; wrote {out / 'skill-usage.csv'} and skill-usage-summary.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
