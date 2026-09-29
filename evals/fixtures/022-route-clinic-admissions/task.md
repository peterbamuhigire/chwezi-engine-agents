# Contract-eval fixture 022-route-clinic-admissions

Case: `evals/cases/022-route-clinic-admissions.yaml` (routing case).

## Task given to the host

Specify a clinic admissions workflow with English and Luganda patient-facing screens, payment collection, billing and refunds. Identify the applicable Uganda statutory and health-data requirements using current sources, then prepare an implementation handoff. Keep medical judgment out of scope.

## Engines in scope

- `chwezi-sdlc-documentation`
- `digital-research-skills`
- `chwezi-dev-engine`
- `chwezi-design-engine`
- `chwezi-accounting-doctrine`

## Status

The deterministic runner checks case shape, fixture presence and that `expected.yaml` agrees with the case. It does not execute a model. Behavioural execution is `NOT_ASSESSED` until M10-05 (zero-spend rule).
