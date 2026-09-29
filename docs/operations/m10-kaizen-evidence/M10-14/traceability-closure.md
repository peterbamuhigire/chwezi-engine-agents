# M10-14-T07 — Traceability closure of the my-10-kaizen backlog

**Date:** 29 September 2026
**Task:** M10-14-T07 (BL-14b), change class metadata
**Executor:** Claude (Opus 5.5) under the orchestrator's brief. Zero spend. No Git state was changed; this file is the only file written. The orchestrator commits it.

## 1. Method

**Sources read.**
- Backlog: `C:\Users\Peter\Documents\my-10-kaizen\05-traceability-backlog.md`. The IDs come from §1. §1.1 (reassignments) and §3 (dropped items) are applied as stated there.
- Phase files: `03-phases\M10-00-*.md` … `M10-14-*.md`, §5 task tables. These map each backlog ID to its task IDs.
- Executor evidence for M10-00 … M10-13 under `docs/operations/m10-kaizen-evidence/`, the running log `docs/operations/m10-kaizen-execution-2026-09-29.md`, `docs/operations/kaizen-2026-09-29-m10-12-context-tours-graph.md` and `docs/operations/third-party-tool-dispositions-2026-09-29.md`.
- Commits: `git -C <repo> log --since=2026-09-28 --format="%h %s"` in all twelve repositories under `C:\wamp64\www`. Commit subjects name the phase. `git log --diff-filter=A` was also used to find the chwezi-engine-agents commit that added each evidence file.

**How each status was set.**
1. Each ID is mapped to its task(s) through the phase task tables.
2. The status is the one the executor evidence states for those tasks, taken as written and never upgraded.
3. Where an ID spans several tasks or parts (SP-01, SP-04, UA-11, and multi-task IDs such as AO-08), the row takes the weakest part status.
4. Where the build was done but the model-executed part was `NOT_ASSESSED` under the zero-spend rule, the row is `DONE_WITH_LIMITATIONS` and the Note says so.
5. `ALREADY DONE` (BL-00b T10) and "recorded as LOST" (BL-00a T02) are folded into the parent row.
6. CV-04 was closed as "NO CHANGE (decision rule not met)". It is shown as `DROPPED-AT-EXECUTION` with that reason.
7. The three M10-14 items are being executed in this phase. Their status reads `DONE (M10-14, commit pending orchestrator)`.

**Reading the columns.**
- Repository prefixes in the Commit(s) column: `agents` chwezi-engine-agents, `dev` chwezi-dev-engine, `design` design-system-skills, `srs` srs-skills, `website` website-skills, `DRE` digital-research-engine, `proposal` proposal-skills, `bp` business-plan-skills, `social` social-media-skills, `linux` linux-skills, `finance` chwezi-accounting-doctrine, `windows` windows-admin-engine-skills.
- Evidence paths are relative to `docs/operations/m10-kaizen-evidence/`.
- Where a change landed outside Git, the commit cited is the evidence commit. This applies to Peter's machine, the global `~/.claude/CLAUDE.md` and git-ignored client projects, and the Note says so.

**Close-out observations.** These are read-only `gh run list` checks made on 29 Sep 2026. They are recorded in Notes but used to upgrade nothing.
- dev `skill-guardrails` passed at `67ae982`.
- agents `validate` passed at `8a438c9`.
- design `Skill engine quality` passed at `25ce1e6`.
- website `Skill engine quality` passed at `ec72bca`.
- srs `Engine` **failed** at `fa85fba`: `validate_skill_engine.py` reports `broken_relative_link: 1`.
- DRE `Skill engine quality` **failed** at `2b9c87d`: `skill_contract_validator.py` reports `broken_relative_link: 2`.

**IDs mentioned in more than one §1 row.**
- These are true splits: SP-01 (dev part M10-06, SRS part M10-08) and SP-04 (drift check M10-02, canonical content M10-04).
- These are cross-references only, not second assignments: AR-01 in the M10-13 row ("reuse of the AR-01 renderer"), AC-04 in the M10-13 row ("from AC-04") and CV-01 in the M10-08 row ("conditional on CV-01 data").
- Each of these IDs has one row below.

## 2. Traceability table

