# Improvement backlog

| Priority | Decision and proof |
|---|---|
| P0 | Critical F-01 remains open in optional MCP dependencies (13 advisories, including one critical). The owning release review requires separate remediation and verification. Security and licensing exceptions remain outside the score. |
| P1 | `evals/runners/run-contract-evals.py`. One parse error caused the lexical pass to read the rejected file again and abort before writing the report. Filter oracle inputs using the recorded shape verdict. Replay one valid oracle beside one malformed case. |
| P2 | Optional MCP dependency advisories and simulated push false refusals require separate impact and compatibility checks. The suite marketplace check is read-only and found a pre-existing count mismatch. |

Owner: repository maintainer. Counter-metric: Exit remains 1 and the valid oracle still ranks. All 77 ordinary case results and the oracle result object match the baseline. Roll back the owning change and its paired regression together if the ordinary case fails. Retain all failed observations.

Nystrom (2021), *Crafting Interpreters*, §6.3.1. Resume at the next independent input after a syntax error.
