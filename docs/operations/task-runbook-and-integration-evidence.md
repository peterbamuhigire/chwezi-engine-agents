# Task runbook and integration evidence

Status: draft coordination runbook reference; promotion requires named-owner
review. It does not certify a vendor, legal position or production integration. Owner: coordination
maintainer. Action: B33-A05. Reviewer: named integration owner before release.

## Purpose and scope

Use this runbook to make one task discoverable from request through integrated
outcome. The authoritative task registry is the source of identity, ownership,
scope and status; consumer indexes are derived views and must not become a
second registry. A completion claim requires propagated scope, evidence and
known exceptions.

## Input and provenance contract

The registry entry records `task_id`, user job, owner, selected engine(s),
inputs and versions, rights/data scope, acceptance oracle, fallback, status,
evidence references, known exceptions and re-audit date. The integration packet
also records source and target paths, change boundary, validation command,
result, reviewer and rollback.

Every record labels observations, inferences and `NOT_ASSESSED` evidence.
Vendor assertions, current legal claims and production outcomes require their
own authoritative evidence; a prose assertion cannot fill an evidence gap.

## Decision procedure

1. Find the task by user job in the index and resolve its authoritative registry
   entry.
2. Check owner, selected engine, input versions, rights scope, oracle and
   fallback before running anything.
3. Execute the documented native validator from the owning engine. Capture the
   exact command, working directory, input hash, exit code, duration and output
   locator.
4. Reconcile consumer indexes with the registry. Conflicting copies are a
   failure until one authoritative value is restored.
5. Mark the task `COMPLETE` only when the integrated outcome, propagated scope,
   evidence and known exceptions are recorded. Otherwise use `BLOCKED`, `HOLD`
   or `NOT_ASSESSED` with a next action.

## Failure, unknown and denied states

| State | Required response |
| --- | --- |
| Task or owner cannot be found | `BLOCKED`; do not invent a route or owner. |
| Registry and index disagree | `FAIL`; repair the derived index from the registry. |
| Validator command or dependency is unavailable | `NOT_ASSESSED`; preserve the reason. |
| Rights, identity or data scope is denied | Stop, retain the denial and escalate. |
| Vendor assertion lacks required evidence | Record an evidence gap; do not mark complete. |
| Integration fails or is interrupted | Keep the task incomplete and use the rollback route. |

No model, agent, vendor or operator may broaden the task's authority by filling
an unknown value. Pure checking is separate from actions; consequential changes
require the existing owner approval boundary.

## Acceptance oracle

A fresh operator can locate the correct task, inputs, owner, acceptance oracle,
fallback and native validation command from the index and registry. The final
packet contains the exact command and result, source/target scope, evidence
references, known exceptions, reviewer and rollback. Any missing required field
or unavailable check remains visibly `NOT_ASSESSED` and blocks completion.

## Synthetic interoperability and identity case

Observation: fixture `synthetic-clinic-procurement-001` links a synthetic
procurement request, a synthetic supplier identity, an engine handoff and an
audit event. It contains no real patient, supplier or legal data.

Expected observation: the operator resolves one registry task, detects an
identity mismatch before integration, records the failed oracle and routes the
case to the named reviewer. The mismatch is not silently repaired.

Inference: a registry-backed runbook may improve handoff traceability for this
fixture. That inference is bounded to the fixture and is not a current
healthcare procurement or legal claim.

## Handoff and rollback

The handoff follows `core/contracts/handoff.yaml`: `scope`, `engines`, `inputs`,
`sequence`, `evidence`, `blockers` and `next_action`. Add task identity,
owner, reviewer, validation result, known exceptions and rollback locator in
the evidence payload. On failure or interruption, retain the incomplete task,
restore the prior route or reference and schedule re-audit; never delete the
audit trail.

## Evidence labels

- **Observation:** directly read or measured from the synthetic fixture or
  named validator run.
- **Inference:** bounded interpretation of those observations.
- **NOT_ASSESSED:** unavailable, unrun or stale evidence; it blocks completion.
