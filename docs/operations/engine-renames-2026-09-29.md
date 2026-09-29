# Engine renames: evidence (29 September 2026)

Status: **DONE**. Executor evidence for harmonising live references after Peter renamed two engines on
GitHub; the orchestrator had already moved the local folders and updated the remotes.

| Old | New repository and folder | Claude Code plugin | Install |
|---|---|---|---|
| `srs-skills` | `chwezi-sdlc-documentation` | marketplace `chwezi-sdlc-documentation`, plugin `sdlc-documentation` | `sdlc-documentation@chwezi-sdlc-documentation` |
| `design-system-skills` | `chwezi-design-engine` | marketplace `chwezi-design-engine`, plugin `design-engine` | `design-engine@chwezi-design-engine` |

Suite marketplace (`chwezi`): entries `srs` and `design-system` are now `sdlc-documentation` and `design-engine`.
Plugin and marketplace ids: decided by the orchestrator under Peter's delegated authority, 29 Sep 2026.

## What changed

- Byte-level replacement (line endings and BOMs preserved) of `srs-skills` and `design-system-skills` in every
  tracked live file of the 13 repositories, plus the plugin install strings. Historical paths were excluded
  (see the list below).
- Engine identity: README titles, manifest `engine_id` and `display_name`, marketplace and plugin names, and
  plugin `description` and `author` added to both renamed engines' `plugin.json` (needed for
  `claude plugin validate --strict`). The kernel distribution name is now `chwezi-sdlc-documentation-engine`
  (the `engine` import package is unchanged), and the SARIF tool name and golden fixture follow it. Live docs
  that used the prose names "SRS-Skills" or "Design System Skills" now use the new names.
- Design trigger block: `<!-- chwezi-design-engine:trigger v4 -->` ... `<!-- /chwezi-design-engine:trigger -->`.
  The canonical copy is `chwezi-design-engine/integration/trigger-block.md`. It was copied byte-identically to
  11 engine `AGENTS.md` files and to `integration/integration-plan.md`, whose version history gains `v3`
  (commit `7a2ab6b`) and `v4` lines. `render_host_files.py` `TRIGGER_MARKER`, the shared-asset block markers
  and the tests use the new marker.
- Cross-engine skill references `design-system-skills:<skill>` are now `chwezi-design-engine:<skill>` (website
  registry, manifest, relocation map and tests). Website sibling checks now read `../chwezi-design-engine`.
- chwezi-engine-agents:
  - catalogue ids, repositories and paths, and shared-asset paths;
  - re-registered the 24 `generate-plugin-manifest` and `install-engine-js` variant hashes;
  - renamed eval cases `065` and `073` and their fixture folders to `065-accept-chwezi-sdlc-documentation`
    and `073-accept-chwezi-design-engine`, and renamed the `evals/plugin/<engine>` folders;
  - updated the routing ownership and baseline keys, CI checkouts, scripts, tests and MCP server tests;
  - regenerated the engine tours with `generate_engine_tour.py --all` and removed the old `srs-skills.*` and
    `design-system-skills.*` tours;
  - regenerated `docs/skill-graph/skill-graph.json` with `skill_graph.py`.
- website-skills: the vendored `chwezi-slop` `registry.schema.json` `$id` follows the source. Its hash in
  `VENDOR.json` was re-registered, and `source_repo` and `update_command` use the new name.
- CHANGELOG entries: `chwezi-sdlc-documentation/docs/CHANGELOG.md`, a new `chwezi-design-engine/CHANGELOG.md`,
  and `chwezi-engine-agents/CHANGELOG.md`.

## Environment repairs (not in Git)

- The SDLC kernel was installed editable from `C:\wamp64\www\srs-skills`. The folder move broke
  `import engine` in `scripts/create_agent_build_brief.py`. It was reinstalled with
  `pip uninstall -y srs-skills-engine`, then `pip install --user --no-deps -e C:/wamp64/www/chwezi-sdlc-documentation`
  (free and local).
- `social-media-skills/projects/chwezi-core-2026-09/delivery-ethos.md` (a git-ignored client project file) had
  sibling links `../../../srs-skills/...` that failed the engine's markdown-link test. The links now point to the
  new folder.

## Verification (29 Sep 2026, all local, zero spend)

| Check | Result |
|---|---|
| Catalogue validators for all 11 engines (`catalog/engines.yaml`), including routing smoke tests with floors | all exit 0 |
| pytest: sdlc (engine 96.86 % coverage; `tests/` exit 0), design 139, dev `tests/` 207 + 3 skipped, accounting 20, DRE 171 + 2 skipped, business-plan 66, social 61, proposal 52, website 131, linux 22 + 12 skipped, windows 24 | all pass |
| chwezi-engine-agents pytest | 162 passed (the test that used to skip now runs because the design sibling resolves) |
| `render_host_files.py --check --workspace-root C:\wamp64\www` | 12 repositories, 0 findings, 0 not assessed |
| `generate-plugin-manifest.js --check-marketplace` | 23 ok, 0 drift |
| `generate-plugin-manifest.js --check` in both renamed engines | current (159 and 101 skills) |
| `lexical_routing.py --collisions`; `validate-runtime-skill-budget.py --collisions --ownership` | exit 0; PASS (15 cross-engine pairs >= 0.75, 0 undeclared) |
| `validate-routing-baseline.py` | PASS |
| `run-contract-evals.py --cases evals/cases` | 77/77 |
| `run-contract-evals.py --route-oracles --min-oracle-primary 74` | exit 0; primary@1 76.9 %. Cases 044 and 057 report "expected_primary is not in the union": their social-media skills were retired by the Social Kaizen, and this change did not touch those cases |
| `validate-portfolio-craft.ps1`, `validate-prompt-capability.ps1`, `validate-catalog.ps1` | PASS |
| `validate-kaizen-cards.py`, `validate-no-book-extractions.py` | PASS |
| `generate_engine_tour.py --all --check` | PASS, 12 tours |
| MCP server `npm test` | 16/16 |
| `claude plugin validate --strict .` (sdlc, design, suite) | all pass |

