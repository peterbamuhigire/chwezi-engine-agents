# M10-14 — Independent review (protocol step 7)

- **Reviewer:** Claude (Opus 5.5), acting as the independent reviewer. The reviewer executed no M10 phase and no part of M10-14.
- **Date:** 29 September 2026.
- **Constraints kept:** zero spend (no paid API call, no model-executed evaluation); no Git state change; this file is the only file written in any repository. Command outputs went to the session scratchpad (`scratchpad/reviewer-M10-14/`, plus a few top-level scratch files), never to a repository. The route oracles were run with `--out` pointing at the scratchpad. `build-doc.sh` was run only on the malformed fixture.
- **Criteria applied:** M10-14 phase file §5 (T01–T12) and §9. Under §9, `REJECT` is mandatory if (a) any `MET` claim lacks a reproducible command and evidence path, (b) a score slot with `NOT_ASSESSED` input is non-zero, or (c) any backlog ID lacks a status.

## Verdict: **REJECT**

The rejection is narrow and mandatory under §9 condition (b). In `eval-readiness.json`, chwezi-engine-agents has a `T2_clean` slot of **1.0 (10 Readiness points) with no measured input**. The package's own skill (`rules-distill`) is not in the union collision scan that feeds that slot:

- `readiness/collision-scan.json` indexes 1,169 skills;
- that total is exactly the sum of the eleven engines in `skills_per_engine`;
- `chwezi-engine-agents` is not listed;
- the string `rules-distill` does not appear in the file.

The script gives this vacuous 1.0 through the rubric's "1.0 when it has none" clause, which treats "no skills scanned" the same as "scanned and clean". The agents audit (`chwezi-engine-agents/docs/audits/2026-09-29-m10-reaudit/11-measured-evidence.md`) labels the slot **measured**.

The fix is mechanical, and none of the other checks found a blocking defect:
- every `MET` claim reproduced;
- the stored readiness file reproduced byte for byte;
- every T3 slot is 0;
- the worked example and the website scorecard reproduce;
- the traceability count holds.

Once finding F1 is corrected and F2–F4 are fixed or dispositioned, the reviewer expects to return `ACCEPT_WITH_DOCUMENTED_LIMITATIONS`.

## 1. `MET` claims in `success-measures.jsonl`, re-run