| ID | Phase | Task(s) | Final status | Commit(s) | Evidence path | Note |
|---|---|---|---|---|---|---|
| SP-02 | M10-00 | T04, T06 | DONE_WITH_LIMITATIONS | agents 4c187d1 | M10-00/M10-00-mobilisation-evidence.md | D1 recorded. Superpowers upgraded from 4.3.1 to 6.4.2 and telemetry turned off on Peter's machine (unversioned; backups are local). The clean-session acceptance prompt is NOT_ASSESSED (zero spend; owner Peter). |
| UA-01 | M10-00 | T04 | DONE | agents 4c187d1 | M10-00/M10-00-mobilisation-evidence.md | D2: reject estate-wide install; defer a bounded pilot (UA-14). |
| AR-18 | M10-00 | T04 | DONE | agents 4c187d1 | M10-00/M10-00-mobilisation-evidence.md | D3: reject estate-wide install; personal use permitted at v3.0.1. |
| GR-13 | M10-00 | T04, T05 | DONE | agents 4c187d1 | M10-00/M10-00-mobilisation-evidence.md | D4 plus the P06 addendum; the LSP-pilot workload is named; P06 remains IN_PROGRESS. |
| UX-15 | M10-00 | T04, T07 | DONE_WITH_LIMITATIONS | agents 4c187d1; design a77ad8f | M10-00/M10-00-mobilisation-evidence.md | D5 recorded. The provenance note uses the plan's third ("UNDETERMINED — attributed defensively") statement, chosen under delegation. |
| BL-00a | M10-00 | T01, T02, T03, T11 | DONE_WITH_LIMITATIONS | agents 4c187d1 | M10-00/M10-00-mobilisation-evidence.md | Log and evidence tree DONE. `skills-kaizen` package RECORDED AS LOST per owner. The manifest is written, but no local Git init in the plan package. The two-run digest equality is NOT_ASSESSED (concurrent edits). |
| BL-00b | M10-00 | T09, T10 | DONE | agents 4c187d1; design b7e1003; dev 7adc9fc | M10-00/M10-00-mobilisation-evidence.md | Font ruling recorded (T09). The memory entry was ALREADY DONE (T10). |
| BL-00c | M10-00 | T08 | DONE | agents 4c187d1 | M10-00/M10-00-mobilisation-evidence.md | Retain Luna/high; no policy file changed. The M10-14-T10 repeat belongs to this phase. |
| BL-01a | M10-01 | T01–T04 | DONE_WITH_LIMITATIONS | dev 6941e08 | M10-01/M10-01-dev-engine-evidence.md | Local CI sequence green. The evidence records the remote run as NOT_ASSESSED (awaiting push), and T02 ratification is pending. At close-out, `gh` shows `skill-guardrails` success at dev 67ae982; the reviewer may upgrade. |
| AO-01 | M10-01 | T07 | DONE | agents c0caf8d | M10-01/M10-01-catalogue-fonts-impeccable-website-global-evidence.md | Validator lists un-piped in the catalogue and the MCP server. |
| AO-02 | M10-01 | T08 | DONE | agents c0caf8d | M10-01/M10-01-catalogue-fonts-impeccable-website-global-evidence.md | Reports regenerated (22/22) and fixtures materialised. §1.1: the "rename `digital-research-skills` in case 022" part was dropped because it is the correct id; only the malformed `fixture_path` was fixed. |
| AR-01 | M10-01 | T09, T10 | DONE | srs 905b9a4 | M10-01/M10-01-srs-render-pipeline-evidence.md | Mermaid rendered before Pandoc, with a post-build guard. The render integration test is skipped in CI (no Node step). |
| AR-02 | M10-01 | T11 | DONE_WITH_LIMITATIONS | srs 905b9a4; agents 9510270 | M10-01/M10-01-srs-render-pipeline-evidence.md | 18 files regenerated (client projects are git-ignored, so the commit cited is tooling plus evidence). Client re-issue is NOT_ASSESSED (awaiting Peter; external release). |
| AR-03 | M10-01 | T12 | DONE | srs 905b9a4 | M10-01/M10-01-srs-render-pipeline-evidence.md | phase06 and phase03 figure gates. Peter's ratification of the gate semantics is pending. |
| IM-05 | M10-01 | T14 | DONE | DRE d4a613d; dev b3161da; design f69c5d4; dev 4121093 | M10-01/M10-01-catalogue-fonts-impeccable-website-global-evidence.md | Source record refreshed at 114ea1d; the dev currentness pointer was repointed in M10-09. |
| BL-01b | M10-01 | T15 | DONE | website 75bc5c9 | M10-01/M10-01-catalogue-fonts-impeccable-website-global-evidence.md | Slop-gate docs made truthful; the full rebuild is IM-03 (M10-11). |
| BL-01c | M10-01 | T16 | DONE | website 75bc5c9 | M10-01/M10-01-catalogue-fonts-impeccable-website-global-evidence.md | `brand-alignment` now routes to `brand-visual-identity`. |
| BL-01d | M10-01 | T17 | DONE | agents c0caf8d | M10-01/M10-01-catalogue-fonts-impeccable-website-global-evidence.md | The edit is to the unversioned `~/.claude/CLAUDE.md`, so the evidence commit is cited. The backup `.bak` was not committed (checked). §1.1: the banned-font part was dropped (done on 29 Sep). |
| AO-21 | M10-01 | T06 | DONE | dev 6941e08; agents c0caf8d | M10-01/M10-01-dev-engine-evidence.md | 50 empty folders removed. They were never in Git, so the deletion itself has no diff. Peter's ratification of the deletion list is pending. |
| BL-01e | M10-01 (+M10-06) | M10-01-T05, T06; M10-06 orphan disposition | DONE | dev 6941e08; dev 65e3315 | M10-01/M10-01-dev-engine-evidence.md; M10-06/M10-06-dev-engine-evidence.md | Rename residues and alias count DONE (M10-01). §1.1 moved the 45 tracked orphan folders to M10-06: 35 merged, 8 quarantined, 1 retained, plus aliases. |
| BL-01f | M10-01 | T13 | DONE | dev b3161da; design f69c5d4; srs 15422d7; proposal ba94f15; bp 2b41c08; social 724970f; linux 9de82cf; DRE d4a613d; website 75bc5c9 | M10-01/M10-01-catalogue-fonts-impeccable-website-global-evidence.md | Banned-font sweep verified; trigger block v2 (now v3 after the watchlist ruling). |
| PT-01 | M10-02 | T01, T02, T03 | DONE_WITH_LIMITATIONS | agents 35340f6; design 655d983; srs f8ce9fa; website 442290f; DRE 2aa54bc; bp 7b21210; social 52399fc; linux 42b3c1b; dev 33574d9; proposal ead7a38; finance a209c26; windows b1100c5 | M10-02/M10-02-host-files-drift-control-evidence.md | 12/12 bridges; 0 lost sentences. T02 needed validator repoints: website landed in website 26677c5; SRS was handled in M10-07. Codex-host behaviour NOT_ASSESSED. |
| PT-02 | M10-02 | T04, T14 | DONE_WITH_LIMITATIONS | agents 35340f6 | M10-02/M10-02-host-files-drift-control-evidence.md | `render_host_files.py` check exits 0. The evidence records the `portfolio-drift` remote run as NOT_ASSESSED; agents `validate` was green at 8a438c9 at close-out. |
| PT-03 | M10-02 | T07 | DONE | agents 35340f6 | M10-02/M10-02-host-files-drift-control-evidence.md | Render is idempotent on all 11 engines. |
| PT-04 | M10-02 | T08 | DONE_WITH_LIMITATIONS | agents 35340f6 (+ engine 1.1.0 commits in the PT-01 row) | M10-02/M10-02-host-files-drift-control-evidence.md | Version 1.1.0 everywhere. Tags are NOT_ASSESSED (awaiting release authority). |
| AR-17 | M10-02 | T04 | DONE | agents 35340f6 | M10-02/M10-02-host-files-drift-control-evidence.md | Hook-shape rules in the host-file check. |
| SP-18 | M10-02 | T04 | DONE | agents 35340f6 | M10-02/M10-02-host-files-drift-control-evidence.md | §1.1: reduced to a regression check inside PT-02's script. 12/12 `hooks.json` pass. |
| SP-04 | M10-02 / M10-04 | M10-02-T05 (drift check); M10-04-T01–T03 (canonical content) | DONE | agents 35340f6; dev 317b475; agents fe10a45; website 0fecec9; DRE 95f69ea; proposal 86996f4; bp 5f5e17d; social 5d955fc; linux c70b73b | M10-02/M10-02-host-files-drift-control-evidence.md; M10-04/M10-04-skill-writing-convergence-evidence.md | Split. Drift check DONE; canonical skill-writing plus six pointer stubs DONE. Both parts DONE. |
| BL-02a | M10-02 | T05, T06 | DONE | agents 35340f6; finance a209c26; windows b1100c5 | M10-02/M10-02-host-files-drift-control-evidence.md | 16 shared assets registered; 0 unexplained drift. The §1.1 addition (stale `digital-research-skills` wording in `engine-orchestrator.md` step 4) is DONE. |
| CV-01 | M10-02 | T12 | DONE | agents 35340f6 | M10-02/M10-02-host-files-drift-control-evidence.md | Router size fields added to the snapshot; porcelain bug fixed. |
| AC-02 | M10-02 | T09 | DONE | agents 35340f6 | M10-02/M10-02-host-files-drift-control-evidence.md | `--check-marketplace`: 13 drift lines, then 23 ok. |
| AC-03 | M10-02 | T10 | DONE_WITH_LIMITATIONS | agents 35340f6 | M10-02/M10-02-host-files-drift-control-evidence.md | Decision recorded ("DONE (delegated); pinning deferred"). Suites stay on `ref: main` until tags exist. |
| BL-02b | M10-02 | T11 | DONE | agents 35340f6 | M10-02/M10-02-host-files-drift-control-evidence.md | Every `SKILL.md` is listed or excluded with a reason. |
| BL-02c | M10-02 | T13 | DONE_WITH_LIMITATIONS | agents 35340f6 | M10-02/M10-02-host-files-drift-control-evidence.md | Budget step in CI. P04 measurement: 291,636 characters against 60,000, with no target set. The evidence records the remote CI as NOT_ASSESSED. |
| AO-03 | M10-03 | T03, T08 | DONE | dev ca226ae; srs 702a5ab; website 488efc8; DRE d2fdf57 | M10-03/M10-03-routing-collision-gate-evidence.md | Owned negatives in five engines. Cross-engine owners are mirrored as oracles. |
| AO-04 | M10-03 | T04 | DONE | dev ca226ae | M10-03/M10-03-routing-collision-gate-evidence.md | Collision gate with an allow-list (mysql/postgresql, delegated). |
| AO-05 | M10-03 | T05 | DONE | dev ca226ae; design 3b7c980; srs 702a5ab; website 488efc8; DRE d2fdf57 | M10-03/M10-03-routing-collision-gate-evidence.md | Fixture lint in five engines. |
| AO-06 | M10-03 | T06 | DONE | design 3b7c980 | M10-03/M10-03-routing-collision-gate-evidence.md | Dev TF-IDF ranker vendored; design p@1 85 % to 94.1 %. |
| AO-07 | M10-03 | T09 | DONE | agents 5a9153f | M10-03/M10-03-routing-collision-gate-evidence.md | 42 lexical route oracles (lexical proxy, not live routing). |
| AO-08 | M10-03 | T01, T02, T16, T17 | DONE_WITH_LIMITATIONS | agents 5a9153f; proposal 1f18b87 | M10-03/M10-03-routing-collision-gate-evidence.md | 0 undeclared pairs ≥ 0.75. T01: dev calibration p@3 99.5 % against the 100 % target. T17: live CI NOT_ASSESSED in the evidence. |
| AO-10 | M10-03 | T07 | DONE | srs 702a5ab | M10-03/M10-03-routing-collision-gate-evidence.md | Business-case and generic-SRS oracles now rank 1. A recorded limitation remains: the spelled-out "software requirements specification" prompt still ranks 8th. |
| AO-12 | M10-03 | T12 | DONE_WITH_LIMITATIONS | dev ca226ae; srs 702a5ab; website 488efc8 | M10-03/M10-03-routing-collision-gate-evidence.md | Tier-1 refinements DONE in dev, srs and website. The design part is a patch (`design-validate_engine-t12.patch`) and was not found applied at close-out (no tier-1 test in design). |
| AO-13 | M10-03 | T11, T17 | DONE_WITH_LIMITATIONS | agents 5a9153f; dev ca226ae; design 3b7c980; srs 702a5ab; website 488efc8; DRE d2fdf57 | M10-03/M10-03-routing-collision-gate-evidence.md | Rank-1 floors plus a baseline with a ledger. The `portfolio-routing` live run is NOT_ASSESSED in the evidence. |
| AO-15 | M10-03 | T15 | DONE | agents 5a9153f | M10-03/M10-03-routing-collision-gate-evidence.md | Rejected-change ledger RC-001 to RC-014. |
| SP-08 | M10-03 (+M10-05) | M10-03-T10; M10-05-T07 | DONE_WITH_LIMITATIONS | agents 5a9153f; agents 5ef3019 | M10-03/M10-03-routing-collision-gate-evidence.md; M10-05/M10-05-behavioural-eval-evidence.md | 12 acceptance cases built. The behavioural run is NOT_ASSESSED (zero spend). |
| SP-14 | M10-03 | T13 | DONE | dev ca226ae; proposal 1f18b87; bp 8919b72; social 9b11fbf; linux e8d10a7 | M10-03/M10-03-routing-collision-gate-evidence.md | Description-narration warning, byte-mirrored. |
| AC-01 | M10-03 | T14 | DONE | agents 5a9153f | M10-03/M10-03-routing-collision-gate-evidence.md | Marketplace `relevance` on 11/11 domain entries. |
| SP-05 | M10-04 | T04, T05 | DONE_WITH_LIMITATIONS | dev 317b475 | M10-04/M10-04-skill-writing-convergence-evidence.md | Pressure-testing reference DONE. The PS01 outcomes are NOT_ASSESSED (zero spend), and PS01 was seeded in a sibling file. |
| SP-06 | M10-04 | T06 | DONE | dev 317b475 | M10-04/M10-04-skill-writing-convergence-evidence.md | `form-matches-failure.md`. |
| SP-17 | M10-04 | T14 | DONE | agents fe10a45 | M10-04/M10-04-agents-governance-evidence.md | Session-diagnosis procedure. |
| SP-20 | M10-04 | T15 | DONE | agents fe10a45; dev 317b475 | M10-04/M10-04-agents-governance-evidence.md | AI-contributor policy (ratification recorded under delegation). |
| CV-06 | M10-04 | T07 | DONE_WITH_LIMITATIONS | dev 317b475; design 34a5ab2; srs 9b8a27f | M10-04/M10-04-skill-writing-convergence-evidence.md | Report-only byte warning. The srs part was delivered as a patch in the evidence and later landed in srs 9b8a27f. |
| GR-09 | M10-04 | T08 | DONE | dev 317b475 | M10-04/M10-04-safety-gate-and-register-evidence.md | Safety-gate items 9–11 with a Graphify worked example (read-only fetch, no install). |
| AR-16 | M10-04 | T09 | DONE | dev 317b475 | M10-04/M10-04-safety-gate-and-register-evidence.md | Bounded outbound check exemplar. |
| AC-04 | M10-04 | T10 | DONE_WITH_LIMITATIONS | agents fe10a45; dev 317b475; DRE 95f69ea | M10-04/M10-04-safety-gate-and-register-evidence.md | Register (15 rows), schema and intake procedure. Several register fields are NOT_ASSESSED. The dev routing fixture was a patch in the evidence. |
| AC-07 | M10-04 | T11 | DONE_WITH_LIMITATIONS | agents fe10a45 | M10-04/M10-04-agents-governance-evidence.md | Injection fixture plus tests. The pattern table is in a sibling file because the README was out of bounds. Runtime resistance is NOT ASSESSED. |
| UA-15 | M10-04 | T12 | DONE_WITH_LIMITATIONS | agents fe10a45; dev 317b475 | M10-04/M10-04-agents-governance-evidence.md; M10-04/M10-04-skill-writing-convergence-evidence.md | Canonical quarantine rule DONE. Register: 53/53 dispositioned, 0 converted; conversions O-1 to O-5 are open. |
| IM-16 | M10-04 | T13 | DONE | design 34a5ab2; agents fe10a45 | M10-04/M10-04-agents-governance-evidence.md | Rule-marker pilot and validator. |
| AO-09 | M10-05 | T01, T06 | DONE_WITH_LIMITATIONS | agents 5ef3019; dev 0a799d8 | M10-05/M10-05-behavioural-eval-evidence.md | Tier-3 runner built (34 tests; self-test 32/32). Suite execution is NOT_ASSESSED (zero spend). |
| AO-11 | M10-05 | T09 | DONE_WITH_LIMITATIONS | agents 5ef3019 | M10-05/M10-05-behavioural-eval-evidence.md | 11 plugin-eval cases, shape PASS. `claude plugin eval` is NOT_ASSESSED (zero spend). |
| AO-18 | M10-05 | T08 | DONE_WITH_LIMITATIONS | dev 0a799d8 | M10-05/M10-05-behavioural-eval-evidence.md | PS03–PS07 authored. Execution is NOT_ASSESSED (zero spend). |
| PT-05 | M10-05 | T01, T02, T06 | DONE_WITH_LIMITATIONS | agents 5ef3019 | M10-05/M10-05-behavioural-eval-evidence.md | Isolated-arm runner built. The live isolation smoke and the 144-cell run are NOT_ASSESSED (zero spend). |
| PT-06 | M10-05 | T04, T05 | DONE | dev 0a799d8 | M10-05/M10-05-behavioural-eval-evidence.md | All 16 fixtures materialised, with checkers and self-tests. |
| PT-07 | M10-05 | T03 | DONE | dev 0a799d8 | M10-05/M10-05-behavioural-eval-evidence.md | `short_prompt` required. |
| PT-12 | M10-05 | T13 | DONE | agents 5ef3019 | M10-05/M10-05-behavioural-eval-evidence.md | Report template applied to the dry-run report. |
| SP-07 | M10-05 | T11 | DONE_WITH_LIMITATIONS | agents 5ef3019 | M10-05/M10-05-behavioural-eval-evidence.md | Micro-test mode built. The control was not executed (zero spend). |
| AC-06 | M10-05 | T10 | DONE_WITH_LIMITATIONS | dev 0a799d8; agents 5ef3019 | M10-05/M10-05-behavioural-eval-evidence.md | Reference plus 10 frozen answers (PASS 10/10 with no model). The model run is NOT_ASSESSED (zero spend). |
| UA-11 | M10-05 / M10-12 | M10-05-T14; M10-12 UA-11 case | DONE_WITH_LIMITATIONS | agents 5ef3019; agents ea7ecbb | M10-05/M10-05-behavioural-eval-evidence.md; M10-12/M10-12-context-tours-graph-evidence.md | Split (§1.1). The case kind and template are DONE (M10-05). Case 077 was built in M10-12; its execution is NOT_ASSESSED (zero spend). The runner must also resolve the tour document from agents (owner M10-05 runner). |
| CV-07 | M10-05 | T12 | DONE | DRE f76c818 | M10-05/M10-05-behavioural-eval-evidence.md | Evidence-rung rule; ratification pending. |
| SP-01 | M10-06 / M10-08 | M10-06-T01, T02; M10-08-T01 | DONE | dev 65e3315; srs 360854a | M10-06/M10-06-dev-engine-evidence.md; M10-08/M10-08-srs-elicitation-asbuilt-testdesign-evidence.md | Split. Dev part DONE (mandatory `superpowers:brainstorming` calls removed); SRS part DONE (protocol usable without Superpowers). |
| SP-03 | M10-06 | T03 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Plan-header reference plus aliases. |
| SP-09 | M10-06 | T04 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Verification table, including the delegated-agent row. |
| SP-10 | M10-06 | T05 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Test-first seams. The "Do not force test-first" paragraph is byte-identical. Ratification pending. |
| SP-11 | M10-06 | T06 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Parallel-lane rules. |
| SP-12 | M10-06 | T07 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Worktree safety reference. |
| SP-13 | M10-06 | T08 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Deviation: a minimal description edit was needed for top-3; ratification pending. |
| PT-08 | M10-06 | T09 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Ladder links plus the ERP never-simplify list. |
| PT-11 | M10-06 | T25 | NOT_ASSESSED | — | M10-06/M10-06-dev-engine-evidence.md | Evidence: "NOT_ASSESSED / DEFERRED". The reach test needs a live Task-spawned subagent model run (zero spend). No hook was added. |
| AO-17 | M10-06 | T10 | DONE_WITH_LIMITATIONS | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Quality-bar guard plus PS02. At the time PS02 was not validated by the tool, because M10-04-T05 had not landed; it later landed in dev 317b475. Ratification pending. |
| CV-02 | M10-06 | T11 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | R0/R1/R2 register; ratification pending. |
| CV-03 | M10-06 | T12 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | §1.1: retargeted to `coding-agent-optimization/references/parallel-execution-lanes.md`. |
| GR-05 | M10-06 | T13 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Graph-first comprehension doctrine; `install graphify` = 0. |
| GR-06 | M10-06 | T15 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Staleness and advisory properties; no hook change. |
| GR-07 | M10-06 | T14 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Evidence tags in the drill-down templates. |
| GR-08 | M10-06 | T20 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | PHP/MySQL map pilot, verdict KEEP (10/10 routes). Client output is kept private and was not committed (checked). |
| UA-02 | M10-06 | T16 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Topology-ordered tour. |
| UA-03 | M10-06 | T17 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | `validate_tour.py` with four failure codes. |
| UA-04 | M10-06 | T18 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Untrusted-content rule. |
| UA-05 | M10-06 | T19 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Change-class map for doc maintenance. |
| AR-10 | M10-06 | T21 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Architecture-as-code reference (C4, with cited sources). |
| AR-11 | M10-06 | T22 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | `verify_diagram_evidence.py` (15 tests). |
| UX-12 | M10-06 | T23 | DONE | dev 65e3315 | M10-06/M10-06-dev-engine-evidence.md | Curated-corpus worked example. |
| IM-15 | M10-06 | T24 | DEFERRED | — | M10-06/M10-06-dev-engine-evidence.md | Gated on the M10-09 detector, which did not exist when M10-06 ran. It was never handed back: no later evidence mentions IM-15. The detector now exists (design 3fe84a6). |
| AR-04 | M10-07 | T01, T02, T11 | DONE_WITH_LIMITATIONS | srs 6218681 | M10-07/M10-07-srs-design-diagrams-evidence.md | Typed diagram IR and generator DONE. The T11 pilot is DONE_WITH_LIMITATIONS: full `engine validate` of the partial fixture fails on pre-existing unrelated gates. |
| AR-05 | M10-07 | T03, T11 | DONE_WITH_LIMITATIONS | srs 6218681 | M10-07/M10-07-srs-design-diagrams-evidence.md | `DiagramTraceCheck` DONE; T11 limitation as for AR-04. |
| AR-06 | M10-07 | T06 | DONE | srs 6218681 | M10-07/M10-07-srs-design-diagrams-evidence.md | HLD/LLD/database skills rewritten for the IR. |
| AR-07 | M10-07 | T07 | DONE | srs 6218681 | M10-07/M10-07-srs-design-diagrams-evidence.md | Baseline delta of diagram elements. |
| AR-08 | M10-07 | T04 | DONE | srs 6218681 | M10-07/M10-07-srs-design-diagrams-evidence.md | `Finding` fields; golden reports byte-identical. |
| AR-09 | M10-07 (delivered in M10-03) | M10-07-T05; M10-03 extra | DONE | agents 5a9153f | M10-03/M10-03-routing-collision-gate-evidence.md | M10-07-T05 is "NOT DONE — outside assigned scope". The `findings[]` extension to `validation-result.schema.json` was delivered by the M10-03 executor ("Extra (M10-07-T05 / AR-09) — DONE"). |
| AR-12 | M10-07 | T08 | DONE_WITH_LIMITATIONS | design 68f373b; design 34a5ab2 | M10-07/M10-07-srs-design-diagrams-evidence.md | Diagram visual standards. The human typographic authority for Public Sans by name is NOT_ASSESSED (escalated to Peter); ratification pending. |
| AR-13 | M10-07 | T09 | DONE | design 68f373b | M10-07/M10-07-srs-design-diagrams-evidence.md | Font gate widened to `.svg`/`.mmd`/`.json`; 32/32. Enablement awaits Peter's exact-diff approval. |
| AR-14 | M10-07 | T10, T11 | DONE_WITH_LIMITATIONS | srs 6218681 | M10-07/M10-07-srs-design-diagrams-evidence.md | Figure manifest DONE; T11 limitation as for AR-04. |
| SP-15 | M10-08 | T02 | DONE | srs 360854a | M10-08/M10-08-srs-elicitation-asbuilt-testdesign-evidence.md | Ceremony classification, section approval and Review Focus. |
| GR-10 | M10-08 | T03 | DONE | srs 360854a | M10-08/M10-08-srs-elicitation-asbuilt-testdesign-evidence.md | As-built recovery procedure. |
| GR-11 | M10-08 | T04 | DEFERRED | — | M10-08/M10-08-srs-elicitation-asbuilt-testdesign-evidence.md | "DEFERRED — NOT_ASSESSED (no annotated codebase)". Garage has no `@req` annotations, so the plan's default applied. |
| UA-06 | M10-08 | T05 | DONE | srs 360854a | M10-08/M10-08-srs-elicitation-asbuilt-testdesign-evidence.md | Orientation guide. Client use is NOT_ASSESSED (expected limitation, not model-executed). |
| UA-07 | M10-08 | T06 | DONE | srs 360854a | M10-08/M10-08-srs-elicitation-asbuilt-testdesign-evidence.md | Commit-pinned staleness check. |
| UA-08 | M10-08 | T07 | DONE | srs 360854a | M10-08/M10-08-srs-elicitation-asbuilt-testdesign-evidence.md | Walkthrough-order rule. |
| AO-19 | M10-08 | T08 | DONE | srs 360854a | M10-08/M10-08-srs-elicitation-asbuilt-testdesign-evidence.md | Agent build brief. |
| AC-05 | M10-08 | T09 | DONE_WITH_LIMITATIONS | srs 360854a; dev 1e87460 | M10-08/M10-08-srs-elicitation-asbuilt-testdesign-evidence.md | Pairwise reference. The ISO/IEC/IEEE 29119-4 clause number is NOT_ASSESSED (standard not available offline). |
| UX-10 | M10-08 | T10 | DONE | srs 360854a | M10-08/M10-08-srs-elicitation-asbuilt-testdesign-evidence.md | Controls search. |
| CV-04 | M10-08 | T11 | DROPPED-AT-EXECUTION | — | M10-08/M10-08-srs-elicitation-asbuilt-testdesign-evidence.md | Reason: the conditional decision rule was not met. V&V SOP plus writing standards are 16.3 % of srs effective bytes, against a 25 % threshold, so there was NO CHANGE (plan default; delegated). The measurement is in evidence commit agents c74d73a. |
| IM-01 | M10-09 | T01, T02, T03, T15 | DONE | design 3fe84a6 | M10-09/M10-09-design-slop-detector-evidence.md | `chwezi-slop` detector (49 rules), with licence notice. |
| IM-02 | M10-09 | T04, T05 | DONE_WITH_LIMITATIONS | design 3fe84a6 | M10-09/M10-09-design-slop-detector-evidence.md | Fixtures and validator floors DONE. The evidence records the CI run URL as NOT_ASSESSED; design CI was green at 25ce1e6 at close-out. |
| IM-04 | M10-09 | T12, T13 | DONE | design 3fe84a6; design 7a2ab6b; agents 20ca40c | M10-09/M10-09-design-slop-detector-evidence.md | Watchlist refresh; doctrine consistency 0 conflicts. Trigger block v3 propagated. |
| IM-06 | M10-09 | T06 | DONE | design 3fe84a6 | M10-09/M10-09-design-slop-detector-evidence.md | Slop hooks, unit-tested with synthesised payloads. A live session is NOT_ASSESSED. |
| IM-07 | M10-09 | T07 | DONE | design 3fe84a6 | M10-09/M10-09-design-slop-detector-evidence.md | Waiver format. |
| IM-08 | M10-09 | T08 | DONE_WITH_LIMITATIONS | design 3fe84a6 | M10-09/M10-09-design-slop-detector-evidence.md | Browser tier. CI has no locked Playwright, so the acceptance test is skipped there. |
| IM-09 | M10-09 | T09 | DONE | design 3fe84a6 | M10-09/M10-09-design-slop-detector-evidence.md | Token-drift rules (CIEDE2000). |
| IM-12 | M10-09 | T10 | DONE | design 3fe84a6 | M10-09/M10-09-design-slop-detector-evidence.md | Side-stripe ruling, Option A. |
| IM-14 | M10-09 | T11 | DONE | design 3fe84a6 | M10-09/M10-09-design-slop-detector-evidence.md | Browser-surfaces section. §1.1: the tabular-numerals part was dropped as already done. |
| UX-14 | M10-09 | T12 | DONE | design 3fe84a6 | M10-09/M10-09-design-slop-detector-evidence.md | UUPM counted as one evidence source for bans only; no data reused. |
| AC-09 | M10-09 | T12 | DONE | design 3fe84a6 | M10-09/M10-09-design-slop-detector-evidence.md | Watchlist evidence rule applied. |
| BL-09a | M10-09 | T14 | DONE | DRE 20564b8 | M10-09/M10-09-design-slop-detector-evidence.md | K5 AS1–AS7 re-audit with detector evidence (retained, before the 3 Oct due date). |
| UX-01 | M10-10 | T01 | DONE | design dab2b6e | M10-10/M10-10-design-data-evidence.md | Doctrine lint. |
| UX-02 | M10-10 | T02, T15 | DONE | design dab2b6e | M10-10/M10-10-design-data-evidence.md; M10-10/M10-10-references-evidence.md | Cited typography records. Peter to ratify the face list. |
| UX-03 | M10-10 | T07 | DONE | design dab2b6e | M10-10/M10-10-design-data-evidence.md | `design_query.py` wired into 4 skills. |
| UX-04 | M10-10 | T03, T15 | DONE | design dab2b6e | M10-10/M10-10-design-data-evidence.md; M10-10/M10-10-references-evidence.md | Palette schema; 0 of 56 contrast failures. |
| UX-05 | M10-10 | T05 | DONE_WITH_LIMITATIONS | design dab2b6e | M10-10/M10-10-design-data-evidence.md | BM25 with calibrated abstention. The floor mechanism works, but no floor currently does any work. |
| UX-06 | M10-10 | T06 | DONE_WITH_LIMITATIONS | design dab2b6e | M10-10/M10-10-design-data-evidence.md | Relevance harness. The cases were judged by their author, and the second-reviewer re-judgement is open. |
| UX-07 | M10-10 | T09 | DONE | design dab2b6e | M10-10/M10-10-design-data-evidence.md | WCAG records and pre-launch checklist. |
| UX-08 | M10-10 | T04 | DONE | design dab2b6e | M10-10/M10-10-design-data-evidence.md | Record lifecycle. |
| UX-09 | M10-10 | T08 | DONE | agents 48af46b; design dab2b6e | M10-10/M10-10-design-data-evidence.md | Shared retrieval metrics module (vendored in design). |
| IM-10 | M10-10 (+M10-11-T13) | T10 | DONE | design dab2b6e; website 7ad522b | M10-10/M10-10-design-data-evidence.md; M10-10/M10-10-references-evidence.md | Visitor modes: runtime and reference halves DONE. The website consumer (M10-11-T13, no backlog ID) is DONE. |
| IM-13 | M10-10 | T11 | DONE | design dab2b6e | M10-10/M10-10-references-evidence.md | Critique vocabulary reference. |
| PT-09 | M10-10 | T12 | DONE | design dab2b6e; dev e0466ba | M10-10/M10-10-references-evidence.md | Evidence: design half DONE; the dev F13 note "NOT DONE (out of scope)" was later landed by the orchestrator in dev e0466ba (subject names M10-10 PT-09). |
| UA-13 | M10-10 | T13 | DONE | design dab2b6e | M10-10/M10-10-references-evidence.md | — |
| AC-08 | M10-10 | T14 | DONE | design dab2b6e | M10-10/M10-10-references-evidence.md | — |
| IM-03 | M10-11 | T01–T05 | DONE_WITH_LIMITATIONS | website 7ad522b; agents 6c65f6c | M10-11/M10-11-website-evidence.md | Slop gate rebuilt on the vendored detector. T03: the literal `--validate-registry --extra-rules` command cannot pass on a vendored copy; a pack validator is used instead. |
| PT-10 | M10-11 | T07, T08 | DONE | website 7ad522b | M10-11/M10-11-website-evidence.md | Minimalism pass plus the `dependency_minimalism` check. |
| SP-16 | M10-11 | T06 | DONE | website 7ad522b | M10-11/M10-11-website-evidence.md | One-question intake, Gate 3 and Journey Review Focus. |
| AO-16 | M10-11 | T09 | DONE | website 7ad522b; agents 6c65f6c | M10-11/M10-11-website-evidence.md | Lighthouse oracle 025 unpinned: rank 94 to rank 1. |
| AC-10 | M10-11 | T10 | DONE | website 7ad522b | M10-11/M10-11-website-evidence.md | Visual-QA pre-flight. |
| GR-12 | M10-11 | T11 | DONE | website 7ad522b | M10-11/M10-11-website-evidence.md | Content link graph (advisory CI step). |
| UX-11 | M10-11 | T12 | DONE_WITH_LIMITATIONS | website 7ad522b | M10-11/M10-11-website-evidence.md | Sector table: 10 of 12 rows evidenced, 2 NOT_ASSESSED. Recheck the SACCO row after 30 Sep 2026. |
| IM-11 | M10-12 | T01–T04 | DONE | agents ea7ecbb; dev dec6bd9; design 2315408; srs 0da72de; website 88d2af4; DRE eaa53c1; proposal fbde091; bp 29d6aa3; social f9b9067; linux 30ac859; finance d2d013c; windows 243221f | M10-12/M10-12-context-tours-graph-evidence.md | `PROJECT.md` contract, doctor, pilots and router read rule in 11 engines. |
| UA-09 | M10-12 | T06 | DONE | agents ea7ecbb | M10-12/M10-12-context-tours-graph-evidence.md | Deterministic engine tours. |
| UA-10 | M10-12 | T07 | DONE | agents ea7ecbb | M10-12/M10-12-context-tours-graph-evidence.md | MCP `engine_tour`. |
| UA-12 | M10-12 | T05 | DONE_WITH_LIMITATIONS | agents ea7ecbb | M10-12/M10-12-context-tours-graph-evidence.md | §1.1: built in agents (`scripts/skill_fanin.py`) with a dev pointer. The named fixture adapters do not exist (generic key walk used instead), and reachability is copied from P01, not recomputed. |
| GR-01 | M10-12 | T08 | DONE | agents ea7ecbb; agents e7c36a8 | M10-12/M10-12-context-tours-graph-evidence.md; M10-12/M10-12-graph-defect-remediation.md | Report-only skill graph, verdict KEEP. Defect remediation followed: missing skill paths 155 to 1 (bp 8949387, dev c29972d, srs 5f58f11, website ec72bca, DRE 2b9c87d, proposal 07722b6, social 09eebe7). |
| GR-03 | M10-12 | T09 | DONE | agents ea7ecbb | M10-12/M10-12-context-tours-graph-evidence.md | MCP `query_skill_graph`. |
| AO-20 | M10-12 | T10 | DONE | agents ea7ecbb | M10-12/M10-12-context-tours-graph-evidence.md | Skill lifecycle map. |
| CV-05 | M10-12 | T11 | DONE | agents ea7ecbb | M10-12/M10-12-context-tours-graph-evidence.md | Usage scan (local evidence). |
| AR-15 | M10-13 | T01, T02 | DONE_WITH_LIMITATIONS | proposal 3e4330d; proposal 5de27f8; srs fa85fba | M10-13/M10-13-cross-engine-extensions-evidence.md; M10-13/M10-13-followup-srs-renderer-fixes.md | Proposal figures via the SRS renderer hand-off. The routing fixture was added in the follow-up (5de27f8). The 8 pt legibility of the 10-step workflow figure at body width is still not met. |
| UX-13 | M10-13 | T03 | DONE | finance af2af30 | M10-13/M10-13-cross-engine-extensions-evidence.md | Read-only effective-date lookup with refusal (13 tests). |
| UA-14 | M10-13 | T04 | NOT_ASSESSED | — | M10-13/M10-13-cross-engine-extensions-evidence.md | Not run (zero spend; no spend approval). A decision record is in DRE 340b200: no adoption, and the re-entry condition is stated. Nothing was installed. |
| BL-13a | M10-13 | T05 | DONE_WITH_LIMITATIONS | DRE 340b200; agents 2500c89 | M10-13/M10-13-cross-engine-extensions-evidence.md | First quarterly ecosystem scan; register grew from 15 to 72 rows. 27 of 47 candidates were triaged only (outbound hosts and overlap NOT_ASSESSED). |
| BL-13b | M10-13 | T01, T06 | DONE_WITH_LIMITATIONS | bp d84a599; srs fa85fba | M10-13/M10-13-cross-engine-extensions-evidence.md; M10-13/M10-13-followup-srs-renderer-fixes.md | Business-plan figure reference. The T06 Gantt was illegible at body width (DONE_WITH_LIMITATIONS in the evidence). The follow-up re-rendered it at 720 px (smallest label about 8.1 pt); the reviewer may upgrade. |
| AO-14 | M10-14 | T01, T02, T05 | DONE (M10-14, commit pending orchestrator) | pending (orchestrator) | M10-14/ | Measured scoring, with NOT_ASSESSED scored as 0. The precursor scoring rule is in M10-05-T15 (agents 5ef3019). |
| BL-14a | M10-14 | T03–T06 | DONE (M10-14, commit pending orchestrator) | pending (orchestrator) | M10-14/ | Portfolio re-audit against roadmap §5. |
| BL-14b | M10-14 | T07–T09, T11, T12 | DONE (M10-14, commit pending orchestrator) | pending (orchestrator) | M10-14/traceability-closure.md | Includes this closure; Kaizen record, memory update and final push. |

