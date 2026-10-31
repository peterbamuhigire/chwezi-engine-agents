#!/usr/bin/env python3
"""Refresh ``released_commit`` in catalog/engines.yaml from each engine's current HEAD (pass-2 K4).

Default is ``--check``: report how far each recorded pin is behind its engine's HEAD and exit 1 when any
engine lags. ``--write`` rewrites only the ``released_commit`` values, in place, preserving comments,
quoting and line endings, and only when every engine is safe to pin:

* the checkout is found (``scripts/lib/engine_roots.py``: catalogue path, repository, id, former names);
* its working tree is clean (no modified, staged or untracked-but-not-ignored file);
* it is on branch ``main`` (``--any-branch`` overrides, for a release branch).

If any engine fails a condition nothing is written and the exit code is 2. A pin is a statement that a
commit was released, so a dirty or missing engine is never pinned from guesswork.

Exit codes: ``--check``: 0 every pin is HEAD, 1 at least one pin lags or is not in the history, 3 an engine
could not be assessed; ``--write``: 0 written (or already current), 2 refused, nothing written.
Output never contains an absolute path.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import engine_roots  # noqa: E402
import released_commits as RC  # noqa: E402

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
ID_RE = re.compile(r"^\s*-\s*id:\s*(\S+)\s*$")
PIN_RE = re.compile(r'(released_commit:\s*")([^"]*)(")')


def survey(catalog: dict, roots: list[Path], required_branch: str | None) -> list[dict]:
    """One record per catalogued engine: resolution, head, branch, dirtiness, pin state, and any blocker."""
    rows = []
    for entry in catalog["engines"]:
        engine = str(entry["id"])
        pin = (entry.get("integration") or {}).get("released_commit")
        resolution = engine_roots.resolve_engine(entry, roots)
        row = {"engine": engine, "pin": pin, "head": None, "behind": None, "state": "not-assessed", "blockers": []}
        if not resolution.found:
            row["blockers"].append(engine_roots.describe(resolution).split(": ", 1)[1])
            rows.append(row)
            continue
        status = RC.pin_status(resolution.path, pin)
        row.update(head=status["head"], behind=status["behind"], state=status["state"])
        dirty = RC.dirty_entries(resolution.path)
        if dirty:
            row["blockers"].append(f"working tree is not clean ({len(dirty)} entries)")
        current = RC.branch(resolution.path)
        if required_branch and current != required_branch:
            row["blockers"].append(f"branch is {current or 'detached HEAD'}, not {required_branch}")
        if not status["head"]:
            row["blockers"].append("HEAD cannot be read")
        rows.append(row)
    return rows


def rewrite(text: str, heads: dict[str, str]) -> tuple[str, list[str]]:
    """Replace each engine's pin in the catalogue text. Raises ValueError if an engine has no single pin field."""
    lines = text.splitlines(keepends=True)
    current: str | None = None
    seen: dict[str, int] = {}
    for index, line in enumerate(lines):
        match = ID_RE.match(line)
        if match:
            current = match.group(1)
            continue
        if current in heads and PIN_RE.search(line):
            seen[current] = seen.get(current, 0) + 1
            lines[index] = PIN_RE.sub(lambda m: f"{m.group(1)}{heads[current]}{m.group(3)}", line, count=1)
    problems = [engine for engine in heads if seen.get(engine) != 1]
    if problems:
        raise ValueError("expected exactly one released_commit field for: " + ", ".join(sorted(problems)))
    return "".join(lines), sorted(heads)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="report pin lag (default)")
    mode.add_argument("--write", action="store_true", help="rewrite the pins from each engine's HEAD")
    parser.add_argument("--engines-root", type=Path, action="append", default=[],
                        help="folder that holds engine checkouts (repeatable; also CHWEZI_ENGINES_ROOT)")
    parser.add_argument("--workspace-root", type=Path, default=PACKAGE_ROOT.parent)
    parser.add_argument("--package-root", type=Path, default=PACKAGE_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--any-branch", action="store_true", help="allow pinning a checkout that is not on main")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    package = args.package_root.resolve()
    catalog_path = package / "catalog" / "engines.yaml"
    raw = catalog_path.read_bytes()
    text = raw.decode("utf-8")
    catalog = yaml.safe_load(text)
    roots = engine_roots.roots_from(args.engines_root, fallback=args.workspace_root)
    rows = survey(catalog, roots, None if (args.any_branch or not args.write) else "main")
    blocked = [row for row in rows if row["blockers"]]

    if args.write:
        if blocked:
            report(rows, args.json, refused=True)
            return 2
        heads = {row["engine"]: row["head"] for row in rows}
        try:
            new_text, _ = rewrite(text, heads)
        except ValueError as error:
            print(f"refused: {error}; nothing written", file=sys.stderr)
            return 2
        changed = [row["engine"] for row in rows if row["pin"] != row["head"]]
        if new_text != text:
            checked = yaml.safe_load(new_text)
            if [e["id"] for e in checked["engines"]] != [e["id"] for e in catalog["engines"]]:
                print("refused: the rewrite altered the engine list; nothing written", file=sys.stderr)
                return 2
            catalog_path.write_bytes(new_text.encode("utf-8"))
        report(rows, args.json, written=changed)
        return 0

    report(rows, args.json)
    if any(row["state"] == "not-assessed" for row in rows):
        return 3
    return 1 if any(row["state"] not in ("current",) for row in rows) else 0


def report(rows: list[dict], as_json: bool, *, refused: bool = False, written: list[str] | None = None) -> None:
    if as_json:
        print(json.dumps({"engines": rows, "refused": refused, "written": written}, indent=2))
        return
    for row in rows:
        detail = {
            "current": "pin is HEAD",
            "behind": f"pin {row['pin']} is {row['behind']} commits behind HEAD {row['head']}",
            "diverged": f"pin {row['pin']} is not an ancestor of HEAD {row['head']}",
            "unknown": f"pin {row['pin']} is not in the history",
            "unverifiable": f"pin {row['pin']} cannot be checked in a shallow clone",
            "no-pin": f"no released_commit recorded (HEAD {row['head']})",
            "not-assessed": "engine not assessed",
            "not-a-repository": "not a git repository",
        }[row["state"]]
        blockers = f"; blocked: {'; '.join(row['blockers'])}" if row["blockers"] else ""
        print(f"{row['engine']}: {detail}{blockers}")
    if refused:
        print(f"refused: {sum(1 for r in rows if r['blockers'])} engine(s) are not safe to pin; nothing written")
    elif written is not None:
        print(f"written: {len(written)} pin(s) updated" if written else "written: nothing to change, every pin is HEAD")
    else:
        lagging = sum(1 for r in rows if r["state"] != "current")
        print(f"{len(rows)} engines; {lagging} not at HEAD")


if __name__ == "__main__":
    raise SystemExit(main())