| # | Command re-run (read-only) | Result | Claim and evidence path |
|---|---|---|---|
| 1 | `gh run list --repo peterbamuhigire/chwezi-dev-engine --workflow skill-guardrails.yml --branch main --limit 3 --json …`; `gh run view 36520091310 --log` | Three latest runs are `success` (`67ae982`, `0a799d8`, `33574d9`). The log runs `node hooks/test-destructive-bash-gate.js && node hooks/test-plugin-hook-config.js` (61/61, 7/7) and pytest reports 207 passed, 3 skipped. Local `HEAD` = `origin/main` = `67ae982`. | Confirmed. The phase's MET rule names the **final pushed HEAD**, which does not exist yet; the JSONL note says so, the Kaizen record §6 does not (F6). |
| 2 | srs: `python -X utf8 scripts/check_docx_diagrams.py --scan projects --exclude _kaizen,render-runs`; `bash scripts/build-doc.sh engine/tests/fixtures/diagram_render/malformed/design FixtureMalformed` | Scan: 691 files, 0 with Mermaid source, 2 GarageFlow placeholder figures, exit 1. Malformed build: exit 1, "no .docx was written"; `git status` unchanged. | Confirmed. The exit-1 caveat is disclosed honestly. |
| 3 | agents: `python -X utf8 scripts/validate-runtime-skill-budget.py --collisions --ownership evals/routing/ownership.yaml --format json` | PASS, exit 0; 1,169 skills; 21 cross-engine pairs ≥ 0.75; 0 undeclared. | Confirmed. |
| 5 | design: `python -X utf8 scripts/routing_smoke_test.py --min-rank1 92 --lint-fixtures`; agents: `python -X utf8 scripts/validate-routing-baseline.py` | p@1 94 %, p@3 100 %, owned negatives 21/21 with 1 not assessed, lint 0, exit 0; baseline PASS. | Confirmed. 64/68 is transcribed from `baseline.json` (the smoke test prints rounded percentages). |
| 6 | dev: `python -X utf8 benchmarks/solution-selection/materialised/run_selftests.py`; run count over `M10-05/runs/*-evidence.json`; `find … -name grading.json` | Self-tests PASS 16/16 with `model_calls: 0`, exit 0. 233 runs across 5 evidence files, all `NOT_ASSESSED`. `grading.json` files in agents `evals/` and dev `benchmarks/`: 0. | Confirmed, but the planned-run denominator is inconsistent across artefacts (F5). The wording is honest: the phase's own MET rule counts `NOT_ASSESSED` case records with causes; "MET against the revised zero-spend target only" and "EXECUTED = 0" are stated plainly, and T3 is 0 everywhere. |
| 7 | agents: `python -X utf8 scripts/render_host_files.py --check --workspace-root .. --json` | 12 repositories checked, 0 findings, 0 not assessed, exit 0. The output is identical to the stored `host-files-check.json` after key-sorted normalisation. | Confirmed. |
| 8 | design: `node tools/slop-detector/cli.mjs --list-rules`; `--validate-registry`; `node --test tools/slop-detector/test/` | 49 rules, byte-identical to `slop-rules.txt`. AS1 11, AS2 4, AS3 4, AS4 11, AS5 1, AS7 18. Registry PASS. Node tests: 116 pass, 0 fail, 1 skipped. Every static rule has a `.flag` and `.pass` fixture in `tests/fixtures/slop/`; the 7 browser rules have theirs in `tests/fixtures/slop-browser/`. | Confirmed. The browser tier is skipped in this run, as disclosed. |
| 9 | `render_host_files.py --check` (the `ai-slop-banned-fonts-json` and `design-trigger-block` rows); design `cli.mjs --doctrine-consistency --json` | Asset row ok (canonical plus 1 byte mirror); trigger block 12 copies ok; doctrine consistency: 0 conflicts, 0 folders. | Confirmed as measured. Two unregistered fallback font lists exist (F7). |
| 10 | `render_host_files.py --check` (skill-writing rows) | `skill-writing-skill` is a registered variant with 6 hash-pinned pointer stubs against the dev canonical; scripts byte-mirrored; status ok. | Confirmed. |

**NOT_MET row 4.** Owned-negative counts reproduce from the stored smoke outputs: locally 74 + 21 + 13 + 21 + 7 = 136 pass and 0 fail; the mirrors are 4 + 1 + 3 + 0 + 2 = 10, of which 9 pass and 1 fails. The reviewer re-ran `run-contract-evals.py --route-oracles --workspace-root .. --out <scratch> --min-oracle-primary 74`: exit 0, contract cases 77/77, primary@1 30/39, engine@1 33/39, must_co_activate@5 3/4, known defects 3. This matches `route-oracles-summary.json`. The row is worded honestly: it names the one failing clause, the failing oracle (055) and an owner.

**Row 6 wording.** It is honest. The measured field and the note both state "EXECUTED = 0" and "no behavioural result exists". The status `MET` follows the phase's own MET rule for row 6 (≥ 28 case records, each executed or `NOT_ASSESSED` with a cause). The Kaizen record carries the qualifier "(zero-spend target)".

Every `MET` line has a command and an evidence path that exists. §9 condition (a) is not triggered.

## 2. Engine Eval Readiness recomputation

- SHA-256 of `eval-readiness.json` **before**: `7ce33264064efb33d3f09b2abfc3dd0db468a615b1006f255b4940ef92e36eed`.
- Command: `python -X utf8 readiness/compute_eval_readiness.py`, run from the M10-14 folder.
- SHA-256 **after**: `7ce33264064efb33d3f09b2abfc3dd0db468a615b1006f255b4940ef92e36eed`. Identical, and equal to the expected value.
- **T3:** 0.0 in all 12 engines. `executed_runs` = 0, so the script's branch sets 0.
- **Slots listed as `NOT_ASSESSED`:** all are 0:
  - `T2_p1`: business-plan, social, linux, windows and finance;
  - `T2_neg`: seven engines;
  - `T2_cov`: finance and agents;
  - the linux `check-distro-matrix.sh` validator: kept in the denominator, so T1 = 2/3.