## 3. Counts and mechanical verification

**Total IDs in §1: 161. Rows in the table: 161.**

| Final status | Count |
|---|---:|
| DONE | 111 |
| DONE_WITH_LIMITATIONS | 42 |
| DONE (M10-14, commit pending orchestrator) | 3 |
| NOT_ASSESSED | 2 |
| DEFERRED | 2 |
| DROPPED-AT-EXECUTION | 1 |
| PARTIAL | 0 |
| **Total** | **161** |

The counts were produced mechanically by `verify_traceability.py`, written in the session scratchpad (not committed). The script:
- extracts every ID from the §1 assignment table of the backlog, using the pattern `(SP|PT|UX|GR|CV|AO|UA|AC|AR|IM)-NN` or `BL-NNx`;
- parses this file's table;
- checks that each §1 ID appears exactly once, that no row carries an ID outside §1, and that every status is in the allowed set;
- checks that every `DONE` and `DONE_WITH_LIMITATIONS` row carries at least one short commit hash.

Command:

```
python -X utf8 C:\Users\Peter\AppData\Local\Temp\claude\C--Users-Peter\7bd42c8b-aaae-434c-add3-01a5072a9c86\scratchpad\verify_traceability.py
```

Output (29 Sep 2026):

```
backlog_section1_ids=161 table_rows=161 unique_table_ids=161
missing=[] extra=[] not_exactly_once=[]
status_counts=DEFERRED: 2; DONE: 111; DONE (M10-14, commit pending orchestrator): 3; DONE_WITH_LIMITATIONS: 42; DROPPED-AT-EXECUTION: 1; NOT_ASSESSED: 2
rows_without_status=0 errors=[]
RESULT: PASS
```

