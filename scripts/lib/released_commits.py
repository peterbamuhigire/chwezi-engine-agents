#!/usr/bin/env python3
"""Read-only git facts used to compare ``released_commit`` pins with engine HEADs (pass-2 K4).

Used by ``scripts/refresh_released_commits.py`` and by ``scripts/render_host_files.py --check`` so
the two never disagree about what a pin means. Nothing here writes to a repository.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

SHORT = 7


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)


def is_repository(root: Path) -> bool:
    return git(root, "rev-parse", "--git-dir").returncode == 0


def head_short(root: Path) -> str | None:
    result = git(root, "rev-parse", f"--short={SHORT}", "HEAD")
    return result.stdout.strip() or None if result.returncode == 0 else None


def branch(root: Path) -> str | None:
    """Current branch name, or None when HEAD is detached."""
    result = git(root, "branch", "--show-current")
    name = result.stdout.strip()
    return name or None


def dirty_entries(root: Path) -> list[str]:
    """Porcelain lines for modified, staged and untracked-but-not-ignored files."""
    result = git(root, "status", "--porcelain", "--untracked-files=normal")
    return [line for line in result.stdout.splitlines() if line.strip()]


def is_shallow(root: Path) -> bool:
    return git(root, "rev-parse", "--is-shallow-repository").stdout.strip() == "true"


def pin_status(root: Path, pin: str | None) -> dict:
    """Relationship between a recorded pin and the engine's HEAD.

    ``state`` is one of: ``current`` (pin is HEAD), ``behind`` (pin is an ancestor, ``behind`` commits back),
    ``diverged`` (pin exists but is not an ancestor of HEAD), ``unknown`` (pin is not in the history),
    ``unverifiable`` (shallow clone that lacks the pin, so history cannot answer), ``no-pin`` or ``not-a-repository``.
    """
    if not is_repository(root):
        return {"state": "not-a-repository", "head": None, "behind": None}
    head = head_short(root)
    if not pin:
        return {"state": "no-pin", "head": head, "behind": None}
    exists = git(root, "rev-parse", "--verify", "--quiet", f"{pin}^{{commit}}").returncode == 0
    if not exists:
        return {"state": "unverifiable" if is_shallow(root) else "unknown", "head": head, "behind": None}
    full_pin = git(root, "rev-parse", f"{pin}^{{commit}}").stdout.strip()
    full_head = git(root, "rev-parse", "HEAD").stdout.strip()
    if full_pin == full_head:
        return {"state": "current", "head": head, "behind": 0}
    if git(root, "merge-base", "--is-ancestor", full_pin, full_head).returncode != 0:
        return {"state": "diverged", "head": head, "behind": None}
    count = git(root, "rev-list", "--count", f"{full_pin}..{full_head}").stdout.strip()
    return {"state": "behind", "head": head, "behind": int(count or 0)}
