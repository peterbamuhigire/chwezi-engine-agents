# Contract-eval fixture 030-route-slop-audit

Case: `evals/cases/030-route-slop-audit.yaml` (route oracle; family: slop audit (dev vs research vs srs)).

## Task given to the host

Grade this finished client report for AI slop and give it an A, B, C or F verdict with evidence.

## Expected first skill

`chwezi-dev-engine/ai-slop-audit`

## Engines in scope

- `chwezi-dev-engine`

## Status

Executed lexically over the union by `run-contract-evals.py --route-oracles` (lexical proxy; not live routing, see agent-skills issue #620). Behavioural execution is `NOT_ASSESSED` until M10-05.

Known defect pinned to later-wave; counted separately from primary@1.