## 4. §3 dropped-list check

Every §3 item stayed dropped. The checks below were run read-only on 29 Sep 2026.

**Installed-state checks** (`~/.claude/plugins/installed_plugins.json`, `known_marketplaces.json`, `settings.json`, `PATH`, `pip`, global `npm`, `~/.claude/skills`):
- Installed plugins: 13 `claude-code-workflows`/`anthropic-agent-skills`/`claude-code-plugins` entries, plus `superpowers@superpowers-marketplace`.
- `grep -ilE "graphify|caveman|headroom|ui-ux-pro-max|uupm|understand-anything|archify|ponytail|impeccable"` over the three files: no match (exit 1).
- `command -v` for graphify, caveman, headroom, archify, understand, ponytail, impeccable and uupm: all absent.
- pip, npm -g and `~/.claude/skills`: no match.
- The same pattern over the 38 tracked `package.json`, `requirements*.txt`, `pyproject.toml`, `hooks.json` and `plugin.json` files in all twelve repositories: 0 matches. No tracked path is named after any of these tools.

| §3 dropped item | Stayed dropped? | Evidence |
|---|---|---|
| Install Superpowers anew / universal TDD Iron Law | Yes | D1 kept the existing install and upgraded it (not a new adoption). M10-06-T05 kept "Do not force test-first" byte-identical, and `grep -c 80% tdd-guide.md` = 0 (M10-06 evidence). |
| SP-19 router word or token budgets | Yes | M10-02: "no target is set (P04)". M10-08 CV-04: "No byte target is proposed (P04)". |
| Systematic debugging, two-axis review, work graph, spikes, shared-understanding gate | Yes | No M10 task re-creates them. M10-06 only links into existing assets (T08 links `two-axis-code-review.md`; T03 validates the existing work graph). |
| Rebuild the Ponytail ladder or the `solution_*` tools | Yes | dev diff `7adc9fc..HEAD` touches only `tools/validate_benchmark_fixtures.py` (modified). M10-05 used the existing `tools/solution_evidence.py`. PT-08 links the existing ladder. |
| Install Ponytail, or its "ultra" level | Yes | Not in `installed_plugins.json`, not on PATH. |
| Install Graphify on this host | Yes | Absent from plugins, PATH and pip. D4 and the P06 addendum. M10-04 fetched `install.py` read-only into the scratchpad. M10-06 `install graphify` = 0. |
| GR-02, GR-04 route-existence and snapshot wiring | Yes | Not re-measured. M10-12 UA-12 copies P01 reachability ("not recomputed"); the GR-01 graph is report-only. |
| Install Caveman or Headroom; new skill-size inventory; description budget gate; 500-line caps; overall token target | Yes | Not installed. BL-02c is the existing K6 validator in `--report-only` with no target. CV-06 is a report-only byte warning (assigned item, not a cap). CV-01 extends the P01 snapshot rather than adding a new inventory. |
| Reuse UUPM font, palette or style data | Yes | Design provenance note: "none of its data is reused". UUPM appears in design code only as attribution headers ("re-implemented"). M10-10 records cite human authorities. |
| A second design retrieval engine | Yes | M10-10 modified `engine/design_engine/catalog.py` and added a CLI (`scripts/design_query.py`) over it. No second engine. |
| A single Chwezi marketplace | Yes | Only the existing `.claude-plugin/marketplace.json` was modified (relevance, counts); no new marketplace file. |
| Re-derive AS1–AS7; add Impeccable as a dependency | Yes | BL-09a retained AS1–AS7 (re-audit, not re-derivation). The detector has no dependencies, and no manifest names Impeccable. |
| New general eval schema or benchmark corpus | Yes | Schemas added: `project-context`, `third-party-skill-register`, the slop registry and the diagram IR; `validation-result` was extended with `findings[]`. All are domain-specific, and there is no `*.schema.json` under `evals/`. Cases 023–077 reuse the 001–022 shape. M10-05 materialised the existing 16 fixtures. |
| Web-performance gates rebuild | Yes | M10-11-T09 changed only the deploy description, the Quick/Deep section and the routing fixture (AO-16). |
| `/understand-knowledge` conversion of the engines | Yes | Only the UA-14 pilot was kept, and it was NOT_ASSESSED with nothing installed. No `index.md`/wikilink conversion. |
| Model-policy work | Yes | M10-00-T08 was the convention recheck only (retain Luna/high); no policy file changed. |

