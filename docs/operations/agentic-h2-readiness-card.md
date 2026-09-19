# H2 scale-readiness and agentic-literacy card

Status: draft coordination reference; promotion requires named-owner review.
Owner: coordination maintainer. Reviewer: named domain owner before promotion.
Action: B01-A04. Scope: one bounded local task in fixture or shadow mode.

## Purpose and scope

Use this card to decide whether an observed, supervised AI-assisted task is
ready for a larger H2 pilot. H2 means a repeatable, bounded operating practice;
an H3 vision or whole-role automation claim remains a hypothesis. The card
records one actor and event, one invariant, one acceptance oracle and one
fallback so a reviewer can stop the route without granting new authority.

## Input and provenance contract

Record these inputs before the exercise:

| Field | Required content |
| --- | --- |
| `task_id` | Stable local task identifier and actor/event. |
| `source_refs` | Source paths, versions or fixture IDs used by the task. |
| `invariant` | Domain rule that must remain true. |
| `rights_scope` | Read/write scope, denied data and approval boundary. |
| `baseline` | Prior manual route, measured criterion and observation date. |
| `reviewer` | Named person who can accept, hold or stop the exercise. |
| `fallback` | Manual or prior-version route and recovery owner. |

`source_refs`, observed outputs and execution metadata are observations. A
claim about likely generalisation, future scale or agentic literacy is an
inference and must be labelled as such. Missing or stale evidence is
`NOT_ASSESSED`; it is never converted into a passing value.

## Decision procedure

1. Inspect the task, source boundary, data rights and prior manual baseline.
2. Run one role-specific supervised exercise on synthetic or explicitly cleared
   inputs. The participant must identify source, authority, stop condition and
   recovery route.
3. Compare the output with the independent acceptance oracle and inspect false
   passes, false alarms and any authority expansion.
4. Record a decision: `READY_FOR_H2_PILOT`, `HOLD`, or `NOT_ASSESSED`.
5. Keep H3 or whole-role statements in the hypothesis field until a separately
   measured review supports them.

## Failure, unknown and denied states

| State | Required response |
| --- | --- |
| Missing owner, reviewer, integration, skill or fallback | `HOLD`; do not scale. |
| Source, authority or rights boundary cannot be identified | `HOLD`; preserve the manual route. |
| Exercise or oracle was not run | `NOT_ASSESSED`; no readiness claim. |
| Input or action is denied or out of scope | Stop, record the denial and escalate to the owner. |
| Regression against the baseline | Disable the new route and restore the prior route. |

Pure checking remains separate from actions. This card never authorises live
changes, model changes, publication or production certification.

## Acceptance oracle

The participant names the source, authority, stop condition and recovery path;
the output satisfies the task invariant; the reviewer can reconstruct the
comparison with the prior baseline; and all missing evidence is visibly
`NOT_ASSESSED`. A readiness decision fails if any required integration, owner,
skill, fallback or independent oracle is absent.

## Synthetic exercise

Observation: fixture `h2-invoice-review-001` contains three synthetic invoices,
one intentionally missing approval metadata and a manual baseline showing the
required escalation.

Expected observation: the participant identifies the missing approval, stops
before posting an entry, cites the fixture and routes the case to the named
reviewer. The measured comparison is limited to this fixture.

Inference: the participant may be ready for a larger supervised H2 sample only
if the acceptance oracle passes and the reviewer records the decision. This is
not evidence of whole-role automation or production impact.

## Handoff and rollback

Handoff fields are `task_id`, `decision`, `observations`, `inferences`,
`evidence_refs`, `unknowns`, `blockers`, `fallback`, `owner`, `reviewer` and
`re_audit_date`. Preserve the prior schema/reference and disable the route on a
regression. The next action is one named supervised fixture or a documented
`NOT_ASSESSED` review.

## Evidence labels

- **Observation:** directly read or measured in the named fixture/run.
- **Inference:** reviewer interpretation that remains bounded by observations.
- **NOT_ASSESSED:** required evidence was unavailable, unrun or stale.

These labels are part of the record, not editorial decoration.
