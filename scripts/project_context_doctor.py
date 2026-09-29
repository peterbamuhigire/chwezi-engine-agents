#!/usr/bin/env python3
"""Read-only doctor for a project's PROJECT.md (M10-12-T02, IM-11).

Checks the front matter against ``schemas/project-context.schema.json``, resolves every pointer
inside ``--workspace-root`` and reports stale, duplicated or visual content. It never writes,
never follows a pointer outside the workspace root, and treats every file it reads as data.

Contract: docs/operations/project-context-contract.md.

Exit codes: 0 no error-severity finding; 1 error findings or bad input; 3 NOT_ASSESSED (a
dependency is missing, the workspace root is absent, or a pointer names a repository folder that
is not present on this machine). NOT_ASSESSED is never a pass.

The durable-truth split and the report-only doctor idea are adapted from pbakaus/impeccable
(Apache-2.0, https://github.com/pbakaus/impeccable, commit
114ea1d3838fca73b253af45f873b9c4f5f213c8); no text is copied.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PACKAGE_ROOT / "schemas" / "project-context.schema.json"
BANNED_FONTS_REL = "chwezi-design-engine/doctrine/references/ai-slop-banned-fonts.json"
POINTER_FIELDS = (
    "srs_context", "research_context", "code_repository", "project_brief",
    "website_repository", "brand_brief", "design_tokens", "design_brief",
)
FRONT_MATTER_RE = re.compile(r"^﻿?---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)$", re.DOTALL)
# Six- and eight-digit hex always count; a three-digit form counts only with a letter, so an
# issue reference such as "#620" is not read as a colour.
HEX_RE = re.compile(r"(?<![\w&])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|(?=[0-9]*[a-fA-F])[0-9a-fA-F]{3})\b")
TYPEFACE_RE = re.compile(r"\b(font-family|typeface|font face|display face|body face|body font|heading font)\b\s*[:=]", re.IGNORECASE)
BUILTIN_BANNED = (
    "Inter", "Geist", "Roboto", "Roboto Mono", "Open Sans", "Lato", "Arial", "Fraunces",
    "IBM Plex", "Space Grotesk", "Instrument Serif", "Poppins", "Montserrat", "Nunito", "Nunito Sans",
)
TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".html", ".rst"}
MAX_DIR_FILES = 400
MAX_FILE_BYTES = 2_000_000
SHINGLE = 5
JACCARD_LIMIT = 0.5
SEVERITY_RANK = {"error": 2, "route": 1, "mention": 0}


class NotAssessed(Exception):
    """A dependency or input needed for the check is unavailable."""


def finding(code: str, severity: str, message: str, subject: dict, evidence: dict,
            fixes: list[str], next_action: str) -> dict:
    return {
        "code": code, "severity": severity, "message": message, "subject": subject,
        "evidence": evidence, "supported_fixes": fixes, "next_action": next_action,
    }


# --------------------------------------------------------------------------- parsing

def parse_project(path: Path) -> tuple[dict | None, str, str | None]:
    """Return (front matter or None, body, error)."""
    import yaml

    text = path.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    match = FRONT_MATTER_RE.match(text)
    if not match:
        return None, text, "no YAML front matter"
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, match.group(2), f"front matter is not valid YAML: {exc.__class__.__name__}"
    if not isinstance(data, dict):
        return None, match.group(2), "front matter is not a mapping"
    return normalise_dates(data), match.group(2), None


def normalise_dates(value):
    if isinstance(value, dict):
        return {key: normalise_dates(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalise_dates(item) for item in value]
    if isinstance(value, (dt.date, dt.datetime)):
        return value.isoformat()[:10]
    return value


def schema_findings(data: dict) -> list[dict]:
    from jsonschema import Draft202012Validator

    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    results: list[dict] = []
    for error in sorted(validator.iter_errors(data), key=lambda e: (list(e.absolute_path), e.message)):
        where = ".".join(str(part) for part in error.absolute_path) or "<root>"
        if error.validator == "required":
            missing = re.findall(r"'([^']+)' is a required property", error.message)
            field = missing[0] if missing else where
            results.append(finding(
                "project/field-missing", "error", f"required field '{field}' is missing",
                {"field": field}, {"location": where}, [f"add '{field}' with a short value"],
                "Add the field; take its value from the owning engine folder, not from memory."))
        else:
            results.append(finding(
                "project/schema-invalid", "error", f"{where}: {error.message}",
                {"field": where}, {"keyword": error.validator}, ["correct or remove the field"],
                "Match the field to schemas/project-context.schema.json."))
    return results


# --------------------------------------------------------------------------- pointers

def resolve_pointer(workspace: Path, value: str) -> tuple[Path | None, str | None]:
    """Return (resolved path, reason when outside the workspace)."""
    raw = str(value).strip()
    if re.match(r"^[A-Za-z]:", raw) or raw.startswith(("/", "\\")) or "\\" in raw:
        return None, "pointer is absolute or uses backslashes"
    parts = PurePosixPath(raw).parts
    if ".." in parts:
        return None, "pointer climbs with '..'"
    candidate = (workspace / Path(*parts)).resolve()
    try:
        candidate.relative_to(workspace)
    except ValueError:
        return None, "pointer resolves outside the workspace root"
    return candidate, None


def git_commit_date(path: Path) -> dt.date | None:
    folder = path if path.is_dir() else path.parent
    try:
        out = subprocess.run(
            ["git", "-C", str(folder), "log", "-1", "--format=%cs", "--", str(path)],
            capture_output=True, text=True, timeout=20, check=False,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return None
    try:
        return dt.date.fromisoformat(out) if out else None
    except ValueError:
        return None


def mtime_date(path: Path) -> dt.date:
    if path.is_file():
        return dt.date.fromtimestamp(path.stat().st_mtime)
    newest = path.stat().st_mtime
    for index, child in enumerate(iter_files(path)):
        if index >= MAX_DIR_FILES:
            break
        newest = max(newest, child.stat().st_mtime)
    return dt.date.fromtimestamp(newest)


def iter_files(folder: Path):
    for root, dirs, files in os.walk(folder):
        dirs[:] = sorted(d for d in dirs if d not in {".git", "node_modules", "vendor"} and not d.startswith("."))
        for name in sorted(files):
            yield Path(root) / name


def target_date(path: Path) -> tuple[dt.date, str]:
    committed = git_commit_date(path)
    if committed is not None:
        return committed, "git-commit"
    return mtime_date(path), "mtime"


def text_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path] if path.suffix.lower() in TEXT_SUFFIXES and path.stat().st_size <= MAX_FILE_BYTES else []
    found: list[Path] = []
    for child in iter_files(path):
        if child.suffix.lower() == ".md" and child.stat().st_size <= MAX_FILE_BYTES:
            found.append(child)
            if len(found) >= MAX_DIR_FILES:
                break
    return found


# --------------------------------------------------------------------------- content checks

def normal_lines(text: str) -> list[str]:
    lines = []
    for line in text.replace("\r\n", "\n").split("\n"):
        cleaned = re.sub(r"[\s>*_`#|-]+", " ", line).strip().lower()
        if cleaned:
            lines.append(cleaned)
    return lines


def shingles(lines: list[str]) -> set[tuple[str, ...]]:
    return {tuple(lines[i:i + SHINGLE]) for i in range(len(lines) - SHINGLE + 1)}


def banned_faces(workspace: Path) -> tuple[list[str], str]:
    source = workspace / BANNED_FONTS_REL
    try:
        data = json.loads(source.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return list(BUILTIN_BANNED), "builtin"
    names: set[str] = set()
    for key, value in data.items():
        if not isinstance(value, list):
            continue
        for item in value:
            if isinstance(item, dict):
                name = item.get("family") or item.get("prefix")
                if isinstance(name, str) and name.strip():
                    names.add(name.strip())
    return sorted(names or BUILTIN_BANNED), BANNED_FONTS_REL


def visual_findings(front_text: str, body: str, workspace: Path) -> list[dict]:
    text = front_text + "\n" + body
    faces, source = banned_faces(workspace)
    hexes = sorted(set(HEX_RE.findall(text)))
    typeface_lines = sorted({line.strip() for line in text.splitlines() if TYPEFACE_RE.search(line)})
    named_banned = sorted(face for face in faces if re.search(rf"(?<![\w-]){re.escape(face)}(?![\w-])", text))
    if not (hexes or typeface_lines or named_banned):
        return []
    return [finding(
        "project/visual-choice-present", "route",
        "PROJECT.md carries a visual choice (colour or typeface)",
        {"file": "PROJECT.md"},
        {"hex_colours": hexes, "typeface_declarations": len(typeface_lines), "banned_faces_named": named_banned,
         "banned_font_source": source},
        ["remove the value and point to the design brief or design tokens"],
        "Route the choice to chwezi-design-engine; keep only the design_brief and design_tokens pointers.")]


# --------------------------------------------------------------------------- doctor

def run(project: Path, workspace: Path, today: dt.date) -> tuple[int, dict]:
    report: dict = {
        "schema_version": "1.0", "tool": "project_context_doctor", "project": project.name,
        "findings": [], "not_assessed": [], "pointers": {},
    }
    if not workspace.is_dir():
        raise NotAssessed(f"workspace root is absent: {workspace}")
    try:
        import jsonschema  # noqa: F401
        import yaml  # noqa: F401
    except ImportError as exc:
        raise NotAssessed(f"dependency unavailable: {exc.name}") from exc
    raw_text = project.read_text(encoding="utf-8-sig").replace("\r\n", "\n")
    data, body, error = parse_project(project)
    findings: list[dict] = report["findings"]
    if data is None or data.get("project_schema") != 1:
        findings.append(finding(
            "project/schema-marker-missing", "error",
            error or "front matter lacks 'project_schema: 1'", {"file": project.name},
            {"reason": error or f"project_schema={data.get('project_schema')!r}"},
            ["add YAML front matter starting with 'project_schema: 1'"],
            "Start from templates/project-context/PROJECT.md."))
        return finalise(report)
    findings.extend(schema_findings(data))
    front_match = FRONT_MATTER_RE.match(raw_text)
    # Comment lines in the front matter are instructions for authors, not project content.
    front_text = "\n".join(
        line for line in (front_match.group(1) if front_match else "").splitlines()
        if not line.lstrip().startswith("#"))
    absent = [str(item).lower() for item in (data.get("evidence_on_hand") or {}).get("absent", []) or []]
    try:
        reviewed = dt.date.fromisoformat(str(data.get("last_reviewed")))
    except ValueError:
        reviewed = None
    project_lines = normal_lines(body)
    project_shingles = shingles(project_lines)

    for field in POINTER_FIELDS:
        value = data.get(field)
        if value is None:
            label = field.replace("_", " ")
            declared = any(label in item or field in item for item in absent)
            findings.append(finding(
                "project/field-missing", "mention", f"pointer '{field}' is omitted",
                {"field": field}, {"declared_absent": declared},
                [] if declared else [f"add '{field}' or list the absence under evidence_on_hand.absent"],
                "No action needed." if declared else "State the absence explicitly or add the pointer."))
            continue
        target, outside = resolve_pointer(workspace, str(value))
        if target is None:
            findings.append(finding(
                "project/pointer-outside-workspace", "error", f"pointer '{field}' leaves the workspace",
                {"field": field}, {"value": str(value), "reason": outside},
                ["use a workspace-relative path with forward slashes"],
                "Rewrite the pointer relative to the workspace root."))
            continue
        repo_folder = workspace / PurePosixPath(str(value)).parts[0]
        if not repo_folder.exists():
            report["not_assessed"].append({"field": field, "value": str(value), "reason": "repository folder not present on this machine"})
            report["pointers"][field] = {"value": str(value), "status": "NOT_ASSESSED"}
            continue
        if not target.exists():
            findings.append(finding(
                "project/pointer-missing-target", "route", f"pointer '{field}' names a missing target",
                {"field": field}, {"value": str(value)},
                ["correct the path", "remove the pointer and list the absence"],
                "Ask the owning engine where the source now lives."))
            report["pointers"][field] = {"value": str(value), "status": "missing"}
            continue
        when, basis = target_date(target)
        report["pointers"][field] = {"value": str(value), "status": "present", "last_changed": when.isoformat(), "basis": basis}
        if reviewed is not None and when > reviewed:
            findings.append(finding(
                "project/stale-pointer-target", "mention", f"'{field}' changed after the last review",
                {"field": field}, {"value": str(value), "target_changed": when.isoformat(), "basis": basis,
                                   "last_reviewed": reviewed.isoformat()},
                ["re-read the target and update last_reviewed"],
                "Review the pointed source; correct PROJECT.md if the durable truth changed."))
        best = 0.0
        runs = 0
        worst_file = None
        for source in text_files(target):
            try:
                other = shingles(normal_lines(source.read_text(encoding="utf-8", errors="replace")))
            except OSError:
                continue
            if not other or not project_shingles:
                continue
            shared = project_shingles & other
            jaccard = len(shared) / len(project_shingles | other)
            if len(shared) > runs or jaccard > best:
                worst_file = source
            best = max(best, jaccard)
            runs = max(runs, len(shared))
        if best >= JACCARD_LIMIT or runs > 0:
            rel = worst_file.relative_to(workspace).as_posix() if worst_file else str(value)
            findings.append(finding(
                "project/duplicated-content", "route", f"PROJECT.md repeats text from '{field}'",
                {"field": field}, {"file": rel, "jaccard": round(best, 3), "shared_five_line_runs": runs},
                ["replace the copied text with a one-line summary and the pointer"],
                "Keep the detail in the engine folder; PROJECT.md points to it."))

    findings.extend(visual_findings(front_text, body, workspace))
    try:
        due = dt.date.fromisoformat(str(data.get("review_due")))
        if due < today:
            findings.append(finding(
                "project/review-overdue", "mention", "review_due has passed",
                {"field": "review_due"}, {"review_due": due.isoformat(), "today": today.isoformat()},
                ["review the file and move review_due forward"], "Schedule the review with the owner."))
    except ValueError:
        pass
    return finalise(report)


def finalise(report: dict) -> tuple[int, dict]:
    report["findings"].sort(key=lambda f: (-SEVERITY_RANK[f["severity"]], f["code"], json.dumps(f["subject"], sort_keys=True)))
    counts = {level: sum(f["severity"] == level for f in report["findings"]) for level in SEVERITY_RANK}
    report["counts"] = counts
    if counts["error"]:
        report["status"] = "FAIL"
        return 1, report
    if report["not_assessed"]:
        report["status"] = "NOT_ASSESSED"
        return 3, report
    report["status"] = "PASS"
    return 0, report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only doctor for PROJECT.md (project_schema 1).")
    parser.add_argument("--project", required=True, type=Path, help="Path to PROJECT.md")
    parser.add_argument("--workspace-root", required=True, type=Path, help="Root that every pointer must stay inside")
    parser.add_argument("--today", help="ISO date used for review-overdue (default: today)")
    parser.add_argument("--json", action="store_true", help="Print the JSON report")
    args = parser.parse_args(argv)
    today = dt.date.fromisoformat(args.today) if args.today else dt.date.today()
    if not args.project.is_file():
        print(f"INVALID: project file not found: {args.project}", file=sys.stderr)
        return 1
    try:
        code, report = run(args.project.resolve(), args.workspace_root.resolve(), today)
    except NotAssessed as exc:
        payload = {"schema_version": "1.0", "tool": "project_context_doctor", "status": "NOT_ASSESSED", "reason": str(exc)}
        print(json.dumps(payload, indent=2) if args.json else f"NOT_ASSESSED: {exc}")
        return 3
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(f"{report['status']}: errors={report['counts']['error']} route={report['counts']['route']} "
              f"mention={report['counts']['mention']} not_assessed={len(report['not_assessed'])}")
        for item in report["findings"]:
            print(f"- [{item['severity']}] {item['code']}: {item['message']}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