- **The exception (F1):** agents `T2_clean` = 1.0 without input, and it is not listed as `NOT_ASSESSED`. The other `T2_clean` = 1.0 values have real input: linux and windows are in the scan with 0 pairs; finance has 1 pair, which is declared.
- The stored T2 inputs agree with the smoke transcripts for dev, design, srs, website and research (p@1 and owned negatives).

## 3. Worked-example arithmetic

File: `chwezi-dev-engine/skills/sdlc-meta/skill-engine-audit/references/eval-readiness-worked-example.md`.

**Readiness.** 67 lines, within the 120-line limit. The file is linked from `scoring-rubric.md` in the unstaged diff. (0.9058 + 1 + 0.0659 + 1) ÷ 4 = 0.742925, × 40 = 29.72; Readiness = 59.72, rounded to 59.7. This matches dev in `eval-readiness.json`.

**Case 1:**
- raw 55.03, rounded to 55.0;
- measured-constrained 54.62, rounded to 54.6;
- without harness output 54.30, rounded to 54.3.

**Case 2:**
- raw 68.30;
- measured-constrained 67.62, rounded to 67.6;
- published `min(67.6, 65)` = 65.0.

The routing cap (`min(72, 50)` = 50) is shown. All arithmetic reproduces.

## 4. One engine end to end: website-skills

Folder: `website-skills/docs/audits/2026-09-29-m10-reaudit/`.

- **Bucket arithmetic reproduces:**
  - output mean(55, 56, 58) = 56.333; depth mean(57, 40) = 48.5;
  - hygiene, raw: mean(50, 62, 64) = 58.667; measured: mean(50, 59.6, 64) = 57.867;
  - raw = 16.900 + 12.125 + 8.700 + 5.500 + 6.200 + 5.867 = 55.29, rounded to 55.3;
  - measured-constrained = 55.21, rounded to 55.2; published 55.2.
- **Weighting:** the folding of accessibility and production into the output bucket is stated as the audit's own choice (`01-methodology-and-rubric.md`).
- **Commands:** the only measured dimension, routing (dimension 10), cites its commands and exit codes in `11-measured-evidence.md`. Readiness was recomputed there (59.62), and T1 = 3/3 matches `tier1-results.json`.
- **Scores of 70 and above:** none. The highest dimension is 64, so no extraordinary-justification paragraph is required. A grep of all six scorecards found no dimension of 70 or more; design's 81 is the historical 22 June self-audit figure and is labelled as not comparable.
- **Independence limit:** one auditor instead of a parallel fleet. This is disclosed.
- **Minor:** `readiness/coverage.json` gives 36 website positive fixtures, while the smoke test reports 37. This has no effect on the coverage slot (1/62).

## 5. Traceability

- **Mechanical count.** The reviewer wrote an independent checker (`scratchpad/reviewer-M10-14/tc.py`). It confirmed:
  - 161 IDs in backlog §1 and 161 table rows, all unique;
  - 0 missing and 0 extra;
  - status counts DONE 111, DONE_WITH_LIMITATIONS 42, DONE (M10-14, commit pending) 3, NOT_ASSESSED 2, DEFERRED 2, DROPPED-AT-EXECUTION 1;
  - every DONE row carries a 7-hex commit hash.

  The claim holds, and §9 condition (c) is not triggered. The executor's own `verify_traceability.py` also returned PASS, but it lives only in the session scratchpad and is not stored with the evidence (F8).
- **Random sample.** Seed 20260929, 10 rows: AR-08, UX-09, SP-12, IM-09, AO-06, CV-04, AO-18, AR-15, AR-04 and BL-09a. For every row:
  - each cited commit exists in the named repository, and its subject names the phase;
  - each evidence path exists;
  - the stated status matches the phase evidence (for example M10-03 "T06 … DONE", M10-09 "T09 drift rules | DONE" and "T14 K5 re-audit | DONE", M10-06 "T07 SP-12 | DONE", M10-07 "T04 (AR-08) | DONE").

  CV-04's drop reason (16.3 % against a 25 % threshold) is recorded.

## 6. Kaizen record: overstatement check

`kaizen-2026-09-29-my-10-kaizen.md` is generally candid: zero executed T3, red CI in seven repositories, the log-verdict gap and the lexical-proxy caveat are all stated. Four points need correction:

- **§5:** "29 of 30 pass" is wrong (F4).
- **§7:** the agents Readiness 47.7 and measured-constrained 52.3 depend on F1.
- **§6 row 1:** reads MET without the final-HEAD caveat (F6).
- **§4 headline:** "the rubric now measures routing" should say that ratification is pending (F9).

## Findings

| # | Severity | Item | Evidence | Required correction |
|---|---|---|---|---|
| F1 | **HIGH: mandatory REJECT (§9 condition b)** | chwezi-engine-agents `T2_clean` = 1.0 (10 Readiness points) with no measured input; the agents audit labels it "measured". | `readiness/collision-scan.json`: `skills` = 1,169, the sum of 11 engines in `skills_per_engine`; agents is absent and `rules-distill` does not appear. `compute_eval_readiness.py` defaults `T2_clean` to 1.0 when an engine has 0 pairs, without checking that its skills were scanned. | Either (a) set agents `T2_clean` = 0 and list it in `not_assessed`, or (b) add the package's skill(s) to the union scan, re-run it and store the output. Make the script return `NOT_ASSESSED` (0) when an engine has no skills in `skills_per_engine`, and qualify the rubric's "1.0 when it has none" clause the same way. Regenerate `eval-readiness.json` and record the new SHA-256. Update agents `09-master-scorecard.md` and `11-measured-evidence.md`; under (a) Readiness becomes 37.7 and measured-constrained/published about 52.0 (hygiene (52 + 37.7 + 66) ÷ 3 = 51.9). Update Kaizen record §7 and the T05 table in `M10-14-close-out-evidence.md`. |
| F2 | MEDIUM | agents T1 = 8/8 comes from an executor-selected check list, not from a `catalog/engines.yaml` validator list, which is the rubric's T1 source. The record itself says the package has no `validators` entry (Kaizen §11 item 37). | `t2-inputs.json` `agents_tier1`; `scoring-rubric.md` T1 row; `eval-readiness.json` shows agents T1 = 1.0 with no `NOT_ASSESSED` note. | Label agents T1 as a surrogate (non-rubric source) in `eval-readiness.json`, the agents audit and Kaizen §7. Preferably, declare the list in `catalog/engines.yaml` (a separate, ratified change) before quoting agents Readiness as rubric-conformant. |
| F3 | MEDIUM | agents `T2_p1` excludes 3 executed and failing known-defect oracles (30/39, not 30/42). This is favourable to the score and sits against the spirit of rubric rule 1 ("never excluded"). | `route-oracles-summary.json` `known_defect_primary_at_1` 0/3; the agents audit's sensitivity note. | Use 30/42 (0.7143), or keep 30/39 but show both figures in `eval-readiness.json` and in Kaizen §7 as the primary figure's caveat. It is already mentioned in §7; make the published figure the stricter one, or record Peter's ruling. |
| F4 | MEDIUM | Kaizen record §5: "29 of 30 pass" is factually wrong. | `readiness/tier1-results.json`: 27 declared validators, 26 PASS, 1 `NOT_ASSESSED` (linux bash). | Correct the figure to "26 of 27 pass; 1 NOT_ASSESSED". |
| F5 | LOW | The row-6 planned-run denominator is inconsistent: 233 in `success-measures.jsonl`, 299 in `t2-inputs.json`, Kaizen §8/§11 and the M10-05 report. Row 6's 46 cases also exclude the 11 plugin-eval cases (66 runs) and the micro-test. | Reviewer count: `M10-05/runs/*-evidence.json` = 233 runs; M10-05 run-report table: 299. | State in row 6 which suites are counted (for example "46 case records in `M10-05/runs/`; plugin evals (11 cases, 66 runs) and the micro-test (15 runs) recorded separately; 299 planned in total"). |
| F6 | LOW | The row-1 MET rule requires the latest run on the **final pushed HEAD**. The measurement is on the checkpoint-3 HEAD `67ae982`, and the M10-14 dev commit is not yet pushed. | JSONL note ("Re-confirm on the HEAD the orchestrator pushes"); Kaizen §6 shows plain MET. | Add "(checkpoint-3 HEAD; re-confirm after the final push)" to Kaizen §6 row 1. After T11, append the CI result for the pushed HEAD as a dated addendum. |
| F7 | LOW | Row 9: two built-in fallback banned-font lists are not in the shared-asset register, and the discovery globs cannot find them. They are stale subsets; the srs list lacks the secondary ban and neither lists DM Sans. They are used whenever the design sidecar is absent, which is the single-repository CI checkout. | `srs-skills/scripts/render_diagrams.py` line 82 `BUILTIN_BANNED`; `chwezi-engine-agents/scripts/project_context_doctor.py` line 41. | Register both as checked variants, or generate them from the canonical JSON, or record them in row 9's note and the next-opportunities register. Row 9 can stay MET (both read the canonical JSON when it is present). |
| F8 | LOW | The traceability "mechanical" verifier is not stored with the evidence. | `traceability-closure.md` §3 cites a session-scratchpad path for `verify_traceability.py`. | Copy the script into `M10-14/readiness/` (or next to the closure) so that the count is reproducible after the session. |
| F9 | LOW | Kaizen §4's headline, "the rubric now measures routing", reads as settled, but the AO-14 rubric change awaits Peter's ratification (§3 says so). | Kaizen record lines 33 and 59. | Add "(pending ratification)" to the headline sentence. |
| F10 | INFO | `coverage.json` counts 36 website positive fixtures; the smoke test reports 37. | `readiness/coverage.json`; `readiness/website-smoke.txt`. | Note the counting difference (no effect on the 1/62 slot). |
| F11 | INFO | T1 = 1.0 in six engines whose remote CI is red because of sibling-relative links. | Close-out evidence "Remote CI"; Kaizen §11 item 1. | None: already disclosed. Keep the caveat beside every quoted T1. |
| F12 | INFO | Pre-condition "every phase has a reviewer verdict in the log" is not met (M10-00 and M10-02 only). | Close-out evidence, pre-conditions; Kaizen §8 and §11 item 30. | None beyond the recorded register item. |
| F13 | INFO | During this review an uncommitted rewrite of `chwezi-engine-agents/README.md` appeared (+131/−21, mtime 07:54, after the six audits were written). It is not part of the M10-14 evidence set and was not made by the reviewer. | `git -C chwezi-engine-agents status --short` shows ` M README.md`, which was absent at the start of the review. | The orchestrator should identify its origin before the final push, and stage it only if it belongs to a ratified change. It must not be swept into the M10-14 commit. |