Pre-existing and unrelated: in `chwezi-dev-engine`, bare `pytest` collects the git-ignored `benchmarks-private/`
folder and errors (`No module named 'core'`), while `pytest tests` passes. The other engines'
`claude plugin validate --strict` runs still warn about a missing plugin `description` and `author`. That warning
is portfolio-wide and was not changed here.

## Remaining `git grep "srs-skills\|design-system-skills"` hits (historical records, left as written)

- All repositories: `docs/audits/**`, `docs/engine-upgrade-july-2026/**`, `docs/superpowers/**`,
  `docs/continuous-improvement/**` (dated logs), `docs/plans/**`, `docs/kaizen/**`, `docs/evaluation/**`,
  `docs/initial-analysis/**`, `docs/updates/**`, `docs/sept-matt-pocock/**`.
- chwezi-sdlc-documentation: `docs/CHANGELOG.md` (past entries and the new rename entry).
- chwezi-design-engine: `integration/migration-manifest.md` (record of the 2026 migration). The new `CHANGELOG.md`
  names the old id on purpose.
- chwezi-dev-engine: `docs/catalog-cleanup/empty-directory-disposition.md` (dated verification record, "Last verified: 2026-07-08").
- chwezi-engine-agents:
  - `CHANGELOG.md` (the new entry names the old ids);
  - `docs/operations/m10-kaizen-evidence/**` and `docs/operations/skills-kaizen-evidence/**`;
  - `docs/operations/kaizen-2026-09-24-four-engine-kaizen.md` and `docs/operations/kaizen-2026-09-29-my-10-kaizen.md`;
  - `docs/operations/m10-kaizen-execution-2026-09-29.md`;
  - `docs/operations/destructive-cleanup-register.md`;
  - `docs/operations/third-party-tool-dispositions-2026-09-29.md`;
  - `docs/operations/decisions/skill-writing-canonical.md` (decision record with measured line numbers);
  - `docs/plans/aug-25/**`;
  - `evals/routing/rejected-changes.md` (dated ledger rows RC-002 to RC-011; no live text in it names the engines);
  - this evidence file.
- chwezi-accounting-doctrine: `integration/changelog-entries.md` and `integration/mirror.ps1.retired`.
- digital-research-engine: `projects/srs-skills-completion-2026/**` (a closed project whose folder name is itself historical).
- social-media-skills: `docs/kaizen/consolidation-2026-09-29/**` (baseline, evidence and preservation) and `docs/gap-analysis-2026-03-*.md`.
- website-skills: `project-log/decisions/2026-09-29-slop-scan-exit-contract.md` (dated decision).
- Git-ignored client project outputs under `chwezi-sdlc-documentation/projects/**` and `docs/alignment-2026-06/**` were not touched.

## Open items for the orchestrator

- Engine tours record each engine's HEAD commit. Regenerate them after committing if exact commit ids matter.
- Not edited because they sit outside the 13 repositories: the `C:\Users\Peter\.claude\CLAUDE.md` routing table and
  the memory files, `C:\wamp64\www\CLAUDE.md` and `AGENTS.md` at the workspace root, and the pre-existing
  `digital-research-skills` id drift.
- `C:\Users\Peter\Documents\my-10-kaizen\README.md` and `social-kaizen-2026-09-29\00-README.md` contain no old names, so they were not changed.

## Files changed (M modified, D removed, A added; absolute paths)

### chwezi-sdlc-documentation  (M=40 D=0 A=0)

- M `C:/wamp64/www/chwezi-sdlc-documentation/.claude-plugin/marketplace.json`
- M `C:/wamp64/www/chwezi-sdlc-documentation/.claude-plugin/plugin.json`
- M `C:/wamp64/www/chwezi-sdlc-documentation/.claude/settings.local.json`
- M `C:/wamp64/www/chwezi-sdlc-documentation/.github/copilot-instructions.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/.skills-engine/engine-manifest.yaml`
- M `C:/wamp64/www/chwezi-sdlc-documentation/01-strategic-vision/15-game-product-and-production-brief/SKILL.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/02-requirements-engineering/19-game-software-requirements-specification/SKILL.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/03-design-documentation/05-ux-specification/SKILL.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/03-design-documentation/05-ux-specification/references/design-system-guide.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/03-design-documentation/05-ux-specification/references/ux-requirements-foundations.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/03-design-documentation/17-game-system-architecture-specification/SKILL.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/09-governance-compliance/31-kaizen-engine-and-product-improvement/SKILL.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/AGENTS.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/ARCHITECTURE.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/DEPENDENCIES.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/PROJECT_BRIEF.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/README.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/SETUP_GUIDE.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/TECH_STACK.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/docs/API.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/docs/CHANGELOG.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/docs/DATABASE.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/docs/control-plane-adoption.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/engine/__init__.py`
- M `C:/wamp64/www/chwezi-sdlc-documentation/engine/cli.py`
- M `C:/wamp64/www/chwezi-sdlc-documentation/engine/diagram_render.py`
- M `C:/wamp64/www/chwezi-sdlc-documentation/engine/registry/schemas/diagram-ir.schema.json`
- M `C:/wamp64/www/chwezi-sdlc-documentation/engine/reporters/sarif.py`
- M `C:/wamp64/www/chwezi-sdlc-documentation/engine/tests/fixtures/findings_golden/report.sarif.json`
- M `C:/wamp64/www/chwezi-sdlc-documentation/prompts/full-kaizen-operation.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/pyproject.toml`
- M `C:/wamp64/www/chwezi-sdlc-documentation/scripts/diagram-render/render-config.json`
- M `C:/wamp64/www/chwezi-sdlc-documentation/scripts/generate-plugin-manifest.js`
- M `C:/wamp64/www/chwezi-sdlc-documentation/scripts/install-engine.js`
- M `C:/wamp64/www/chwezi-sdlc-documentation/scripts/plan-canvas.js`
- M `C:/wamp64/www/chwezi-sdlc-documentation/scripts/setup-srs-project.ps1`
- M `C:/wamp64/www/chwezi-sdlc-documentation/scripts/setup-srs-project.sh`
- M `C:/wamp64/www/chwezi-sdlc-documentation/skill_overview.md`
- M `C:/wamp64/www/chwezi-sdlc-documentation/tests/agent-integration/test_srs_agent_contract.py`
- M `C:/wamp64/www/chwezi-sdlc-documentation/tests/test_validate_skill_engine_tier1.py`
### chwezi-design-engine  (M=27 D=0 A=1)

