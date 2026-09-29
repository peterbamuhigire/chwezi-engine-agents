# M10-11 executor evidence: website truthful gates, minimalism and intake

- Executor: Claude agent (M10-11 scope, website-skills plus the listed chwezi-engine-agents files), 29 Sep 2026
- Phase file: `my-10-kaizen/03-phases/M10-11-website-truthful-gates-minimalism-and-intake.md`
- Pre-existing state at start: website-skills worktree clean at `3c9fdca`; design-system-skills clean at `3fe84a6` (M10-09 detector); chwezi-engine-agents had other executors' edits (`scripts/validate-contracts.py`, untracked M10-12/M10-05 files). During the run another executor (M10-12) edited website `AGENTS.md` and chwezi-engine-agents `AGENTS.md`, `CHANGELOG.md`, `README.md`, `validate.yml`, `mcp-server/*`, `core/instructions/*`, `evals/cases/065-076` and a `plugin_exclusions` row in `catalog/shared-assets.yaml`. None of those are mine.
- Zero spend: no model runs. The DRE evidence pass for T12 used free web search and fetch only.
- Decisions taken under delegated authority are marked "decided by orchestrator under Peter's delegated authority, 29 Sep 2026" and still need Peter's ratification before merge (phase §9): the exit-code contract, the three "automatic block" downgrades, the Gate 3 wording and the bounded/architectural rule, the "Optional plugins" wording, and the sector table.

## Task status

| Task | Status | One line |
|---|---|---|
| T01 IM-03 vendor | DONE | 20 files vendored from design `3fe84a6` with `VENDOR.json`; `check-vendored-detector.py` (hash plus sibling comparison, `--sync-from`); byte-registered in `shared-assets.yaml` |
| T02 IM-03 wrapper | DONE | `slop-scan.sh` + `slop-scan-run.mjs` wrap the detector; exit 0/1/5; `slop.json` canonical, `slop-scan.md` rendered |
| T03 IM-03 pack | DONE_WITH_LIMITATIONS | 20-rule pack; validated by `node scripts/validate-slop-pack.mjs`; the literal `cli.mjs --validate-registry --extra-rules` command cannot pass on a vendored copy (see limitations) |
| T04 IM-03 fixtures and docs | DONE | pass/fail `slop-dist`, `slop` gate case, `slop-rules.md` table with rule IDs, severities and evidence modes; families 4, 5 and 10 relabelled `human_review` |
| T05 waivers | DONE | exam item A25a; waiver section in `slop-rules.md` |
| T06 SP-16 intake | DONE | one-question conduct rule; Gate 3 items and rollback; job classification; §4a Journey Review Focus; "Optional plugins" wording in `CLAUDE.md` via the engine manifest |
| T07 PT-10 minimalism | DONE | "Minimalism pass" in `page-builder/SKILL.md` (139 lines) |
| T08 PT-10 fixture check | DONE | `dependency_minimalism` in the benchmark; `quality/picker-libraries.json`; pass and fail fixtures |
| T09 AO-16 | DONE | deploy description, Quick/Deep section, routing fixture; oracle 025 unpinned and passing |
| T10 AC-10 | DONE | pre-flight in visual-qa `SKILL.md` and `screenshot-diff-harness.md` (lackeyjb/playwright-skill, MIT, commit dd47a6a) |
| T11 GR-12 | DONE | `scripts/content_link_graph.py`, fixture, tests, seo-audit decision row, advisory CI step |
| T12 UX-11 | DONE_WITH_LIMITATIONS | 12-row table, 10 rows with verified or partial evidence, 2 rows `NOT_ASSESSED`; no row comes from Peter's client project records (none exist yet for these sectors) |
| T13 visitor mode | DONE | optional `pages[].visitor_mode` in the schema and brief template; the wrapper runs `--mode` per declared page; `tests/test_project_artifacts.py` |
| Hand-off: liquid glass | DONE | `liquid-glass-effects.md` rewritten as a no-ship doctrine page; three inbound references corrected |
| Hand-off: legacy-guidance | DONE | DM Sans and other banned examples removed; bounce curve replaced |
| Hand-off: slop-scan header claims | DONE | header rewritten; it no longer claims to read `banned-patterns.md` directly or declares unused codes |

## Commands and results (website-skills unless stated)

