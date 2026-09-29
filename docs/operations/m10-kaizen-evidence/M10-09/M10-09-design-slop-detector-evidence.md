# M10-09 evidence: design deterministic slop detector, hooks and doctrine refresh

- **Executor:** Claude (Opus 5.5), 29 Sep 2026.
- **Scope:** all tasks of M10-09 in `design-system-skills`. Also the K5 re-audit record in `digital-research-engine`, the one-file Inter fix in `website-skills`, and the Impeccable pointer in the dev currentness register.
- **Git:** no git state changes were made. Every edit is left unstaged for the orchestrator.

## Phase-start state (dirty-worktree discipline)

- `design-system-skills` was clean at phase start (`git status --short` empty). HEAD was `34a5ab2`. Entry precondition E1 was met by `b7e1003`.
- An M10-03 executor worked in the same repository at the same time. The orchestrator committed its work as `3b7c980` during this phase.
  - That commit swept in two of this phase's edits: the Node CI steps in `.github/workflows/skill-engine-quality.yml`, and one body line of `pdf-proposal-and-bankable-document-design/SKILL.md` (Newsreader to Libre Caslon Text). See "Orchestrator attention".
- `digital-research-engine` and `chwezi-dev-engine` already had other executors' changes (routing and benchmark files). None of those files were touched by this phase.

## Environment

| Item | Value |
|---|---|
| Node | v24.8.0 |
| Python | 3.13.7 |
| Registry | `tools/slop-detector/rules/registry.json`, SHA-256 `750eaf523fda9be3de2dd783d793498a035ec7a66c16323cfd89310dafd66cd0`, 49 rules (42 static, 7 browser) |
| Fixtures | 98 flag/pass files for 49 rules, plus the T08 and T09 acceptance fixtures and 6 waiver fixtures |
| Browser tier | Playwright 1.61.1, exact and lockfile-backed, in a scratch consuming project in the session scratchpad (not in any engine repository). Chromium build 1228 was already cached on the host. The install was free, and no browser was downloaded. |

## Decisions taken under delegation

All were decided by the orchestrator under Peter's delegated authority, 29 Sep 2026.

- **Severity ladder (T01):**
  - `block` needs a WCAG criterion, an engine doctrine line or a dated house ruling. The schema enforces this.
  - `warning` needs an engine doctrine line.
  - Rules with only AI-tool evidence are `advisory` and never fail a run.
- **Waiver format (T07):**
  - Location: `.chwezi/slop.json`, or an inline `chwezi-slop-disable[-next-line|-line]` / `-enable` comment.
  - Reason: must read "<who>: <evidence>", matching `^[^:\n]{2,80}: \S.{9,}$`.
  - Agents may grant `value`-scope waivers only.
- **Side stripes (T10):** Option A, the phase file's recommended option.
  - Decorative coloured side stripes wider than 1 px on cards, callouts, alerts and list items are `warning`.
  - Status stripes stay only with a status token plus a text or icon marker and a recorded waiver.
  - Blockquotes, pull quotes, state indicators and neutral grey rules are out of scope.
  - The ruling is written into `doctrine/references/ai-slop-taxonomy.md` with the marker `rule:layout.decorative-side-stripe`.
- **Watchlist (T12, IM-04/UX-14/AC-09):**
  - A face named as an AI default by 2 or more independent AI-tool sources goes to `secondaryBan` with reason `[AI]`, is removed from the baselines and is replaced by a face with a human-authority citation.
  - A face with 1 source goes on the watchlist, with a recheck on 2026-12-29.
  - Independence rule applied: the Impeccable detector list and reflex list count as one source. The Anthropic bundles and the Claude Cookbook count as one source. UUPM counts only when a face appears in 2 or more of its pairings. v0/shadcn defaults were not verified, so they were not counted.
  - The full record, with 18 dated rows, is `design-system-skills/docs/continuous-improvement/slop-doctrine-refresh-2026-10-font-watchlist.md`.
- **K5 re-audit (T14):** retain AS1-AS7 and add the `cli` and `browser` evidence modes. The re-audit was opened on 29 Sep, before the 3 Oct due date, with measured detector evidence, so no `NOT_ASSESSED` deviation line was needed. A dated re-audit log entry was appended to the K5 record.

### T12 face decisions

