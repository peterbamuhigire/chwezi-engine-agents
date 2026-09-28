# M10-01 evidence — dev engine (T01–T06)

| Field | Value |
|---|---|
| Phase | M10-01 Stop-the-Line Defects |
| Scope | Tasks T01–T06, `C:\wamp64\www\chwezi-dev-engine` |
| Executor date | 29 Sep 2026 |
| Base commit | `7adc9fc` (clean tree at start) |
| Authority | Peter's approval "Implement the Plan!"; D-M10-01 early push approved; AO-21 empty-directory removal approved. Decisions below marked "decided by orchestrator under Peter's delegated authority, 29 Sep 2026" |
| Git actions | None. All edits are unstaged; the orchestrator commits and pushes |
| Spend | Zero. Only local tools, free `gh` API reads and a no-op `pip install` of the pinned CI requirements |
| Not touched | `AGENTS.md` (another executor owns its design trigger block); the tracked orphan folders that contain files (M10-06) |

## Remote CI failure causes (confirmed with `gh`, 29 Sep 2026)

`gh run list --workflow skill-guardrails.yml --branch main --limit 15`: the last green run is `35496487888` (2026-09-20T07:17Z). Every run since has failed. There are **13** consecutive failures, not the 12 in the baseline, because `7adc9fc` (28 Sep 23:10Z) added one.

| Run | Date | Failing step and cause (from `gh run view <id> --log-failed`) |
|---|---|---|
| 36496589385 | 2026-09-28 | pytest: `test_current_active_count_matches_filesystem_and_documented_surfaces` and `test_count_surface_mutation_is_rejected` fail with `{'README.md': [None]}`. The 2026-09-28 README refresh (`204e321`) removed the count row. Result: 2 failed, 127 passed, 3 skipped |
| 36298521814 | 2026-09-27 | contract gate: `council`, `github-ops` and `santa-method` report "missing ## Evidence Produced section" (161 scanned, 3 errors) |

## T01 — Restore the README count surface — DONE

- **Change:** `README.md` now has a small table at the end of the Skills section containing `| Active \`SKILL.md\` files | 167 |` and `| Guardrail maximum | 200 |`. A sentence above the table says it is a checked count surface. The test was not weakened.
- **Files changed:** `C:\wamp64\www\chwezi-dev-engine\README.md`
- **Verification:** `python -X utf8 -m pytest tests -q -p no:cacheprovider` → **132 passed, 3 skipped, 0 failed**, exit 0. This includes both count-surface tests and the new alias-count test from T05.

## T02 — Evidence Produced sections — DONE (ratification pending)

- **Change:**
  - **council:** added a `## Evidence Produced` table.
    - Release evidence: the dated council decision record under the Persistence Rule.
    - Correctness: the in-context position fixed before the external voices are read.
    - A note under the table: a verdict that changes nothing is not persisted.
  - **github-ops:** added a table with four rows.
    - Operability: a CI-diagnosis note with the run ID, failing step, first error and whether the failure is real or flaky.
    - Correctness: an issue-triage log.
    - Release evidence: a release record.
    - Security: an alert-disposition log.
  - **santa-method:** added a table with three rows.
    - Correctness: the two independent reviewer verdicts in JSON.
    - Release evidence: the reconciliation record, ending in SHIP or escalation.
    - Correctness: a batch-sample record.
- **Why the structure also changed:** the contract gate requires the section to sit inside the `<!-- dual-compat-start/end -->` block, and `council` and `santa-method` had no block. Both skills are now wrapped in the block. To avoid duplicate headings, existing headings were renamed to the portable names rather than added a second time:
  - "When to Use" / "When to Activate" became "Use When";
  - "When NOT to Use" became "Do Not Use When";
  - "Architecture" became "Workflow";
  - "Failure Modes and Mitigations" became "Anti-Patterns";
  - "Related Skills" / "Integration with This Engine" became "References".
