# Phase 1 — Compatibility Baseline Implementation Plan

> **For agentic workers:** Use `superpowers:executing-plans` or `superpowers:subagent-driven-development`. Complete the checklist in order and attach command output to the phase evidence.

**Goal:** Define exactly what “works with all AI models” means by separating model providers from host applications and documenting support, capability, and fallback levels.

**Depends on:** Current `skills-engine-agents` repository, `README.md`, `.codex-plugin/plugin.json`, three existing agents, and `catalog/engines.yaml`.

**Produces:** A compatibility contract that every later adapter, installer, MCP tool, and evaluation case must consume.

## Files

- Create: `docs/architecture/compatibility-contract.md` — definitions, support levels, and non-goals.
- Create: `docs/architecture/host-model-capability-matrix.md` — host/provider/capability table.
- Create: `docs/architecture/decision-records/ADR-001-hosts-versus-models.md` — decision record explaining why adapters target hosts.
- Create: `tests/fixtures/compatibility-matrix.yaml` — machine-readable support baseline.
- Modify: `README.md` — link to the compatibility model.
- Modify: `docs/distribution.md` — explain installation versus model configuration.

## Canonical decisions

```yaml
support_levels:
  native: host loads the package format directly
  adapter: host requires a thin host-specific wrapper
  generic: user loads Markdown and runs portable scripts manually
  not_assessed: no verified installation or execution evidence

capabilities:
  - read_files
  - write_files
  - shell
  - git
  - web
  - subagents
  - mcp
  - structured_output
  - user_approval

verdicts:
  check: [PASS, FAIL, NOT ASSESSED]
  aggregate: [PASS, FAIL, PARTIAL, NOT ASSESSED]
```

## Tasks

- [ ] Record the distinction between Codex, Claude Code, Gemini CLI, OpenCode, and generic clients as hosts.
- [ ] Record GPT, Claude, DeepSeek, Gemini, and other providers as models or model backends selected by a host.
- [ ] State that a model API alone cannot install a repository plugin without a host-side file and tool layer.
- [ ] Assign a support level to Codex, Claude Code, Gemini CLI, OpenCode, generic CLI, and MCP-capable hosts.
- [ ] Define capability requirements for routing, validation, maintenance, and write-with-approval modes.
- [ ] Define fallback behavior when shell, web, subagents, structured output, or user approval is unavailable.
- [ ] Add current official documentation starting points and mark them for re-verification during adapter implementation.
- [ ] Add a matrix row for DeepSeek used through a compatible host, while explicitly avoiding a claim that every host supports every DeepSeek model.
- [ ] Add acceptance cases for an unknown host, an unknown engine, a forked engine, and a missing validator.

## Required matrix fields

Each matrix row must contain:

```yaml
host: codex|claude-code|gemini-cli|opencode|generic|mcp
installation: native|adapter|generic|not_assessed
instruction_discovery: string
agent_entrypoints: string
tool_transport: scripts|mcp|none
approval_transport: host_prompt|confirmation_token|manual|not_assessed
model_configuration: host_owned|provider_owned|not_applicable
tested_on: []
known_limits: []
```

## Tests and evidence

Run:

```powershell
rg -n "host|model|adapter|native|generic|not_assessed|read_files|user_approval" docs/architecture tests/fixtures/compatibility-matrix.yaml
git diff --check
```

Expected evidence:

- Every target host has one matrix row.
- Every capability has a defined fallback.
- No section promises equal quality, tool access, or model behavior across providers.

## Failure handling

- If a host’s official discovery rules are unavailable, set its installation status to `not_assessed` and record the missing source.
- If a provider can be configured but the host cannot load local instructions, classify the provider integration as out of scope for this package.
- If the matrix conflicts with current host behavior, stop adapter implementation for that host until the matrix is corrected.

## Exit criteria

- A reviewer can classify any new request as a host adapter, provider configuration, generic workflow, or unsupported integration.
- Later phases can reference fixed support levels and capability names without inventing new terms.

## Commit checkpoint

```powershell
git add docs/architecture docs/distribution.md tests/fixtures/compatibility-matrix.yaml README.md
git commit -m "docs: define multi-host compatibility contract"
```
