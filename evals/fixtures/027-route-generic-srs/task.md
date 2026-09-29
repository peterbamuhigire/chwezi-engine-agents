# Contract-eval fixture 027-route-generic-srs

Case: `evals/cases/027-route-generic-srs.yaml` (route oracle; family: generic SRS vs game SRS (probe misroute)).

## Task given to the host

Write the SRS for the patient billing module.

## Expected first skill

`srs-skills/01-initialize-srs`

## Engines in scope

- `srs-skills`

## Status

Executed lexically over the union by `run-contract-evals.py --route-oracles` (lexical proxy; not live routing, see agent-skills issue #620). Behavioural execution is `NOT_ASSESSED` until M10-05.
