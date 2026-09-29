# M10-06 evidence: dev engine (all tasks + BL-01e orphan folders)

| Field | Value |
|---|---|
| Phase | M10-06 Dev Engine: Methodology and Comprehension Absorption |
| Scope | Tasks T01–T26 and the 45 tracked orphan folders handed from M10-01, in `C:\wamp64\www\chwezi-dev-engine` |
| Executor date | 29 Sep 2026 |
| Base commit | `b3161da` at start; M10-02 committed `33574d9` (CLAUDE.md, `.claude-plugin/`, `.skills-engine/`, `tests/test_engine_control_plane.py`) during the run. None of those files was touched by this executor |
| Git actions | None. All edits unstaged |
| Spend | Zero. Local tools; three free `WebFetch` reads of c4model.com for the C4 source record; no model-run evals |
| Not touched | `CLAUDE.md`, `AGENTS.md`, `.claude-plugin/`, `.skills-engine/` (M10-02). The Garage repository was only read |
| Full changed-path list | `M10-06-dev-engine-changed-files.tsv` in this folder (506 paths: 77 modified, 191 deleted by move, 238 added) |

Decisions marked "delegated" were taken as the plan's recommended option: decided by orchestrator under Peter's delegated authority, 29 Sep 2026.

## Baseline (before any edit, HEAD `b3161da`) — `baseline.txt`

167 active; guardrails 0 findings; routing 184 fixtures, p@1 178/184, p@3 184/184; contract gate 161/0 errors; compliance 136/165 fully compliant; pytest 133 passed, 3 skipped; hooks 61/61 and 7/7; control plane PASS; manifest 165; benchmark PASS; book-extraction 0.

## Orphan folders (BL-01e) — DONE

**Finding.** The May 2026 consolidation (`84d37a5`) renamed each retired `skills/<name>/SKILL.md` to `<parent>/references/<name>.md` but left the retired skill's `references/`, `templates/` and `examples/` behind. The moved entrypoints therefore pointed at files that were no longer beside them.

**Disposition (delegated).**

| Group | Count | Disposition |
|---|---:|---|
| Retired-skill payloads with a parent entrypoint | 35 | **Merge**: moved to `<parent>/references/<name>/`, links repointed |
| `finance-accounting/_chwezi-finance-engine-skeletons` | 1 | **Merge** into `accounting-engine/references/chwezi-finance-engine-skeletons/`; linked from `posting-engine-contract.md` |
| `ios/` TODO stubs (macOS, Swift concurrency, Xcode) | 8 | **Quarantine** out of active roots to tracked `docs/plans/apple-todo-backlog/` (+ README); history note in the WWDC26 plan |
| `finance-accounting/finance` | 1 | **Retain**: namespace for 17 routed finance aliases |
| `sdlc-meta/plan-implementation` | (in the 35) | Merge + **alias** `ALIAS.md` → `implementation-status-auditor` |
| `sdlc-meta/spec-architect` (removed empty by M10-01) | — | **Alias** recreated: `ALIAS.md` → `project-requirements` |
| `sdlc-meta/references` (not a skill folder) | — | Retain: shared reference linked from `ai-agent-runtime-architecture` |

- **Method:** `orphan-merge-migrate.py` (dry run reviewed, then `--apply`). It moved 183 files with `shutil.move` and rewrote 441 relative tokens in 90 files. Each token was resolved against the file's old location, and the reference file is kept as the anchor. Emptied folders were removed with `os.rmdir`, which refuses a non-empty directory. No file was deleted. The move map is in `orphan-merge-plan.json`; the rmdir log is in `orphan-merge-apply-log.txt`.
- **Link check:** `linkcheck.py` and `lcdiff.py`, HEAD archive against the working tree:
  - broken relative file tokens on the active roots went from 770 to 423;
  - 348 were fixed and 0 newly broken;
  - the one transient break, in the `plan-implementation` alias, was repaired.
- **Registry:** `docs/skill-aliases.yml` has two new routes. `docs/skill-routing-index.md` alias count 76 → 78, matching the files on disk.
- **After:** a rescan shows only `finance-accounting/finance` and `sdlc-meta/references` remaining; both are retained by design. Guardrails show 0 findings with alias integrity intact.
- **Scope note:** the relinking also repaired dangling `cicd-devsecops/SKILL.md`-style tokens in six `linux-security-hardening` references and in `professional-word-output/references/manual-guide/entrypoint.md`, because they pointed into the same retired folders.

## Tasks