- **Short sections added:** "Required Inputs", "Quality Standards" (including a degraded mode) and "Outputs" were added to both skills. They restate the skills' own workflow and add no new method. `council` and `santa-method` stay separate skills (the K17 decision stands). Descriptions are unchanged, so routing is unaffected.
- **Files changed (line counts, all ≤ 500):**
  - `C:\wamp64\www\chwezi-dev-engine\skills\sdlc-meta\council\SKILL.md` (202 lines)
  - `C:\wamp64\www\chwezi-dev-engine\skills\sdlc-meta\github-ops\SKILL.md` (159)
  - `C:\wamp64\www\chwezi-dev-engine\skills\sdlc-meta\santa-method\SKILL.md` (206)
  - `C:\wamp64\www\chwezi-dev-engine\.github\workflows\skill-guardrails.yml`. The comment "Missing evidence sections remain warnings" was replaced by "Enforcing: a missing or malformed ## Evidence Produced section in any active skill … fails the build". The step is renamed "Validate evidence declarations".
- **Verification:**
  - `python -X utf8 skills/sdlc-meta/skill-writing/scripts/contract_gate.py --all` → `scanned 161 | 0 errors | 0 warnings | 6 exempt`, exit 0.
  - `python -X utf8 scripts/skill_catalog_guardrails.py` → 167 active, 0 findings, exit 0.
  - `quick_validate.py`: `github-ops` and `santa-method` are valid. `council` still fails on one pre-existing item: its description does not start with "Use when". Changing it was left out of scope because it would alter routing signals.
  - `engine_compliance.py`: `portable_sections` and `output_contract` now pass for these skills. The remaining gaps (input, capability and degraded-mode contracts, decision rules, five anti-patterns) belong to the M10-04 authoring convergence.
- **Ratification:** T02 is doctrine text. Peter's ratification is required under §9 of the phase file.

## T03 — CI workflow Node hook-test step — DONE

- **Change:** in `.github/workflows/skill-guardrails.yml`:
  - `actions/checkout@v4` → `@v7`, `actions/setup-python@v5` → `@v7`;
  - new `actions/setup-node@v7` with `node-version: "24"`;
  - new step "Test plugin hooks": `node hooks/test-destructive-bash-gate.js && node hooks/test-plugin-hook-config.js`. It sits **before** the evidence (contract-gate) step, as T03 requires;
  - the header comment is updated.
- **Action majors checked at execution** (`gh api repos/actions/<name>/releases/latest` and `action.yml` read at the `v7` tag):
  - checkout v7.0.1 (2026-07-20), `node24`;
  - setup-python v7.0.0 (2026-07-20), `node24`;
  - setup-node v7.0.0 (2026-07-14), `node24`.

  The v7 release notes list no breaking change that affects this workflow. The one removed setup-python input, `pip-install`, is not used here.
- **Files changed:** `C:\wamp64\www\chwezi-dev-engine\.github\workflows\skill-guardrails.yml`
- **Verification:**
  - `actionlint .github/workflows/skill-guardrails.yml` → exit 0, no findings;
  - PyYAML parse → 11 steps, "Test plugin hooks" before "Validate evidence declarations";
  - local hook tests: 61/61 and 7/7 passed, exit 0.
  - The destructive-gate test calls `git init` and `git config`; `git` is present on `ubuntu-latest`. Its runtime behaviour on Linux is **NOT_ASSESSED** until the remote run.
- **Decision (delegated):** Node 24 was chosen as the LTS line at or above the required Node 22. Decided by orchestrator under Peter's delegated authority, 29 Sep 2026.

## T04 — Whole CI sequence locally — DONE locally; remote NOT_ASSESSED (awaiting push)

The steps were run in the order of the workflow file. The T04 task text lists hook tests last, but T03 requires them before the contract gate, so the workflow order was followed. The full transcript is in `M10-01-dev-engine-ci-local-transcript.txt` in this folder.

| # | Step | Command | Result |
|---|---|---|---|
| 0 | Install dependencies | `python -m pip install --requirement requirements-ci.txt` | Already satisfied (pytest 9.0.3, PyYAML 6.0.2) |
| 1 | Guardrails (enforcing) | `python -X utf8 scripts/skill_catalog_guardrails.py` | exit 0; 167 active; `findings: 0 (errors: 0, warnings: 0)` |
| 2 | Source-ingestion unittest | `python -X utf8 -m unittest tests/test_skill_catalog_guardrails.py` | exit 0; 10 tests OK (8 existing + 2 new) |
| 3 | pytest | `python -X utf8 -m pytest tests -q -p no:cacheprovider` | exit 0; 132 passed, 3 skipped |
| 4 | Routing smoke | `python -X utf8 scripts/routing_smoke_test.py` | exit 0; 184 fixtures, p@1 178/184 (96 %), p@3 184/184, 0 findings |
| 5 | Control plane | `python -X utf8 scripts/validate_engine_control_plane.py` | exit 0; "PASS: control-plane registry is valid" |
| 6 | Hook tests | `node hooks/test-destructive-bash-gate.js && node hooks/test-plugin-hook-config.js` | exit 0; 61/61, 7/7 |
| 7 | Contract gate | `python -X utf8 skills/sdlc-meta/skill-writing/scripts/contract_gate.py --all` | exit 0; 161 scanned, 0 errors |

