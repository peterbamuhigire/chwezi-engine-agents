# Next cycle: open work, exact commands, decisions and handoffs (31 October 2026)

Owner: Peter Bamuhigire. **Re-audit: 2026-11-13**, or straight after the Linux and documentation waves land if that is sooner (it follows the
first date-triggered failure, Windows on 2026-11-11). Full cycle on 2026-11-30. Raw score now 48.09; the plan still targets 95.

Placeholders in angle brackets are checkout folders. On this workstation the engines are under `~/skill-engines/` and `~/.claude/skills/`
(see the first example), and the checks find them through `--engines-root` (repeatable) or `CHWEZI_ENGINES_ROOT`.

## Decisions needed from Peter

| # | Decision | Why it is yours | Default if unanswered |
|---|---|---|---|
| 1 | Authorise the MCP lock refresh (F-01): `npm install` of two minor versions | The one permitted command was `npm ci --ignore-scripts` | Critical finding stays open |
| 2 | Pin policy: keep default allowance 0 (the drift check fails after any engine commit, locally) or set a standing `--pin-lag-max` | It decides whether the check is a per-commit signal or a release-time one | Allowance 0; skipped in shallow CI clones |
| 3 | Codex identity and layout: keep `skills-engine-agents` and the `.codex-plugin/` fallback, or migrate to a root `plugin.json` | The identity is a documented deliberate choice; the Codex page now calls `.codex-plugin/` a compatibility fallback | Unchanged |
| 4 | History: dev and Linux still track `.claude/settings.local.json` (SDLC and design repaired the tree only); about 340 lines in dev records and 1,667 across the portfolio name paths | Removing a tracked file from public history means a rewrite and force-push | No rewrite; ceilings freeze the record lines |
| 5 | May the public hygiene policy name the workstation account (`private_user_names: [peter]`)? | It is a personal name in a public repository (it already occurs widely in dated records) | Stays as is |
| 6 | One version for the package: plugin manifests say 1.1.0, `release/manifest.json` and the MCP package say 1.0.0, tag `v1.1.0` exists | A release decision | Unchanged |
| 7 | Retire or renew the two overdue documents: `portfolio-craft-standard-2026-09-04.md` (review 2026-10-04) and `domain-prompt-compilation-contract-2026-09-16.md` (2026-10-16) | Doctrine | Both stay overdue |
| 8 | Add a per-validator platform field to the catalogue schema | It is a data-contract change; today a Windows-only validator on Linux is `NOT ASSESSED` only because of K7 | Not added |

## F-01: the lock refresh (exact commands)

```
cd mcp-server
npm install --save-exact --ignore-scripts @modelcontextprotocol/sdk@1.32.2 vitest@4.1.12
npm audit            # record the residual; expect no critical entry
npm run build && npm test   # expect 18 of 18
```

If a transitive entry remains, run `npm update --ignore-scripts` and audit again; do not run `npm audit fix --force` (it proposes major upgrades).
Commit `package.json` and `package-lock.json` alone. Acceptance: audit output with no critical entry, build and 18 of 18 tests recorded, no
major version change. The delegated check reports TypeScript 7, Vitest 5 and `@types/node` 26 as new majors: leave them for their own cycle.

## Documentation wave: what the shared source now fixes

Run from this package's checkout. Nothing here edits an engine on its own.

**Routers that still carry a workstation path** (re-render the three managed sentences, then commit inside each engine):

| Engine | Lines | Sentences rewritten |
|---|---|---|
| Accounting Doctrine | `AGENTS.md` 56, 145 | currentness-gate location, craft-standard location |
| Social Media | `AGENTS.md` 47, 60, 443 | currentness-gate location, control-plane location, craft-standard location |

```
python3 -X utf8 scripts/render_host_files.py --render-router-blocks --engine ~/skill-engines/chwezi-accounting-doctrine --dry-run
python3 -X utf8 scripts/render_host_files.py --render-router-blocks --engine ~/skill-engines/chwezi-accounting-doctrine
python3 -X utf8 scripts/render_host_files.py --render-router-blocks --engine ~/skill-engines/social-media-skills
python3 -X utf8 scripts/render_host_files.py --check --engines-root ~/skill-engines --engines-root ~/.claude/skills --pin-lag-max 1000 | grep router
```

Proved this cycle on scratch copies of both routers: rewritten, idempotent on a second run, no path finding left. No other engine's router carries
the legacy form (research, business-plan, SDLC, Linux and website were cleaned during their pass 2; no former engine name occurs in any router).
`accounting/governance/how-to-reference-this-doctrine.md` line 7 and `design/doctrine/design-doctrine.md` line 161 also name a workstation path but are
not managed sentences; the design line is canonical doctrine.

