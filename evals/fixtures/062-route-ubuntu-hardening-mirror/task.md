# Contract-eval fixture 062-route-ubuntu-hardening-mirror

Case: `evals/cases/062-route-ubuntu-hardening-mirror.yaml` (route oracle; family: mirrored dev owned negative (linux vs dev)).

## Task given to the host

Harden SSH, fail2ban and unattended upgrades on our Ubuntu server.

## Expected first skill

`linux-skills/linux-server-hardening`

## Engines in scope

- `linux-skills`

## Status

Executed lexically over the union by `run-contract-evals.py --route-oracles` (lexical proxy; not live routing, see agent-skills issue #620). Behavioural execution is `NOT_ASSESSED` until M10-05.
