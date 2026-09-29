# M10-14 evidence — Re-audit with measured evidence, scoring and close-out

- Executor: Claude (Opus 5.5) under the orchestrator's brief, 29 September 2026. Zero spend: no paid call and no model-executed evaluation. No Git state was changed; every edit is unstaged for the orchestrator.
- Independent contributors: one traceability agent (T07) and six audit agents (T06), none of which executed an M10 phase; one independent reviewer (protocol step 7).
- Decisions marked "delegated" were taken by the orchestrator's executor under Peter's delegated authority, 29 Sep 2026, taking the plan's recommended option.

## Pre-conditions (protocol step 1)

| Condition | Result |
|---|---|
| Every M10 phase has a reviewer verdict in the log | **Not met as written.** The running log holds sections for M10-00 and M10-02 only; M10-01 and M10-03 to M10-13 are recorded in their evidence folders and commits, and were accepted by the orchestrator through three push checkpoints. Recorded as a documented limitation; the log's final section (T08) points to every evidence folder. |
| Repositories clean or dirty paths recorded | Met. At the freeze all 12 repositories were clean and each `HEAD` equalled `origin/main` (`close-snapshot.json`). |
| Harness artefacts from M10-03 and M10-05 | Present. Tier-3 results absent (0 `grading.json`), recorded `NOT_ASSESSED (zero-spend rule)`. |

## Per-task record

