#!/usr/bin/env python3
"""Fail when an engine stores book extractions, book summaries, or book-study digests.

Portfolio rule (copyright): book knowledge enters an engine only as paraphrased,
task-oriented skill content (procedures, decision rules, checklists, rubrics,
original examples) with a short Sources line. Extraction digests are never stored.

The check is path-based so that domain topics are not flagged:

1. A directory named in BANNED_DIR_NAMES is always a failure (no allowlist).
2. A book-digest file name is always a failure (no allowlist): the hyphen- or
   underscore-delimited token "book"/"books" immediately followed by
   extraction, extract(s), summary, summaries, notes, digest or study, e.g.
   "wave1-ifrs-book-extraction.md" or "clean-code-book-notes.md". Words that
   merely contain the letters ("runbook", "playbook") and provenance notes such
   as "book-informed-implementation-notes.md" are not matched.
3. Any other "*-extraction.md" file passes when it sits inside a skill's
   references/, templates/ or examples/ folder (domain topics such as
   food-processing "juice-extraction.md" or "pdf-extraction.md").
4. Any other "*-extraction.md" file fails unless its engine-relative path is
   listed in the allowlist file (default catalog/content-integrity-allowlist.txt)
   as "<engine-folder>/<relative/path>  # reason".

Exit codes: 0 PASS, 1 FAIL (findings), 3 PARTIAL (no findings, but a root was
missing and is NOT_ASSESSED; never a pass).

Only files stored or storable in the repository are checked: in a Git checkout
that is tracked plus untracked-but-not-ignored files; git-ignored local working
data is out of scope.

Engines are read from catalog/engines.yaml (path field) under --workspace-root,
plus this coordination package. Use --root to scan an explicit folder instead.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

import yaml

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
BANNED_DIR_NAMES = {"book-extractions", "extracted-books", "book-study", "book-studies", "book-summaries"}
DOMAIN_TOPIC_DIRS = {"references", "templates", "examples"}
BOOK_DIGEST_NAME = re.compile(r"(?:^|[-_.])books?[-_](?:extraction|extracts?|summary|summaries|notes|digest|study)\.md$")
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".pytest_cache"}


def load_allowlist(path: Path) -> set[str]:
    if not path.is_file():
        return set()
    entries: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        entry = line.split("#", 1)[0].strip().replace("\\", "/")
        if entry:
            entries.add(entry.lower())
    return entries


def repository_files(root: Path) -> list[str]:
    """Return engine-relative file paths that are, or could be, stored in the repo.

    In a Git checkout this is tracked plus untracked-but-not-ignored files, so
    git-ignored local working data (for example research project scratch) is
    not reported. Outside Git every file is walked.
    """
    result = subprocess.run(
        ["git", "-C", str(root), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        capture_output=True,
        check=False,
    )
    if result.returncode == 0:
        return sorted({entry for entry in result.stdout.decode("utf-8", "replace").split("\0") if entry})
    files: list[str] = []
    for path in root.rglob("*"):
        relative = path.relative_to(root)
        if path.is_file() and not any(part in SKIP_DIRS for part in relative.parts):
            files.append(relative.as_posix())
    return sorted(files)


def inspect_root(root: Path, allowlist: set[str]) -> list[str]:
    findings: list[str] = []
    reported_dirs: set[str] = set()
    for relative in repository_files(root):
        parts = relative.split("/")
        banned = next((i for i, part in enumerate(parts[:-1]) if part.lower() in BANNED_DIR_NAMES), None)
        if banned is not None:
            folder = "/".join(parts[: banned + 1])
            if folder not in reported_dirs:
                reported_dirs.add(folder)
                findings.append(f"{root.name}/{folder}: banned book-extraction folder '{parts[banned]}/'")
            continue
        key = f"{root.name}/{relative}".lower()
        name = parts[-1].lower()
        if BOOK_DIGEST_NAME.search(name):
            findings.append(f"{key}: book digest file name (book extraction/summary/notes)")
            continue
        if not name.endswith("-extraction.md"):
            continue
        if any(part.lower() in DOMAIN_TOPIC_DIRS for part in parts[:-1]):
            continue  # domain topic inside a skill reference/template/example
        if key in allowlist:
            continue
        findings.append(f"{key}: '*-extraction.md' outside skill references/templates/examples and not allowlisted")
    return findings


def catalog_roots(workspace: Path, catalog: Path) -> list[Path]:
    data = yaml.safe_load(catalog.read_text(encoding="utf-8")) or {}
    roots = [workspace / entry["path"] for entry in data.get("engines", [])]
    roots.append(PACKAGE_ROOT)
    return roots


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", action="append", default=[], help="Scan this folder (repeatable); skips the catalog.")
    parser.add_argument("--workspace-root", default=str(PACKAGE_ROOT.parent))
    parser.add_argument("--catalog", default=str(PACKAGE_ROOT / "catalog" / "engines.yaml"))
    parser.add_argument("--allowlist", default=str(PACKAGE_ROOT / "catalog" / "content-integrity-allowlist.txt"))
    args = parser.parse_args()

    roots = [Path(r) for r in args.root] or catalog_roots(Path(args.workspace_root), Path(args.catalog))
    allowlist = load_allowlist(Path(args.allowlist))
    findings: list[str] = []
    not_assessed: list[str] = []
    for root in roots:
        if not root.is_dir():
            not_assessed.append(str(root))
            continue
        findings.extend(inspect_root(root.resolve(), allowlist))

    for finding in findings:
        print(f"FAIL {finding}", file=sys.stderr)
    if findings:
        print(f"book-extraction check: roots={len(roots)} findings={len(findings)}", file=sys.stderr)
        return 1
    if not_assessed:
        for root in not_assessed:
            print(f"NOT_ASSESSED {root}: folder not found")
        print(f"PARTIAL: book-extraction check roots={len(roots)} findings=0 not_assessed={len(not_assessed)}")
        return 3
    print(f"PASS: book-extraction check roots={len(roots)} findings=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
