# Phase 5 — Codex Adapter Implementation Plan

> **For agentic workers:** Use executing-plans or subagent-driven-development. Preserve the current Codex entrypoints and validate the plugin manifest before changing installation behavior.

**Goal:** Keep the existing Codex plugin working while making it an explicit adapter over the canonical core.

**Depends on:** Phases 1–4.

**Produces:** A versioned Codex adapter manifest, thin Codex wrappers, and install/smoke tests.

## Files

- Modify: .codex-plugin/plugin.json — display name, version, and adapter metadata.
- Modify: agents/engine-orchestrator.md — wrapper to canonical ID.
- Modify: agents/engine-maintainer.md — wrapper to canonical ID.
- Modify: agents/engine-validator.md — wrapper to canonical ID.
- Create: adapters/codex/README.md — Codex-specific installation and invocation.
- Create: adapters/codex/adapter.yaml — host-to-core mapping.
- Create: tests/adapters/test_codex_adapter.ps1 — entrypoint and manifest smoke tests.
- Modify: scripts/install.ps1 — support explicit -Host codex.
- Modify: README.md — link to the Codex adapter guide.

## Adapter manifest

The manifest must contain:

- id: codex
- host: codex
- version: 1.0.0
- core_version: 1.0.0
- entrypoints for the three existing agent names
- install target .codex-plugin
- required capability read_files

## Tasks

- [ ] Verify the current Codex plugin schema and keep .codex-plugin/plugin.json valid.
- [ ] Add canonical ID and output contract references to all three wrappers.
- [ ] Keep the user-facing agent names unchanged.
- [ ] Ensure wrappers do not duplicate routing, pull, or verdict policy.
- [ ] Add a smoke test for all three agent files and their frontmatter.
- [ ] Add a test that every manifest target resolves to an existing file.
- [ ] Update the installer to copy the Codex adapter plus required core and schema files.
- [ ] Add a managed-install manifest entry with source commit and adapter version.
- [ ] Document Codex plugin-directory installation separately from model-provider selection.

## Tests and evidence

Run:
- python C:\Users\BIRDC\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\adapters\test_codex_adapter.ps1
- powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate-catalog.ps1 -CatalogPath "$PWD\catalog\engines.yaml"

Expected evidence: plugin validation, adapter smoke tests, and catalog validation pass. If the Codex validator is unavailable, record NOT ASSESSED with the command and dependency.

## Failure handling

- If a plugin manifest field is rejected, remove only the unsupported field and retain adapter metadata in adapters/codex/adapter.yaml.
- If an agent wrapper cannot load the core file, fail installation rather than installing a detached wrapper.
- If an existing user installation contains unmanaged files, do not overwrite them without explicit force confirmation.

## Exit criteria

- Existing Codex users can still install and invoke all three agents.
- The Codex adapter can be updated without editing canonical instructions.

## Commit checkpoint

Stage the files listed above and commit:
feat: formalize Codex host adapter
