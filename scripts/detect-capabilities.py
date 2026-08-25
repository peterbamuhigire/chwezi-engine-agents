#!/usr/bin/env python3
"""Detect local capabilities without performing mutations."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def git_available(root: Path) -> tuple[bool, str]:
    executable = shutil.which("git")
    if executable is None:
        return False, "git executable was not found"
    try:
        result = subprocess.run(
            [executable, "-C", str(root), "rev-parse", "--show-toplevel"],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return False, f"git probe failed: {exc}"
    if result.returncode != 0:
        return False, "target is not a Git checkout"
    return True, result.stdout.strip()


def profile(root: Path, host: str) -> dict[str, Any]:
    read_files = root.is_dir() and os.access(root, os.R_OK)
    write_files = root.is_dir() and os.access(root, os.W_OK)
    shell = any(shutil.which(name) for name in ("pwsh", "powershell", "bash", "sh"))
    git, git_detail = git_available(root)
    capabilities = {
        "read_files": read_files,
        "write_files": write_files,
        "shell": shell,
        "git": git,
        "web": False,
        "subagents": False,
        "mcp": False,
        "structured_output": True,
        "user_approval": False,
    }
    evidence = [
        {"capability": "read_files", "method": "directory access check", "result": "available" if read_files else "unavailable", "detail": str(root)},
        {"capability": "write_files", "method": "directory access check", "result": "available" if write_files else "unavailable", "detail": "Observed access is not approval."},
        {"capability": "shell", "method": "PATH executable resolution", "result": "available" if shell else "unavailable", "detail": "Checked pwsh, powershell, bash, and sh."},
        {"capability": "git", "method": "git rev-parse --show-toplevel", "result": "available" if git else "unavailable", "detail": git_detail},
    ]
    for capability in ("web", "subagents", "mcp", "user_approval"):
        evidence.append({"capability": capability, "method": "host declaration required", "result": "not_assessed", "detail": "The local detector cannot grant this capability."})
    evidence.append({"capability": "structured_output", "method": "JSON output requested", "result": "available", "detail": "This process can emit the contract as JSON."})
    return {"schema_version": "1.0", "host": host, "detected_at": datetime.now(UTC).isoformat(), "capabilities": capabilities, "evidence": evidence}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--format", choices=["json"], default="json")
    parser.add_argument("--host", default="generic")
    parser.add_argument("--path", type=Path, default=Path.cwd())
    args = parser.parse_args()
    print(json.dumps(profile(args.path.resolve(), args.host), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