| Command | Result |
|---|---|
| `python -X utf8 scripts/validate-skill-contracts.py --baseline quality/skill-contract-baseline.json` | 62 active skills, zero debt |
| `python -X utf8 scripts/routing-smoke-test.py --min-rank1 92 --lint-fixtures` | before: 36/36 top-3, p@1 94.4%; after: 37/37 top-3, p@1 35/37 94.6%, owned negatives 21/21, lint 0 |
| `python -X utf8 scripts/validate-skill-registry.py` | registry valid: 62 skills |
| `python -X utf8 scripts/validate-search-doctrine.py` | PASS |
| `python -X utf8 scripts/check-vendored-detector.py` | manifest PASS (20 files, source `3fe84a6`), source comparison PASS |
| tamper test (pytest, one byte in `lib/util.mjs`) | exit 1, names `util.mjs` |
| `bash scripts/slop-scan.sh tests/gates/pass/slop-dist` | exit 0 (block 0, warning 0, advisory 0) |
| `bash scripts/slop-scan.sh tests/gates/fail/slop-dist` | exit 1 (block 9, warning 2, advisory 3) |
| `bash scripts/slop-scan.sh does-not-exist` | exit 5, `NOT_ASSESSED` report |
| tampered vendored registry (pytest) | slop-scan exit 5, reason names the tampered file |
| `node scripts/validate-slop-pack.mjs` | PASS: 20 pack rules against 49 registry rules |
| `node scripts/vendor/chwezi-slop/cli.mjs --validate-registry --extra-rules quality/slop-rules.website.json` | exit 1: fixtures and doctrine files of the design engine are not vendored (expected); the same command from the design checkout: PASS 49 rules |
| `python -X utf8 scripts/website_fixture_benchmark.py --fixture fixtures/website-native-controls-pass` | exit 0, `dependency_minimalism: PASS` |
| `... --fixture fixtures/website-native-controls-fail` | exit 1, `dependency_minimalism: FAIL` (flatpickr via script, link and package.json) |
| `python -X utf8 scripts/website_fixture_benchmark.py` | website-kaizen PASS |
| `python -X utf8 scripts/content_link_graph.py fixtures/website-link-graph` (twice) | exit 1; 1 orphan, 1 broken link, 1 missing anchor; both runs SHA-256 `3bdcf611734add8d95e7379e69205f93efad381e22c8622f8d958463437f5b95` |
| `... fixtures/website-kaizen` | exit 0 |
| `python -X utf8 -m pytest -q` | 131 passed (90 before) |
| `node hooks/test-*.js` (4 files) | all exit 0 |
| `grep -rn "palette-check\|reports/visual/slop-scan.json" skills scripts` | no output (vendored files excluded; they contain neither) |
| `python -X utf8 scripts/source_ingestion_guardrail.py --root .` | findings 0 |
| `python -X utf8 scripts/drift_check.py --root . --reports-dir <scratch> --as-of 2026-09-29` | PASS, 586 Markdown files |
| chwezi-engine-agents: `python -X utf8 scripts/render_host_files.py --check --workspace-root C:\wamp64\www` | exit 0, 12 repositories, findings 0; a one-byte tamper of the vendored `util.mjs` produced `shared-asset-byte-drift` (then restored) |
| chwezi-engine-agents: `run-contract-evals.py --route-oracles --workspace-root C:\wamp64\www` | case 025 rank 94 → rank 1 (deploy 0.460, design `performance-as-ux-and-core-web-vitals` 0.401 at rank 2, so design co-activates); gated primary@1 29/38 76.3% → 30/39 76.9%; engine@1 84.6%; co-activate@5 3/4; known defects 4 → 3; 77/77 cases pass |
| chwezi-engine-agents: `validate-routing-baseline.py` | PASS |
| chwezi-engine-agents: `validate-runtime-skill-budget.py --collisions ...` | PASS, undeclared ≥0.75: 0 |
| chwezi-engine-agents: `pytest tests/test_render_host_files.py` | 30 passed |

Tool versions: Node 24.8.0, Python 3.13, Git Bash (Windows 11).

Machine artefacts in this folder: `slop-pass-fixture.json`, `slop-fail-fixture.json`, `VENDOR.json`, `link-graph-fixture.json`.

## Decisions and notes per task

