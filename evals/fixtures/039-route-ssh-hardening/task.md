# Contract-eval fixture 039-route-ssh-hardening

Case: `evals/cases/039-route-ssh-hardening.yaml` (route oracle; family: SSH hardening (linux vs dev; control)).

## Task given to the host

Harden SSH on the Ubuntu server and disable password logins.

## Expected first skill

`linux-skills/linux-server-hardening`

## Engines in scope

- `linux-skills`

## Status

Executed lexically over the union by `run-contract-evals.py --route-oracles` (lexical proxy; not live routing, see agent-skills issue #620). Behavioural execution is `NOT_ASSESSED` until M10-05.
