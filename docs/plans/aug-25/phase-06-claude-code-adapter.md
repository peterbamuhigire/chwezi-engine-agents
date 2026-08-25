# Phase 6 — Claude Code Adapter Implementation Plan

> **For agentic workers:** Use executing-plans or subagent-driven-development. Re-check Claude Code’s current discovery rules before implementation and keep provider configuration outside the adapter.

**Goal:** Provide Claude Code project/user installation files that point to the canonical agents and preserve the same handoff, verdict, and safety behavior as Codex.

**Depends on:** Phases 1–5 and current Anthropic host documentation.

**Produces:** Claude project instructions, agent wrappers, skill wrapper, manifest, and installation tests.

## Files

- Create: adapters/claude-code/README.md — prerequisites, install, update, uninstall, and troubleshooting.
- Create: adapters/claude-code/adapter.yaml — Claude host mapping.
- Create: adapters/claude-code/CLAUDE.md — project discovery instructions.
- Create: adapters/claude-code/agents/engine-orchestrator.md.
- Create: adapters/claude-code/agents/engine-maintainer.md.
- Create: adapters/claude-code/agents/engine-validator.md.
- Create: adapters/claude-code/skills/skills-engine-agents/SKILL.md.
- Create: tests/adapters/test_claude_code_adapter.ps1.
- Modify: scripts/install.ps1 — support -Host claude-code.
- Modify: docs/distribution.md — Claude installation details.

## Adapter manifest

The manifest must contain:

- id: claude-code
- host: claude-code
- version: 1.0.0
- core_version: 1.0.0
- entrypoints for the three agents and the routing skill
- project and user installation targets
- required capability read_files

## Tasks

- [ ] Verify current Claude Code locations for project instructions, agents, skills, and supported plugin packaging.
- [ ] Write CLAUDE.md so the host resolves the current Git root and reads the canonical engine router before selecting skills.
- [ ] Write three wrappers that refer to canonical IDs and never duplicate domain behavior.
- [ ] Write the skill wrapper for routing and capability negotiation.
- [ ] Document project-local and user-level installation separately.
- [ ] Add a fixture for Claude Code using a DeepSeek-compatible endpoint; test host/tool behavior, not model quality.
- [ ] Add a fixture for no shell access; expected maintenance and validation result is NOT ASSESSED.
- [ ] Add an approval section for pulls, writes, submissions, and external messages.
- [ ] Add smoke tests for all paths, frontmatter, and manifest references.

## Tests and evidence

Run:
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\adapters\test_claude_code_adapter.ps1
- python scripts\validate-contracts.py --schema schemas\adapter-manifest.schema.json --instance adapters\claude-code\adapter.yaml
- rg -n "engine-orchestrator|engine-maintainer|engine-validator|NOT ASSESSED" adapters\claude-code

Expected evidence: every wrapper resolves to a canonical ID, the adapter manifest validates, and provider configuration is absent from canonical instructions.

## Failure handling

- If official Claude discovery behavior changes, update the adapter document and manifest before changing installer paths.
- If a host-level plugin marketplace is unavailable, retain project-local installation as the supported adapter route.
- If the DeepSeek fixture cannot be run, label it NOT ASSESSED and keep the generic adapter available.

## Exit criteria

- Claude Code users can install the adapter into a project and invoke the same three workflows.
- The adapter does not require Claude models and does not alter host model configuration.

## Commit checkpoint

Stage the files listed above and commit:
feat: add Claude Code host adapter