- M `C:/wamp64/www/chwezi-design-engine/.claude-plugin/marketplace.json`
- M `C:/wamp64/www/chwezi-design-engine/.claude-plugin/plugin.json`
- M `C:/wamp64/www/chwezi-design-engine/.skills-engine/engine-manifest.yaml`
- M `C:/wamp64/www/chwezi-design-engine/AGENTS.md`
- M `C:/wamp64/www/chwezi-design-engine/CONTRIBUTING.md`
- M `C:/wamp64/www/chwezi-design-engine/README.md`
- M `C:/wamp64/www/chwezi-design-engine/docs/RESUME.md`
- M `C:/wamp64/www/chwezi-design-engine/docs/control-plane-adoption.md`
- M `C:/wamp64/www/chwezi-design-engine/doctrine/design-doctrine.md`
- M `C:/wamp64/www/chwezi-design-engine/governance/design-quality-gate.md`
- M `C:/wamp64/www/chwezi-design-engine/governance/standards-source-register.md`
- M `C:/wamp64/www/chwezi-design-engine/integration/integration-plan.md`
- M `C:/wamp64/www/chwezi-design-engine/integration/trigger-block.md`
- M `C:/wamp64/www/chwezi-design-engine/prompts/full-kaizen-operation.md`
- M `C:/wamp64/www/chwezi-design-engine/scripts/generate-plugin-manifest.js`
- M `C:/wamp64/www/chwezi-design-engine/scripts/install-engine.js`
- M `C:/wamp64/www/chwezi-design-engine/scripts/validate_engine.py`
- M `C:/wamp64/www/chwezi-design-engine/skills/00-cross-cutting-ops-qa-a11y/plan-canvas-design-review/SKILL.md`
- M `C:/wamp64/www/chwezi-design-engine/skills/04-web-and-ui-design/premium-ui-ux-design/SKILL.md`
- M `C:/wamp64/www/chwezi-design-engine/skills/05-ux-process-research-and-psychology/enterprise-ux-process/SKILL.md`
- M `C:/wamp64/www/chwezi-design-engine/skills/09-design-systems-tokens-and-theming/design-handoff-and-dev-spec/SKILL.md`
- M `C:/wamp64/www/chwezi-design-engine/skills/13-presentations-and-documents/docx-report-and-document-formatting/references/diagram-visual-standards.md`
- M `C:/wamp64/www/chwezi-design-engine/tests/agent-integration/test_design_agent_contract.py`
- M `C:/wamp64/www/chwezi-design-engine/tests/cross-engine-route-fixtures.yml`
- M `C:/wamp64/www/chwezi-design-engine/tests/routing-fixtures.yml`
- M `C:/wamp64/www/chwezi-design-engine/tests/test_routing_smoke_test.py`
- M `C:/wamp64/www/chwezi-design-engine/tools/slop-detector/rules/registry.schema.json`
- A `C:/wamp64/www/chwezi-design-engine/CHANGELOG.md`
### chwezi-dev-engine  (M=37 D=0 A=0)

- M `C:/wamp64/www/chwezi-dev-engine/00-meta-initialization/new-project/SKILL.md`
- M `C:/wamp64/www/chwezi-dev-engine/AGENTS.md`
- M `C:/wamp64/www/chwezi-dev-engine/SKILL.md`
- M `C:/wamp64/www/chwezi-dev-engine/benchmarks/solution-selection/fixtures.json`
- M `C:/wamp64/www/chwezi-dev-engine/benchmarks/solution-selection/pressure-scenarios.json`
- M `C:/wamp64/www/chwezi-dev-engine/docs/engine-control-plane.md`
- M `C:/wamp64/www/chwezi-dev-engine/docs/overview/README.md`
- M `C:/wamp64/www/chwezi-dev-engine/docs/quality-gates/release-blocking-gates.md`
- M `C:/wamp64/www/chwezi-dev-engine/docs/skill-aliases.yml`
- M `C:/wamp64/www/chwezi-dev-engine/docs/skill-routing-index.md`
- M `C:/wamp64/www/chwezi-dev-engine/prompts/full-kaizen-operation.md`
- M `C:/wamp64/www/chwezi-dev-engine/references/engineering-standards.md`
- M `C:/wamp64/www/chwezi-dev-engine/scripts/generate-plugin-manifest.js`
- M `C:/wamp64/www/chwezi-dev-engine/scripts/install-engine.js`
- M `C:/wamp64/www/chwezi-dev-engine/scripts/routing_fixtures.yml`
- M `C:/wamp64/www/chwezi-dev-engine/scripts/validate_approval_adapters.py`
- M `C:/wamp64/www/chwezi-dev-engine/scripts/validate_engine_control_plane.py`
- M `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-web-apps/SKILL.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/backend-databases/database-design-engineering/references/data-contracts-and-schema-evolution.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/frontend-ux/frontend-architecture/references/spa-route-contract-and-legacy-modernisation.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/frontend-ux/pos-sales-operations-engineering/SKILL.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/frontend-ux/pos-sales-operations-engineering/references/pos-operations-contract.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/frontend-ux/ux-principles-101/ALIAS.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/game-development/game-development-orchestration/SKILL.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/game-development/mobile-game-design/SKILL.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/gis/gis-platform-engineering/references/gis-maps-integration/references/a11y-maps.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/product-business/product-led-growth/references/habit-forming-products/entrypoint.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/product-business/professional-word-output/SKILL.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/product-business/professional-word-output/references/typography-layout.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-managed-visual-assets/SKILL.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/advanced-testing-strategy/SKILL.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/advanced-testing-strategy/references/accessibility-testing-automated-and-manual.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/skill-engine-audit/references/parallel-agent-method.md`
- M `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/world-class-engineering/references/solution-selection.md`
- M `C:/wamp64/www/chwezi-dev-engine/templates/delivery-dod/evidence-pack.md`
- M `C:/wamp64/www/chwezi-dev-engine/tests/test_all_engine_currentness_policy.py`
- M `C:/wamp64/www/chwezi-dev-engine/tests/test_routing_smoke_test.py`
### chwezi-engine-agents  (M=121 D=22 A=22)

