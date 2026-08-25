#!/usr/bin/env python3
"""Resolve an explicit host adapter destination without mutating it."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

HOSTS = {"codex", "claude-code", "gemini-cli", "opencode", "generic", "mcp"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True, choices=sorted(HOSTS))
    parser.add_argument("--destination", required=True, type=Path)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    source = args.source.resolve()
    adapter = source / "adapters" / args.host / "adapter.yaml"
    if not adapter.is_file():
        parser.error(f"requested host adapter is missing: {adapter}")
    destination = args.destination.expanduser().resolve()
    print(json.dumps({"host": args.host, "source": str(source), "destination": str(destination), "adapter": str(adapter), "manifest": str(destination / ".skills-engine-agents-install.json")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
