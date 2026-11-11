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
3. Add `chwezi-design-engine` when the requested output changes visual design,
   typography, layout, accessibility, or document appearance. Any Chwezi app or
   system interface work (see "Chwezi app and system interface work" below)
   always adds it, with its `chwezi-product-excellence-standard` skill as a
   mandatory gate.
4. Add `digital-research-skills` when claims are current, uncertain,
   source-sensitive, regulatory, comparative, or evidence-heavy. This is the
   catalog id and GitHub repository name; its local checkout folder is
   `digital-research-engine` (use the `path` field in `catalog/engines.yaml`
   when calling `discover_engine(path)`).
5. For each selected engine, call `discover_engine(path)` and then
   `read_router(engine_identity)` before selecting any skill.
6. Select the smallest relevant set of skills from the router. Keep the local
   router and `SKILL.md` files as the domain source of truth.
7. For every non-trivial output, require the portfolio craft brief: audience,
   job or decision, selected slice, constraints, evidence boundary, and failure
   consequence. Pre-fill the craft brief from `PROJECT.md` when present
   (`docs/operations/project-context-contract.md`); the task-specific fields
   are still asked for. Route development and visual work through the corresponding
   engineering/design handoffs so requirements detail, data flow, interaction
   detail, and release proof remain connected.
8. Produce the handoff contract with the requested scope, selected engines,
   inputs, ordered sequence, craft brief, evidence, blockers, and next action.

## Cross-engine handoff boundaries

Each engine owns one question. Record the owner in `engines[].reason` and the
order in `sequence`; a downstream engine consumes the upstream artefact and
does not re-decide it.

| Question | Owner | Artefact handed on |
|---|---|---|
| What does success mean? | `chwezi-sdlc-documentation` | Prescriptive, verifiable requirements with actors, states, measurable acceptance criteria, traceability, and open questions. No implementation choices. |
| How is it built safely? | `chwezi-dev-engine` | Architecture, data flow, security and failure handling, tests traced to the acceptance criteria, release and rollback proof. |
| How does it look, behave, and get evaluated? | `chwezi-design-engine` | Visual and interaction rationale, all key states, accessibility and render review; unperformed render/device/assistive-technology checks stay `NOT ASSESSED`. |
| What is currently true? | `digital-research-skills` | Claim-level sources with access dates for versions, platform rules, law, prices, and benchmarks. |
| What happens to the money? | `chwezi-accounting-doctrine` | Recognition, posting, reconciliation, controls, and tax treatment; no invented rate or statutory value. |

Sequence product work as requirements, then research for any volatile claim
the requirements or build depend on, then engineering and design in
coordinated slices, then finance wherever money moves. When a downstream
engine finds a missing or untestable requirement, route it back to the owner
as a blocker; do not invent an acceptance criterion, stakeholder intent, or
source to close the gap.

## Chwezi app and system interface work

The Chwezi Product Excellence Standard was adopted by Lead Developer Peter
Bamuhigire and the Chwezi Core Systems design team, effective 01 November 2026
until further communication is given on the matter. It is mandatory for every
Chwezi app and system: Android, iOS, tablet, desktop and web, including internal
tools, tenant portals and admin consoles.

Trigger: the request designs, builds, changes, reviews or releases a screen,
flow, component, state, interface string or front-end of a Chwezi app or system,
on any stack. Marketing websites, decks and print collateral are out of scope
unless they reproduce product screens.

| Gate | Owner | What it decides |
|---|---|---|
| Product-quality gate (mandatory) | `chwezi-design-engine`, skill `skills/00-cross-cutting-ops-qa-a11y/chwezi-product-excellence-standard` (binding text `doctrine/product-excellence-standard.md`) | Screen contract and state matrix, the hard release gates, the weighted scorecard and the PASS, CONDITIONAL or BLOCKED verdict |
| Visual layer | `chwezi-design-engine`, `chwezi-business-app-house-style` | Tokens, type pair, shapes, components and motion |
| Engineering gates | `chwezi-dev-engine` front-end, mobile, offline and POS skills (for example `frontend-architecture`, `kmp-development`, `android-development`, `ios-development`, `pwa-offline-first`, `pos-sales-operations-engineering`) | Idempotency, offline durability, backend authorisation, performance on the declared baseline device, tests |
| Interface wording | `chwezi-design-engine` `ux-writing-and-microcopy`; where the operator's local routing table lists a private writing engine, its interface-copy skill owns the wording | Labels, state and error messages, payment and sync wording, number and date wording, translation-ready strings |
| Money, tax and statutory values | `chwezi-accounting-doctrine` | Recognition, posting and reconciliation behind the figures shown |

Rules:

- The product-quality gate is added to the handoff `sequence` for every
  triggered request, even when the user asks only for code. A request routed
  without it is incomplete.
- A release verdict comes only from that skill's scorecard and hard gates. A
  gate with `NOT_ASSESSED` evidence blocks release; the orchestrator never
  reports a pass the gate did not record.
- The skill defines 13 hard gates, `PX-GATE-01` to `PX-GATE-13`; any open
  gate means `BLOCKED`. `PASS` needs a weighted score of at least 85 out of
  100, no dimension below 2 and zero open gates; 70 to 84 with every shortfall
  owned, dated and accepted in writing is `CONDITIONAL`, which is not
  production-ready. `PX-GATE-13` (contiguous document numbering) applies
  wherever a screen issues numbered documents.
- Engines that carry a local copy of the standard apply it from that copy; the
  design engine's text is canonical, and a difference is a drift finding for the
  copy's owner, not a second standard.

Output must read as the work of a senior practitioner in each domain: specific
to the named user, decision, and context, never a generic template. Apply
`docs/operations/portfolio-craft-standard-2026-09-04.md`.

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


## Unattended development handoff

For a user-authorised long-running development plan, route to the project-local `auto-agents/README.md` and `auto-agents/config.json`. Require a committed plan, appropriate independent checks, explicit publication settings and a recovery handoff. The driver inherits host permissions; a worktree is not a security sandbox. Report live-runtime and unattended acceptance as NOT_ASSESSED until actually exercised.
