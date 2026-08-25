# Phase 4 — Capability Negotiation Implementation Plan

> **For agentic workers:** Use `superpowers:executing-plans` or `superpowers:subagent-driven-development`. Capability detection must describe what is available; it must never grant a permission that was not observed.

**Goal:** Make routing, validation, maintenance, and write workflows degrade truthfully when a host lacks shell, Git, web, subagents, MCP, structured output, or approval prompts.

**Depends on:** Phases 1–3.

**Produces:** Capability registry, detection scripts, fallback instructions, and fixture tests.

## Files

- Create: `core/capabilities/capability-registry.yaml` — capability names, detection method, and risk.
- Create: `core/capabilities/degraded-modes.md` — fallback behavior.
- Create: `core/instructions/capability-negotiator.md` — mode selection.
- Create: `schemas/capability-profile.schema.json`.
- Create: `scripts/detect-capabilities.ps1`.
- Create: `scripts/detect-capabilities.py`.
- Create: `tests/fixtures/capability-profiles/readonly-generic.yaml`.
- Create: `tests/fixtures/capability-profiles/codex-full.yaml`.
- Create: `tests/fixtures/capability-profiles/mcp-only.yaml`.
- Create: `tests/test_capability_fallbacks.ps1`.
- Modify: canonical agent instructions to consume the selected mode.

## Capability rules

| Operation | Required capabilities | Missing capability result |
|---|---|---|
| Route | `read_files` | `NOT ASSESSED` with required path |
| Validate | `read_files`, `shell` | `NOT ASSESSED` if shell unavailable |
| Inspect Git | `read_files`, `git` | `NOT ASSESSED` if Git unavailable |
| Pull | `read_files`, `git`, `user_approval` | blocked; no pull attempted |
| Web/current-source check | `web` | `NOT ASSESSED`; no freshness inference |
| Parallel agents | `subagents` | sequential execution |
| MCP tools | `mcp` | portable script fallback |
| Structured handoff | `structured_output` | Markdown fields with same names |

## Detection interface

```yaml
host: string
detected_at: ISO-8601 string
capabilities:
  read_files: boolean
  write_files: boolean
  shell: boolean
  git: boolean
  web: boolean
  subagents: boolean
  mcp: boolean
  structured_output: boolean
  user_approval: boolean
evidence:
  - capability: string
    method: string
    result: available|unavailable|not_assessed
    detail: string
```

## Tasks

- [ ] Define detection methods that do not execute mutations.
- [ ] Detect Git by resolving `git --version` and the current repository root.
- [ ] Detect shell by checking the host-provided execution boundary, not by assuming Windows or POSIX.
- [ ] Treat approval as unavailable unless the host explicitly exposes a confirmation channel.
- [ ] Implement `full`, `sequential`, `read_only`, and `not_assessed` execution modes.
- [ ] Add sequential fallback for independent routing or validation lanes.
- [ ] Add Markdown fallback with exact contract field names.
- [ ] Add fixtures for a fully capable Codex host, readonly generic host, and MCP-only host.
- [ ] Add tests proving missing shell prevents validation and maintenance.
- [ ] Add tests proving missing approval prevents pulls and writes.

## Tests and evidence

```powershell
python scripts\detect-capabilities.py --format json
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\detect-capabilities.ps1 -Format Json
powershell -NoProfile -ExecutionPolicy Bypass -File tests\test_capability_fallbacks.ps1
git diff --check
```

Expected evidence: capability JSON validates against the schema, readonly fixtures expose no mutating operation, and fallback tests pass.

## Failure handling

- A detection command that cannot run is `not_assessed`, not `available`.
- A host that reports write access without an approval channel is classified `read_only` for this package.
- If the host supplies no structured output, preserve the handoff as a Markdown table rather than dropping fields.

## Exit criteria

- Agents can explain exactly why a requested operation is unavailable.
- No later adapter needs to invent its own capability names or fallback rules.

## Commit checkpoint

```powershell
git add core/capabilities core/instructions/capability-negotiator.md schemas/capability-profile.schema.json scripts/detect-capabilities.ps1 scripts/detect-capabilities.py tests/fixtures/capability-profiles tests/test_capability_fallbacks.ps1
git commit -m "feat: add capability negotiation and fallbacks"
```
