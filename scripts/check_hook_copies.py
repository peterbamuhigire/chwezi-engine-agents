#!/usr/bin/env python3
"""Check that every copy of the shared hook files equals the canonical copy (pass-2 K3). Read-only.

The canonical copy of the destructive-command gate and its companions is the one in this package's
``hooks/`` folder (``catalog/shared-assets.yaml`` rows ``hooks-*``, owner ``chwezi-engine-agents``;
procedure in ``docs/operations/hook-canonical-copy.md``). Two kinds of copy are compared byte for byte
(line endings normalised, as the shared-asset register does):

* the copy in each catalogued engine repository, found through ``scripts/lib/engine_roots.py``;
* every copy installed for a host: Claude Code plugin folders under a plugin directory
  (default ``~/.claude/plugins``). Folders named ``.trash`` are ignored because the host does not load them.

An installed copy can fall behind its repository, and the host loads whichever plugin's copy it reaches
first, so an installed copy that differs matters even when every repository copy is clean.

Output never contains an absolute path: engines appear by catalogue id and installed copies relative to
the plugin directory.

Exit codes: 0 every compared copy is identical; 1 any difference, missing file or missing canonical;
3 only NOT_ASSESSED (an engine checkout is missing or ambiguous). Missing is never a pass.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent / "lib"))
import engine_roots  # noqa: E402

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
SHARED_FILES = (
    "destructive-bash-gate.js",
    "plugin-hook-config.js",
    "test-destructive-bash-gate.js",
    "test-plugin-hook-config.js",
)
GATE = "destructive-bash-gate.js"
SKIPPED_PARTS = {".trash", "node_modules", ".git"}


@dataclass
class Row:
    kind: str       # "engine" or "installed"
    label: str
    file: str
    status: str     # "identical" | "differs" | "missing"
    sha256: str | None = None


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest()


def compare_dir(kind: str, label: str, hooks_dir: Path, canonical: dict[str, str], files: tuple[str, ...]) -> list[Row]:
    rows = []
    for name in files:
        path = hooks_dir / name
        if not path.is_file():
            rows.append(Row(kind, label, name, "missing"))
            continue
        sha = digest(path)
        rows.append(Row(kind, label, name, "identical" if sha == canonical[name] else "differs", sha[:12]))
    return rows


def installed_hook_dirs(plugins_dir: Path) -> list[tuple[str, Path]]:
    """Plugin ``hooks`` folders that hold a copy of the gate, relative label first."""
    found = []
    for gate in sorted(plugins_dir.rglob(GATE)):
        rel = gate.relative_to(plugins_dir)
        if SKIPPED_PARTS & set(rel.parts) or gate.parent.name != "hooks":
            continue
        found.append((rel.parent.parent.as_posix(), gate.parent))
    return found


def run(package: Path, roots: list[Path], plugin_dirs: list[Path], files: tuple[str, ...] = SHARED_FILES) -> tuple[list[Row], list[dict], list[str]]:
    rows: list[Row] = []
    not_assessed: list[dict] = []
    notes: list[str] = []
    canonical: dict[str, str] = {}
    for name in files:
        path = package / "hooks" / name
        if path.is_file():
            canonical[name] = digest(path)
        else:
            rows.append(Row("canonical", "chwezi-engine-agents", name, "missing"))
    usable = tuple(name for name in files if name in canonical)
    catalog = yaml.safe_load((package / "catalog" / "engines.yaml").read_text(encoding="utf-8"))
    for entry in catalog["engines"]:
        resolution = engine_roots.resolve_engine(entry, roots)
        if not resolution.found:
            not_assessed.append({"engine": str(entry["id"]), "reason": engine_roots.describe(resolution)})
            continue
        rows.extend(compare_dir("engine", str(entry["id"]), resolution.path / "hooks", canonical, usable))
    if not plugin_dirs:
        notes.append("installed copies: no plugin directory found, not compared")
    for plugins_dir in plugin_dirs:
        copies = installed_hook_dirs(plugins_dir)
        if not copies:
            notes.append("installed copies: none found under the plugin directory")
        for label, hooks_dir in copies:
            rows.extend(compare_dir("installed", label, hooks_dir, canonical, usable))
    return rows, not_assessed, notes


def summarise(rows: list[Row], not_assessed: list[dict], notes: list[str]) -> str:
    lines = []
    bad = [r for r in rows if r.status != "identical"]
    for r in bad:
        lines.append(f"[{r.status}] {r.kind} {r.label}: {r.file}" + (f" (sha256 {r.sha256}...)" if r.sha256 else ""))
    for item in not_assessed:
        lines.append(f"NOT_ASSESSED {item['engine']}: {item['reason']}")
    lines.extend(notes)
    engines = {r.label for r in rows if r.kind == "engine"}
    installed = {r.label for r in rows if r.kind == "installed"}
    lines.append(f"compared {len(engines)} engine repositories and {len(installed)} installed plugin copies "
                 f"({len(rows)} files); differences {len(bad)}; not assessed {len(not_assessed)}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--engines-root", type=Path, action="append", default=[],
                        help="folder that holds engine checkouts (repeatable; also CHWEZI_ENGINES_ROOT)")
    parser.add_argument("--workspace-root", type=Path, default=PACKAGE_ROOT.parent)
    parser.add_argument("--plugins-dir", type=Path, action="append", default=None,
                        help="host plugin directory (repeatable; default ~/.claude/plugins when it exists)")
    parser.add_argument("--package-root", type=Path, default=PACKAGE_ROOT, help=argparse.SUPPRESS)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    package = args.package_root.resolve()
    roots = engine_roots.roots_from(args.engines_root, fallback=args.workspace_root)
    if args.plugins_dir is None:
        default = Path.home() / ".claude" / "plugins"
        plugin_dirs = [default] if default.is_dir() else []
    else:
        plugin_dirs = [p.resolve() for p in args.plugins_dir if p.is_dir()]
    rows, not_assessed, notes = run(package, roots, plugin_dirs)
    if args.json:
        print(json.dumps({"rows": [asdict(r) for r in rows], "not_assessed": not_assessed, "notes": notes}, indent=2))
    else:
        print(summarise(rows, not_assessed, notes))
    if any(r.status != "identical" for r in rows):
        return 1
    return 3 if not_assessed else 0


if __name__ == "__main__":
    raise SystemExit(main())