## Items checked and found sound

- The T01 rubric section contains the formula, the input table, `NOT_ASSESSED` = 0 (4 matches), the routing cap of 50, the three published numbers and the attribution. `SKILL.md` has step 0 in the unstaged diff.
- T05 is deterministic: the byte-identical SHA-256 was reproduced.
- All 12 re-run commands for the nine `MET` rows and the `NOT_MET` row reproduce the stored figures.
- The website audit is internally consistent and cites its commands.
- Traceability: 161/161 IDs, each once, each with a status and hash; the 10-row sample is consistent with the phase evidence.

## Re-review (29 September 2026, after the executor's corrections)

The same reviewer checked the corrections under the same rules: zero spend, no Git state change, and this file as the only file written.

### Checks re-run

- **Readiness recomputation.**
  - `eval-readiness.json` SHA-256 before the run: `96961167d4c163375d2e57bf96dccd2930bbc8b5f5661918504f1f6603596465`.
  - Command: `python -X utf8 readiness/compute_eval_readiness.py`.
  - SHA-256 after the run: identical. The file is deterministic and matches the stated hash.
- **F1 (closed).**
  - `compute_eval_readiness.py` now scores `T2_clean` from the scan only when the engine appears in `skills_per_engine`. An engine absent from the scan gets `T2_clean` = 0 with the note `NOT_ASSESSED` "engine not in the union collision scan".
  - Agents slots: `T2_clean` = 0.0 and `T2_p1` = 0.7143 (30/42). T2 = 40 × 0.1786 = 7.14, so Readiness = 30.00 + 7.14 + 0 = **37.1**. This reproduces.
  - Every T3 slot is 0. Every slot listed as `NOT_ASSESSED` is 0 in all 12 engines. The other 11 engines' Readiness values are unchanged.
  - §9 condition (b) is no longer triggered.