| Task | Status | Files | Evidence |
|---|---|---|---|
| T01 SP-01 | DONE | `00-meta-initialization/new-project/SKILL.md`, `skills/execution-plan-scripts/SKILL.md` | The only `superpowers:brainstorming` line is the optional-helper sentence (line 69); no "MANDATORY" or "Before anything else"; quick validate: valid |
| T02 SP-01 | DONE | `world-class-engineering/SKILL.md` | "spike, bounded" present; Superpowers attribution present; SKILL.md 368 lines (≤ 380 after T02+T09) |
| T03 SP-03 | DONE | new `execution-plan-scripts/references/plan-header-and-proportion.md` (71 lines) linked from SKILL.md; prose repointed in `saas-accounting-system` and `validation-contract` (relative paths so guardrails resolve them); 2 `ALIAS.md` + routes | Guardrails 0 findings (no `alias-stale` or `alias-unrouted`); `validate_work_graph.py templates/work-graph.yml` passes; remaining `plan-implementation`/`spec-architect` mentions in SKILL.md files resolve to the existing references |
| T04 SP-09 | DONE | `rules/common/verification.md` (55 lines), `world-class-engineering/references/verification-loop.md` | 8 data rows, including the delegated-agent row; banned phrasing list; `grep delegated` = 1 |
| T05 SP-10 | DONE (ratification) | `advanced-testing-strategy/references/test-first-seams-and-oracles.md`, `agents/tdd-guide.md` | `git diff`: additions only; "Do not force test-first" paragraph byte-identical; "suite defines green" present; `grep -c 80% tdd-guide.md` = 0; dead `sdlc-meta/e2e-testing` pointer repointed |
| T06 SP-11 | DONE | `parallel-execution-lanes.md` (140 lines) | All five rules present; model-ID grep returns nothing; quick validate `coding-agent-optimization`: valid |
| T07 SP-12 | DONE | new `coding-agent-optimization/references/worktree-safety.md` (65 lines); links from SKILL.md "When this skill applies" and the lanes Execution Rules | `untracked` = 2; `node hooks/test-destructive-bash-gate.js` 61/61 |
| T08 SP-13 | DONE (**deviation**) | new `git-collaboration-workflow/references/receiving-review-feedback.md` (67 lines); links from SKILL.md and `two-axis-code-review.md`; fixture in `scripts/routing_fixtures.yml` | With the description unchanged, the fixture ranked outside the top 5, so it failed. Minimal description edit made: "deciding whether reviewer feedback is right" (241 → 286 characters). Result: rank 1; full smoke has 0 failures. The phase's §7.10 "no description edited" is therefore not met for this one skill. **Needs Peter's ratification** |
| T09 PT-08 | DONE (ratification) | `world-class-engineering/SKILL.md` | Both ladder links; all eight never-simplify items; routing p@1 not reduced in absolute terms (see routing) |
| T10 AO-17 | DONE_WITH_LIMITATIONS (ratification) | new `world-class-engineering/references/quality-bar-guard.md` (114 lines), linked from References; PS02 in `benchmarks/solution-selection/fixtures.json` | `validate_benchmark_fixtures.py` PASS, `SPECIFIED_NOT_EXECUTED`. It does not yet validate `pressure_scenarios` (M10-04-T05 not landed). A manual check against the M10-04 T05 field list passed: all fields, `PS\d{2}`, 3 allowed pressures, forced choice A/B/C, compliant B |
| T11 CV-02 | DONE (ratification) | `docs/continuous-improvement/english-output-standard-2026-09-02.md`, `rules/common/agentic-engineering.md` | R0 names proposals, SRS, business plans, website copy; `validate_engine_control_plane.py` PASS |
| T12 CV-03 | DONE | `parallel-execution-lanes.md`; new `tests/test_report_shapes.py` | 22 passed; reference 140 lines (≤ 200) |
| T13 GR-05 | DONE | new `ai-assisted-development/references/graph-first-codebase-comprehension.md` (104 lines); one routing bullet in SKILL.md (167 lines ≤ 170); fixture | Fixture rank 2 (top-3); `install graphify` = 0; P06 disposition stated |
| T14 GR-07 | DONE | `implementation-status-auditor/references/drill-down-templates.md` | Evidence column; three worked tag rows; `full commit` = 3 |
| T15 GR-06 | DONE | `engine-control-plane/SKILL.md` (175 lines ≤ 180) | Both properties with Graphify attribution. **Review:** `hooks/hooks.json` registers only `destructive-bash-gate.js` (PreToolUse/Bash). It is a safety gate: it denies on every attempt, fails closed on missing input, and has an administrator override only. The advisory properties do not apply; no hook change |
| T16 UA-02 | DONE | `doc-architect/references/code-tour.md` (179 lines ≤ 220) | "Topology-ordered tour" section; bands mapped onto the persona budgets; attribution |
| T17 UA-03 | DONE | new `doc-architect/scripts/validate_tour.py`; `tests/fixtures/tours/` (valid + 4 failing tours, a 3-file synthetic project); new `tests/test_validate_tour.py` | `valid.tour` exit 0. The failing tours each exit 1 with a distinct code: `tour/missing-file`, `tour/line-out-of-range`, `tour/unanchored-first-step`, `tour/absent-at-ref` (the last in a throwaway repository with tag `fixture-base`). 11 tests passed. The budget table is test-pinned to `code-tour.md` |
| T18 UA-04 | DONE | `doc-architect/SKILL.md` | `untrusted` = 1; contract gate unchanged (0 errors) |
| T19 UA-05 | DONE | `doc-architect/references/doc-maintenance-after-change.md` | Class column in the existing map; four classes each mapped to named documents; pathspec example; `generated_from_commit`; no second table |
| T20 GR-08 | DONE: pilot **KEEP** | new `ai-assisted-development/scripts/php_mysql_map.py`; `tests/fixtures/php-mysql-map/` (5 controllers, 8 tables, 1 procedure); new `tests/test_php_mysql_map.py` | See the pilot section below |
| T21 AR-10 | DONE | new `system-architecture-design/references/architecture-as-code.md` (109 lines); SKILL.md link; cross-link in `practical-architecture-knowledge.md` | Five C4 claims, each citing c4model.com with access date 29 Sep 2026 (read with WebFetch; the research engine's WebFetch verification route was followed directly rather than a full research wave). Guardrails pass |
| T22 AR-11 | DONE | new `system-architecture-design/scripts/verify_diagram_evidence.py`; new `tests/test_verify_diagram_evidence.py` | 15 tests passed. CLI on a scratch repository: valid exit 0. The bad model gives `evidence/line-out-of-range`, `evidence/path-escape` and `evidence/missing-at-revision`, exit 1. A short SHA gives `evidence/revision-not-full`, exit 1 |
| T23 UX-12 | DONE | new `ai-rag-patterns/references/curated-corpus-worked-example.md` (107 lines), linked from SKILL.md | Links the BM25 text in `production-rag.md`; attribution names the harness design only |
| T24 IM-15 | **DEFERRED** (hand-off) | none | Gated on M10-09 IM-01; the detector command does not exist yet. Hand back to M10-09. Not faked |
| T25 PT-11 | **NOT_ASSESSED / DEFERRED** | none | The reach test needs a live Task-spawned subagent model run, excluded by the zero-spend rule. No hook was added, so there is no runtime-configuration change |
| T26 | DONE | new `docs/updates/2026-09-29-m10-06-methodology-and-comprehension.md`; `CHANGELOG.md`; new `docs/source-registers/m10-06-third-party-attributions.md` (attribution index + C4 source record) | README checked against AGENTS.md "Documentation Updates": no stale fact (count still 167), so it is unchanged |

## GR-08 pilot (read-only on `C:\wamp64\www\Garage`, named by Peter)

**Read-only proof.** `git status --porcelain | sha256sum` gave `60500b0e…612604` both before and after every run. The script reads only `*.php`, `*.sql` and `composer.json`, and `.env` or credential files are never opened. The pilot ran in place, read-only as the brief directs, rather than on a disposable copy.

**Run.**
- 86 file-routed endpoints (`public/api/*.php`), 132 known tables and 347 stored procedures parsed.
- Edges: 459 EXTRACTED, 0 INFERRED and 0 AMBIGUOUS.
- Runtime is about 6 s.
- Output files: `GR-08-garage-pilot-map.txt`/`.json` and `garage-table-question.txt` were moved by the orchestrator to a private folder outside this repository (`Documents\my-10-kaizen-private\GR-08-garage\`); they map a client codebase and are not published.
- Tuning made during the pilot:
  - union of procedure redefinitions across files;
  - `PREPARE`-built SQL tagged INFERRED;
  - bootstrap and config treated as cross-cutting.

**Hand check of 10 routes.** Each was read in the endpoint source. Procedure bodies were checked with `handcheck.sh`, which greps every definition site independently of the script.

| Route | Tables in source | Map | Result |
|---|---|---|---|
| appointment_types | appointment_types | same | correct (exact) |
| banks | banks | banks + audit_trails¹ | correct (recall) |
| chart_of_accounts | chart_of_accounts, account_types, tax_codes | same + audit_trails¹ | correct (recall) |
| clients_linkable | clients, users | same | correct (exact) |
| departments | departments | same | correct (exact) |
| email_template_get | email_templates | same | correct (exact) |
| leave-types | leave_types | same + audit_trails¹ | correct (recall) |
| roles | roles (`sp_get_all_roles` fallback is undefined in the SQL files) | roles | correct (exact) |
| tax_codes | tax_codes, tax_rates, chart_of_accounts, users, tax_transactions, journal_transactions | same + audit_trails¹ | correct (recall) |
| vehicle_makes | vehicle_makes | same | correct (exact) |

¹ `audit_trails` is reached through `RequirePermission` → `PermissionChecker.php:84` `sp_log_audit`, which logs a permission denial. That is a real write path, but it is cross-cutting.

**Score:**
- 10/10 routes recover every table (the phase criterion is ≥ 8/10);
- 6/10 are exact;
- 4/10 carry the audit edge, reported with its evidence path.

**Grep-incomplete question (`garage-table-question.txt`):**
- "What touches `tax_transactions`?" The map returns `public/api/tax_codes.php`, via `sp_get_tax_summary`. `git grep -w tax_transactions -- public src` returns nothing.
- "What touches `journal_reversals`?" The map returns `journal_entries.php` and `payroll_run.php`. Grep finds only `src/Service/JournalEntryService.php`.

**Verdict: KEEP** (delegated).

**Synthetic fixture:**
- all 10 route→table edges are reported and tagged EXTRACTED;
- tests also cover INFERRED (concatenated name), AMBIGUOUS (variable table), read-only behaviour, determinism and the `--table` query.

Runs under PowerShell 5.1.26100 (`--table ledger_entries`, exit 0) and Git Bash.

**Limitations recorded:**
- Laravel routes map at controller-file granularity, not method granularity.
- Middleware edges appear unless they are excluded (`--exclude-dir`, shared-file threshold used only when there are 20 or more routes).
- Undefined procedures are silent.

**Privacy note for the orchestrator:** the pilot map lists Garage's route and table names (no secrets). If this evidence folder is published, consider keeping only the hand-check table and removing `GR-08-garage-pilot-map.*`.

## Verification after the phase (`verify-after.txt`, `grep-matrix.txt`)

| # | Command | Result |
|---|---|---|
| 1 | SKILL.md count / guardrails | 167 / "167 active", 0 findings (errors 0, warnings 0) |
| 2 | `routing_smoke_test.py` | 187 fixtures (184 + 3). p@1 is 179/187 (95.7 %) against 178/184 (96.7 %) before: one more correct in absolute terms, but the rate fell because two of the new fixtures rank 2. p@3 187/187; 0 failures. The M10-03 floor is not yet set, so the floor comparison is **NOT_ASSESSED** |
| 2b | `--collisions` | 2 pairs, both pre-existing; neither involves a touched skill |
| 3 | `contract_gate.py --all` / `engine_compliance.py --root .` | 161 scanned, 0 errors / 136 of 165 fully compliant (unchanged) |
| 4 | `quick_validate.py` on 15 touched skills | all "Skill is valid." |
| 5 | pytest / hook tests | 187 passed, 3 skipped (rerun after M10-02's commit: same) / 61/61, 7/7. `test-subagent-doctrine-digest.js`: N/A (no hook) |
| 6 | control plane / manifest | PASS / "plugin.json is current — 165 skills" |
| 7 | `validate_benchmark_fixtures.py` | PASS, `SPECIFIED_NOT_EXECUTED` (PS02 not validated by the tool until M10-04-T05) |
| 8 | `validate_tour.py tests/fixtures/tours/valid.tour` / `verify_diagram_evidence.py` | PASS exit 0 / PASS exit 0 on the scratch fixture repository; failing cases as in T22 |
| 9 | Grep matrix (17 items) | all ≥ 1 |
| 10 | `validate-no-book-extractions.py` | 0 findings. The runtime budget `--report-only` was not run: dev description characters changed by +45 for `git-collaboration-workflow` only (T08 deviation) |

## Open items for the orchestrator

1. **Ratification by Peter:** T01, T02, T05 (the `tdd-guide.md` agent wording), T09, T10, T11, and the **T08 description edit**. That edit is the only description change and was needed to meet the T08 top-3 acceptance.
2. **M10-04-T05** must extend `validate_benchmark_fixtures.py` for `pressure_scenarios`. PS02 already exists in the array, so M10-04 should add PS01 alongside it, not replace the array.
3. **M10-09** must hand T24 back. **M10-05** executes PS02, and a paid or live run is needed for the PT-11 reach test.
4. **Pre-existing debt not in scope:** about 420 broken relative tokens remain inside old deep-dive references. For example, `skill-deep-dive.md` files still say `references/x.md` relative to themselves.
5. The Garage pilot output is sensitive if the evidence folder is published (see the privacy note).