## 5. M10-00 value measure (b): no rejected install proposed

**Result: met. 0 phases proposed an install that D1–D5 reject.**

Command, over all phase evidence:

```
grep -rniE "(graphify|caveman|headroom|ui.ux.pro.max|uupm|understand.anything|understand-knowledge|archify|ponytail|impeccable).{0,80}install|install.{0,80}(graphify|caveman|headroom|ui.ux.pro.max|uupm|understand|archify|ponytail|impeccable)" --include=*.md docs/operations/m10-kaizen-evidence
```

It returned five hits, none of them a proposal:

| Hit | What it is |
|---|---|
| M10-04 safety-gate evidence l.21, l.31 | A read-only `curl` of Graphify's `install.py`, kept in the scratchpad only, used as the GR-09 worked example of red flags. |
| M10-06 evidence l.61 | `install graphify` = 0 (a check that no install is recommended). |
| M10-07 evidence l.5 | The Archify pattern attribution line ("Paraphrased; no schema, code or test text copied"). |
| M10-08 evidence l.80 | "No install command and no product recommendation". |

A second grep for `plugin install|marketplace add|npx skills add|curl … | bash` returned two hits: a README plugin-install pointer in M10-01 (the Chwezi plugin itself) and a DRE status note in M10-13. Neither is a rejected tool.