- **Rubric.** In the dev `scoring-rubric.md`, the `T2_clean` row now reads "1.0 when the engine is in the scan and has none; `NOT_ASSESSED` (0) when the engine is not in the scan". This agrees with the script.
- **Agents audit.** `README.md`, `00`, `09` and `11` each carry the dated correction note. The arithmetic reproduces: hygiene (52 + 37.1 + 66) ÷ 3 = 51.70; the overall is 16.20 + 11.875 + 7.50 + 5.20 + 6.00 + 5.17 = 51.945, rounded to **51.9**; published is `min(51.9, 65)` = 51.9.
- **F3 (closed).** p@1 is 30/42 in `t2-inputs.json` and in the recomputed file.
- **F2 (closed as a documented limitation).** `t2-inputs.json` labels the agents T1 (8/8) a stand-in because `catalog/engines.yaml` declares no validators for the package. The label is repeated in Kaizen §7 (both the table row and the reading), in the agents audit correction notes, and as next-opportunities item 41.
- **F4 (closed).** Kaizen §5 now reads "26 of 27 pass; 1 NOT_ASSESSED", which matches `tier1-results.json`.
- **F5 (closed).** `success-measures.jsonl` row 6 and Kaizen §6 row 6 now state the scope: 46 cases and 233 runs with run evidence, plus 11 plugin-eval cases (66 runs), 299 runs planned in all, with the micro-test counted separately.
- **F6 (closed).** JSONL row 1 and Kaizen §6 row 1 now say "MET on the checkpoint-3 HEAD `67ae982`; re-confirm on the final pushed HEAD".
- **F7 (closed as deferred).** Recorded as Kaizen §11 item 40 and in the close-out findings-disposition table.
- **F8 (closed).** `readiness/verify_traceability.py` is now stored with the evidence. Running it gives PASS: 161 IDs, 0 rows without a status. It agrees with the reviewer's independent count.
- **F9 (closed).** Kaizen §4 now says "(pending Peter's ratification of the AO-14 change)".
- **F10 (closed).** The close-out disposition table explains the counting difference, which affects no score.
- **F13 (closed for M10-14).** The agents README rewrite was committed as `86a7776` by someone else and is outside M10-14 scope.

### Remaining findings

| # | Severity | Item | Evidence | Required action |
|---|---|---|---|---|
| R1 | LOW | Kaizen §10 ("Final (M10-14)" row) still says the pre-push `origin/main` equals the checkpoint-3 heads. For chwezi-engine-agents that is no longer true. | Local `origin/main` is now `86a7776`, and `cea785e` also follows the checkpoint-3 head `8a438c9`. The freeze snapshot no longer matches agents `HEAD`. | Before T11, the orchestrator must `git fetch`, record the actual pre-push `origin/main` for agents (and any other repository that moved), and note that `86a7776` and `cea785e` are post-freeze commits outside M10-14. Do not rebase silently (T11 push discipline). |
| R2 | LOW | The agents T1 stand-in (30 points) is labelled in `t2-inputs.json` and in the prose, but not in `eval-readiness.json` itself: agents' `not_assessed` list has no T1 note. | `eval-readiness.json`, `engines.chwezi-engine-agents.not_assessed`. | Optional: add a `T1 (stand-in list; no catalogue validators)` label to the script output the next time it is regenerated. It is disclosed elsewhere, so this is not blocking. |
| R3 | INFO | Every limitation from the first review remains a documented limitation: T3 is unexecuted (EXECUTED = 0); Tier 2 is a lexical proxy; T1 is 1.0 beside red remote CI in seven repositories; the running log has reviewer verdicts for M10-00 and M10-02 only; the audits were run by a single auditor rather than a fleet; row 4 is NOT_MET. | Kaizen §8 and §11. | None beyond the register items. Peter's ratification is still required for the AO-14 rubric change, the published scores, the final push and any tag. |

### Re-review verdict: **ACCEPT_WITH_DOCUMENTED_LIMITATIONS**

None of the three mandatory-REJECT conditions in §9 now applies:
- every `MET` line has a reproducible command and an evidence path;
- every slot with `NOT_ASSESSED` input, including every T3 slot, is 0;
- all 161 backlog IDs carry a status.

The remaining items are low severity and documented. R1 must be resolved at T11 before the push.
