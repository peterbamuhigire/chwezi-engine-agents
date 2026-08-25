---
canonical_id: engine-orchestrator
contract_version: "1.0"
required_capabilities:
  - read_files
output_contract: core/contracts/handoff.yaml
---

# Engine orchestrator

Use this instruction when a request must be routed across the independent
skills engines.

First apply `core/instructions/capability-negotiator.md`. A missing read
capability changes routing to `NOT ASSESSED`; missing structured output changes
only the serialization format, not the required handoff fields.

## Procedure

1. Read the canonical catalog and identify candidate engines by the request's
   actual domain. Do not load every engine by default.
2. Add `chwezi-accounting-doctrine` for finance, accounting, IFRS, IAS, tax,
   bookkeeping, controls, payroll, or statutory reporting.
3. Add `design-system-skills` when the requested output changes visual design,
   typography, layout, accessibility, or document appearance.
4. Add `digital-research-skills` when claims are current, uncertain,
   source-sensitive, regulatory, comparative, or evidence-heavy.
5. For each selected engine, call `discover_engine(path)` and then
   `read_router(engine_identity)` before selecting any skill.
6. Select the smallest relevant set of skills from the router. Keep the local
   router and `SKILL.md` files as the domain source of truth.
7. Produce the handoff contract with the requested scope, selected engines,
   inputs, ordered sequence, evidence, blockers, and next action.

## Abstract operations

Adapters map these operations to their own tools:

```text
discover_engine(path) -> engine_identity
read_router(engine_identity) -> router_text
select_skills(router_text, request) -> skill_paths
inspect_engine(engine_identity) -> maintenance_result(read_only=true)
run_validator(engine_identity, validator_id) -> validation_check
maintain_remote(engine_identity, approval) -> maintenance_result
```

If a catalog entry, router, path, capability, or validator does not establish
something, mark it unknown or `NOT ASSESSED`. Do not invent a domain rule,
provider detail, command, source, or repository path.

## Handoff

Return a payload that satisfies `core/contracts/handoff.yaml`. A host without
structured output must preserve the same field names in Markdown.
