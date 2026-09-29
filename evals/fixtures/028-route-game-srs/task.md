# Contract-eval fixture 028-route-game-srs

Case: `evals/cases/028-route-game-srs.yaml` (route oracle; family: generic SRS vs game SRS (control)).

## Task given to the host

Specify requirements for our mobile puzzle game: levels, player progression, in-app purchases and store certification.

## Expected first skill

`srs-skills/19-game-software-requirements-specification`

## Engines in scope

- `srs-skills`

## Status

Executed lexically over the union by `run-contract-evals.py --route-oracles` (lexical proxy; not live routing, see agent-skills issue #620). Behavioural execution is `NOT_ASSESSED` until M10-05.
