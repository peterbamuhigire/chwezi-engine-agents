# M10-02 evidence — host files, single source and drift control (T01–T14)

Executor: M10-02 executor (Claude Code), 29 Sep 2026. Zero spend: no model-executed checks, no paid services. Nothing staged, committed or tagged. Decisions marked "delegated" were taken by the orchestrator's executor under Peter's delegated authority, 29 Sep 2026, using the plan's recommended option.

## Summary

| Task | Status | One line |
|---|---|---|
| T01 | DONE | Portfolio bridge contract written; dev `bridge_failures()` aligned (allowed section is now `## Claude-only notes`, ≤ 25 lines); dev tests 133 passed, 3 skipped. |
| T02 | DONE_WITH_LIMITATIONS | Seven fat routers converted (design pilot first, then linux, research, social, business-plan, website, SRS) and three existing bridges aligned; 11 preservation maps, 0 lost, 1 obsolete row (research S86). Website registry validator and SRS `validate_engine.py` need a one-line repoint each (outside this executor's file scope; patches supplied). |
| T03 | DONE | `chwezi-engine-agents/AGENTS.md` created from the old `CLAUDE.md`; `CLAUDE.md` is now the bridge; `rules-distill` "all twelve" claim corrected. Codex-host behaviour `NOT_ASSESSED`. |
| T04 | DONE | `scripts/render_host_files.py` (rules a–i), 30 seeded tests pass; live portfolio exits 0. |
| T05 | DONE | `catalog/shared-assets.yaml`: 16 rows (byte, block, registered-variant, external) plus one documented exclusion; 0 unexplained drift. |
| T06 | DONE (delegated) | Trigger block `v2` added to accounting and windows `AGENTS.md`, and to engine-agents only through its new `AGENTS.md`. |
| T07 | DONE | `--render --engine` writes the closed list; second render is a zero diff on all 11 engines; malformed YAML exits 1 and writes nothing (tested). |
| T08 | DONE (delegated); tags `NOT_ASSESSED (awaiting release authority)` | `version: "1.1.0"` in all 11 engine manifests; all version-bearing files and suite entries at 1.1.0; tagging rule in `docs/distribution.md`. |
| T09 | DONE | `--check-marketplace` added to the agents generator: before 13 drift lines (exit 1), after 23 ok (exit 0); fixture tests for count drift, missing relative source, missing sibling. |
| T10 | DONE (delegated); pinning deferred | Decision record in `docs/distribution.md`: stay on `ref: main` until tags; `released_commit` refreshed; Codex plugin URLs corrected, `name` kept intentionally. |
| T11 | DONE | Every `SKILL.md` is in `plugin.json` or in `plugin_exclusions` with a reason (dev 3, design 1, SRS 1, website 1, research 2, business-plan 1 glob covering 3, linux 1 glob covering 3, windows 1, coordination 1 glob covering 2). 0 unexplained. |
| T12 | DONE | Snapshot gains `router_bytes`, `router_import_bytes`, `router_effective_bytes`, `router_imports`; global `~/.claude/CLAUDE.md` size printed to console only. Two runs: identical digests. Porcelain leading-space bug fixed with tests. |
| T13 | DONE; remote CI `NOT_ASSESSED (awaiting push)` | CI step for the package's own skills (passes locally); portfolio measured report-only: 1,160 skills, 291,636 metadata characters against 60,000; 27 duplicate names. |
| T14 | DONE locally; remote run `NOT_ASSESSED (awaiting push)` | `portfolio-drift` job (push, pull request, weekly schedule, dispatch; eleven sibling checkouts). Locally the host-file and marketplace checks exit 0; the prompt-capability check fails on a pre-existing accounting README gap. |

Extra items:
- `kaizen_portfolio_snapshot.py` porcelain bug: DONE. `git()` gains `strip=False`; `parse_porcelain()` reads the path from column 4 and handles renames and quoted paths. Tests in `tests/test_kaizen_portfolio_snapshot.py` (6 pass), including a real temporary repository whose first dirty path is ` M README.md`.
- `core/instructions/engine-orchestrator.md` step 4: DONE (clarified, not renamed). `digital-research-skills` there is the catalogue id and GitHub repository name, not a path; the step now says the local folder is `digital-research-engine` and that `discover_engine(path)` takes the `path` field from `catalog/engines.yaml`.
- Trigger block `v2` registered as a `block` asset with canonical source `design-system-skills/integration/trigger-block.md`: DONE (12 copies: 11 `AGENTS.md` plus `integration/integration-plan.md`; design's own router is a documented exclusion as the block owner).

## T01 — bridge contract

Files: `chwezi-engine-agents/docs/operations/claude-bridge-contract.md` (new); `chwezi-dev-engine/CLAUDE.md` (duplicated book-extraction section removed, all nine sentences already in `AGENTS.md`, map `preservation/chwezi-dev-engine.md`); `chwezi-dev-engine/tests/test_engine_control_plane.py` (`BRIDGE_ALLOWED_SECTION = "## Claude-only notes"`, 25-line limit, new test that the book-extraction section is now rejected in the bridge).

Command: `python -X utf8 -m pytest tests -q -p no:cacheprovider` in dev → `133 passed, 3 skipped` (a later full run, while the M10-06 executor was also editing dev, gave `181 passed, 3 skipped`).

## T02 — conversions

Preservation maps: `preservation/<engine>.md` for design (pilot), linux, digital-research-engine, social, business-plan, website, SRS, dev, and `preservation/bridge-alignments.md` (proposal, accounting, windows).

| Engine | CLAUDE.md-only sentences | duplicate | doctrine-moved | Claude-mechanics | obsolete | lost |
|---|---|---|---|---|---|---|
| design (pilot) | 30 | 18 | 10 | 2 | 0 | 0 |
| linux | 37 rows | 10 | 24 | 3 | 0 | 0 |
| digital-research-engine | 90 | 27 | 51 | 11 | 1 | 0 |
| social-media | 51 rows | 2 | 49 | 0 | 0 | 0 |
| business-plan | 31 rows | 17 | 12 (row groups) | 2 | 0 | 0 |
| website | 63 rows | 17 | 42 | 4 | 0 | 0 |
| srs | 58 rows | 14 | 44 | 0 | 0 | 0 |
| dev | 10 | 9 | 0 | 0 | 0 | 0 |
| proposal | 5 | 0 | 3 | 0 | 0 | 0 |
| accounting | 4 | 2 | 0 | 0 | 0 | 0 |
| windows | 17 | 6 | 7 | 2 | 0 | 0 |

Obsolete row needing Peter's tick: research S86, the old "See also: `AGENTS.md` — Codex / generic-agent equivalent of this file", false once `AGENTS.md` is the single router. SRS's 17-row table was checked: it describes the dev engine's 17 current categories and is labelled as such, so it was moved, not marked obsolete.

`AGENTS.md` sentences edited because the conversion made them false (recorded in each map): design L80, research "See also", SRS Purpose line, SRS categories pointer and SRS Compatibility Notes. Portfolio doctrine localised (not a move, delegated): the book-extraction ban added to linux and accounting `AGENTS.md`, whose routers had none, from the coordination package's existing rule "Never store book extractions in any engine or in this package".

`british-english` invariant exemptions (no British English rule in the router; adding one would be new doctrine): design, SRS, website, linux, dev, accounting, windows and the coordination package. Present in research, social, business-plan and proposal. For the orchestrator: roadmap rule 5 makes British English binding for plan outputs; whether each engine router should state it is a doctrine decision for a later phase.

Router bytes (T12 fields; before = working tree before this phase; the old fat `CLAUDE.md` files imported nothing, so Claude loaded only them; after = `CLAUDE.md` plus `@AGENTS.md`):

| Repository | before effective | after CLAUDE.md | after effective |
|---|---|---|---|
| business-plan-skills | 19,781 | 222 | 38,376 |
| chwezi-accounting-doctrine | 7,022 | 44 | 8,727 |
| chwezi-dev-engine | 16,231 | 44 | 15,238 |
| design-system-skills | 4,093 | 212 | 11,489 |
| digital-research-engine | 11,435 | 889 | 20,457 |
| linux-skills | 10,502 | 362 | 21,544 |
| proposal-skills | 30,765 | 44 | 30,560 |
| social-media-skills | 21,416 | 44 | 40,398 |
| srs-skills | 33,849 | 44 | 49,732 |
| website-skills | 21,323 | 606 | 40,929 |
| windows-admin-engine-skills | 11,391 | 250 | 12,096 |
| chwezi-engine-agents | 2,516 | 324 | 4,757 |

Effective bytes rose for the seven converted engines because Claude now loads the full runner-neutral router (and the moved doctrine) that it previously did not see. No byte target is set (P04); this is the input for CV-04 (M10-08).

Validators after conversion (engine root; details in each map):
- design: `validate_engine.py --baseline tests/quality-baseline.json` skills=101 fully_compliant=101; `routing_smoke_test.py` 68 fixtures, p@3 100%; agent contract PASS; pytest 99 passed.
- linux: `validate_skills.py` 48/48; `routing_smoke_test.py` 30/30; `check-distro-matrix.sh` (Git Bash) 41 passed, Linux-native behaviour `NOT_ASSESSED`; agent contract PASS.
- research: `skill_contract_validator.py` 59/59; `routing_smoke_test.py` 29/29; `validate_engine.py` pass; agent contract PASS; pytest 129 passed, 2 skipped.
- social: `validate_skill_engine.py` 191/191; `routing_smoke_test.py` 56/56; `check_source_freshness.py` PASS; agent contract PASS; pytest 1 failure (link under ignored `projects/maduuka-2026-09/node_modules/`, pre-existing).
- business-plan: `validate_skill_engine.py` 137 compliant; `routing_smoke_test.py --threshold 1.0` 61/61; agent contract PASS; pytest 1 failure (`test_runtime_orchestration_guidance`, README lacks the runtime-orchestration link since the README refresh, pre-existing).
- website: `routing-smoke-test.py` 36/36; `validate-skill-contracts.py` 62, zero debt; `website_fixture_benchmark.py` pass; agent contract PASS; **`validate-skill-registry.py` FAILS** (`CLAUDE.md category counts {}`) and pytest 2 failures from the same cause — the validator and `tests/test_kaizen_wave1_contracts.py` read category counts from `CLAUDE.md`, which moved to `AGENTS.md`. Patch: `patches-for-orchestrator/website-registry-repoint.patch` (verified by the fork against the live tree: `registry valid: 62 skills`).
- SRS: `validate_skill_engine.py` 159, no failures; `routing_smoke_test.py` 54/54; agent contract PASS; **`validate_engine.py` 4 findings**: 3 pre-existing README findings and 1 caused by the conversion (`CLAUDE.md missing required text: projects/<ProjectName>/`). One-line fix in `patches-for-orchestrator/srs-validate-engine-claude-md.md`; not applied because another executor holds `srs-skills/scripts/`.
- proposal: `validate_skills.py` 115, 0 findings; `routing_smoke_test.py` 25, p@3 100%; agent contract PASS; pytest 1 pre-existing README failure.
- accounting: `tools/validate-doctrine.ps1 -Strict` all sections pass; agent contract PASS.
- windows: `validate_engine.py` 19, 0 findings; `routing_smoke_test.py` 19, 0 failures; `source_ingestion_guardrail.py` 0; `unittest discover -s tests/python` 23 OK.

## T03 — engine-agents router

`AGENTS.md` created (21 sentences moved, 1 to the Claude-only block, 0 lost; map `preservation/chwezi-engine-agents.md`); `CLAUDE.md` is the bridge with a two-bullet Claude-only section. `skills/rules-distill/SKILL.md` now says all eleven catalogued domain engines have `rules/` (checked 29 Sep), the coordination package has none, and dev's `rules/common/` has topic files, not `core.md`. `grep -n "all twelve" skills/rules-distill/SKILL.md` → no match. Codex-host behaviour: `NOT_ASSESSED`.

## T04/T05/T07 — check, register, render

- `python -X utf8 -m pytest tests/test_render_host_files.py -q` → `30 passed`. Seeded failures, each a distinct finding code: `bridge-drift`, `bridge-render-drift`, `invariant-missing`, `invariant-undeclared`, `version-mismatch`, `version-tag-mismatch`, `bom`, `model-id-corruption`, `hook-single-quoted-root`, `hook-bare-script`, `hook-heredoc`, `hook-missing-file`, `shared-asset-byte-drift`, `shared-asset-block-drift`, `shared-asset-unregistered-variant`, `shared-asset-unregistered-copy`, `plugin-unlisted-skill`, `marketplace-count-drift`; CRLF-only difference is not drift; missing sibling → exit 3; render idempotent, never touches `AGENTS.md` or skills, refuses malformed YAML.
- Live: `python -X utf8 scripts/render_host_files.py --check --workspace-root .. --json > …/host-files-check.json` → exit 0, 0 findings, 0 not assessed, 12 repositories; register rows all `ok` (see `host-files-check.json`).
- One real finding during development: a deliberate quotation of a corrupted model ID in `chwezi-dev-engine/docs/updates/2026-09-24-book-extraction-removal-and-kaizen.md` (the K12 repair record). Recorded in `model_id_allowlist` with a reason rather than edited.
- Hooks: all twelve `hooks.json` files pass (double-quoted `${CLAUDE_PLUGIN_ROOT}`, explicit `node`, no heredoc, files exist) — SP-18 regression check in place.
- Render: `--render --engine ../<e>` then `--render --dry-run` → `{"changed": []}` for all 11 engines.

## T08/T09/T10/T11

- Versions: 1.1.0 in every engine manifest, `plugin.json`, engine marketplace entry, suite marketplace entry (12) and both agents plugin manifests. Rule c passes on 12/12.
- Marketplace: `marketplace-check-before.txt` (13 drift, exit 1) and `marketplace-check-after.txt` (23 ok, exit 0). Corrected counts: dev 169/183 → 165; design 91/97 → 101; SRS 158 → 159; website 61 → 62; proposal 94/113 → 115; business-plan 94/128 → 134; social suite 178 → 191; linux suite 48 → 45; windows 18 → 20.
- Engine generators: each engine's own `generate-plugin-manifest.js --check` (with its documented `--root`/`--exclude` for SRS and linux) reports current. The plan's loop using the agents copy reports "stale" for every engine because the agents variant writes a shorter `userConfig.hooks_enabled.description`; that is registered-variant drift (row `generate-plugin-manifest`), not a manifest defect.
- `released_commit` refreshed from `origin/main` tracking refs (21–59 commits behind before): srs 905b9a4, business-plan 2b41c08, website 75bc5c9, social 724970f, linux 9de82cf, proposal ba94f15, dev b3161da, accounting 8c1d683, design f69c5d4, research d4a613d, windows 132cbe9. `validate-contracts.py` on the catalogue: PASS.
- `.codex-plugin/plugin.json`: `homepage`/`repository` now `chwezi-engine-agents`; `name: skills-engine-agents` kept on purpose (recorded in `docs/distribution.md`).
- Tag checks: `NOT_ASSESSED (awaiting release authority)`.

## T12/T13/T14

- Snapshot: two runs → `baseline.json` SHA-256 `9c5c97ff…a699` both times; `skill-inventory.jsonl` `c9863841…3e45` both times. Local-only global `CLAUDE.md` size printed to console (8,529 bytes), not written to output files.
- Runtime budget: `runtime-budget-portfolio.json` (K6 validator functions over every skill listed in the twelve `plugin.json` files): 1,160 skills, 262,118 description characters, 291,636 metadata characters against the self-declared 60,000; 27 duplicate names; 12 descriptions over 400 characters. `runtime-budget-cli-report-only.txt`: the CLI in `--report-only` over the engine skill roots (1,146 skills, 288,193 characters). This is the P04 measurement; no target set. Package step: `validate-runtime-skill-budget.py --root skills` → `PASS: skills=1 … findings=0`.
- CI: `.github/workflows/validate.yml` gains the budget step and a pytest step in the `windows` job, a weekly `schedule`, and the `portfolio-drift` job. Remote run `NOT_ASSESSED (awaiting push)`. Local equivalents: host-file check exit 0; marketplace check exit 0; `validate-prompt-capability.ps1 -WorkspaceRoot C:/wamp64/www` **fails**: `chwezi-accounting-doctrine: missing marker 'DOMAIN PROMPT GENERATION CONTRACT'` (catalogue router for accounting is `README.md`, whose refresh in `f186f63` dropped the marker; pre-existing, not caused by M10-02). The new job will be red on that step until the accounting README (or its catalogue router entry) is fixed.

Other package checks run: `pytest tests` 53 passed, 1 failed (`test_kaizen_coordination_cards`: README does not link three cards — pre-existing, README untouched); catalogue, adapter, install, security and host-smoke PowerShell tests all pass; `run-contract-evals.py` 22/22; `validate-no-book-extractions.py` PASS (12 roots); `mcp-server npm test` 8 passed. `validate-portfolio-craft.ps1` fails for all eleven engine READMEs (no `## Capability map` heading since the README refresh; pre-existing).

## Open items for the orchestrator

1. Apply `patches-for-orchestrator/website-registry-repoint.patch` (website validator and one test read counts from `CLAUDE.md`), and route the SRS one-line `validate_engine.py` change to the SRS executor.
2. Peter's tick: research S86 obsolete row; the design pilot diff; T06, T08 and T10 decisions (taken here under delegation).
3. Pre-existing README regressions from the "refresh engine README" commits: accounting prompt-contract marker (will fail `portfolio-drift`), portfolio-craft `## Capability map` in eleven READMEs, proposal/business-plan runtime-orchestration link, agents coordination-card links.
4. The dev engine is being edited concurrently by the M10-06 executor; `.claude-plugin/plugin.json` and `marketplace.json` carry this phase's version change; if M10-06 regenerates `plugin.json`, rerun `render_host_files.py --render --engine ../chwezi-dev-engine` and the check.
5. At the push checkpoint: tag `v1.1.0` per repository, then pin suite sources to tags and set `released_commit` to the tagged commits (T10).
