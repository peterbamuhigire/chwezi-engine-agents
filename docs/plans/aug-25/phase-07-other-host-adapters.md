# Phase 7 — Gemini CLI, OpenCode, and Generic Adapter Implementation Plan

> **For agentic workers:** Use executing-plans or subagent-driven-development. Verify each host’s current file conventions before publishing its adapter.

**Goal:** Give non-Codex/non-Claude users a supported host adapter where a verified convention exists and a plain Markdown/CLI fallback everywhere else.

**Depends on:** Phases 1–6.

**Produces:** Gemini CLI, OpenCode, and generic adapter bundles with installation smoke tests.

## Files

- Create: adapters/gemini-cli/README.md, adapter.yaml, project-instructions.md.
- Create: adapters/gemini-cli/commands/engine-orchestrator.md.
- Create: adapters/gemini-cli/commands/engine-maintainer.md.
- Create: adapters/gemini-cli/commands/engine-validator.md.
- Create: adapters/opencode/README.md, adapter.yaml, AGENTS.md.
- Create: adapters/opencode/skills/skills-engine-agents/SKILL.md.
- Create: adapters/generic/README.md.
- Create: adapters/generic/engine-orchestrator.prompt.md.
- Create: adapters/generic/engine-maintainer.prompt.md.
- Create: adapters/generic/engine-validator.prompt.md.
- Create: tests/adapters/test_other_host_adapters.ps1.
- Modify: scripts/install.ps1 and README.md.

## Adapter contract

Every manifest must declare id, host, version 1.0.0, core_version 1.0.0, entrypoints, install_targets, required_capabilities, and fallback generic.

## Tasks

- [ ] Verify Gemini CLI project instruction and command discovery rules from maintained documentation.
- [ ] Verify OpenCode project instruction and skill discovery rules from maintained documentation.
- [ ] Write Gemini wrappers that point to canonical IDs and preserve the same output fields.
- [ ] Write OpenCode instruction and skill wrappers with no duplicated domain rules.
- [ ] Write generic prompts that a human can paste into any model host with repository access.
- [ ] Add generic PowerShell and POSIX command examples for discovery, validation, and read-only inspection.
- [ ] Define host-not-catalogued behavior: inspect the repository, but do not invent engine-specific validators.
- [ ] Add tests for missing host directories and fallback to generic prompts.
- [ ] Mark each adapter adapter only after its smoke test passes; otherwise mark not_assessed.

## Tests and evidence

Run:
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\adapters\test_other_host_adapters.ps1
- python scripts\validate-contracts.py --schema schemas\adapter-manifest.schema.json --instance adapters\gemini-cli\adapter.yaml
- python scripts\validate-contracts.py --schema schemas\adapter-manifest.schema.json --instance adapters\opencode\adapter.yaml

Expected evidence: every adapter has a readable entrypoint, valid manifest, generic fallback, and documented limitations.

## Failure handling

- If a host convention cannot be verified, publish its adapter as not_assessed and exclude it from the default installer.
- If a host uses different command syntax, translate only in that host directory.
- If a generic host lacks shell, return commands without executing them and label validation NOT ASSESSED.

## Exit criteria

- Developers have a supported path for Gemini CLI and OpenCode where verified.
- Every other client has a useful generic prompt and script path.

## Commit checkpoint

Stage the files listed above and commit:
feat: add non-Codex host adapters
