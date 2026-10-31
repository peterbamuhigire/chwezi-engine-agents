# Frozen baseline: portfolio kaizen pass 2 (31 October 2026)

Frozen before any change, from HEAD `edc0a70` and the eleven engines at the HEADs in
[`evidence/engine-heads-baseline.txt`](evidence/engine-heads-baseline.txt). Scores are reviewer judgements against the named evidence
(inference), on the same eleven dimensions and equal weights as the 29 October baseline
(`skills/sdlc-meta/skill-engine-audit/references/audit-dimensions.md` in the dev engine). The published figure is `min(raw, 65)`.
Missing proof lowers a score; a dimension is never raised for a plan.

| Dimension | 29 Oct baseline | Raw /100 now | Evidence and deficiency |
|---|---:|---:|---|
| Doctrine and philosophy | 65 | 62 | Router boundaries and safety rules are explicit. The supply-chain policy still claims release checks the workflow does not run (F-07); `AGENTS.md:14` carries a Windows web-root path (F-08). |
| Taxonomy and structure | 60 | 56 | Eleven-engine catalogue is schema-valid, but every `released_commit` lags (11 of 11, 451 commits), validators are stale for at least four engines, suite marketplace counts are stale for two (F-03). |
| Skill depth and rigour | 55 | 56 | Hook gate has 61 assertions and the plugin-hook config 7, all pass. The cross-OS fixture-path defect was fixed in `edc0a70`. CI runs 12 of 19 test files and no hook test (F-06). |
| Worked examples and applied proof | 40 | 40 | 77 contract assertions pass; two real handoff records now validate against the schema (stand-in validator) and 20 requests were routed; no executed behavioural grading exists (Tier 3 is zero). |
| Standards currency | 40 | 40 | `npm audit` unchanged at 13 packages; SDK pinned at 1.30.0 against 1.32.2; host plugin formats and the MCP specification (2026-07-28 per the currency agent, not yet re-read by this cycle) were not yet reconciled. |
| Output readiness and coverage | 40 | 40 | Union metadata is 290,189 characters against a 60,000 budget; the package assumes a single-workspace layout that this host does not have; `skill_graph.py` crashes on it (F-04). |
| Accessibility and inclusivity | 45 | 45 | Plain text and host-neutral prose; no assistive-use or readability evidence. Unchanged. |
| Production, handoff and release | 35 | 34 | Tag `v1.1.0` exists, but `release/manifest.json` says 1.0.0 and the MCP package 1.0.0 against 1.1.0 plugin manifests; the release workflow omits promised checks; `npm test` fails off `main` (F-02, F-07). |
| Redundancy and hygiene | 45 | 40 | 21 drift findings (8 before); 27 duplicate skill names; about 1,630 machine-path lines in tracked text; two tracked local settings files in public repositories (F-03, F-05). |
| Discovery and routing | 45 | 37 | Engine Eval Readiness, stand-in basis (rule 3 of the rubric), 37.4; the strict basis is 19.4. Lexical only: p@1 31 of 42 with the three known defects in the denominator, acceptance prompts 2 of 12, 20 new requests 6 of 15 and 2 of 5. |
| Safety and integrity | 35 | 36 | Hook and fixture-path controls are tested; one critical dependency finding is unresolved (F-01); a local settings file is tracked in two public repositories (F-05). |

**Raw sum 486, raw mean 486 / 11 = 44.18. Standard published score `min(44.18, 65) = 44.18`.** The cap does not bind and hides no
defect. The 29 October scorecard printed 46.82, but its eleven rows sum to 505, a mean of 45.91; the table values are used here and the
printed mean is an arithmetic slip of 10 points. The fresh figure is 1.73 lower than the corrected 45.91 because this pass measured
things that cycle did not (drift grew from 8 to 21 findings as engines changed, the plain-function test gap, tracked local
settings, the branch-dependent MCP test) and because dimension 10 follows the rubric rule below. Target 95 is not claimed. Any
safety blocker (F-01) overrides the aggregate.

## Engine Eval Readiness for the coordinator (recomputed)

