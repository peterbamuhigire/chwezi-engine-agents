# 10 — Roadmap to world-class

Current published score 52.3; Readiness 47.7. Targets are measured-constrained and assume no
Tier-3 spend until P1 is authorised.

## P0 — correctness of what already exists (target 56; Readiness up to 67.7 if the new fixtures pass, ceiling 70 while T3 is unexecuted)

| Move | Files | Effect |
|---|---|---|
| Retire the legacy name and align versions | `.codex-plugin/plugin.json` (`name`), `.github/workflows/release.yml` (archive and artefact names), `mcp-server/package.json` and `mcp-server/src/index.ts` (name, version 1.1.0) | Hygiene |
| Extend drift control to those surfaces | `scripts/render_host_files.py` (version and name invariants), `tests/test_render_host_files.py` | Stops recurrence |
| Correct the bridge contract | `docs/operations/claude-bridge-contract.md` line 56 (the coordination bridge has a registered Claude-only block) | Doctrine consistency |
| Make the supply-chain policy true | either add adapter, installer, security tests and a secret scan to `release.yml`, or reduce the claims in `docs/security/supply-chain-policy.md` | Safety |
| Give `rules-distill` routing fixtures: 3 positives, 2 owned negatives | a new fixture file read by `scripts/skill_fanin.py` and the Readiness script | T2_cov 0 → 1.0 and T2_neg 0 → measured; Readiness up to about 67.7 if all pass |
| Self-catalogue the package's validators | `catalog/engines.yaml` (or a sibling register) and `schemas/engine-catalog.schema.json` | Declared T1 denominator; MCP can validate the package |
| Complete the running log | `docs/operations/m10-kaizen-execution-2026-09-29.md` sections M10-03 to M10-14 with verdicts | Governance |

## P1 — routing quality and first behavioural proof (target 61; Readiness 60–75)

| Move | Files | Effect |
|---|---|---|
| Fix the nine gated oracle misses (031, 036, 037, 042, 045, 050, 051, 053, 055) and the three known defects | owning engines' descriptions or fixtures; `evals/routing/rejected-changes.md` rows; `evals/routing/baseline.json` floor raise | T2_p1 towards 0.95 |
| Converge the duplicated meta-skills the register names (`validation-contract`, `ai-slop-audit`, `anti-ai-slop`, `excel-spreadsheets`) to pointers | owning engines; `evals/routing/ownership.yaml` follow-ups | Redundancy |
| Authorised Tier-3 pilot: 12 acceptance cases, n = 3, one pinned model and CLI version | `scripts/run_behavioural_eval.py --suite acceptance --allow-model-calls`; commit summaries under `evals/behavioural/` | T3 > 0; lifts the 70 Readiness ceiling |
| Add a filled multi-engine handoff example | `core/examples/handoff-clinic-admissions.md` (from case 022) | Worked examples |
| `released_commit` freshness check with a stated tolerance | `scripts/validate-catalog.ps1` or `render_host_files.py` | Registry hygiene |

## P2 — release and scale (target 65; published remains capped at 65 until craft acceptance evidence exists)

| Move | Files | Effect |
|---|---|---|
| Cut and sign the first release; pin marketplace refs to tags | `release.yml`, `release/checksums.txt`, `.claude-plugin/marketplace.json` | Production readiness |
| Put all 20 pytest files and the hook JS tests in CI | `.github/workflows/validate.yml` | Safety, hygiene |
| Set a portfolio metadata target against the 60,000-character budget, or retire the budget | `docs/runtime-skill-budget.md`, `scripts/validate-runtime-skill-budget.py` | Hygiene |
| Render adapter prompts and wrappers from `core/` | `scripts/render_host_files.py`, `adapters/*` | Single source |
| Pilot `PROJECT.md` on one client project; regenerate tours in CI | `templates/project-context/`, `scripts/generate_engine_tour.py` | Output types 6 |
| Split `scripts/` by function with an index; separate contracts from logs in `docs/operations/` | repository layout | Taxonomy |

A score above 65 needs, at minimum, executed Tier-3 results at acceptable pass rates and the portfolio
craft standard's acceptance evidence; neither is in reach without authorised spend.