| Face | Independent sources counted | Grade | Decision |
|---|---|---|---|
| Plus Jakarta Sans | Impeccable, UUPM | moderate | secondary ban [AI] |
| Instrument Sans | Impeccable, Anthropic | moderate | secondary ban [AI] |
| Outfit | Impeccable, UUPM, Anthropic | strong | secondary ban [AI] |
| Playfair Display | Impeccable, UUPM, Anthropic | strong | secondary ban [AI] |
| Crimson Pro | Impeccable, UUPM, Anthropic | strong | secondary ban [AI]; removed from the 01 baselines (replacement Arapey, Eduardo Tunni) |
| Newsreader | Impeccable, Anthropic | moderate | secondary ban [AI]; removed from the 02 baselines (replacement Libre Caslon Text, Impallari Type, a Caslon revival) |
| Cormorant / Cormorant Garamond | Impeccable, UUPM | moderate | secondary ban [AI]; removed from the 02 baselines (replacement Theano Didot, Alexey Kryukov, display only) |
| Lora | Impeccable, Anthropic | moderate | secondary ban [AI] |
| DM Sans | Impeccable, UUPM | moderate | secondary ban [AI] |
| Space Mono | Impeccable, UUPM | moderate | secondary ban [AI]; short labels now use JetBrains Mono |
| Syne, DM Serif Display/Text, Helvetica, Mona Sans, Recoleta, DejaVu Sans | 1 each | weak | watchlist; recheck 2026-12-29 |
| Geist Mono | Impeccable, Anthropic | moderate | `Geist` added to `hardBanFamilyPrefixes` (clarifies the existing ban) |
| Instrument Serif | Impeccable, Anthropic | corroboration | no change (already banned) |

- **Source pins:**
  - Impeccable `114ea1d`
  - UUPM `09170ee`
  - `anthropics/skills` `3337550` (canvas list identical to `fa0fa64`)
  - Claude Cookbook notebook last changed `944b94a`
- **Font folders of newly banned faces (report only, not deleted):**
  - `fonts/01-formal-institutional/crimson-pro/`
  - `fonts/02-editorial-literary/newsreader/`
  - `fonts/02-editorial-literary/cormorant-garamond/`

  Removing each folder needs Peter's confirmation for that operation.

## Per-task status

