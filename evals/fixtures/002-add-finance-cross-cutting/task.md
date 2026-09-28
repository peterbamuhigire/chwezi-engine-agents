# Contract-eval fixture 002-add-finance-cross-cutting

Case: `evals/cases/002-add-finance-cross-cutting.yaml` (routing case).

## Task given to the host

Route business plan finance work to business-plan-skills plus accounting doctrine

## Engines in scope

- `business-plan-skills`
- `chwezi-accounting-doctrine`

## Status

The deterministic runner checks case shape, fixture presence and that `expected.yaml` agrees with the case. It does not execute a model. Behavioural execution is `NOT_ASSESSED` until M10-05 (zero-spend rule).