- M `C:/wamp64/www/chwezi-engine-agents/.claude-plugin/marketplace.json`
- M `C:/wamp64/www/chwezi-engine-agents/.github/workflows/validate.yml`
- M `C:/wamp64/www/chwezi-engine-agents/AGENTS.md`
- M `C:/wamp64/www/chwezi-engine-agents/CHANGELOG.md`
- M `C:/wamp64/www/chwezi-engine-agents/README.md`
- M `C:/wamp64/www/chwezi-engine-agents/catalog/engines.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/catalog/shared-assets.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/core/instructions/engine-orchestrator.md`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/business-plan-skills.json`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/business-plan-skills.md`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/chwezi-accounting-doctrine.json`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/chwezi-accounting-doctrine.md`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/chwezi-dev-engine.json`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/chwezi-dev-engine.md`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/chwezi-engine-agents.json`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/chwezi-engine-agents.md`
- D `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/design-system-skills.json`
- D `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/design-system-skills.md`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/digital-research-skills.json`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/digital-research-skills.md`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/linux-skills.json`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/linux-skills.md`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/proposal-skills.json`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/proposal-skills.md`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/social-media-skills.json`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/social-media-skills.md`
- D `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/srs-skills.json`
- D `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/srs-skills.md`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/website-skills.json`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/website-skills.md`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/windows-admin-engine-skills.json`
- M `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/windows-admin-engine-skills.md`
- M `C:/wamp64/www/chwezi-engine-agents/docs/operations/project-context-contract.md`
- M `C:/wamp64/www/chwezi-engine-agents/docs/security/third-party-skill-register.json`
- M `C:/wamp64/www/chwezi-engine-agents/docs/skill-graph/skill-graph.json`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/001-route-srs.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/003-add-design-cross-cutting.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/009-route-design.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/021-route-product-build-handoff.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/022-route-clinic-admissions.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/023-route-business-case-roi.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/024-route-business-case-erp.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/025-route-lighthouse-cwv.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/026-route-invoice-typeface.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/027-route-generic-srs.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/028-route-game-srs.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/038-route-hospitality-design.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/041-route-rest-contract.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/051-route-prd.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/052-route-colour-contrast.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/053-route-word-report.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/054-route-business-case-content-mirror.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/cases/063-route-srs-api-section-mirror.yaml`
- D `C:/wamp64/www/chwezi-engine-agents/evals/cases/065-accept-srs-skills.yaml`
- D `C:/wamp64/www/chwezi-engine-agents/evals/cases/073-accept-design-system-skills.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/001-route-srs/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/001-route-srs/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/003-add-design-cross-cutting/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/003-add-design-cross-cutting/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/009-route-design/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/009-route-design/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/011-maintain-clean/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/011-maintain-clean/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/012-maintain-dirty/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/012-maintain-dirty/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/013-maintain-diverged/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/013-maintain-diverged/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/014-maintain-no-upstream/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/014-maintain-no-upstream/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/015-validate-pass/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/015-validate-pass/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/016-validate-fail/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/016-validate-fail/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/021-route-product-build-handoff/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/021-route-product-build-handoff/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/022-route-clinic-admissions/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/022-route-clinic-admissions/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/023-route-business-case-roi/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/023-route-business-case-roi/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/024-route-business-case-erp/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/024-route-business-case-erp/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/025-route-lighthouse-cwv/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/025-route-lighthouse-cwv/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/026-route-invoice-typeface/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/026-route-invoice-typeface/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/027-route-generic-srs/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/027-route-generic-srs/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/028-route-game-srs/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/028-route-game-srs/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/038-route-hospitality-design/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/038-route-hospitality-design/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/041-route-rest-contract/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/041-route-rest-contract/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/051-route-prd/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/051-route-prd/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/052-route-colour-contrast/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/052-route-colour-contrast/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/053-route-word-report/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/053-route-word-report/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/054-route-business-case-content-mirror/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/054-route-business-case-content-mirror/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/063-route-srs-api-section-mirror/expected.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/063-route-srs-api-section-mirror/task.md`
- D `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/065-accept-srs-skills/expected.yaml`
- D `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/065-accept-srs-skills/task.md`
- D `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/073-accept-design-system-skills/expected.yaml`
- D `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/073-accept-design-system-skills/task.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/plugin/README.md`
- D `C:/wamp64/www/chwezi-engine-agents/evals/plugin/design-system-skills/invoice-typeface-fires/graders/no-banned-font.md`
- D `C:/wamp64/www/chwezi-engine-agents/evals/plugin/design-system-skills/invoice-typeface-fires/graders/skill-fired.md`
- D `C:/wamp64/www/chwezi-engine-agents/evals/plugin/design-system-skills/invoice-typeface-fires/prompt.md`
- D `C:/wamp64/www/chwezi-engine-agents/evals/plugin/design-system-skills/lighthouse-cwv-co-activates-fires/graders/skill-fired.md`
- D `C:/wamp64/www/chwezi-engine-agents/evals/plugin/design-system-skills/lighthouse-cwv-co-activates-fires/prompt.md`
- D `C:/wamp64/www/chwezi-engine-agents/evals/plugin/srs-skills/billing-srs-fires/graders/game-srs-not-fired.md`
- D `C:/wamp64/www/chwezi-engine-agents/evals/plugin/srs-skills/billing-srs-fires/graders/skill-fired.md`
- D `C:/wamp64/www/chwezi-engine-agents/evals/plugin/srs-skills/billing-srs-fires/prompt.md`
- D `C:/wamp64/www/chwezi-engine-agents/evals/plugin/srs-skills/billing-srs-game-stays-quiet/graders/not-fired.md`
- D `C:/wamp64/www/chwezi-engine-agents/evals/plugin/srs-skills/billing-srs-game-stays-quiet/prompt.md`
- D `C:/wamp64/www/chwezi-engine-agents/evals/plugin/srs-skills/business-case-roi-fires/graders/skill-fired.md`
- D `C:/wamp64/www/chwezi-engine-agents/evals/plugin/srs-skills/business-case-roi-fires/prompt.md`
- M `C:/wamp64/www/chwezi-engine-agents/evals/routing/baseline.json`
- M `C:/wamp64/www/chwezi-engine-agents/evals/routing/ownership.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/mcp-server/tests/contracts.test.ts`
- M `C:/wamp64/www/chwezi-engine-agents/schemas/validation-result.schema.json`
- M `C:/wamp64/www/chwezi-engine-agents/scripts/generate-plugin-manifest.js`
- M `C:/wamp64/www/chwezi-engine-agents/scripts/generate_engine_tour.py`
- M `C:/wamp64/www/chwezi-engine-agents/scripts/install-engine.js`
- M `C:/wamp64/www/chwezi-engine-agents/scripts/kaizen_portfolio_snapshot.py`
- M `C:/wamp64/www/chwezi-engine-agents/scripts/project_context_doctor.py`
- M `C:/wamp64/www/chwezi-engine-agents/scripts/render_host_files.py`
- M `C:/wamp64/www/chwezi-engine-agents/scripts/run_behavioural_eval.py`
- M `C:/wamp64/www/chwezi-engine-agents/scripts/validate-catalog.ps1`
- M `C:/wamp64/www/chwezi-engine-agents/scripts/validate-portfolio-craft.ps1`
- M `C:/wamp64/www/chwezi-engine-agents/scripts/validate-prompt-capability.ps1`
- M `C:/wamp64/www/chwezi-engine-agents/templates/project-context/PROJECT.md`
- M `C:/wamp64/www/chwezi-engine-agents/tests/fixtures/invalid-validation-result-unknown-finding-field.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/tests/fixtures/invalid-validation-result.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/tests/fixtures/valid-handoff.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/tests/fixtures/valid-validation-result-with-findings.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/tests/fixtures/valid-validation-result.yaml`
- M `C:/wamp64/www/chwezi-engine-agents/tests/test_render_host_files.py`
- M `C:/wamp64/www/chwezi-engine-agents/tests/test_run_contract_evals.py`
- M `C:/wamp64/www/chwezi-engine-agents/tests/test_validate_rule_markers.py`
- A `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/chwezi-design-engine.json`
- A `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/chwezi-design-engine.md`
- A `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/chwezi-sdlc-documentation.json`
- A `C:/wamp64/www/chwezi-engine-agents/docs/engine-tours/chwezi-sdlc-documentation.md`
- A `C:/wamp64/www/chwezi-engine-agents/evals/cases/065-accept-chwezi-sdlc-documentation.yaml`
- A `C:/wamp64/www/chwezi-engine-agents/evals/cases/073-accept-chwezi-design-engine.yaml`
- A `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/065-accept-chwezi-sdlc-documentation/expected.yaml`
- A `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/065-accept-chwezi-sdlc-documentation/task.md`
- A `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/073-accept-chwezi-design-engine/expected.yaml`
- A `C:/wamp64/www/chwezi-engine-agents/evals/fixtures/073-accept-chwezi-design-engine/task.md`
- A `C:/wamp64/www/chwezi-engine-agents/evals/plugin/chwezi-design-engine/invoice-typeface-fires/graders/no-banned-font.md`
- A `C:/wamp64/www/chwezi-engine-agents/evals/plugin/chwezi-design-engine/invoice-typeface-fires/graders/skill-fired.md`
- A `C:/wamp64/www/chwezi-engine-agents/evals/plugin/chwezi-design-engine/invoice-typeface-fires/prompt.md`
- A `C:/wamp64/www/chwezi-engine-agents/evals/plugin/chwezi-design-engine/lighthouse-cwv-co-activates-fires/graders/skill-fired.md`
- A `C:/wamp64/www/chwezi-engine-agents/evals/plugin/chwezi-design-engine/lighthouse-cwv-co-activates-fires/prompt.md`
- A `C:/wamp64/www/chwezi-engine-agents/evals/plugin/chwezi-sdlc-documentation/billing-srs-fires/graders/game-srs-not-fired.md`
- A `C:/wamp64/www/chwezi-engine-agents/evals/plugin/chwezi-sdlc-documentation/billing-srs-fires/graders/skill-fired.md`
- A `C:/wamp64/www/chwezi-engine-agents/evals/plugin/chwezi-sdlc-documentation/billing-srs-fires/prompt.md`
- A `C:/wamp64/www/chwezi-engine-agents/evals/plugin/chwezi-sdlc-documentation/billing-srs-game-stays-quiet/graders/not-fired.md`
- A `C:/wamp64/www/chwezi-engine-agents/evals/plugin/chwezi-sdlc-documentation/billing-srs-game-stays-quiet/prompt.md`
- A `C:/wamp64/www/chwezi-engine-agents/evals/plugin/chwezi-sdlc-documentation/business-case-roi-fires/graders/skill-fired.md`
- A `C:/wamp64/www/chwezi-engine-agents/evals/plugin/chwezi-sdlc-documentation/business-case-roi-fires/prompt.md`
### chwezi-accounting-doctrine  (M=9 D=0 A=0)

