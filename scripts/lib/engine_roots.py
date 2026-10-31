#!/usr/bin/env python3
"""Resolve catalogued engines to local directories on any workstation layout.

Portfolio checks used to assume one workspace folder that holds every engine under its
catalogue ``path``. That fails on a machine where engines sit under more than one parent or
keep a former folder name after a repository rename. This module resolves an engine from an
ordered list of roots and a short list of candidate folder names, and reports what it could
not resolve instead of guessing.

Candidate folder names for a catalogue entry, in priority order: ``path``, ``repository``,
``id``, then each entry of the optional ``aliases`` list (former folder names).

Resolution outcomes (``Resolution.status``):

``found``       exactly one directory was found for the first root that has any candidate.
``ambiguous``   the first root that has a candidate holds two different directories (for
                example a renamed checkout and a stale copy under the old name). The caller
                must treat this as ``NOT_ASSESSED``: picking one would hide a stale copy.
``missing``     no root holds any candidate.

Roots are tried in the order given. Roots come from ``--engines-root`` style arguments, then
the ``CHWEZI_ENGINES_ROOT`` environment variable (a path-separator list), then, when asked, the
parent folder of the coordination package. A root that is not a directory is ignored.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

ENV_VAR = "CHWEZI_ENGINES_ROOT"
COORDINATION = "chwezi-engine-agents"


@dataclass
class Resolution:
    engine_id: str
    status: str
    path: Path | None = None
    tried: list[str] = field(default_factory=list)
    candidates: list[Path] = field(default_factory=list)

    @property
    def found(self) -> bool:
        return self.status == "found"


def roots_from(values: Iterable[str | Path] | None = None, *, environ: dict | None = None,
               fallback: Path | None = None) -> list[Path]:
    """Ordered, de-duplicated roots: explicit values, then the environment, then ``fallback``."""
    environ = os.environ if environ is None else environ
    raw: list[str | Path] = list(values or [])
    env_value = environ.get(ENV_VAR)
    if env_value:
        raw.extend(part for part in env_value.split(os.pathsep) if part)
    if fallback is not None:
        raw.append(fallback)
    roots: list[Path] = []
    seen: set[Path] = set()
    for item in raw:
        path = Path(item).expanduser()
        try:
            real = path.resolve()
        except OSError:
            continue
        if real in seen or not real.is_dir():
            continue
        seen.add(real)
        roots.append(real)
    return roots


def candidate_names(entry: dict) -> list[str]:
    """Folder names to try for a catalogue entry, most specific first, without duplicates."""
    names: list[str] = []
    for key in ("path", "repository", "id"):
        value = entry.get(key)
        if isinstance(value, str) and value and value not in names:
            names.append(value)
    for value in entry.get("aliases") or []:
        if isinstance(value, str) and value and value not in names:
            names.append(value)
    return names


def resolve_engine(entry: dict, roots: list[Path]) -> Resolution:
    engine_id = str(entry.get("id") or entry.get("path") or "?")
    names = candidate_names(entry)
    result = Resolution(engine_id, "missing", tried=[f"{root.name or root}/{name}" for root in roots for name in names])
    for root in roots:
        found: list[Path] = []
        for name in names:
            candidate = root / name
            if candidate.is_dir():
                real = candidate.resolve()
                if real not in found:
                    found.append(real)
        if len(found) == 1:
            result.status, result.path = "found", found[0]
            return result
        if len(found) > 1:
            result.status, result.candidates = "ambiguous", found
            return result
    return result


def resolve_catalog(catalog: dict, roots: list[Path], *, include_coordination: Path | None = None) -> dict[str, Resolution]:
    """Resolve every engine in a loaded catalogue; optionally add the coordination package itself."""
    resolved = {str(entry["id"]): resolve_engine(entry, roots) for entry in catalog.get("engines", [])}
    if include_coordination is not None:
        resolved[COORDINATION] = Resolution(COORDINATION, "found", include_coordination.resolve())
    return resolved


def describe(resolution: Resolution) -> str:
    """One-line description that never contains an absolute path."""
    if resolution.status == "found":
        return f"{resolution.engine_id}: found"
    if resolution.status == "ambiguous":
        names = ", ".join(sorted(path.name for path in resolution.candidates))
        return f"{resolution.engine_id}: ambiguous (more than one checkout under one root: {names})"
    return f"{resolution.engine_id}: missing (looked for {len(resolution.tried)} root/name combinations)"
