# Contract-eval fixture 064-route-firewall

Case: `evals/cases/064-route-firewall.yaml` (route oracle; family: Linux networking (control)).

## Task given to the host

Configure the firewall and install a Let's Encrypt certificate on our Ubuntu web server.

## Expected first skill

`linux-skills/linux-firewall-ssl`

## Engines in scope

- `linux-skills`

## Status

Executed lexically over the union by `run-contract-evals.py --route-oracles` (lexical proxy; not live routing, see agent-skills issue #620). Behavioural execution is `NOT_ASSESSED` until M10-05.
