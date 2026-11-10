# Changelog

## Unreleased - Model classes and token economy (10 November 2026)

- New `docs/operations/model-classes-and-token-economy-2026-11.md`: version-free model classes (M, N, X, S), escalation triggers, token rules for Claude Code and Codex, plan-resume rule.
- New `scripts/check_token_budget.py` (rules T-01 to T-07: instruction-file sizes, class block present and version-free, subagent model pins, plan-file size).
- Agent definitions in `agents/` pin a model through `model:` front matter; `AGENTS.md` carries the class block.

## Unreleased - Chwezi Product Excellence Standard routing (8 November 2026)

The Chwezi Product Excellence Standard was adopted by Lead Developer Peter Bamuhigire and the Chwezi Core Systems design
team, effective 01 November 2026 until further communication. It is mandatory for every Chwezi app and system.

- `core/instructions/engine-orchestrator.md`: step 3 and a new section "Chwezi app and system interface work". Any screen,
  flow, component, interface string or front-end of a Chwezi app or system routes to `chwezi-design-engine` with its
  `chwezi-product-excellence-standard` skill as a mandatory gate in the handoff sequence, alongside the house style (visual
  layer), `chwezi-dev-engine` front-end, mobile, offline and POS skills (engineering gates), interface wording and the finance
  engine for money values. A verdict comes only from that skill's scorecard and hard gates; `NOT_ASSESSED` gate evidence blocks.
- `catalog/shared-assets.yaml`: row `chwezi-product-excellence-standard` (mode `external`, canonical
  `chwezi-design-engine/doctrine/product-excellence-standard.md`, owner `chwezi-design-engine`). Local copies kept in
  repositories outside the public register are described by role and not listed; a discover glob flags any unregistered public
  copy at `skills/product-excellence-standard/`.
- `catalog/engines.yaml` has no capability lists, so it is unchanged.
- Wave 2 (Kaizen, 8 Nov 2026): every path and skill named in the orchestrator section and the shared-assets row was
  re-checked against the design and dev engine working copies (all present). The orchestrator now states the 13 hard gates
  (`PX-GATE-01` to `PX-GATE-13`), the PASS / CONDITIONAL / BLOCKED rule and the document-numbering gate, and lists
  `ios-development` and `pos-sales-operations-engineering` among the engineering gates. The shared-assets reason no longer
  names which private repository holds a local copy.

## 2026-11-07 - Cross-engine negative fixture check

- Added a read-only checker using the existing lexical union index and native Dev/Research fixtures. It preserves missing/malformed cases, rejects ties and checks resolved private paths before reading. [Usage, validation and limits](docs/operations/cross-engine-negative-check.md).

## Unreleased - README kaizen and README standard (31 October 2026)

A scoped cycle on this README and on the README practice of the portfolio. It publishes no score. The record is
[`docs/kaizen/2026-10-readme-kaizen/readme-kaizen-record.md`](docs/kaizen/2026-10-readme-kaizen/readme-kaizen-record.md).
Nothing was pushed, tagged or released. No existing script, catalogue entry, marketplace entry or lockfile was changed.

- Added `scripts/readme_metrics.py` (readability measures and `--check` limits) and `scripts/check_readme_preservation.py`
  (lost links, lost commands and broken anchors between two git revisions), with 90 tests in `tests/test_readme_metrics.py`
  and `tests/test_readme_preservation.py`. Forty-seven one-line mutations over the two scripts were each caught. Commits
  `398c4f4` and `0e559fa`.
- Added `docs/operations/readme-standard-2026-10-31.md`: the shared README structure, limits, preservation rules, the procedure
  for an engine README kaizen and the measured result for the eleven engines. Linked from the README, `AGENTS.md` and the
  documentation index. CI runs both scripts on this README (`3dd7f8b`).
- README restructured (`abe8c65`): front door, contents list, plain English, smaller sections. The tool detail moved to
  `docs/operations/package-tools-reference.md` and the reference lists to `docs/references.md`. Words 7,470 to 7,538, longest
  section 3,100 to 1,136, lines over 300 characters 61 to 7, words per sentence 19.6 to 12.1, reading ease 44 to 59.
- Corrections made while rewriting, each re-measured on 2026-10-31: the MCP server has one approval-gated tool, so it is not
  "read-only"; every `released_commit` pin is 5 to 9 commits behind (was 4 to 8) now that the engines merged their README work;
  the documentation wave is on `main`; the suite reads 352 passed and 3 skipped.
