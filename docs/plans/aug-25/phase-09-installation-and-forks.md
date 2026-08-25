# Phase 9 — Installation, Update, Uninstall, and Fork Discovery Plan

> **For agentic workers:** Use executing-plans or subagent-driven-development. Installation must be recoverable, path-safe, and explicit about files it owns.

**Goal:** Provide one host-aware installer and updater while allowing forked engine repositories to work from their own checkout.

**Depends on:** Phases 1–8.

**Produces:** PowerShell, POSIX, and Python target resolution; managed installation manifests; fork tests.

## Files

- Create or replace: scripts/install.ps1.
- Create: scripts/install.sh.
- Create: scripts/update.ps1 and scripts/update.sh.
- Create: scripts/uninstall.ps1 and scripts/uninstall.sh.
- Create: scripts/resolve-install-target.py.
- Create: tests/install/test_install_targets.ps1.
- Create: tests/install/test_fork_discovery.ps1.
- Create: tests/install/fixtures/forked-engine/AGENTS.md.
- Modify: scripts/discover-engine.ps1 and docs/distribution.md.

## Interfaces

PowerShell:
- install.ps1 -Host codex|claude-code|gemini-cli|opencode|generic|mcp -Destination path [-Force]
- update.ps1 -Destination path
- uninstall.ps1 -Destination path [-Force]

POSIX:
- install.sh --host host --destination path [--force]
- update.sh --destination path
- uninstall.sh --destination path [--force]

Managed manifest fields:
- source_repository
- source_commit
- adapter_id
- adapter_version
- core_version
- destination
- installed_files
- installed_at
- installer_version

## Tasks

- [ ] Define the managed manifest at .skills-engine-agents-install.json.
- [ ] Resolve destination paths to absolute paths before writing.
- [ ] Refuse an unmanaged non-empty destination unless explicit force is supplied and no protected files would be overwritten.
- [ ] Copy files instead of requiring Windows symlink permissions.
- [ ] Stage updates in a temporary sibling directory and replace only after validation.
- [ ] Make uninstall remove only manifest-listed files and retain user-created files.
- [ ] Add WhatIf support to PowerShell mutation paths where practical.
- [ ] Make the installer fail if the requested host adapter is absent.
- [ ] Make discovery resolve Git root, origin repository name, folder name, and local router without C:\wamp64\www.
- [ ] Add a fork mode that inspects an uncatalogued repository but does not invent validator commands.
- [ ] Add Windows and POSIX parity tests for destination and manifest generation.
- [ ] Document the difference between project-local and user-level installation.

## Tests and evidence

Run:
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\install\test_install_targets.ps1
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\install\test_fork_discovery.ps1
- powershell -NoProfile -ExecutionPolicy Bypass -File scripts\install.ps1 -Host generic -Destination "$env:TEMP\skills-engine-agents-test"

Expected evidence: installation is reproducible, managed files are listed, fork discovery does not assume the catalogue, and unmanaged files are not deleted.

## Failure handling

- A missing host adapter blocks installation before any destination is modified.
- A partial copy is removed from the temporary staging directory; the existing installation remains intact.
- A fork with no router is reported as unmatched and no validation command is run.
- A dirty plugin installation is not overwritten unless the user explicitly confirms force replacement.

## Exit criteria

- A user can install a host adapter without cloning engines into a fixed global directory.
- A forked engine works from its checkout and is marked uncatalogued when no validator is defined.

## Commit checkpoint

Stage the files listed above and commit:
feat: add safe host-aware installers