- M `C:/wamp64/www/chwezi-accounting-doctrine/AGENTS.md`
- M `C:/wamp64/www/chwezi-accounting-doctrine/docs/analysis/05-roadmap-for-uplift.md`
- M `C:/wamp64/www/chwezi-accounting-doctrine/doctrine/accounting-finance-doctrine.md`
- M `C:/wamp64/www/chwezi-accounting-doctrine/governance/cleanup-backlog.md`
- M `C:/wamp64/www/chwezi-accounting-doctrine/governance/finance-accounting-quality-gate.md`
- M `C:/wamp64/www/chwezi-accounting-doctrine/governance/how-to-reference-this-doctrine.md`
- M `C:/wamp64/www/chwezi-accounting-doctrine/integration/integration-plan.md`
- M `C:/wamp64/www/chwezi-accounting-doctrine/scripts/generate-plugin-manifest.js`
- M `C:/wamp64/www/chwezi-accounting-doctrine/scripts/install-engine.js`
### digital-research-engine  (M=10 D=0 A=0)

- M `C:/wamp64/www/digital-research-engine/AGENTS.md`
- M `C:/wamp64/www/digital-research-engine/SKILL.md`
- M `C:/wamp64/www/digital-research-engine/docs/quality-gates/anti-slop-governance.md`
- M `C:/wamp64/www/digital-research-engine/scripts/generate-plugin-manifest.js`
- M `C:/wamp64/www/digital-research-engine/scripts/install-engine.js`
- M `C:/wamp64/www/digital-research-engine/skills/capability-matrix/SKILL.md`
- M `C:/wamp64/www/digital-research-engine/skills/capability-matrix/references/companion-rules.md`
- M `C:/wamp64/www/digital-research-engine/skills/professional-word-output/SKILL.md`
- M `C:/wamp64/www/digital-research-engine/skills/professional-word-output/references/typography-layout.md`
- M `C:/wamp64/www/digital-research-engine/tests/fixtures/machine-error-gate-baseline.json`
### business-plan-skills  (M=10 D=0 A=0)

