# Contract-eval fixture 059-route-funding-request-mirror

Case: `evals/cases/059-route-funding-request-mirror.yaml` (route oracle; family: mirrored srs owned negative (business case must not win)).

## Task given to the host

Prepare the funding request section of a bankable business plan for the lender.

## Expected first skill

`business-plan-skills/11-funding-request`

## Engines in scope

- `business-plan-skills`

## Status

Executed lexically over the union by `run-contract-evals.py --route-oracles` (lexical proxy; not live routing, see agent-skills issue #620). Behavioural execution is `NOT_ASSESSED` until M10-05.
