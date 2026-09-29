# 11 — Measured evidence

> **Correction (29 Sep 2026, after the M10-14 independent review, finding F1/F3).** The Engine Eval Readiness used here (47.7) scored collision cleanliness 1.0 although the coordination package is not in the union collision scan, and excluded three executed known-defect oracles from p@1. Corrected: collision-clean `NOT_ASSESSED` = 0, p@1 30/42 = 0.7143, T2 = 40 x 0.1786 = 7.14, **Readiness 37.1**. Measured-constrained: hygiene = (52 + 37.1 + 66) / 3 = 51.70, overall 16.20 + 11.875 + 7.50 + 5.20 + 6.00 + 5.170 = **51.9**; **published 51.9**. The T1 of 8/8 uses a stand-in validator list (no `validators` entry for the package in `catalog/engines.yaml`). Source: `docs/operations/m10-kaizen-evidence/M10-14/eval-readiness.json`.

Host: Windows 11, Python 3.13, Node (local). Working directory: repository root at HEAD `8a438c9`.
`PYTHONDONTWRITEBYTECODE=1`. Run 29 Sep 2026 by the auditor. Outputs were written to the auditor's
scratch directory, not the repository. `git status` after the runs showed only files under
`docs/operations/` created by the concurrent M10-14 executor.

## Validators (the brief's list)

| # | Command | Exit | Key output |
|---:|---|---:|---|
| 1 | `python -X utf8 scripts/render_host_files.py --check --workspace-root ..` | 0 | `checked 12 repositories; findings 0; not assessed 0` |
| 2 | `node scripts/generate-plugin-manifest.js --check-marketplace --workspace-root ..` | 0 | `marketplace check: 23 ok, 0 drift, 0 not assessed` |
| 3 | `python -X utf8 evals/runners/run-contract-evals.py --out <scratch>/contract-evals.json` | 0 | `{"failed": 0, "passed": 77, "total": 77}` |
| 4 | `python -X utf8 scripts/validate-no-book-extractions.py` | 0 | `PASS: book-extraction check roots=12 findings=0` |
| 5 | `python -X utf8 scripts/validate-kaizen-cards.py` | 0 | three cards PASS; `Coordination Kaizen card structure valid.` |
| 6 | `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate-catalog.ps1` | 0 | `Catalog valid: 11 unique engines.` |
| 7 | `python -X utf8 -m pytest tests -q -p no:cacheprovider` | 0 | `162 passed in 79.22s` |
| 8 | `python -X utf8 scripts/validate-routing-baseline.py` | 0 | `PASS: routing baseline ratchet (5 engines + portfolio; lexical proxy, not live routing)` |
| 9 | `cd mcp-server; npm test` (node_modules present; no install) | 0 | `Test Files 6 passed (6); Tests 16 passed (16)` |

## Additional free checks

| Command | Exit | Key output |
|---|---:|---|
| `python -X utf8 evals/runners/run-contract-evals.py --route-oracles --workspace-root .. --out <scratch>` | 0 | primary@1 30/39 (76.9 %); engine@1 33/39 (84.6 %); must-co-activate@5 3/4; known defects 3 (primary@1 0/3); ties@1: 029; acceptance lexical primary@1 2/12, engine@1 6/12, behavioural NOT_ASSESSED |
| `python -X utf8 scripts/run_behavioural_eval.py --selftest` | 0 | `status: PASS`, 32/32 checks, `model_calls: 0` |
| `python -X utf8 scripts/skill_fanin.py --engine chwezi-engine-agents --json` | 0 | 1 active skill, 0 fixture files, `zero_inbound: 1`; reader notes "M10-03 adapters not delivered" |

Gated oracle misses (rank of expected primary): 031 anti-slop live 435; 050 website build 7; 045
East African English proposal 6; 051 PRD 5; 036 hospitality social 4; 055 release evidence 4; 042
EFRIS 3; 037 hospitality proposal 2; 053 Word report 2. Known defects (excluded from the gated
denominator): 030 rank 2, 032 rank 2, 044 rank 5.

All T2 figures are a lexical proxy, a drift guard, not proof of live routing.

## Portfolio facts cited from the M10-14 executor (not re-run)

Union collision scan (`docs/operations/m10-kaizen-evidence/M10-14/readiness/collision-scan.json`):
1,169 skills; 21 cross-engine pairs ≥ 0.75, all declared; 0 undeclared; 24 within-engine pairs
≥ 0.75 (reported, not gated; `evals/routing/baseline.json` still records 26). Tier 3: 0
`grading.json` files; 299 planned runs NOT_ASSESSED. Remote CI `validate` success at `8a438c9`
(two earlier runs failed on 29 Sep).

## Engine Eval Readiness arithmetic

| Slot | Input | Fraction | Label |
|---|---|---:|---|
| T1 | 8 of 8 package validators pass (executor-selected set; auditor re-ran all 8 plus `npm test`, all exit 0) | 1.0000 | measured |
| T2_p1 | Route-oracle primary@1 30/39, known defects excluded (auditor reproduced) | 0.7692 | measured |
| T2_neg | No owned negatives for the package's skill | 0 | NOT_ASSESSED |
| T2_cov | No routing fixtures for `rules-distill` (0/1) | 0 | NOT_ASSESSED |
| T2_clean | 0 cross-engine pairs ≥ 0.75 involve the package | 1.0000 | measured |
| T3 | 0 executed of planned runs | 0 | NOT_ASSESSED (zero-spend rule) |

- T1 points = 30 × 1.0000 = 30.00
- T2 mean = (0.7692 + 0 + 0 + 1.0000) ÷ 4 = 0.4423; T2 points = 40 × 0.4423 = 17.69
- T3 points = 30 × 0 = 0.00
- **Readiness = 47.7.** The auditor agrees with the executor's figure.

Sensitivity note: counting the three known-defect oracles as executed failures (30/42 = 0.7143)
gives T2 points 17.14 and Readiness 47.1. The rubric's denominator rule is written for unexecuted
items; these three were executed and failed, so the stricter reading is arguable. The published
figure uses the executor's convention; the difference is 0.6 Readiness points and 0.02 overall.

## NOT_ASSESSED list

- T2_neg and T2_cov for this package (no fixtures for its own skill).
- T3: every behavioural suite (solution-selection, acceptance, pressure, MCP, orientation), zero-spend rule.
- Acceptance prompts, behavioural arm.
- Dimension 7 (accessibility): not applicable, unweighted.
- Standards currency: no fresh external research; judged from the engine's own records.
- Remote CI: not re-queried by the auditor; cited from the executor.