- M `C:/wamp64/www/business-plan-skills/AGENTS.md`
- M `C:/wamp64/www/business-plan-skills/README.md`
- M `C:/wamp64/www/business-plan-skills/scripts/generate-plugin-manifest.js`
- M `C:/wamp64/www/business-plan-skills/scripts/install-engine.js`
- M `C:/wamp64/www/business-plan-skills/skills/advisory-deliverables/internal-controls-and-risk-framework/SKILL.md`
- M `C:/wamp64/www/business-plan-skills/skills/advisory-deliverables/internal-controls-and-risk-framework/references/document-blueprint.md`
- M `C:/wamp64/www/business-plan-skills/skills/meta-pitch/meta-presentation-design/references/innovative-presentations-anthony.md`
- M `C:/wamp64/www/business-plan-skills/skills/meta-pitch/meta-presentation-design/references/persuasive-presentations-duarte.md`
- M `C:/wamp64/www/business-plan-skills/skills/meta-pitch/meta-presentation-design/references/presentation-skills-edwards.md`
- M `C:/wamp64/www/business-plan-skills/skills/pipeline/00-plan-assembly/references/plan-figures.md`
### social-media-skills  (M=34 D=0 A=0)

- M `C:/wamp64/www/social-media-skills/AGENTS.md`
- M `C:/wamp64/www/social-media-skills/README.md`
- M `C:/wamp64/www/social-media-skills/docs/ux-foundations.md`
- M `C:/wamp64/www/social-media-skills/scripts/generate-plugin-manifest.js`
- M `C:/wamp64/www/social-media-skills/scripts/install-engine.js`
- M `C:/wamp64/www/social-media-skills/skills/advertising/ad-to-site-journey-handoff/SKILL.md`
- M `C:/wamp64/www/social-media-skills/skills/advertising/ad-to-site-journey-handoff/references/destination-ux-heuristics.md`
- M `C:/wamp64/www/social-media-skills/skills/advertising/ad-to-site-journey-handoff/references/measurement-and-ownership-spec.md`
- M `C:/wamp64/www/social-media-skills/skills/advertising/ad-to-site-journey-handoff/references/ux-engagement-diagnostics.md`
- M `C:/wamp64/www/social-media-skills/skills/advertising/creative-brief-and-big-idea/SKILL.md`
- M `C:/wamp64/www/social-media-skills/skills/advertising/creative-brief-and-big-idea/references/campaign-structure-and-copy-image.md`
- M `C:/wamp64/www/social-media-skills/skills/content-writing/direct-response-funnel-copy/references/long-copy-sales-letter-system.md`
- M `C:/wamp64/www/social-media-skills/skills/content-writing/premium-commercial-writing/references/brochure-copy.md`
- M `C:/wamp64/www/social-media-skills/skills/meta-analytics-ops/meta-competitor-analysis/references/competitive-matrix-and-analysis.md`
- M `C:/wamp64/www/social-media-skills/skills/meta-analytics-ops/meta-content-repurposing/references/capture-for-repurposing.md`
- M `C:/wamp64/www/social-media-skills/skills/meta-analytics-ops/meta-reporting/SKILL.md`
- M `C:/wamp64/www/social-media-skills/skills/meta-analytics-ops/meta-reporting/references/dashboard-specification.md`
- M `C:/wamp64/www/social-media-skills/skills/meta-analytics-ops/meta-reporting/references/quarterly-marketing-mix-review.md`
- M `C:/wamp64/www/social-media-skills/skills/meta-analytics-ops/meta-sentiment-analysis/ALIAS.md`
- M `C:/wamp64/www/social-media-skills/skills/meta-analytics-ops/meta-social-listening/references/sentiment-and-share-of-voice-method.md`
- M `C:/wamp64/www/social-media-skills/skills/meta-analytics-ops/meta-social-marketing-mix-review/ALIAS.md`
- M `C:/wamp64/www/social-media-skills/skills/meta-analytics-ops/meta-social-metrics-framework/SKILL.md`
- M `C:/wamp64/www/social-media-skills/skills/meta-utility/kaizen-improvement-system/SKILL.md`
- M `C:/wamp64/www/social-media-skills/skills/pipeline/01-client-brief/references/intake-question-bank.md`
- M `C:/wamp64/www/social-media-skills/skills/pipeline/01-client-brief/references/ux-strategy-and-product-lenses.md`
- M `C:/wamp64/www/social-media-skills/skills/pipeline/06-digital-marketing-strategy/references/channel-creative-and-service-lab.md`
- M `C:/wamp64/www/social-media-skills/skills/pipeline/06-digital-marketing-strategy/references/premium-growth-operating-contract.md`
- M `C:/wamp64/www/social-media-skills/skills/platforms/platform-instagram/SKILL.md`
- M `C:/wamp64/www/social-media-skills/skills/platforms/platform-instagram/references/grid-and-visual-system.md`
- M `C:/wamp64/www/social-media-skills/skills/playbooks/playbook-agency-operations/SKILL.md`
- M `C:/wamp64/www/social-media-skills/skills/playbooks/playbook-agency-operations/references/agency-economics-and-governance.md`
- M `C:/wamp64/www/social-media-skills/skills/strategy/strategy-personal-brand/references/brand-partnership-guide.md`
- M `C:/wamp64/www/social-media-skills/skills/training/training-ai-foundations/SKILL.md`
- M `C:/wamp64/www/social-media-skills/skills/training/training-ai-foundations/references/prompt-writing-module.md`
### proposal-skills  (M=10 D=0 A=0)

