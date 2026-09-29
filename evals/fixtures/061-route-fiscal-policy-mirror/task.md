# Contract-eval fixture 061-route-fiscal-policy-mirror

Case: `evals/cases/061-route-fiscal-policy-mirror.yaml` (route oracle; family: mirrored dev owned negative).

## Task given to the host

Set the fiscal-tax controls and authority reporting policy for e-receipts, separate from ledger truth.

## Expected first skill

`chwezi-accounting-doctrine/electronic-fiscal-taxing`

## Engines in scope

- `chwezi-accounting-doctrine`

## Status

Executed lexically over the union by `run-contract-evals.py --route-oracles` (lexical proxy; not live routing, see agent-skills issue #620). Behavioural execution is `NOT_ASSESSED` until M10-05.