### T01 — AO-14 rubric extension — DONE (Peter's ratification pending)
- Files (chwezi-dev-engine): `skills/sdlc-meta/skill-engine-audit/references/scoring-rubric.md` (new section "Engine Eval Readiness (measured)": formula, input table with source files, six rules including `NOT_ASSESSED` = 0 and "without harness output, routing cannot score above 50", the three published numbers); `references/audit-dimensions.md` (discovery-and-routing and worked-examples rows cite harness output); `references/report-structure.md` (`09-master-scorecard.md` labels, new `11-measured-evidence.md`); `SKILL.md` workflow step 0 (run the harness before scoring) and two reference lines.
- Attribution: addyosmani/agent-skills (MIT, https://github.com/addyosmani/agent-skills, commit `2686b62`), paraphrased.
- `SKILL.md` 141 → 146 lines (≤ 500). No new skill.
- Verification (`dev-verification.txt`): `skill_catalog_guardrails.py` 14 findings, **0 errors** (14 pre-existing byte warnings), exit 0; `contract_gate.py --all` 161 scanned, 0 errors, exit 0; `engine_compliance.py --root .` 136 of 165 fully compliant (unchanged), exit 0; `routing_smoke_test.py --min-rank1 88 --lint-fixtures` exit 0; `pytest tests` 207 passed, 3 skipped; `quick_validate.py skills/sdlc-meta/skill-engine-audit` valid. `Select-String references/scoring-rubric.md 'NOT_ASSESSED'` ≥ 1 (4 matches). Active `SKILL.md` count 167 (guardrail), unchanged.
- Note on the phase text: the plan calls this `python -X utf8 scripts/skill_catalog_guardrails.py → 0 findings`; the guardrail reports 14 report-only byte warnings that predate M10-14, with 0 errors.

### T02 — worked example — DONE
- File: `skills/sdlc-meta/skill-engine-audit/references/eval-readiness-worked-example.md` (67 lines ≤ 120), linked from `scoring-rubric.md` and `SKILL.md`.
- Uses the measured dev inputs (T1 1.0; p@1 173/191; owned negatives 78/78 with 4 union mirrors; coverage 11/167; collision-clean 1.0; T3 `NOT_ASSESSED`) → Readiness 59.7. Shows the routing cap (judged 72 → 50 without harness output) and the published cap (67.6 → 65). The arithmetic was re-checked by hand and matches `eval-readiness.json` for dev.

### T03 — freeze and snapshot — DONE
- `close-snapshot.json`; diff and findings in `close-snapshot-diff.md`. Two runs gave identical digests (`baseline.json` `ccc9febe…3ac512`), which closes the M10-00-T11 limitation.
- Finding: Claude-loaded router bytes rose in 11 of 12 repositories because the bridges import `AGENTS.md` (for example srs 33,533 → 51,212). Recorded for the next Kaizen; no budget exists to judge it against (P04).

### T04 — roadmap §5 measures — DONE: 9 MET, 1 NOT_MET, 0 NOT_ASSESSED
`success-measures.jsonl` (10 lines; targets copied from roadmap §5 before measuring; every MET line has a command and an evidence path).

| # | Measure | Measured | Status |
|---|---|---|---|
| 1 | Dev CI on `main` | `skill-catalog-guardrails` success on `67ae982` (run 36520091310) and the two previous pushes; log runs both `hooks/test-*.js` (61/61, 7/7) | MET (re-confirm on the M10-14 push) |
| 2 | SRS `.docx` with raw Mermaid | 0 of 691; malformed fixture build exits 1 and writes no `.docx` | MET (the scan exits 1 on 2 missing GarageFlow figures, a separate open item) |
| 3 | Undeclared cross-engine pairs ≥ 0.75 | 0 (21 declared) | MET |
| 4 | Engines with owned negatives, all passing | 5 of 5 at minimum; 1 cross-engine mirror (oracle 055) fails | **NOT_MET** |
| 5 | Design p@1 | 94.1 % (floor 92) | MET |
| 6 | Tier 3 | 46 case records with run evidence (233 runs); with the 11 plugin-eval cases (66 runs), 299 planned runs; micro-test separate; **0 executed**; checker self-tests 16/16 | MET against the zero-spend target only |
| 7 | Thin bridges | 12 of 12 | MET |
| 8 | Slop rules with fixtures | 49 (AS1–AS5, AS7; none maps to AS6) | MET |
| 9 | Banned-font copies | 1 canonical JSON + checked mirror; 0 drift | MET |
| 10 | Silent `skill-writing` drift | 0 | MET |

Secondary measures (no targets): dev `engine_compliance.py` 136 of 165 fully compliant (baseline 138/167 as recorded in the plan; M10-06 measured 136/165 before its own work); dev p@1 90.6 % (baseline 96 %; the fall follows the M10-03 fixture-lint rewrites, floor 88); SRS routing 55/55 top-3, p@1 47/55; router bytes per repository in `close-snapshot-diff.md`; portfolio metadata 292,390 characters over 1,160 plugin-listed skills against the 60,000 self-declared budget, 27 duplicate names (`runtime-budget-portfolio.json`; M10-02 measured 291,636); marketplace check 23 ok, 0 drift (11 of 11 engines).

### T05 — Engine Eval Readiness — DONE
- Script and stored inputs: `readiness/run_tier1.py` (T1: every `catalog/engines.yaml` validator run in its engine root), `readiness/fixture_coverage.py` (T2 coverage), `readiness/collision-scan.json`, the smoke outputs `readiness/*-smoke.txt`, `readiness/t2-inputs.json`, `readiness/compute_eval_readiness.py`. Output `eval-readiness.json` (records the input SHA-256s). Two recomputations gave the same file SHA-256: `7ce33264…2e36eed` as first published, `96961167…3596465` after the review corrections (agents row only).
- Rule applied: `NOT_ASSESSED` = 0 in its slot. Every T3 slot is 0.

| Repository | T1 | p@1 | Owned neg | Coverage | Clean | T3 | **Readiness** |
|---|---|---|---|---|---|---|---|
| chwezi-dev-engine | 1.00 | 0.906 | 1.000 | 0.066 | 1 | 0 (NA) | **59.7** |
| website-skills | 1.00 | 0.946 | 1.000 | 0.016 | 1 | 0 (NA) | **59.6** |
| design-system-skills | 1.00 | 0.941 | 1.000 | 0 | 1 | 0 (NA) | **59.4** |
| srs-skills | 1.00 | 0.855 | 1.000 | 0 | 1 | 0 (NA) | **58.5** |
| digital-research-engine | 1.00 | 0.862 | 0.889 | 0 | 1 | 0 (NA) | **57.5** |
| chwezi-engine-agents | 1.00 (8/8, stand-in list) | 0.714 (oracles 30/42) | 0 (NA) | 0 (NA) | 0 (NA: not in scan) | 0 (NA) | **37.1** |
| proposal-skills | 1.00 | 0.731 | 0 (NA) | 0 | 1 | 0 (NA) | **47.3** |
| business-plan-skills | 1.00 | 0 (NA) | 0 (NA) | 0 | 1 | 0 (NA) | **40.0** |
| social-media-skills | 1.00 | 0 (NA) | 0 (NA) | 0 | 1 | 0 (NA) | **40.0** |
| windows-admin-engine-skills | 1.00 | 0 (NA) | 0 (NA) | 0 | 1 | 0 (NA) | **40.0** |
| chwezi-accounting-doctrine | 1.00 | 0 (NA) | 0 (NA) | 0 (NA) | 1 | 0 (NA) | **40.0** |
| linux-skills | 0.67 (bash suite NA on Windows) | 0 (NA) | 0 (NA) | 0 | 1 | 0 (NA) | **30.0** |

- Limits: T2 is a lexical proxy, not live routing. T1 is measured on this Windows host; remote CI is red in seven repositories for reasons that do not reproduce locally (see "Remote CI" below), so T1 = 1.0 must be read beside that table. Proposal p@1 is derived from the harness's printed top-3 lists. Five engines' harnesses print p@3 only, and finance has no routing harness, so their p@1 slot is 0.

### T06 — measured re-audits of six repositories — DONE_WITH_LIMITATIONS (see "T06 results")

### T07 — traceability closure — DONE
`traceability-closure.md`: 161 backlog IDs, each exactly once (mechanical check PASS). DONE 111, DONE_WITH_LIMITATIONS 42, DONE (M10-14, commit pending) 3, NOT_ASSESSED 2 (PT-11, UA-14), DEFERRED 2 (IM-15, GR-11), DROPPED-AT-EXECUTION 1 (CV-04: decision rule not met), PARTIAL 0. All 16 §3 dropped items stayed dropped (no Graphify, Caveman, Headroom, UUPM, Understand Anything, Archify, Ponytail or Impeccable install anywhere). M10-00 value measure (b) met: no phase proposed an install that D1–D5 rejected.

### T08 — Kaizen record and log close — DONE
- `docs/operations/kaizen-2026-09-29-my-10-kaizen.md` (12 sections, in the K17 record format) and a final section in `m10-kaizen-execution-2026-09-29.md` pointing to it.
- "commit: pending": **ALREADY DONE**. M10-00's pre-work table already reads "No line reads 'commit: pending'"; `grep -i "commit: pending"` finds only that sentence.
- Heading grep, `validate-no-book-extractions.py` and `validate-kaizen-cards.py`: see "Final verification" below.

### T09 — Claude memory — DONE
- `C:\Users\Peter\.claude\projects\C--Users-Peter\memory\project_my10_kaizen_2026-09-29.md` already existed (plan-only content); it was **updated in place** rather than duplicated, to the template's shape (decisions, not narrative). The `MEMORY.md` index line was rewritten to match; `Select-String MEMORY.md 'my-10-kaizen'` returns 1 line.
- `project_design_system_engine.md`: **not changed**. It already records the 29 Sep house ruling, the watchlist-to-secondary-ban ruling, the JetBrains Mono / Fira Code threshold flag, the 49-rule detector and trigger block v3.
- M10-00 font feedback memory: M10-00-T10 recorded "ALREADY DONE" (the ruling lives in `project_design_system_engine.md`; no separate feedback file was added). Confirmed unchanged.

### T10 — model-policy recheck — DONE (no recheck due)
Within 7 days of M10-00-T08 (29 Sep 2026); the M10-00 record ("retain Luna/high") stands.

### T11 — final push — prepared, not executed (orchestrator)
Pre-push state and proposed tag commands are in the Kaizen record §10. The executor did not fetch or push.

### T12 — next-opportunities register — DONE
Section 11 of the Kaizen record: every NOT_MET, NOT_ASSESSED, PARTIAL and DEFERRED item as a numbered candidate with evidence, owner and earliest date.

## Remote CI (read-only `gh run list --limit 3`, 29 Sep 2026)

| Repository | Workflow at HEAD | Conclusion | Cause (`gh run view --log-failed`) | Red since |
|---|---|---|---|---|
| chwezi-engine-agents | validate @ `8a438c9` | success | earlier 29 Sep runs failed at `5ef3019`, `35340f6` | — |
| chwezi-dev-engine | skill-catalog-guardrails @ `67ae982` | success | — | — |
| design-system-skills | Skill engine quality @ `25ce1e6` | success | — | — |
| website-skills | Skill engine quality @ `ec72bca` | success | — | — |
| chwezi-accounting-doctrine | Doctrine Validation @ `82279fa` | success | — | — |
| srs-skills | Engine @ `fa85fba` | **failure** | `validate_skill_engine.py`: `hospitality-operating-model-srs/SKILL.md` lines 156–157 link to absolute `C:/wamp64/…` paths | ≤ 20 Sep (14 runs shown, all red) |
| digital-research-engine | Skill engine quality @ `2b9c87d` | **failure** | `skill_contract_validator.py`: 2 broken relative links | ≤ 25 Sep |
| proposal-skills | Skill quality @ `5de27f8` | **failure** | `validate_skills.py`: 4 broken links | ≤ 23 Sep |
| business-plan-skills | Skill quality @ `8949387` | **failure** | 4 broken links into sibling repositories (`../../../../chwezi-dev-engine/…`, `../../../../digital-research-engine/…`, an absolute `C:/wamp64/www/…` link) | ≤ 24 Sep |
| social-media-skills | Skill engine quality @ `09eebe7` | **failure** | 5 broken relative links | ≤ 23 Sep |
| linux-skills | Skill quality @ `87c6421` | **failure** (Bash suites success) | 1 broken link to `../../../digital-research-engine/…` | ≤ 27 Sep |
| windows-admin-engine-skills | windows-engine-ci @ `55c53cc` | **failure** | `ERROR: missing module function: Get-WseAdminActivityReport` | ≤ 16 Sep |

Diagnosis: the six link failures share one cause. Skills link to sibling engines by relative path (`../../../<engine>/…`) or by absolute `C:/wamp64/www/…` path; on the Windows host the siblings exist, so every validator passes locally, but CI checks out one repository, so the links break. Every one predates M10 (red on the earliest run listed). **Not fixed**: the fix is a validator policy or skill-file change in six repositories, not a report file, so it is outside this executor's scope. Windows: the module-function check fails on the CI runner while `validate_engine.py` passes locally; not diagnosed further (outside scope). All seven are recorded as stop-the-line candidates in the next-opportunities register.

## T06 results

Six independent audit agents (none executed an M10 phase), one per repository, each following `skill-engine-audit` with the T01 extension and writing only its own folder `docs/audits/2026-09-29-m10-reaudit/` (README, 00, 01, 02, 03, 05, 09, 10, 11; dev also 06; 04/07/08 marked "not re-run").

| Repository | Raw | Measured-constrained | Published | Readiness (auditor agrees?) | 70+ scores |
|---|---|---|---|---|---|
| design-system-skills | 57.1 | 57.1 | 57.1 | 59.4 (yes) | none |
| website-skills | 55.3 | 55.2 | 55.2 | 59.6 (yes) | none |
| srs-skills | 54.6 | 54.6 | 54.6 | 58.5 (yes; T2 28.55 vs 28.54 rounding) | none |
| chwezi-dev-engine | 52.7 | 52.5 | 52.5 | 59.7 (yes) | none |
| chwezi-engine-agents | 52.5 | 51.9 | 51.9 | 37.1 after correction (the auditor agreed with 47.7 as first published) | none |
| digital-research-engine | 51.6 | 51.6 | 51.6 | 57.5 (yes; 47.5 with CI's T1 of 2/3) | none |

Limitations: each audit was one agent working through the fleet's concerns in turn rather than a six-agent fleet; standards currency judged mostly from the engines' own records (dev and research made a few cited official-documentation checks); fan-in not run for dev. Folders are dated 29 Sep 2026, not "2026-10-<dd>" as the phase file anticipated, because the audits ran on 29 Sep. Findings feed next-opportunities items 32–39.

## Final verification (after all M10-14 files were written)

| Check | Result |
|---|---|
| Kaizen record heading grep (`^## `) | 12 sections: scope and dates; baseline; decisions; per-engine findings and changes; validator and harness evidence; before/after; scores; NOT_ASSESSED; rollback points; push record; next opportunities; traceability closure |
| `validate-no-book-extractions.py` | PASS, roots 12, findings 0 |
| `validate-kaizen-cards.py` | exit 0 |
| `render_host_files.py --check --workspace-root ..` | 12 repositories, 0 findings |
| srs `validate_skill_engine.py --baseline …`; design `validate_engine.py --baseline …`; website registry and contract validators; research contract validator and `validate_engine.py`; dev guardrails and control plane; source-ingestion guardrails (srs, website, research, dev) | all exit 0 with the new audit folders present |
| dev rubric checks (T01) | see T01; `dev-verification.txt` |
| Git state | no commit, push, checkout or stash; all changes unstaged |

## Changed files (for the orchestrator)

- chwezi-dev-engine: M `skills/sdlc-meta/skill-engine-audit/SKILL.md`, `references/scoring-rubric.md`, `references/audit-dimensions.md`, `references/report-structure.md`; A `references/eval-readiness-worked-example.md`; A `docs/audits/2026-09-29-m10-reaudit/` (10 files).
- design-system-skills, srs-skills, website-skills, digital-research-engine: A `docs/audits/2026-09-29-m10-reaudit/` (9 files each).
- chwezi-engine-agents: M `docs/operations/m10-kaizen-execution-2026-09-29.md`; A `docs/operations/kaizen-2026-09-29-my-10-kaizen.md`; A `docs/audits/2026-09-29-m10-reaudit/` (9 files); A everything new under `docs/operations/m10-kaizen-evidence/M10-14/`.
- Outside Git: Claude memory `project_my10_kaizen_2026-09-29.md` and `MEMORY.md`; plan package `README.md` (local repository, not committed).

## Independent review and corrections (29 Sep 2026)

Reviewer file: `M10-14-independent-review.md`. Verdict **REJECT** (mandatory ground: F1). Disposition of each finding:

| Finding | Disposition |
|---|---|
| F1 agents collision-clean 1.0 without input | Fixed: `compute_eval_readiness.py` scores an engine absent from the union scan `NOT_ASSESSED` = 0; rubric rule reworded; agents Readiness 47.7 to 37.1; agents audit carries a correction note; published 52.3 to 51.9 |
| F2 agents T1 from a chosen list | Labelled a stand-in in `t2-inputs.json`, the rubric (T1 row) and the Kaizen record; declaring the list is next-opportunities item 41 |
| F3 known-defect oracles excluded | Fixed: agents p@1 30/42; the rubric's T2_p1 row says executed known-defect cases stay in the denominator |
| F4 "29 of 30" | Fixed: 27 declared, 26 pass, 1 `NOT_ASSESSED` |
| F5 Tier-3 run scope | Stated in `success-measures.jsonl` row 6 and the record |
| F6 row 1 on the checkpoint-3 HEAD | Caveat in the record section 6 and the row 1 note; re-confirm after the final push |
| F7 fallback font lists outside the register | Next-opportunities item 40 |
| F8 traceability script in scratch | Stored: `readiness/verify_traceability.py` (RESULT: PASS) |
| F9 ratification qualifier | Added to the record section 4 |
| F10 website 36 vs 37 fixtures | Noted: the coverage parser counts one record per expected-skill fixture (36); the smoke test reports 37. No effect on any score |
| F11, F12 | Already disclosed; unchanged |
| F13 agents README rewrite | Not M10-14 work; since committed by someone else as `86a7776` (agents `HEAD` is now ahead of the freeze). Keep it out of the M10-14 commit; the orchestrator should confirm whether `86a7776` (and `cea785e`) are pushed |