**Other hygiene findings** (run `python3 -X utf8 scripts/check_public_hygiene.py --engines-root ~/skill-engines --engines-root ~/.claude/skills` for the live list):
Linux 11 (tracked settings file, `scripts/setup-claude-code.sh` lines 105 to 119, `linux-cloud-init` and `linux-log-management` references, the `skill-writing` stub),
dev 1 (tracked settings file), social 3, accounting 3, design 1. After an engine is clean, lower its ceiling in `catalog/hygiene-policy.yaml`.

**Research's protected documents** (`portfolio-kaizen-standard-2026-08.md` line 76, `kaizen-currentness-gate.md` lines 51 to 52): apply the replacement text proposed in
the research engine's own `06-next-cycle.md`; the drift check does not cover them.

## End-of-waves sequence (after Linux and documentation land)

1. Every engine on `main` with a clean tree.
2. Pins: `python3 -X utf8 scripts/refresh_released_commits.py --engines-root ~/skill-engines --engines-root ~/.claude/skills` (report), then `--write`. It refuses (exit 2,
   nothing written) if any engine is dirty, missing, ambiguous or off `main`. Review `git diff catalog/engines.yaml` (11 lines), commit.
3. Suite counts: `node scripts/generate-plugin-manifest.js --check-marketplace --workspace-root <folder with catalogue-named engines>` and edit any drifted count
   in `.claude-plugin/marketplace.json` (this script has not moved to the locator yet).
4. Shared-asset variants (16) and the design `install.sh` drift: review each variant's content first, then register the new hash with owner and reason in
   `catalog/shared-assets.yaml`. Hash for a file: `tr -d '\r' < <file> | sha256sum`. Findings by engine are in the table below. Do this after the last wave, not before.
5. Website's vendored detector: in the website repository, `python -X utf8 scripts/check-vendored-detector.py --sync-from <design checkout>`, review, commit; then the three byte-drift findings clear.
6. Re-run `python3 -X utf8 scripts/render_host_files.py --check --engines-root ~/skill-engines --engines-root ~/.claude/skills`; expect 0 pin, router, validator and marketplace findings.

## Open work in this package

| Priority | Finding | Acceptance evidence |
|---|---|---|
| P0 | F-01 lock refresh (above) | Audit without a critical entry; 18 of 18 tests |
| P1 | Shared-asset variants: 16 unregistered, one byte drift. By engine: business-plan, dev, SDLC, proposal, Linux, Windows (`routing_smoke_test.py`); SDLC, website, Linux (`rules/common/core.md`); business-plan, research, proposal, social, website (`skill-writing` stub); design (`generate-plugin-manifest.js`, `install-engine.js`, `install.sh`) | `--check` shows 0 `shared-asset-*` findings |
| P1 | Engine manifests of accounting and design omit the checks their pass 2 added (the catalogue now lists them); business-plan's `.skills-engine/engine-manifest.yaml` has a stale `country-context/*` exclusion | `validator-undeclared` stays at 0; `plugin-exclusion-stale` clears |
| P1 | Locator coverage: only `render_host_files.py`, the hygiene check, the hook check and the pin script use it; `kaizen_portfolio_snapshot.py`, `validate-runtime-skill-budget.py`, `run-contract-evals.py`, `skill_fanin.py`, `skill_graph.py`, `generate_engine_tour.py`, `project_context_doctor.py`, `run_behavioural_eval.py`, `validate-no-book-extractions.py`, `generate-plugin-manifest.js` and the PowerShell scripts still need `--workspace-root` with catalogue-named folders | Each runs on the real layout with no symlink folder and gives identical output |
| P1 | Release: version split (decision 6); `release.yml` archive and prefix still say `skills-engine-agents`; no provenance manifest, signing or publication gate; remote CI of the edited workflows | A green remote run of `validate.yml` and `release.yml` on a branch; policy text still true |
| P1 | Codex layout and identity (decision 3); Gemini adapter file name `project-instructions.md` is not a documented context file; OpenCode adapter layout was not re-tested | A dated source for each host and one live install per host, or `NOT_ASSESSED` kept |
| P2 | Routing: the coordinator's one skill has no fixtures; the PRD request ranked its owner 691st (the SDLC skill `01-prd-generation` is invisible to the phrase "product requirements document") | Fixtures; the SDLC cycle looks at its description |
| P2 | Duplicate skill names (27) and union metadata (290,189 characters against 60,000) | A decision on the budget, then owners |
| P2 | Real `pytest` run and `jsonschema` in a pinned CI image; retire the stand-in runner | Real pytest output for the seven pytest-style files |
| P2 | Windows PowerShell defaults in `scripts/validate-portfolio-craft.ps1` and `scripts/validate-prompt-capability.ps1` (allow-listed with reasons) | A run on a host with `pwsh`, then remove the allow entries |
| P2 | `validate_machine_error_gate.py` (research) is not in the portfolio CI | A step that passes `--engines-root` |

