# Phase 2 — Canonical Core Implementation Plan

> **For agentic workers:** Use `superpowers:executing-plans` or `superpowers:subagent-driven-development`. Canonical behavior must be written once and wrapped by each host adapter.

**Goal:** Extract routing, maintenance, validation, safety, and handoff behavior into model-neutral instructions that no host adapter can silently fork.

**Depends on:** Phase 1 compatibility contract.

**Produces:** Canonical agent instructions, output contracts, and thin Codex wrappers.

## Files

- Create: `core/instructions/engine-orchestrator.md` — routing procedure and handoff contract.
- Create: `core/instructions/engine-maintainer.md` — read-only inspection and approved fast-forward pull procedure.
- Create: `core/instructions/engine-validator.md` — documented-check selection and verdict procedure.
- Create: `core/contracts/handoff.yaml` — required orchestration fields.
- Create: `core/contracts/maintenance-result.yaml` — required maintenance fields.
- Create: `core/contracts/validation-result.yaml` — required validation fields.
- Create: `core/policies/safety-boundaries.md` — shared denylist and approval rules.
- Modify: `agents/engine-orchestrator.md` — Codex wrapper only.
- Modify: `agents/engine-maintainer.md` — Codex wrapper only.
- Modify: `agents/engine-validator.md` — Codex wrapper only.
- Modify: `skills/README.md` — explain canonical/adapters separation.

## Stable interfaces

The canonical instructions use these abstract operations:

```text
discover_engine(path) -> engine_identity
read_router(engine_identity) -> router_text
select_skills(router_text, request) -> skill_paths
inspect_engine(engine_identity) -> maintenance_result(read_only=true)
run_validator(engine_identity, validator_id) -> validation_check
maintain_remote(engine_identity, approval) -> maintenance_result
```

The instructions must never require a host-specific command such as a Codex deeplink, model name, provider API parameter, or proprietary tool identifier.

## Tasks

- [ ] Copy current orchestrator intent into the canonical file and replace Codex invocation language with abstract operations.
- [ ] Copy current maintainer safety rules and preserve `git pull --ff-only`, dirty-tree skip, divergence block, and no-reset/no-force-push rules.
- [ ] Copy current validator rules and preserve `NOT ASSESSED` for missing commands or dependencies.
- [ ] Define handoff fields `scope`, `engines`, `inputs`, `sequence`, `evidence`, `blockers`, and `next_action`.
- [ ] Add frontmatter fields `canonical_id`, `contract_version`, `required_capabilities`, and `output_contract` to all three canonical files.
- [ ] Define the safety denylist in one policy file and make each canonical instruction reference it.
- [ ] Replace each Codex agent body with a thin wrapper that states the Codex entrypoint and points to the canonical instruction.
- [ ] Add a source-integrity test that fails if canonical instructions contain `codex://`, provider API names, or model-specific parameters.
- [ ] Preserve existing agent names so current Codex users do not lose entrypoints.

## Handoff contract

```yaml
scope: string
engines:
  - id: string
    reason: string
inputs: []
sequence: []
evidence: []
blockers: []
next_action: string
```

## Tests and evidence

```powershell
rg -n "codex://|Responses API|Anthropic|DeepSeek|GPT-|Claude" core/instructions
python C:\Users\BIRDC\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .
git diff --check
```

Expected evidence: the provider-specific search returns no matches in `core/instructions`, the Codex validator passes, and all three existing agent filenames remain present.

## Failure handling

- If behavior cannot be expressed without a host-specific tool, define an abstract operation and put the mapping in the adapter.
- If two canonical files disagree on a verdict, stop and resolve the contract before creating adapters.
- If a current agent contains undocumented behavior, preserve it in a named policy section or record its removal decision; do not drop it silently.

## Exit criteria

- Exactly one canonical instruction exists for each agent role.
- Every adapter can point to a canonical ID and output contract.
- Codex wrappers contain no independent routing or maintenance policy.

## Commit checkpoint

```powershell
git add core agents skills/README.md
git commit -m "refactor: separate canonical agent instructions"
```
