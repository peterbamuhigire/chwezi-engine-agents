# chwezi-engine-agents — M10-14 measured re-audit (29 Sep 2026)

> **Correction (29 Sep 2026, after the M10-14 independent review, finding F1/F3).** The Engine Eval Readiness used here (47.7) scored collision cleanliness 1.0 although the coordination package is not in the union collision scan, and excluded three executed known-defect oracles from p@1. Corrected: collision-clean `NOT_ASSESSED` = 0, p@1 30/42 = 0.7143, T2 = 40 x 0.1786 = 7.14, **Readiness 37.1**. Measured-constrained: hygiene = (52 + 37.1 + 66) / 3 = 51.70, overall 16.20 + 11.875 + 7.50 + 5.20 + 6.00 + 5.170 = **51.9**; **published 51.9**. The T1 of 8/8 uses a stand-in validator list (no `validators` entry for the package in `catalog/engines.yaml`). Source: `docs/operations/m10-kaizen-evidence/M10-14/eval-readiness.json`.

Independent audit of the portfolio coordination package at committed HEAD `8a438c9`. Method:
`chwezi-dev-engine/skills/sdlc-meta/skill-engine-audit` with the AO-14 "Engine Eval Readiness
(measured)" rules. The package is not a domain skill engine; its output types are the coordination
products listed in `05-per-output-type-readiness.md`.

## Headline numbers

| Number | Score /100 | Basis |
|---|---:|---|
| Raw | **52.5** | Weighted overall from judged dimensions, routing judged at 55 |
| Measured-constrained | **52.3** | Routing replaced by Engine Eval Readiness 47.7 |
| Published | **52.3** | `min(52.3, 65)`; the cap does not bind |
| Engine Eval Readiness | **47.7** | T1 30.00 + T2 17.69 + T3 0 (NOT_ASSESSED); recomputed and agreed |

Weighting: output readiness 30, skill depth and worked examples 25, standards currency 15,
taxonomy 10, doctrine 10, hygiene 10 (hygiene = mean of redundancy, discovery/routing, safety).

## Verdict

The package has moved from a structural registry with shape-only evals (baseline, 29 Sep morning) to
a genuine portfolio control plane: a host-file and shared-asset drift checker that passes across
twelve repositories, a union collision gate with an ownership register and zero undeclared pairs,
executed lexical route oracles with a ratchet, a zero-spend Tier-3 harness whose 32 self-checks pass,
and 162 passing Python tests. All nine validators run for this audit exited 0. It stays well short of
the bar because none of its routing evidence is behavioural (Tier 3 has 0 of 299 planned runs, the
acceptance prompts reach the right primary skill lexically only 2 times in 12), its own release chain
has never produced a tag and still contradicts its supply-chain policy, legacy `skills-engine-agents`
naming survives in three shipped surfaces that the drift checker does not inspect, and the M10
running log stops at M10-02 while phase ratifications remain open.

## Files

| File | Contents |
|---|---|
| [00-executive-summary.md](00-executive-summary.md) | Verdict, headline findings, strengths, path to the bar |
| [01-methodology-and-rubric.md](01-methodology-and-rubric.md) | Method, commands, rubric, weighting, limitations, independence statement |
| [02-coverage-and-taxonomy.md](02-coverage-and-taxonomy.md) | Taxonomy score and named deficiencies |
| [03-existing-groups-audit.md](03-existing-groups-audit.md) | Per-group and per-unit scores |
| [05-per-output-type-readiness.md](05-per-output-type-readiness.md) | Nine output types scored and ranked |
| [09-master-scorecard.md](09-master-scorecard.md) | Eleven dimensions, groups, output types, the three numbers with arithmetic |
| [10-roadmap-to-world-class.md](10-roadmap-to-world-class.md) | P0/P1/P2 moves and target scores |
| [11-measured-evidence.md](11-measured-evidence.md) | Commands, exit codes, output lines, Readiness arithmetic, NOT_ASSESSED list |

Not re-run in the M10-14 measured re-audit:

- `04-gap-analysis-new-skills.md` — not re-run in the M10-14 measured re-audit (gaps are listed in 02 and 10).
- `06-standards-benchmark.md` — not re-run in the M10-14 measured re-audit (no fresh external research; standards currency is judged from the engine's own currentness records).
- `07-hardening-existing-skills.md` — not re-run in the M10-14 measured re-audit (hardening moves are named in 10).
- `08-reading-list.md` — not re-run in the M10-14 measured re-audit.
