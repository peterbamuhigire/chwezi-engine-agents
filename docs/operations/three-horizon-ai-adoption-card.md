# Three-horizon adoption and capability-frontier card

Status: draft coordination reference; promotion requires named-owner review.
Capability claims remain task bounded. Owner: coordination maintainer. Reviewer:
named owner before use.
Action: B02-A04. Scope: one bounded local experiment with a re-review date.

## Purpose and scope

Use this card to connect an immediate practice to longer-term adoption without
claiming that a task-level result automates a whole role. Each horizon has an
owner, an evidence state and a stop condition. The capability frontier is
recorded as jagged: an ability demonstrated on one task does not transfer to
adjacent tasks without evidence.

## Input and provenance contract

Record `task_id`, current baseline, source/version references, task owner,
reviewer, rights and data scope, measured criterion, fallback, re-review date
and the three horizon records. Current or volatile capability claims require a
currentness review; absent currentness evidence is `NOT_ASSESSED`.

Each horizon record contains `horizon`, `outcome`, `owner`, `evidence_refs`,
`evidence_state`, `stop_condition` and `next_action`. Use only observations
from the named task and clearly label any inference about future capability.

## Decision procedure

1. Map current task waste and choose one 30-day bounded practice with a baseline.
2. Define the three horizons separately:
   - **H1 — now:** a measured task-level improvement and its fallback.
   - **H2 — next:** a structural integration hypothesis with owner and evidence
     needed before a supervised pilot.
   - **H3 — later:** a human-need or operating-model hypothesis, never a measured
     outcome unless independent evidence exists.
3. Record capability gaps, denied states, review date and stop condition for each
   horizon.
4. Re-review the frontier at the stated date; do not promote an unsupported
   capability or infer whole-role automation.

## Failure, unknown and denied states

| State | Required response |
| --- | --- |
| Missing horizon owner, evidence or stop condition | `HOLD`; roadmap entry is incomplete. |
| Task result is absent or not comparable to baseline | `NOT_ASSESSED`; do not score improvement. |
| Currentness review is required but unavailable | `NOT_ASSESSED`; retain the claim as a hypothesis. |
| Rights, data or action is denied | Stop and preserve the fallback; record the denial. |
| Frontier regression or false pass | Disable the new route and re-open H1 evidence. |

Unsupported capability remains `NOT_ASSESSED`. A roadmap link is not evidence,
and an inference cannot satisfy an acceptance oracle by itself.

## Acceptance oracle

H1 contains a measured criterion and baseline; H2 contains an integration owner,
evidence requirement and supervised stop condition; H3 is explicitly marked as
a hypothesis unless independently supported. The record links the immediate
experiment to medium-term integration work and names the next re-review date.

## Synthetic exercise

Observation: fixture `frontier-routing-001` measures the time and error count
for routing one synthetic request across two known engines. The same fixture
does not test new domains or production throughput.

H1 observation: the bounded route reduces the declared manual steps on the
fixture while preserving the documented fallback. H2 inference: a supervised
registry integration may be useful after owner and currentness review. H3
hypothesis: human review remains necessary for ambiguous or consequential work.

The example is deliberately narrow; it does not establish a role-level or
production capability claim.

## Handoff and rollback

Handoff fields are `task_id`, `horizon_records`, `observations`, `inferences`,
`evidence_refs`, `unknowns`, `blockers`, `fallback`, `owner`, `reviewer`,
`re_review_date` and `next_action`. Preserve the earlier baseline and record
the reason for any horizon change. If the experiment regresses, return to the
prior route and mark the affected horizon `HOLD` or `NOT_ASSESSED`.

## Evidence labels

- **Observation:** directly measured or read in the named fixture/run.
- **Inference:** bounded interpretation tied to those observations.
- **NOT_ASSESSED:** missing, stale or unrun evidence; no capability claim.