- **T01.** The vendored copy keeps the design engine's relative layout (`tools/slop-detector/`, `hooks/lib/font-matcher.js`, `doctrine/references/ai-slop-banned-fonts.json`) because the detector resolves those paths relative to itself. `scripts/vendor/chwezi-slop/cli.mjs` is a website-owned one-line shim so the phase's command path works. A local `package.json` (`"type": "commonjs"`) stops a client project's `"type": "module"` from breaking the CommonJS font matcher. A `.gitattributes` keeps LF so `registry_sha256` is stable. Hashes are CRLF-normalised, matching the portfolio byte mode. `browser.mjs` is vendored (inert without the client's locked Playwright) because the CLI imports its siblings statically. The banned-font JSON copy was added to the existing `ai-slop-banned-fonts-json` asset (its reason text anticipated this); the other 19 files are new byte assets.
- **T02.** Retired codes recorded in `project-log/decisions/2026-09-29-slop-scan-exit-contract.md`. Detector exit 2 maps to 1; detector exit 1 (operational) maps to 5. Findings are reported dist-relative. Also fixed two pre-existing silent passes: `visual-qa.sh` tested `-x` on a script stored as mode 100644, so the slop step was skipped on Linux; and both `visual-qa.sh` and `design-quality-score.sh` treated a missing slop script as a warning. Both now fail as `NOT_ASSESSED`.
- **T03.** The literal acceptance command cannot pass on a vendored copy: the CLI's `--validate-registry` checks the design engine's fixtures and doctrine anchors (not vendored) and ignores `--extra-rules`. `scripts/validate-slop-pack.mjs` performs the pack-side checks (schema, data-only kinds, id uniqueness, doctrine anchors in this engine, flag and pass fixture per rule, and every "flag" line reported). Three headline patterns listed only in `slop-rules.md` §3 were consolidated into `banned-patterns.md` and the pack. DRE's copy doctrine is cited, not forked.
- **T04.** Downgrades (decided by orchestrator under Peter's delegated authority, 29 Sep 2026; flagged for Peter's review): family 4 low-information hero and family 5 icon overuse (no detector rule), family 10 colour discipline (`design-system-color` is advisory). Every remaining "automatic block" row names the rule its fail fixture proves; `tests/test_slop_scan.py` reads the table.
- **T06.** The heading "Optional plugins (engine gates remain authoritative)" lives in the Claude-only block. Because the bridge contract allows only one `## Claude-only notes` section in `CLAUDE.md`, it is a bold lead-in rather than a heading. It was edited in `.skills-engine/engine-manifest.yaml` `claude_only_block` and in `CLAUDE.md` identically; the bridge check passes. `AGENTS.md` was not touched. `grep -n "Optional plugins" CLAUDE.md AGENTS.md` matches once.
- **T09.** Description (295 characters) keeps "Use when" and contains the phrase "Lighthouse or Core Web Vitals audit of a built site". Case 025's `known_defect: M10-11` line was removed and its fixture note updated; `evals/routing/baseline.json` updated to the measured values (website p@1 94.6, fixtures 37; portfolio primary@1 76.9, engine@1 84.6, gated 39, known defects 3, co-activate 75.0). The regenerated `evals/reports/latest.json` was restored to HEAD content (my runs used `--out` in the scratchpad afterwards).
- **T11.** Owner chosen: `seo-audit` (orphans and crawl reach are SEO findings). Unreachable pages also fail, which is slightly stricter than the phase wording; `404.html` is an automatic entry.
- **T12.** DRE pass: regulator claims checked on live sites on 29 Sep 2026 and graded with `digital-research-engine/skills/source-evaluation` tiers. Corrections found: UMRA's dissolution was approved by Parliament on 6 Nov 2024 (assent unconfirmed); large SACCOs move to Bank of Uganda licensing (deadline reported as 30 Sep 2026); UNABCEC is now UNABSEC. Every regulatory claim carries a recheck date (28 Dec 2026; SACCO 6 Oct 2026). No UUPM row, name or wording is used (grep for `uupm|landing.csv|products.csv`: 0).
- **Hand-offs.** `liquid-glass-effects.md` now states the no-ship boundary, alternatives and the single functional exception; legacy guidance lost its banned-font examples (DM Sans, Nunito Sans, Instrument Serif, Playfair Display, Plus Jakarta Sans, Outfit) and the overshoot curve.

## Open items

1. M10-09 hand-off: the detector CLI's `--validate-registry` ignores `--extra-rules` and needs non-vendored fixtures; a `--pack-only` mode would let the phase's literal command pass.
2. Peter's ratification: exit contract, three downgrades, Gate 3 and job classification, "Optional plugins" wording, sector table (exact-diff review).
3. Re-vendoring is manual: `python -X utf8 scripts/check-vendored-detector.py --sync-from ../design-system-skills`, then update the byte assets only if the file list changes.
4. Recheck the SACCO row after 30 Sep 2026; read the UCC Q2 2026 chart by hand.
5. `legacy-guidance.md` still lists display faces (Clash Display, Satoshi and others) without a human-authority trace; out of this phase's scope.
6. `evals/plugin/*lighthouse-cwv*` prompts (another executor's untracked files) still say "expected to fail until M10-11"; their owner should update the note.
