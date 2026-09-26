# Codex model-policy conflict register

**Recorded:** 2026-09-27 (Africa/Kampala)  
**Owner:** Portfolio/runtime policy owner (Peter)  
**Scope:** P00 precedence resolution for plan, engine policy, saved config and runtime catalogue. This register preserves superseded text; it does not revive it.

## Controlling decision

The latest explicit user instruction supplied for this task controls: use GPT-6 Luna/high by default across orchestration, implementation, research, review and execution; use GPT-6 Astra only if Peter explicitly selects Astra for the task; never use GPT-5.6 or silently fall back to it. Report an unavailable required GPT-6 model. Do not infer the running session model from saved config or local catalogue. This resolves the pilot route without inventing a different model split for research/audit work. API/runtime visibility is evidence of catalogue listing only, not user/account entitlement.

## Superseded plan-level assignment (preserved verbatim)

Source: skills-kaizen/evidence/model-and-input-evidence.json, historical audit input. It records the pre-correction user target and separate planning/coding assignments:

~~~json
{
  "planning_design": [
    "gpt-6-astra",
    "medium"
  ],
  "coding_implementation": [
    "gpt-6-luna",
    "high"
  ]
}
~~~

The historical proposal in skills-kaizen/03-source-and-tool-assessment.md was:

~~~text
| Historical work label | Historical proposal |
|---|---|
| Planning and design | gpt-6-astra / medium |
| Coding and implementation | gpt-6-luna / high |
| Research, audit and acceptance review | Explicit assignment needed for each run |
~~~

This proposal is historical evidence only. It conflicted with the later universal Luna/high rule and explicit-only Astra exception.

## Superseded engine policy (preserved verbatim)

Source: Chwezi Dev .codex/model-policy.md at parent of commit 69c8a58 (pre-P00 copy); SHA-256 e267a1b26966873164fc0695c70e038bec71e6dd4bc546e66fa9fc29eb2afa9c. The 2026-09-07 policy text retained a GPT-5.6 Luna default while allowing explicit Astra:

~~~text
## Codex model and delegation policy

Peter's rule, effective 2026-09-07. Apply only in Codex. Claude and other
consumers retain their own model selection and all domain-engine capabilities.

- Root/orchestrator, final reviewer, and execution subagents default to
  `gpt-5.6-luna` with high reasoning.
- Use `gpt-6-astra` only when Peter explicitly selects it for a task that needs
  its additional capability. Astra is never selected automatically.
- Every spawned role must explicitly use `gpt-5.6-luna` with high reasoning
  unless Peter has manually selected Astra for that task. On hosts that prohibit
  model overrides with full-history forks, use a bounded-context or no-history
  fork with a sufficient task brief. Preserve the selected model through nested
  execution.
- Give each worker its outcome, context, exact scope, file ownership,
  constraints, acceptance checks and evidence handoff. Use parallel writers
  only for independent ownership. Keep trivial tasks with the root.
- On worker failure, record it, inspect the cause, narrow or retry the task,
  and return unresolved decisions to the user. Never silently substitute
  another model or claim delegation occurred without an actual spawn.
- Before final delivery, the assigned model reviews the real diff and relevant
  tests, integrates material findings, resolves conflicts and waits for required
  agents. Missing tests, sources or reviewers remain `NOT_ASSESSED`.
- Every Kaizen operation MUST check current official model releases and the
  active runtime/account model catalogue before retaining or proposing changes
  to the model policy. Record dated source URLs, model IDs, availability,
  task-fit evidence, cost/latency/quality considerations, uncertainties and a
  retain/change decision. Newer does not automatically mean better. Use the
  Digital Research currentness gate; do not infer latest status from memory.
- These pins remain until Peter authorises a verified replacement. A new
  release triggers evaluation, not a silent model switch. If current sources
  or model selection are unavailable, report the limitation and leave the
  model evaluation `NOT_ASSESSED`; do not weaken the engine's other gates.
- Configuration applies to newly started sessions; do not claim a running
  root changed models because a file was edited. Report any session override
  or unavailable pin. This is a configuration and agent-instruction policy,
  not an administrative restriction on the user's model controls.
~~~

That instruction predates Peter's 2026-09-26 GPT-6-only policy. The full historical block is retained above so its constraints and caveats remain reviewable.

## Saved configuration conflict and resolution

Observed before correction: root model gpt-6-luna, root reasoning effort medium, review model gpt-6-luna. This conflicted with the explicit Luna/high saved-default requirement. P00 changed only model_reasoning_effort to high, with a byte backup and parsed-value preservation check. The setting affects new sessions; the active session identity remains NOT_ASSESSED. Hashes and backup path are recorded in skills-kaizen/evidence/P00/result.json.

## Runtime catalogue versus policy

The latest local Codex cache recorded in skills-kaizen/evidence/model-currentness-2026-09-27.json lists GPT-6 Astra, Sol and Luna and also lists GPT-5.6 Sol, Terra and Luna. Cache listing does not override the explicit prohibition on GPT-5.6 and is not proof of account entitlement. Hidden catalogue IDs, account access and live-session model remain separately unassessed.

## Decision rights and residuals

- **Policy owner:** Peter supplies and accepts model-policy changes.
- **Implementer:** changes only the exact authorized plan/helper/config scope; config changes require verified drift, backup and preservation evidence.
- **Reviewer:** independent review of the actual cross-repository diff is still required before P00 closure; none is claimed here.
- **Runtime maintainer:** verifies which settings a future session loads; no current session switch is claimed.

P00 remains **IN_PROGRESS** until its written independent-review and policy-owner acceptance gates close. No P01 dependent implementation or phase-count push is implied by this register.