- `42cfab7` recorded a conflict: `scripts/validate-portfolio-craft.ps1` still expected a Capabilities heading that ten engine READMEs
  no longer had. Resolved the same day: each of the ten READMEs regained a `## Capabilities` section within its first four H2 headings
  (their commits are titled "restore a Capabilities section"), and `scripts/check_readme_contract.py` now applies the rule on any host
  with 17 tests and six caught mutations.

## Unreleased - Documentation wave and pin refresh (31 October 2026)

The pass-2 entry below has no commit hashes and says the catalogue pins were not refreshed; this entry adds the hashes by theme
and records what happened after. The pass-2 commits are on `main`; the documentation commits are on branch `kaizen/2026-10-docs`
and are not merged. Nothing was pushed, tagged or released from this package.

- Engine location: `eb8dae1` (locator and catalogue `aliases`), `9329a82` (`--engines-root` for the drift check).
- New checks: `5d7dbc8` and `2259900` (public-repository hygiene), `0d539fa` (canonical hook copy, installed copies compared),
  `2af312e` (`released_commit` refresh script and pin-lag rule), `608f466` (catalogue validators checked against engine
  manifests), `d4450f7` (path-free router wording, router rules and `--render-router-blocks`).
- MCP server: `0267684` (discovery test follows the checkout's branch; an unstartable validator is `NOT ASSESSED`). The critical
  lockfile finding F-01 is still open and needs the maintainer's authority.
- CI and policy: `6763854` (every Python test file and both hook tests; the release workflow calls validate; the supply-chain policy
  matches the workflows). Suite marketplace counts: `f099c75`.
- Teaching and evidence: `903243e` (router and changelog), `39ee3a1` and `c887dfa` (baseline and backlog), `dc743e3`, `4b9a30e`
  and `3dde18e` (experiment log, validation record, final report, next cycle and the evidence logs).
- `f1e4565` refreshed the catalogue `released_commit` pins to the eleven engines' `main` commits, which supersedes the pass-2 entry's
  "deliberately not refreshed". The pin-lag rule fails again as soon as an engine moves past its pin.
- Documentation (`ce48567`, `62ca327`, `a706b4d`, `b216053`, `eb2134b`): README gains measured installation notes, a Validation
  section (commands, dependencies, results, `NOT_ASSESSED` items), a Portfolio table of the twelve repositories with current GitHub
  names and pass-2 scores, and Quality and improvement (open findings, maintainer decisions, the portfolio calendar of
  date-triggered gates); `AGENTS.md` and `CONTRIBUTING.md` lose a stale Codex validator path and point at those sections;
  `docs/README.md` is a new index; `docs/runtime-skill-budget.md` loses five workstation paths; the portable links rule states the
  research repository name correctly; [`07-docs-followups.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/07-docs-followups.md) lists
  what the wave could not fix. No script, catalogue entry, marketplace entry or lockfile was changed. This package has no managed
  router sentences, so the router renderer was not applied (dry run: nothing to change).
- The README section [What the October 2026 kaizen improved](README.md#what-the-october-2026-kaizen-improved) lists each kept
  change with its check and figures; this entry does not repeat it.

## Unreleased - Portfolio kaizen pass 2 (31 October 2026)

- Added `scripts/lib/engine_roots.py` (engine locator with catalogue `aliases` for the four renamed engines) and
  `--engines-root` / `CHWEZI_ENGINES_ROOT` for the drift check; `skill_graph.py` no longer fails when engines sit
  outside the workspace root.
- Added `scripts/check_public_hygiene.py` and `catalog/hygiene-policy.yaml`, `scripts/check_hook_copies.py` and
  `docs/operations/hook-canonical-copy.md`, `scripts/refresh_released_commits.py` with a pin-lag rule in the drift
  check, validator and router rules in the drift check, and `templates/agents-blocks/` with
  `render_host_files.py --render-router-blocks`. The `hooks-test-plugin-hook-config` row joined the shared-asset register.
- Catalogue validators refreshed for windows, website, proposal, accounting, design and research; suite marketplace
  counts corrected for business-plan and design-engine; catalogue `released_commit` pins deliberately not refreshed.
- MCP server: the discovery test follows the checkout's branch; a validator that could not start (shell exit 126 or 127)
  is `NOT ASSESSED`, not `FAIL`. The critical lockfile finding is escalated, not fixed.
- CI runs every Python test file on the ubuntu job, both hook test files and the hygiene scan; the release workflow calls
  the validate workflow; `docs/security/supply-chain-policy.md` states what the workflows do and what they do not.

## Unreleased - Engine renames (29 September 2026)

- `srs-skills` is now `chwezi-sdlc-documentation` and `design-system-skills` is now
  `chwezi-design-engine` (GitHub repositories and local folders). Catalogue ids and paths,
  shared-asset paths, eval cases and fixtures (065 and 073 renamed), routing ownership and
  baseline keys, plugin eval folders, scripts, tests, MCP server tests, CI checkouts and live
  docs follow the new names; engine tours and the skill graph were regenerated.
- Suite marketplace entries renamed: `srs` is now `sdlc-documentation` and `design-system` is
  now `design-engine`, pointing at the new repository URLs.
- Design trigger block marker is now `<!-- chwezi-design-engine:trigger v4 -->`;
  `render_host_files.py` and the shared-asset register follow it.
- Dated records (Kaizen logs, M10 evidence, execution logs, plans, rejected-change ledger rows)
  keep the old names as written.

## Unreleased - M10-12 context contract, engine tours and skill graph

- Added the `PROJECT.md` project context contract
  (`docs/operations/project-context-contract.md`), its schema
  (`schemas/project-context.schema.json`), template
  (`templates/project-context/PROJECT.md`) and the read-only
  `scripts/project_context_doctor.py` with seeded fixtures;
  `validate-contracts.py` now validates a Markdown instance's front matter.
- Added one identical project-context read rule to every engine's `AGENTS.md`
  and to this package's `AGENTS.md`; the orchestrator pre-fills the craft
  brief from `PROJECT.md` when present.
- Added `scripts/skill_fanin.py` (inbound links, mentions, aliases, router and
  fixture references per active skill) and `scripts/generate_engine_tour.py`
  with committed tours for all twelve repositories under `docs/engine-tours/`.
- Added the report-only skill graph (`scripts/skill_graph.py`,
  `docs/skill-graph/skill-graph.json`), kept after the spike found defects no
  existing guardrail reports; it is never a routing input or a gate.
- MCP server: read-only `engine_tour` and `query_skill_graph` tools with tests.
- Added `scripts/skill_usage_scan.py` (local-only; tool calls only; refuses
  output inside a repository), a lifecycle map in `README.md` and the UA-11
  orientation case `077-orientation-dev-tour` (execution `NOT_ASSESSED`).

## Unreleased - 2026-09-24 Kaizen

- Added `scripts/validate-no-book-extractions.py`, a path-based portfolio
  copyright guard (banned `book-extractions/`, `extracted-books/`,
  `book-study/` folders and book-digest file names; domain-topic
  `*-extraction.md` files in skill `references/`/`templates/`/`examples/`
  pass; other exceptions via `catalog/content-integrity-allowlist.txt`;
  git-ignored working data out of scope), with tests. Wired into `CLAUDE.md`,
  the Claude Code adapter, the maintainer and validator instructions, and the
  portfolio craft standard.
- Added cross-engine handoff boundaries to the orchestrator (SRS, dev, design,
  research, finance ownership and sequence) and eval case
  `021-route-product-build-handoff`.
- Added a senior-practitioner bar and content-integrity section to the
  portfolio craft standard; requirements floor now demands buildable,
  implementation-free requirements.
- Fixed `validate-portfolio-craft.ps1`: accepts the 2026-09-20 README layout
  (capability section within the first four H2s) and reports every failure
  instead of stopping at the first.
- Catalog: `digital-research-skills` repository corrected to its GitHub name
  `digital-research-skills`; `windows-admin-engine-skills` integration status
  set to `pending` because its `.skills-engine/engine-manifest.yaml` does not
  exist.
- Evals 007 and 018 now target `chwezi-dev-engine` (renamed from
  `skills-web-dev` on 2026-09-20). README restores the coordination-card links
  required by `validate-kaizen-cards.py` and fixes the engineering plugin label.

## 1.0.0 - 2026-08-26

- Added a model-neutral canonical core with stable handoff, maintenance, and
  validation contracts.
- Added Codex, Claude Code, Gemini CLI, OpenCode, generic, and MCP adapters.
- Added capability negotiation, staged managed installers, fork discovery,
  path and mutation controls, and deterministic cross-host evaluations.
- Added release guides, CI gates, provenance metadata, and checksum policy.