Extra checks:
- `node scripts/generate-plugin-manifest.js --engine . --check` → "plugin.json is current — 165 skills".
- `git diff --check` → clean.

Limitation: the local host runs Python 3.13.7 and Node v24.8.0 on Windows, while CI runs Python 3.12 and Node 24 on Ubuntu.

**Remote:** `gh run list --workflow skill-guardrails.yml --branch main --limit 3 --json conclusion,headSha,createdAt` → the latest run is `failure` at `7adc9fc`, which predates these edits. **NOT_ASSESSED (awaiting push)**. The orchestrator pushes under D-M10-01 and must then record `success` here. Until a green remote run is recorded, `AGENTS.md`'s claim that the gate "runs in CI on every push and PR" is not yet shown to pass.

## T05 — Rename residues and alias count — DONE

- **Changes:**
  - root `SKILL.md`: H1 is now "Chwezi Dev Engine Router". Line 10 reads "Chwezi Dev Engine July 2026 upgrade baseline (engine formerly named Skills Web Dev; folder renamed 2026-09-20)".
  - `.skills-engine/engine-manifest.yaml`: `display_name: Chwezi Dev Engine`.
  - `prompts/full-kaizen-operation.md`: the title and line 3 are renamed.
  - `docs/skill-routing-index.md`: "Inactive alias files retained" 47 → **76** (the `ALIAS.md` count on disk). The table lead-in now says the test suite checks both counts.
  - `REPLICATE-ROUTING.md`: the body is replaced by a short superseded stub. It points to the global routing table, to `chwezi-engine-agents` `docs/distribution.md` and `docs/adapters/`, and to the README plugin install. The history stays in Git.
  - `tests/test_engine_control_plane.py`: a new test, `test_routing_index_alias_count_matches_alias_files`, asserts the index count equals the `ALIAS.md` count under `skills/` and `00-meta-initialization/`, and that a mutated count is rejected.
- **Files changed:**
  - `C:\wamp64\www\chwezi-dev-engine\SKILL.md`
  - `C:\wamp64\www\chwezi-dev-engine\.skills-engine\engine-manifest.yaml`
  - `C:\wamp64\www\chwezi-dev-engine\prompts\full-kaizen-operation.md`
  - `C:\wamp64\www\chwezi-dev-engine\docs\skill-routing-index.md`
  - `C:\wamp64\www\chwezi-dev-engine\REPLICATE-ROUTING.md`
  - `C:\wamp64\www\chwezi-dev-engine\tests\test_engine_control_plane.py`
- **Verification:**
  - `Select-String -Path SKILL.md,.skills-engine/engine-manifest.yaml,prompts/full-kaizen-operation.md -Pattern 'Skills Web Dev'` → exactly one hit, `SKILL.md:10` (the "formerly" line).
  - pytest: 132 passed, including the new alias-count test.
  - No file in `chwezi-engine-agents` (yaml, json, py or ts) references "Skills Web Dev".
- **Open item:** `docs/engine-upgrade-july-2026/10-appendix-file-inventory.md` still lists `REPLICATE-ROUTING.md`. It is a historical inventory and was left unchanged.

## T06 — Empty-directory check and removal — DONE

- **Check added:** `scripts/skill_catalog_guardrails.py` gains `check_empty_directories()`.
  - It emits an `empty-directory` **warning** for every file-less directory under the active roots. Only the topmost such directory is reported, and hidden paths are skipped.
  - The exit code now counts **errors only**. Before this change every finding had error severity, so existing behaviour is unchanged.
  - The summary line is now `findings: N (errors: E, warnings: W)`.
  - Two unit tests were added to `tests/test_skill_catalog_guardrails.py`: a synthetic empty directory produces the warning, and a directory holding files does not.