- M `C:/wamp64/www/proposal-skills/AGENTS.md`
- M `C:/wamp64/www/proposal-skills/scripts/generate-plugin-manifest.js`
- M `C:/wamp64/www/proposal-skills/scripts/install-engine.js`
- M `C:/wamp64/www/proposal-skills/skills/pipeline/06-methodology/references/technical-approach-figures.md`
- M `C:/wamp64/www/proposal-skills/skills/profiles-sectors/sectors/hospitality-hotel-restaurant/SKILL.md`
- M `C:/wamp64/www/proposal-skills/skills/strategy-positioning/premium-client-proposal-strategy/references/marketing-and-digital-services-proposals.md`
- M `C:/wamp64/www/proposal-skills/skills/strategy-positioning/tender-orals-and-proposal-presentation/SKILL.md`
- M `C:/wamp64/www/proposal-skills/skills/strategy-positioning/tender-orals-and-proposal-presentation/references/orals-preparation-and-room-readiness.md`
- M `C:/wamp64/www/proposal-skills/skills/strategy-positioning/website-design-proposal-strategy/SKILL.md`
- M `C:/wamp64/www/proposal-skills/skills/strategy-positioning/website-design-proposal-strategy/references/website-ownership-care-plans-and-direction-boards.md`
### website-skills  (M=77 D=0 A=0)

