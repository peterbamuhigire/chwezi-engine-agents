# Contract-eval fixture 025-route-lighthouse-cwv

Case: `evals/cases/025-route-lighthouse-cwv.yaml` (route oracle; family: Lighthouse / Core Web Vitals (website vs design)).

## Task given to the host

Run a Lighthouse audit on the company website and fix the Core Web Vitals failures before launch.

## Expected first skill

`website-skills/deploy`

## Engines in scope

- `website-skills`
- `chwezi-design-engine`

## Status

Executed lexically over the union by `run-contract-evals.py --route-oracles` (lexical proxy; not live routing, see agent-skills issue #620). Behavioural execution is `NOT_ASSESSED` until M10-05.

Formerly a known defect pinned to M10-11; unpinned after M10-11-T09 (deploy description names the Lighthouse or Core Web Vitals audit of a built site). Now gated in primary@1.