- **Temp-copy proof:**
  - A copy of `scripts/`, `skills/`, `00-meta-initialization/`, `doctrine/` and `docs/skill-aliases.yml` was made in the executor scratchpad, with the extra directory `skills/ai/synthetic-empty-skill`.
  - The run produced `findings: 1 (errors: 0, warnings: 1)` and `[WARNING] empty-directory: skills\ai\synthetic-empty-skill …`, exit 0.
  - Pre-existing limitation, not fixed: `--root` pointing outside the repository crashes in `check_alias_integrity` (`relative_to(REPO_ROOT)`). The proof therefore used a temp copy.
- **Removal:**
  - Before removal, `(Get-ChildItem skills,00-meta-initialization -Recurse -Directory -Force | ? { -not (Get-ChildItem $_.FullName -Force) }).Count` → **50**. All 50 were leaf directories and none was tracked by Git (`git ls-files -- <path>` → 0 for each).
  - Each was removed one at a time with `cmd /c rmdir <path>`, which refuses a non-empty directory. No recursive delete was used.
  - After removal the same count is **0**, and the guardrails report 0 warnings.
- **Confirmation:** the approval to remove empty directories (AO-21) comes from the executor brief. The phase file asks for per-operation confirmation of the listed paths. It was taken as the plan's recommended option under Peter's standing approval: decided by orchestrator under Peter's delegated authority, 29 Sep 2026. Peter's ratification of the deletion list remains listed in §9.
- **Also changed:** `docs/catalog-cleanup/empty-directory-disposition.md` has a dated 2026-09-29 section. It records the new warning and the removal, notes that the 8 July paths no longer exist, and records that the `references/`- and `templates/`-only orphans were left for M10-06.
- **Files changed:**
  - `C:\wamp64\www\chwezi-dev-engine\scripts\skill_catalog_guardrails.py`
  - `C:\wamp64\www\chwezi-dev-engine\tests\test_skill_catalog_guardrails.py`
  - `C:\wamp64\www\chwezi-dev-engine\docs\catalog-cleanup\empty-directory-disposition.md`
- **Out of scope, untouched:** tracked orphan directories that hold files, such as `skills/sdlc-meta/plan-implementation/` (M10-06). `skills/sdlc-meta/spec-architect/` was one of the 50 and **was empty**, so it was removed. M10-06 SP-03 will create its alias there afresh if it is still wanted.

### Paths removed (50)

