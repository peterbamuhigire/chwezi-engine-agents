# Contract-eval fixture 047-route-ad-group-policy

Case: `evals/cases/047-route-ad-group-policy.yaml` (route oracle; family: Windows administration (control)).

## Task given to the host

Audit Group Policy objects and fix the ones that are not applying to the finance OU.

## Expected first skill

`windows-admin-engine-skills/windows-group-policy`

## Engines in scope

- `windows-admin-engine-skills`

## Status

Executed lexically over the union by `run-contract-evals.py --route-oracles` (lexical proxy; not live routing, see agent-skills issue #620). Behavioural execution is `NOT_ASSESSED` until M10-05.