| Task | Status | Evidence |
|---|---|---|
| T01 registry and schema | DONE | 49 rules, JSON Schema 2020-12 subset validated in-tool. `--validate-registry` exit 0. Every rule has `as_overlay` and a non-empty authority. Block rules carry a standard or house ruling, and the schema rejects them otherwise (test). |
| T02 CLI and libraries | DONE | `cli.mjs` plus `lib/{util,colour,parse-css,parse-html,tailwind,document,checks,drift,waivers,registry,schema,detector,doctrine-consistency,browser-rules,browser}.mjs`. No dependencies. Frozen JSON shape and exit codes 0/2/1. All specified flags present. The fixture run reports every flag rule and no finding in any pass fixture (`fixtures-run.json`, 84 files). Network guard test passes. |
| T03 font-gate gaps | DONE | `hooks/lib/font-matcher.js`, shared by the gate and the detector, covers all five categories. Source Sans quoted-literal false positive removed. `.cjs`/`.mjs` added, plus `--font-*` custom properties and Tailwind `fontFamily` objects. `node hooks/test-banned-font-gate.js`: 45/45, including the four acceptance cases and 9 others. |
| T04 fixtures and Node tests | DONE | `tests/fixtures/slop/**`. Tests: `fixtures`, `mutation` (disabling a rule, and stubbing its check function, each remove the finding), `network-guard`, `registry`, `waivers`, `drift`, `browser`, `doctrine-consistency`. `node --test tools/slop-detector/test/`: 114 pass, 1 skipped (browser acceptance needs `CHWEZI_SLOP_PLAYWRIGHT_PROJECT`), about 7 s on this host. |
| T05 validator, baseline and CI | DONE_WITH_LIMITATIONS | `scan_slop_registry` in `validate_engine.py` checks fixtures, doctrine anchors (heading slug or `rule:` marker) and unique IDs. Floors in `tests/quality-baseline.json`: `slop_rules` 49, `slop_fixtures` 98. `tests/test_slop_registry.py` has 3 tests, including a seeded failure. CI steps: `setup-node@v7` on Node 24 (Node 20 reached end of life on 2026-04-30; v7 is the latest release, checked with `gh api`), the detector suite and all 6 hook tests. **CI run URL: NOT_ASSESSED** (no push from this executor). |
| T06 hooks | DONE | `hooks/slop-immediate.js` (PostToolUse, 5 s) and `hooks/slop-deep-pass.js` (Stop, 30 s) are registered in `hooks/hooks.json`, with a `description` recording the Codex degraded mode. Shared code is in `hooks/lib/slop-hook-common.js`. Tests: immediate 12/12, deep pass 10/10. Cases covered: clean, finding, malformed, disabled by plugin setting, `CHWEZI_SLOP_HOOKS=off`, missing detector, `stop_hook_active`, block-once, de-duplication. Immediate hook median on a 500-line CSS file is 239-261 ms including process start (target 1 s or less). `generate-plugin-manifest --check` passes. |
| T07 waivers | DONE | `lib/waivers.mjs`, template table and gate sentence. Tests: non-conforming inline reason exits 1; agent `file` waiver exits 1; non-conforming config reason exits 1; valid value waiver moves the finding to `waived[]`; disable/enable blocks; `--no-waivers`. |
| T08 browser tier | DONE_WITH_LIMITATIONS | `lib/browser.mjs` (lock rule reimplemented; local-only unless `--allow-remote`; remote requests aborted) and `lib/browser-rules.mjs` (7 rules, 390x844 and 1440x900). With a locked Playwright: `failed-reveal-and-clipped-tooltip.html` fires `content-hidden-at-rest` and `clipped-positioned-child`; `clean.html` fires nothing; all 7 flag/pass pairs behave (`browser-acceptance.json`, `browser-fixtures-run.json`, `browser-test-with-locked-playwright.txt`). Playwright absent: all 7 rules are `not_assessed` and exit is 0 (test). Limitation: CI has no locked Playwright, so the acceptance test is skipped there (never counted as a pass). |
| T09 drift rules | DONE | `lib/drift.mjs` resolves the token source in order: `--tokens`, `.chwezi/slop.json`, `design-tokens.json`, DTCG. Colours match within CIEDE2000 2.0; the implementation is verified against Sharma, Wu & Dalal (2005) pairs 1, 7 and 19. `tests/fixtures/slop-drift/` yields exactly 1 advisory (`design-system-color`) and 1 block (`design-system-font`) (`drift-acceptance.json`, test). |
| T10 side stripes | DONE | Option A. Remediations were made by the fork sub-agent: tint, icon and label, or a 1 px full border (practical-application 154/160, accessibility-contrast 300, 4 sector templates). The healthcare status encodings are kept, with a waiver and a reason line. `node tools/slop-detector/cli.mjs --rule decorative-side-stripe --json skills` gives 0 findings and 2 waived. |
| T11 browser surfaces | DONE | New "Browser surfaces" section in `interface-craft-micro-details/SKILL.md` (217 lines; body only, description untouched). It covers `::selection`, `caret-color`, scrollbars, focus ring (2.4.7, 2.4.11, 1.4.11), `text-underline-offset`, and a cross-reference to `tabular-nums`. The `focus-indicator-removed` rule is registered. `validate_engine` and `routing_smoke_test` pass. |
| T12 doctrine refresh | DONE | Applied under the orchestrator's evidence rule (table above). Markdown, JSON, markers (29, PASS), `font-groups-and-usage.md`, `pairing-principles.md`, `pairing-catalog.md`, the AGENTS.md ban line, font MANIFESTs, skill examples and sector templates (including the older Nunito and Instrument Serif residue), and the website `african-language-pack.md` (Inter removed). |
| T13 doctrine consistency | DONE | `--doctrine-consistency` gives 0 conflicts on the current tree (exit 0) and reports the 3 banned font folders as report-only. Against the pre-refresh baselines (HEAD) with the refreshed ban list it reports 12 conflicts (Crimson Pro, Newsreader, Cormorant, Space Mono) (`doctrine-consistency-pre-refresh-baselines.json`). The Fraunces and IBM Plex residues had already been cleared by `b7e1003`. |
| T14 K5 re-audit | DONE | `digital-research-engine/docs/continuous-improvement/kaizen-impeccable-anti-slop-reaudit-2026-10.md` contains the AS matrix, the detector runs, the true/false-positive review, the 12/12 adapter check and the decision. A re-audit log entry was appended to `kaizen-impeccable-anti-slop-2026-09-03.md`. |
| T15 licence and README | DONE | `THIRD_PARTY_NOTICES.md` (the Impeccable notice as specified) and `tools/slop-detector/README.md` (CLI contract, exit codes, waivers, evidence modes, drift, browser, hooks, vendoring). Every rule citing Impeccable carries `114ea1d` (test). |
| Dev currentness pointer | DONE | The `impeccable-slop-catalog` row in `chwezi-dev-engine/docs/source-registers/skills-engine-currentness-2026-09.json` now points at the 2026-09-29 DRE source record, pinned to commit `114ea1d`, with review due 2026-12-29. DRE `validate_source_currency.py` gives 0 findings, and the row no longer goes overdue on 2026-10-04. |

## Self-scan and false-positive review (value measure)

- **First development self-scan:** 111 findings, mostly false positives. Examples:
  - card parts such as `card-header` read as nested cards;
  - pull quotes and drop caps;
  - an email preheader at 1 px;
  - colour-only transitions and `img { outline: none }` resets;
  - a documented `--font-system` fallback token and neutral tree-guide borders;
  - text typed in capitals, and lead or display-size text;
  - JS hook classes and a baseline-grid debug overlay.

  Each class was fixed in the rule and pinned by a pass fixture where practical.
