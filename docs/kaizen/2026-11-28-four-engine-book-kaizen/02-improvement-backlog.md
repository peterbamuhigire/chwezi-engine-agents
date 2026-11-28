# Improvement backlog

| Priority | Decision and proof |
|---|---|
| P0 | F-01 opened with 13 MCP dependency findings, including one critical. The second wave cleared this lockfile's findings and exercised the clean Windows build and tests. [Validation record](04-validation-record.md#second-wave-mcp-dependency-check). Security and licensing exceptions remain outside the score. |
| P1 | `evals/runners/run-contract-evals.py`. One parse error caused the lexical pass to read the rejected file again and abort before writing the report. Filter oracle inputs using the recorded shape verdict. Replay one valid oracle beside one malformed case. |
| P2 | Simulated push false refusals and the suite marketplace count mismatch remain tracked separately. |

Owner: repository maintainer. Counter-metric: Exit remains 1 and the valid oracle still ranks. All 77 ordinary case results and the oracle result object match the baseline. Roll back the owning change and its paired regression together if the ordinary case fails. Retain all failed observations.

Nystrom (2021), *Crafting Interpreters*, §6.3.1. Resume at the next independent input after a syntax error.