- M `C:/wamp64/www/website-skills/AGENTS.md`
- M `C:/wamp64/www/website-skills/README.md`
- M `C:/wamp64/www/website-skills/docs/onboarding-validation/2026/report.md`
- M `C:/wamp64/www/website-skills/docs/relocation-map.md`
- M `C:/wamp64/www/website-skills/glossary.md`
- M `C:/wamp64/www/website-skills/new-project.ps1`
- M `C:/wamp64/www/website-skills/new-project.sh`
- M `C:/wamp64/www/website-skills/prompts/full-kaizen-operation.md`
- M `C:/wamp64/www/website-skills/prompts/new-project-kickstart.md`
- M `C:/wamp64/www/website-skills/prompts/techguypeter-portfolio-content.md`
- M `C:/wamp64/www/website-skills/scripts/check-vendored-detector.py`
- M `C:/wamp64/www/website-skills/scripts/generate-plugin-manifest.js`
- M `C:/wamp64/www/website-skills/scripts/install-engine.js`
- M `C:/wamp64/www/website-skills/scripts/slop-scan-run.mjs`
- M `C:/wamp64/www/website-skills/scripts/slop-scan.sh`
- M `C:/wamp64/www/website-skills/scripts/validate-skill-registry.py`
- M `C:/wamp64/www/website-skills/scripts/vendor/chwezi-slop/VENDOR.json`
- M `C:/wamp64/www/website-skills/scripts/vendor/chwezi-slop/package.json`
- M `C:/wamp64/www/website-skills/scripts/vendor/chwezi-slop/tools/slop-detector/rules/registry.schema.json`
- M `C:/wamp64/www/website-skills/skills/agency-ops/agency-positioning/SKILL.md`
- M `C:/wamp64/www/website-skills/skills/agency-ops/agency-positioning/references/legacy-guidance.md`
- M `C:/wamp64/www/website-skills/skills/agency-ops/agency-positioning/references/qualification-guide.md`
- M `C:/wamp64/www/website-skills/skills/agency-ops/launch-campaigns/references/touchpoint-consistency-audit.md`
- M `C:/wamp64/www/website-skills/skills/agency-ops/social-media/references/legacy-guidance.md`
- M `C:/wamp64/www/website-skills/skills/brand/brand-storytelling/references/brand-story-spine-roles-drivers-plots.md`
- M `C:/wamp64/www/website-skills/skills/brand/brand-storytelling/references/legacy-guidance.md`
- M `C:/wamp64/www/website-skills/skills/brand/brand-storytelling/references/sb7-brandscript-worksheet.md`
- M `C:/wamp64/www/website-skills/skills/brand/brand-strategy/references/legacy-guidance.md`
- M `C:/wamp64/www/website-skills/skills/build/design-reference/SKILL.md`
- M `C:/wamp64/www/website-skills/skills/build/design-reference/references/legacy-guidance.md`
- M `C:/wamp64/www/website-skills/skills/build/design-reference/references/style-fit-questions-and-direction-handoff.md`
- M `C:/wamp64/www/website-skills/skills/build/design-reference/references/trend-selection-and-progressive-enhancement.md`
- M `C:/wamp64/www/website-skills/skills/build/design-system/SKILL.md`
- M `C:/wamp64/www/website-skills/skills/build/design-system/liquid-glass-effects.md`
- M `C:/wamp64/www/website-skills/skills/build/design-system/references/behaviour-and-visual-pattern-rules.md`
- M `C:/wamp64/www/website-skills/skills/build/design-system/references/data-tables-charts-and-svg-rules.md`
- M `C:/wamp64/www/website-skills/skills/build/design-system/references/design-system-governance-and-designops.md`
- M `C:/wamp64/www/website-skills/skills/build/design-system/references/grid-colour-gradient-and-surface-craft-rules.md`
- M `C:/wamp64/www/website-skills/skills/build/design-system/references/ui-composition-colour-and-icon-rules.md`
- M `C:/wamp64/www/website-skills/skills/build/page-builder/references/form-layout-flow-and-validation-rules.md`
- M `C:/wamp64/www/website-skills/skills/build/page-builder/references/navigation-mobile-and-form-pattern-rules.md`
- M `C:/wamp64/www/website-skills/skills/content-copy/blog-writer/references/human-voice-standards.md`
- M `C:/wamp64/www/website-skills/skills/content-copy/blog-writer/references/legacy-guidance.md`
- M `C:/wamp64/www/website-skills/skills/content-copy/content-writing/references/consultant-and-creator-site-kit.md`
- M `C:/wamp64/www/website-skills/skills/content-copy/content-writing/references/legacy-guidance.md`
- M `C:/wamp64/www/website-skills/skills/content-copy/sales-copywriting/references/legacy-guidance.md`
- M `C:/wamp64/www/website-skills/skills/launch-ops/deploy/references/legacy-site-performance-audit.md`
- M `C:/wamp64/www/website-skills/skills/manifest.yml`
- M `C:/wamp64/www/website-skills/skills/orchestration/africa-excellence/references/african-language-pack.md`
- M `C:/wamp64/www/website-skills/skills/orchestration/premium-ui-ux-design/SKILL.md`
- M `C:/wamp64/www/website-skills/skills/orchestration/premium-ui-ux-design/references/ai-feature-discovery-and-risk-framing.md`
- M `C:/wamp64/www/website-skills/skills/orchestration/premium-ui-ux-design/references/ai-interface-trust-and-control-spec.md`
- M `C:/wamp64/www/website-skills/skills/orchestration/premium-ui-ux-design/references/lean-design-cycle-and-deliverable-selection.md`
- M `C:/wamp64/www/website-skills/skills/orchestration/premium-website-product/references/premium-value-and-delivery-proof.md`
- M `C:/wamp64/www/website-skills/skills/orchestration/website-builder/SKILL.md`
- M `C:/wamp64/www/website-skills/skills/orchestration/website-builder/references/agency-operations-handbook-index.md`
- M `C:/wamp64/www/website-skills/skills/orchestration/website-builder/references/discovery-to-build-artifact-map.md`
- M `C:/wamp64/www/website-skills/skills/orchestration/website-builder/references/kaizen-website-product-loop.md`
- M `C:/wamp64/www/website-skills/skills/orchestration/website-builder/references/narrative-information-architecture-and-empathy.md`
- M `C:/wamp64/www/website-skills/skills/orchestration/website-builder/references/role-based-training-map.md`
- M `C:/wamp64/www/website-skills/skills/orchestration/website-experience-mapping/references/innovation-sprint-dvfs-reframe-and-assumption-testing.md`
- M `C:/wamp64/www/website-skills/skills/quality-gates/accessibility-audit/references/cognitive-affordance-and-memory-review.md`
- M `C:/wamp64/www/website-skills/skills/quality-gates/accessibility-audit/references/question-mark-and-scan-audit.md`
- M `C:/wamp64/www/website-skills/skills/quality-gates/accessibility-audit/references/remediation-playbook.md`
- M `C:/wamp64/www/website-skills/skills/quality-gates/cross-page-design-consistency-audit/SKILL.md`
- M `C:/wamp64/www/website-skills/skills/quality-gates/kaizen-engine-and-product-improvement/SKILL.md`
- M `C:/wamp64/www/website-skills/skills/quality-gates/security-gate/references/compliance-matrix.md`
- M `C:/wamp64/www/website-skills/skills/quality-gates/visual-qa/SKILL.md`
- M `C:/wamp64/www/website-skills/skills/quality-gates/visual-qa/references/slop-rules.md`
- M `C:/wamp64/www/website-skills/skills/seo-search/seo-audit/references/legacy-guidance.md`
- M `C:/wamp64/www/website-skills/skills/ux-conversion/cro-audit/references/design-critique-scorecard.md`
- M `C:/wamp64/www/website-skills/skills/ux-conversion/cro-audit/references/visitor-psychology-and-cultural-fit-review.md`
- M `C:/wamp64/www/website-skills/templates/README.md`
- M `C:/wamp64/www/website-skills/tests/test_design_routes.py`
- M `C:/wamp64/www/website-skills/tests/test_kaizen_wave1_contracts.py`
- M `C:/wamp64/www/website-skills/tests/test_routing_ratchet_and_lint.py`
- M `C:/wamp64/www/website-skills/universal-guidelines/UNIVERSAL-DESIGN-GUIDELINES.md`
### linux-skills  (M=3 D=0 A=0)

- M `C:/wamp64/www/linux-skills/AGENTS.md`
- M `C:/wamp64/www/linux-skills/scripts/generate-plugin-manifest.js`
- M `C:/wamp64/www/linux-skills/scripts/install-engine.js`
### windows-admin-engine-skills  (M=4 D=0 A=0)

- M `C:/wamp64/www/windows-admin-engine-skills/AGENTS.md`
- M `C:/wamp64/www/windows-admin-engine-skills/docs/release/delivery-evidence-pack.md`
- M `C:/wamp64/www/windows-admin-engine-skills/scripts/generate-plugin-manifest.js`
- M `C:/wamp64/www/windows-admin-engine-skills/scripts/install-engine.js`
### political-essay-skills  (M=4 D=0 A=0)

- M `C:/wamp64/www/political-essay-skills/AGENTS.md`
- M `C:/wamp64/www/political-essay-skills/CLAUDE.md`
- M `C:/wamp64/www/political-essay-skills/README.md`
- M `C:/wamp64/www/political-essay-skills/references/cross-engine-integration.md`

Added: `C:/wamp64/www/chwezi-engine-agents/docs/operations/engine-renames-2026-09-29.md` (this file).