- **Final design self-scan** (`engine-self-scan.json`, 623 files; `engine-self-scan-wide.json`, 642 files): 0 block, 8 warning, 0 advisory, and 9 waived.
  - All 8 unwaived findings are true positives on review: 2 kickers, a tiny-text finding, a skipped heading, and 4 templates without a reduced-motion path.
  - **False-positive rate: 0 of 8 (0 %), against a target of 5 % or less.**
  - One `block` true positive in the engine's own template (an `animate-bounce` scroll arrow) was remediated.
- **Waivers issued, each with a "<who>: <evidence>" reason:**
  - 2 status-encoding side stripes (healthcare);
  - 6 findings in 2 deliberate before-state counter-examples (the typography audit and the before/after UI example).
- **Cross-engine scans (read-only):**
  - website Kaizen fixture: 1 true positive (cream ground);
  - website `skills/`: 8 true positives against design doctrine, including a `liquid-glass-effects.md` glassmorphism conflict for M10-11;
  - dev `frontend-ux`: 1 true positive (`text-black` paragraph). There are no `examples/` folders, so all 77 files were scanned;
  - browser pass on the website fixture and the Kraal example: 0 findings.

## Commands run (final tree)

The full outputs are in `verification-log.txt`. Every command exited 0.

- **Engine validators:**
  - `python -X utf8 scripts/validate_engine.py --baseline tests/quality-baseline.json`: 101/101 compliant; `slop_rules=49`, `slop_fixtures=98`.
  - `python -X utf8 scripts/routing_smoke_test.py`: precision@1 94 %.
  - `validate_route_existence.py`, `validate_design_catalog.py`, `validate_design_delivery_evidence.py` and `validate_token_example.py` all pass.
  - `python -X utf8 -m pytest -q -p no:cacheprovider`: 108 passed.
- **Hook tests:**
  - `node hooks/test-banned-font-gate.js`: 45/45.
  - `test-token-file-gate`: 10/10.
  - `test-plugin-hook-config`: 7/7.
  - `test-destructive-bash-gate`: 61/61.
  - `test-slop-immediate`: 12/12.
  - `test-slop-deep-pass`: 10/10.
- **Detector:**
  - `node --test tools/slop-detector/test/`: 114 pass, 1 skipped. The skipped test passed separately with a locked Playwright (4/4).
  - `node tools/slop-detector/cli.mjs --validate-registry`: PASS.
  - `--doctrine-consistency`: PASS.
  - The fixture run and the self-scan are saved as JSON files next to this record.
- **Other checks:**
  - `node scripts/generate-plugin-manifest.js --engine . --check`: current.
  - `python -X utf8 chwezi-engine-agents/scripts/validate-rule-markers.py doctrine/references/ai-slop-banned-fonts.md`: PASS, 29 markers.
  - DRE: `validate_machine_error_gate.py` FAILS as committed (a stale `digital-research-skills` path), and PASSES 12/12 with that path corrected in a scratch copy. `validate_engine.py` exit 0; `source_ingestion_guardrail.py` 0 findings; `validate_source_currency.py` on the dev register 0 findings.
  - Dev: `pytest tests/test_all_engine_currentness_policy.py`: 1 passed, 2 skipped.
- **NOT_ASSESSED:**
  - the CI run URL (no push);
  - double-firing with the website `quality-gate.js` when both plugins are installed;
  - a live Claude Code session exercising the new hooks, which were unit-tested with synthesised payloads only;
  - model-executed evaluations (zero-spend rule).

## Open items

1. Stale banned-font lists in shared copies were not edited:
   - `integration/trigger-block.md` and `integration/integration-plan.md`, the canonical design trigger block copied into 11 engines' `AGENTS.md`;
   - `rules/common/core.md`.

   They still list the old secondary-ban set. The orchestrator should decide whether to propagate the change (M10-02 host-file flow).
2. For Peter's re-check: under the same two-source rule, the approved mono faces JetBrains Mono (UUPM and Anthropic) and Fira Code (UUPM and Cookbook) also reach the threshold. No action was taken, because they are outside IM-04/UX-14/AC-09 scope and are the only approved monospace faces (watchlist record §7).
3. DRE fixture `tests/fixtures/machine-error-gate-baseline.json`: change `digital-research-skills` to `digital-research-engine` in the `digital-research` target.
4. Website M10-11: resolve the `liquid-glass-effects.md` conflict and the DM Sans and bounce findings in `legacy-guidance.md`. Also wire `slop-scan.sh` to the frozen CLI and load AS6 as a data pack.
5. Design follow-up: add reduced-motion variants to 4 sector templates.
6. Peter's exact-diff ratification of the doctrine-class items is pending at phase acceptance: the severity ladder, waiver format, side-stripe option, T12 face decisions and K5 decision.