Formula (rubric): `30 x T1 + 40 x mean(T2_p1, T2_neg, T2_cov, T2_clean) + 30 x T3`. `NOT_ASSESSED` scores zero and stays in the
denominator.

| Input | Value now | Basis |
|---|---|---|
| T1 | 2 of 5 = 0.40 (strict) / 1.00 (stand-in) | The five commands declared in the prompt: drift check fails (exit 1), book-path check passes, Kaizen cards pass, `pytest tests` is `NOT_ASSESSED` here, `npm test` fails (15 of 16). The 29 October stand-in credited the "historical eight contracts" as 1.00 and is labelled as such. |
| T2_p1 | 31 / 42 = 0.738 | Oracle harness; the three known-defect cases stay in the denominator (0 of 3). Identical to 29 October. |
| T2_neg | 0 (not established) | No owned-negative set exists for the coordinator's single skill. |
| T2_cov | 0 (not established) | `rules-distill` has no three-positive, two-negative fixture set. |
| T2_clean | 0 (`NOT_ASSESSED`) | The coordinator's own skill is not in the collision scan (1,091 engine skills; 15 cross-engine pairs at 0.75 or above, none undeclared). |
| T3 | 0 | No grading file exists; behavioural runs need paid calls and were not authorised. |

**Strict readiness 12.0 + 7.38 = 19.4. Stand-in basis (T1 = 1) 30 + 7.38 = 37.4**, equal to the 29 October upper bound and in line with
the corrected September figure of 37.1. Neither is a measure of behavioural quality. Twelve acceptance prompts: 2 of 12 reach the
expected primary skill (unchanged); engine-level hits fell from 6 to 5 (`066` rank 67 to 70; `072` rank 3 to 4), a sign that pass-2
description changes moved the lexical neighbours. Dimension 10 uses the stand-in 37 so that the series stays comparable; the strict
figure is the one to move.

## Portfolio measures (baseline)

| Measure | Value | Source |
|---|---|---|
| Engines assessed | 11 of 11 public engines; `political` is not installed (`NOT_ASSESSED`, not searched for) | heads file |
| `released_commit` lag | 11 of 11 engines behind; 28 to 51 commits each; 451 in all; all pins are ancestors of HEAD | `baseline-12-measures.txt` |
| Drift check findings | 21 (8 on 29 October) | `baseline-0-render-check.log` |
| Suite marketplace counts | 2 drifted (business-plan 134 vs 137; design 101 vs 102) | `baseline-9-marketplace.log` |
| Duplicate skill names | 27, all across engines (`skill-writing` x7, `skill-safety-audit` x6, five names x5) | `baseline-13-duplicates.txt` |
| Runtime metadata size | 290,189 characters over 1,097 skills against a 60,000 budget (29 September: 291,636) | `baseline-10-budget-union-summary.json` |
| Union routing collisions | 15 cross-engine pairs at 0.75 or above; 0 undeclared; 157 at 0.50 (155 on 29 October) | `baseline-5-collisions.log` |
| Dangling cross-engine skill references | 0 by the skill-graph scan; 14 stale intra-engine "moved from" paths (13 social, 1 website); 117 mentions of retired aliases | `baseline-11-graph.log` |
| Machine-specific paths in tracked text | about 1,630 lines in 12 repositories, 877 of them here; live (non-record) counts are measured by the new check | `baseline-12-measures.txt` |
| Tracked local settings in public repos | 2 (dev engine, Linux); SDLC fixed | `baseline-12-measures.txt` |
| Hook copies | 11 repository, 7 plugin-cache, 2 other copies, all identical (`0b1465ca`) | `04-validation-record.md` |
| Python tests | `unittest discover`: 102 run, 2 failures and 6 errors all from missing `jsonschema`, 2 collection errors from pytest-only files; stand-in runner over the 7 plain-function files: 58 pass, 3 skipped, 0 fail | `baseline-3-*.txt` |
| MCP server | build clean; 15 of 16 tests pass; audit 6 moderate, 6 high, 1 critical | `baseline-15`, `baseline-17` |

Measured but not scored: no behavioural run, no archive count, no live host install, no remote CI, no PowerShell test run.
