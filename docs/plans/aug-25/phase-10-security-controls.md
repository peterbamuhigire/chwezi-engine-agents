# Phase 10 — Security, Permission, and Supply-Chain Controls Plan

> **For agentic workers:** Use executing-plans or subagent-driven-development. Security failures block publication; missing security tooling is NOT ASSESSED.

**Goal:** Prevent a universal package from becoming a broad shell-execution, arbitrary-repository, or destructive-maintenance channel.

**Depends on:** Phases 1–9.

**Produces:** Threat model, permission model, approval contract, path/command tests, and dependency controls.

## Files

- Create: docs/security/threat-model.md.
- Create: docs/security/permission-model.md.
- Create: docs/security/supply-chain-policy.md.
- Create: schemas/approval-token.schema.json.
- Create: scripts/audit-managed-files.ps1.
- Create: tests/security/test_path_boundaries.ps1.
- Create: tests/security/test_mutation_gates.ps1.
- Create: tests/security/test_command_allowlist.ps1.
- Modify: core/policies/safety-boundaries.md and agents/engine-maintainer.md.
- Modify: .gitignore and CI workflow.

## Permission model

Operations are classified as:
- read: inspect files, Git metadata, routers, and documented commands.
- validate: run an allowlisted engine check in its documented working directory.
- approved_write: install, update, pull, or edit only after explicit user confirmation.
- blocked: reset, clean, force-push, arbitrary shell, broad recursive deletion, or unapproved external publication.

Every approved write records:
- requested_by
- approved
- target_repo
- target_branch
- operation
- confirmation_id
- before_head
- after_head
- result

## Tasks

- [ ] Threat-model prompt injection in engine files, malicious fork routers, malformed catalog entries, and hostile Git remotes.
- [ ] Threat-model path traversal, junctions, symlinks, nested repositories, and temporary-directory replacement.
- [ ] Threat-model malicious validator commands and dependency install scripts.
- [ ] Define fixed allowlists for validators, install destinations, and Git operations.
- [ ] Require explicit confirmation for pull, overwrite, update, uninstall, and external publication.
- [ ] Add checks that this repository’s publishing target is main.
- [ ] Pin Node and Python dependencies and add a lockfile audit step.
- [ ] Add secret scanning to CI and exclude credentials from release archives.
- [ ] Add tests that reject paths outside the approved root before any command starts.
- [ ] Add tests that reject model-provided command strings.
- [ ] Add tests that prove a dirty or diverged repository cannot be pulled.
- [ ] Add a rollback note for every mutating operation.

## Tests and evidence

Run:
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\security\test_path_boundaries.ps1
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\security\test_mutation_gates.ps1
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\security\test_command_allowlist.ps1
- git diff --check

Expected evidence: denied operations produce no filesystem or Git side effect; every pass names its command and target.

## Failure handling

- Any path-boundary failure blocks release.
- A dependency with an unresolved security advisory is blocked or explicitly excluded from the package.
- If a host cannot represent approval, restrict it to read-only operations.
- A tool that cannot prove its target root is blocked rather than guessed.

## Exit criteria

- The package has a threat model and permission model.
- MCP and script paths cannot turn model text into arbitrary shell commands.
- Every mutation has a confirmation and rollback record.

## Commit checkpoint

Stage the files listed above and commit:
security: add mutation and supply-chain controls