| Path | Tracked files | Result |
|---|---:|---|
| `skills/ai/coding-agent-optimization/assets` | 0 | removed with rmdir; path absent afterwards |
| `skills/android/android-ai-ml` | 0 | removed with rmdir; path absent afterwards |
| `skills/android/android-biometric-login` | 0 | removed with rmdir; path absent afterwards |
| `skills/android/android-pdf-export` | 0 | removed with rmdir; path absent afterwards |
| `skills/android/android-room` | 0 | removed with rmdir; path absent afterwards |
| `skills/android/jetpack-compose-ui` | 0 | removed with rmdir; path absent afterwards |
| `skills/architecture/api-testing-verification` | 0 | removed with rmdir; path absent afterwards |
| `skills/architecture/event-driven-architecture` | 0 | removed with rmdir; path absent afterwards |
| `skills/architecture/microservices-fundamentals` | 0 | removed with rmdir; path absent afterwards |
| `skills/architecture/microservices-resilience` | 0 | removed with rmdir; path absent afterwards |
| `skills/architecture/realtime-systems` | 0 | removed with rmdir; path absent afterwards |
| `skills/backend-databases/postgresql-advanced-sql` | 0 | removed with rmdir; path absent afterwards |
| `skills/backend-databases/postgresql-fundamentals` | 0 | removed with rmdir; path absent afterwards |
| `skills/backend-databases/postgresql-performance` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-app-security` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-architecture-advanced` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-at-scale` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-biometric-login` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-bluetooth-printing` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-debugging-mastery` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-networking-advanced` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-pdf-export` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-production-patterns` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-project-setup` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-push-notifications` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-rbac` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-stability-solutions` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-swift-design-patterns` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-swift-recipes` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-swiftdata` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-tdd` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/ios-uikit-advanced` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/swiftui-design` | 0 | removed with rmdir; path absent afterwards |
| `skills/ios/swiftui-pro-patterns` | 0 | removed with rmdir; path absent afterwards |
| `skills/languages/javascript-advanced` | 0 | removed with rmdir; path absent afterwards |
| `skills/languages/javascript-php-integration` | 0 | removed with rmdir; path absent afterwards |
| `skills/languages/php-vs-nextjs` | 0 | removed with rmdir; path absent afterwards |
| `skills/mobile-cross/app-store-review` | 0 | removed with rmdir; path absent afterwards |
| `skills/mobile-cross/google-play-store-review` | 0 | removed with rmdir; path absent afterwards |
| `skills/mobile-cross/kmp-compose-multiplatform` | 0 | removed with rmdir; path absent afterwards |
| `skills/mobile-cross/kmp-tdd` | 0 | removed with rmdir; path absent afterwards |
| `skills/mobile-cross/mobile-custom-icons` | 0 | removed with rmdir; path absent afterwards |
| `skills/mobile-cross/mobile-rbac` | 0 | removed with rmdir; path absent afterwards |
| `skills/mobile-cross/mobile-report-tables` | 0 | removed with rmdir; path absent afterwards |
| `skills/mobile-cross/mobile-saas-planning` | 0 | removed with rmdir; path absent afterwards |
| `skills/sdlc-meta/sdlc-maintenance` | 0 | removed with rmdir; path absent afterwards |
| `skills/sdlc-meta/sdlc-post-deployment` | 0 | removed with rmdir; path absent afterwards |
| `skills/sdlc-meta/spec-architect` | 0 | removed with rmdir; path absent afterwards |
| `skills/sdlc-meta/update-claude-documentation/references` | 0 | removed with rmdir; path absent afterwards |
| `skills/security/graphql-security` | 0 | removed with rmdir; path absent afterwards |

## Complete file list (chwezi-dev-engine, all unstaged modifications; no additions)

- `C:\wamp64\www\chwezi-dev-engine\.github\workflows\skill-guardrails.yml`
- `C:\wamp64\www\chwezi-dev-engine\.skills-engine\engine-manifest.yaml`
- `C:\wamp64\www\chwezi-dev-engine\README.md`
- `C:\wamp64\www\chwezi-dev-engine\REPLICATE-ROUTING.md`
- `C:\wamp64\www\chwezi-dev-engine\SKILL.md`
- `C:\wamp64\www\chwezi-dev-engine\docs\catalog-cleanup\empty-directory-disposition.md`
- `C:\wamp64\www\chwezi-dev-engine\docs\skill-routing-index.md`
- `C:\wamp64\www\chwezi-dev-engine\prompts\full-kaizen-operation.md`
- `C:\wamp64\www\chwezi-dev-engine\scripts\skill_catalog_guardrails.py`
- `C:\wamp64\www\chwezi-dev-engine\skills\sdlc-meta\council\SKILL.md`
- `C:\wamp64\www\chwezi-dev-engine\skills\sdlc-meta\github-ops\SKILL.md`
- `C:\wamp64\www\chwezi-dev-engine\skills\sdlc-meta\santa-method\SKILL.md`
- `C:\wamp64\www\chwezi-dev-engine\tests\test_engine_control_plane.py`
- `C:\wamp64\www\chwezi-dev-engine\tests\test_skill_catalog_guardrails.py`

The 50 empty directories were never in Git, so their removal produces no Git change.

## Open items

1. **T04 remote run:** NOT_ASSESSED (awaiting push). After the push, record `gh run list --workflow skill-guardrails.yml --branch main --limit 1 --json conclusion` → `success`.
2. **Ratification by Peter:** T02 (doctrine text in three skills) and T06 (deletion list) are required under §9.
3. **`council` description:** it does not start with "Use when" (`quick_validate.py`). Hand to M10-04 with the other compliance gaps.
4. **Guardrail `--root` outside the repository:** it crashes in `check_alias_integrity`. This is a minor pre-existing defect.
5. **Historical inventory:** `docs/engine-upgrade-july-2026/10-appendix-file-inventory.md` still names `REPLICATE-ROUTING.md`. It is left as history.
