# Contract-eval fixture 042-route-efris-integration

Case: `evals/cases/042-route-efris-integration.yaml` (route oracle; family: fiscal tax (dev integration, finance co-activation)).

## Task given to the host

Integrate EFRIS e-invoicing into our POS backend with offline queueing and retries.

## Expected first skill

`chwezi-dev-engine/electronic-fiscal-taxing`

## Engines in scope

- `chwezi-dev-engine`
- `chwezi-accounting-doctrine`

## Status

Executed lexically over the union by `run-contract-evals.py --route-oracles` (lexical proxy; not live routing, see agent-skills issue #620). Behavioural execution is `NOT_ASSESSED` until M10-05.