Other install-adjacent actions, none of them rejected:
- The Superpowers upgrade is D1's own decision (ABSORB, UPGRADE).
- The M10-09 Playwright browser tier ran in a scratch project, not an engine repository, and is not a D1–D5 tool.
- The M10-13 ecosystem scan was desk review only ("nothing installed, cloned or executed").
- The UA-14 pilot installed nothing.

## 6. Open items for the next-opportunities register

| ID | Status | Owner engine | What is open |
|---|---|---|---|
| PT-11 | NOT_ASSESSED | chwezi-dev-engine | Subagent doctrine reach test needs a live Task-spawned model run (spend approval). |
| UA-14 | NOT_ASSESSED | digital-research-engine | Understand Anything `/understand-knowledge` sandbox pilot needs spend approval and a UA-01 reversal trigger. |
| IM-15 | DEFERRED | chwezi-dev-engine (with design-system-skills) | Was gated on the M10-09 detector, which now exists (design 3fe84a6); hand back and execute. |
| GR-11 | DEFERRED | srs-skills | `@req` code-to-requirement trace awaits a codebase whose team maintains annotations. |
| CV-04 | DROPPED-AT-EXECUTION | srs-skills | Re-evaluate only if a new CV-01 measurement meets the 25 % rule. |

DONE_WITH_LIMITATIONS items that need a model run under spend approval: SP-02, SP-05, SP-07, SP-08, AO-09, AO-11, AO-18, PT-05, AC-06, UA-11. These were closed as `DONE_WITH_LIMITATIONS` because the build is done; the run belongs in the same register.

**Side findings from the close-out CI check (not backlog IDs):**
- srs-skills `Engine` fails at `fa85fba` (`broken_relative_link: 1`).
- digital-research-engine `Skill engine quality` fails at `2b9c87d` (`broken_relative_link: 2`).
- Both followed the M10-12/M10-13 link edits; owners are the srs and DRE engines.
- The AO-12 design Tier-1 patch (`M10-03/patches-for-orchestrator/design-validate_engine-t12.patch`) is still unapplied.