## Cross-engine mismatches (recorded, not edited; ids as in `05`)

| ID | This package or the portfolio side | Engine side (file) |
|---|---|---|
| M1 | `templates/agents-blocks/`; `--render-router-blocks` | accounting `AGENTS.md` 56, 145; social `AGENTS.md` 47, 60, 443 |
| M2 | `catalog/engines.yaml` entry `digital-research-skills` (alias `chwezi-research-engine`) | research `docs/continuous-improvement/portfolio-kaizen-standard-2026-08.md:76`, `kaizen-currentness-gate.md:52` |
| M3 | `catalog/shared-assets.yaml` rows `website-vendored-chwezi-slop-*` | website `scripts/vendor/chwezi-slop/**` (VENDOR.json source commit `3fe84a6`) against design `tools/slop-detector/**` at `7582bbf` |
| M4 | `catalog/shared-assets.yaml` variants for `routing-smoke-test`, `rules-common-core`, `skill-writing-skill`, `generate-plugin-manifest`, `install-engine-js`; row `engine-install-sh` | the engines listed in the table above |
| M5 | `render_host_files.py` rule `plugin-exclusion-stale` | business-plan `.skills-engine/engine-manifest.yaml` |
| M6 | `catalog/hygiene-policy.yaml`; `scripts/check_public_hygiene.py` | Linux `.claude/settings.local.json`, `scripts/setup-claude-code.sh`; dev `.claude/settings.local.json`; social, accounting, design lines above |
| M7 | `catalog/engines.yaml` validators (refreshed) | accounting and design `.skills-engine/engine-manifest.yaml` `validation` blocks |
| M8 | n/a | business-plan `AGENTS.md` (line 278 template), `country-context/*/SKILL.md` section 4 against accounting `doctrine/source-register/uganda/*.yaml` (`draft`) |
| M9 | n/a | research `scripts/validate_source_currency.py:21` against windows `engine/source-register.yaml`, website `docs/source-registers/*.json`, one record each in social, business-plan, proposal |
| M10 | n/a | research `scripts/skill_contract_validator.py:226` against business-plan release schema (`not-assessed`) |
| M11 | `evals/cases/055-route-release-evidence-mirror.yaml`; `evals/routing/ownership.yaml` | dev `validation-contract` against research `validation-contract`; research `tests/fixtures/machine-error-gate-baseline.json:31` (`political-essay-skills`, unbound) |
| M12 | `scripts/lib/engine_roots.py` is the shared resolver now available | dev `scripts/engine_roots.py` and `tests/test_all_engine_currentness_policy.py:11-23`; proposal `tests/agent-integration/` line 28 (`ROOT.parent`) |
| M13 | n/a | each router's hard-ban font list against design `doctrine/references/ai-slop-banned-fonts.json` (only the secondary list was compared) |
| M14 | `evals/routing/ownership.yaml` | SDLC owned negatives `neg-business-case-vs-social-roi`, `-vs-proposal-roi`, `-vs-business-plan` |
| M15 | n/a | proposal `skills/pipeline/10-financial-proposal/SKILL.md` and business-plan `AGENTS.md`; proposal `06-methodology/references/technical-approach-figures.md` and SDLC `scripts/render_diagrams.py` |
| M16 | n/a | Linux `AGENTS.md` and dev deployment policy ("package branch, not upstream stable"); dev `docs/source-registers/skills-engine-currentness-2026-09.json` rows for Windows, Cisco and BIND |

## One small experiment for next time

Move `kaizen_portfolio_snapshot.py` and `validate-runtime-skill-budget.py` onto `engine_roots.resolve_catalog` (one function call each), keep
`--workspace-root` as the fallback root, and replay the baseline commands on this workstation with no symlink folder. Measure: the count of portfolio
scripts that run unaided on the real layout (4 of about 15 now) and byte-identical output against the symlink-folder run. Keep it only if the outputs are
identical. No paid call, no new dependency; revert by restoring the two scripts.
