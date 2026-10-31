# Validation record: portfolio kaizen pass 2 (31 October 2026)

Every command below was run after the last code change (`903243e`), on HEAD of branch `kaizen/2026-10-pass2`, against the eleven
engines at the HEADs in [`evidence/engine-heads-final.txt`](evidence/engine-heads-final.txt) (unchanged since the baseline). Logs are in
`evidence/final-*`; exit codes are in [`evidence/final-results-exit-codes.txt`](evidence/final-results-exit-codes.txt). Workspace paths
are shown as `<workspace>` (a symlink folder named by catalogue path) or `--engines-root` (the real two-parent layout); the two give
identical output for the drift check.

## 1. The five commands named in the prompt

| Command | Exit | Result |
|---|---:|---|
| `python -X utf8 scripts/render_host_files.py --check --workspace-root <workspace>` | 1 | 37 findings, 0 not assessed. 21 are the same engine-side findings as the baseline (16 unregistered shared-asset variants, 4 byte drifts, 1 stale plugin exclusion). 16 are newly visible through rules added here: 11 `released-commit-lag` (pins deliberately not refreshed yet) and 5 `router-host-path` (accounting 2, social 3). No marketplace, validator or hook finding remains. |
| `python -X utf8 scripts/validate-no-book-extractions.py --workspace-root <workspace>` | 0 | `PASS: book-extraction check roots=12 findings=0` |
| `python -X utf8 scripts/validate-kaizen-cards.py` | 0 | three cards valid |
| `python -m pytest tests` | not run | **NOT_ASSESSED**: `pytest` is not installed on this host. `python3 -m unittest discover -s tests -p 'test_*.py'` ran instead, see section 3 |
| `npm ci --ignore-scripts && npm test` in `mcp-server/` | 0 | `npm ci --ignore-scripts` run once at baseline (only command that installed anything; `node_modules/` is gitignored). After the last change: 6 files, **18 of 18 tests pass** (baseline 15 of 16); `npm run build` exit 0 |

## 2. Other registered and new commands

| Command | Exit | Result |
|---|---:|---|
| `scripts/kaizen_portfolio_snapshot.py --workspace-root <workspace> --coordination-root . --as-of 2026-10-31` | 0 | 11 engines, 1,096 raw skill files |
| `scripts/validate-runtime-skill-budget.py --collisions --ownership evals/routing/ownership.yaml` | 0 | 1,091 skills, 15 cross-engine pairs at 0.75 or above, 0 undeclared (lexical proxy) |
| `evals/runners/run-contract-evals.py --route-oracles` | 0 | 77 of 77 assertions; primary at 1: 31 of 39 (31 of 42 with the three known defects); acceptance prompts primary 2 of 12, engine 5 of 12 |
| `scripts/validate-routing-baseline.py`; `scripts/validate-runtime-skill-budget.py --root skills` | 0; 0 | ratchet passes; package metadata 255 characters |
| `node scripts/generate-plugin-manifest.js --check-marketplace --workspace-root <workspace>` | 0 | 23 ok, 0 drift (baseline: 2 drift) |
| `node hooks/test-destructive-bash-gate.js`; `node hooks/test-plugin-hook-config.js` | 0; 0 | 61 of 61; 7 of 7 |
| `scripts/check_hook_copies.py --engines-root ...` | 0 | 11 repositories and 8 installed plugin copies, 76 files, 0 differences |
| `scripts/check_public_hygiene.py --engines-root ...` | 1 | 19 findings in 5 repositories (linux 11, social 3, accounting 3, dev 1, design 1): 2 tracked settings files (dev, Linux) and 17 live path lines; no credential-shaped string anywhere; 1,667 path lines in dated records, all within ceilings |
| `scripts/check_public_hygiene.py --repo .` | 0 | this package: 0 findings (7 at baseline) |
| `scripts/refresh_released_commits.py --engines-root ...` (check mode) | 1 | 11 of 11 pins behind HEAD (28 to 51 commits each); intended until the final refresh |
| `scripts/skill_graph.py --workspace-root <workspace>` | 0 | 1,105 nodes and 12,035 edges on the linked layout (baseline: crash on that layout) |
| `claude plugin validate .` (Claude Code 2.1.316, local) | 0 | valid; two warnings (a `CLAUDE.md` at the plugin root is not loaded as context; no plugin icon). `--strict` exits 1 on those warnings |
| `npm audit` in `mcp-server/` | 1 | 13 vulnerabilities (6 moderate, 6 high, 1 critical), unchanged: F-01 escalated |

## 3. Python tests

- `python3 -X utf8 -m unittest discover -s tests -p 'test_*.py'`: **203 run** (102 at baseline), 2 failures, 8 errors, 1 skipped. All ten
  failures are environmental and were present before any change: eight need `jsonschema` (project-context doctor, template schema) and
  two files import `pytest` and fail to load. They are `NOT_ASSESSED`, not passes.
- New suites (all `unittest`): engine locator 13, public hygiene 26, hook copies 13, pin refresh and pin rule 21, drift-check layout 5,
  validator rules 8, router rule and renderer 14, linked-layout graph 1: 101 tests, 0 failures.
- Seven pytest-style files were run through a **stand-in runner** (a scratch script that supplies `tmp_path`, `capsys`, `monkeypatch`,
  `raises`, `parametrize`, `skipif` and `importorskip`; it is not pytest and is not committed): 58 passed, 3 skipped (the dev-engine
  sibling and `jsonschema` are absent), 0 failed. Five of these files are silently skipped by `unittest discover`. This includes the
  29 October fixture-boundary test, which passes.
- Mutation controls: 27 single-line mutations across the new code were applied one at a time; two survived on first run and each
  gained a test that kills it. Details per item are in `03-experiment-log.md`.

## 4. Measures: baseline against now

| Measure | Baseline | Now | Note |
|---|---:|---:|---|
| Drift check findings | 21 | 37 | like for like 21 (engine-side, unchanged); +16 from new rules revealing existing defects |
| Suite marketplace drift | 2 | 0 | K9 |
| Package-side machine-path findings | 7 | 0 | K6 and the policy |
| Portfolio hygiene findings | not measurable | 19 | check added; 2 tracked settings files, 17 live path lines |
| `released_commit` lag | 11 of 11 | 11 of 11 | by decision, refreshed last |
| Hook copies identical | not checked for installed copies | 76 of 76 files | K3 |
| Python tests collected by `unittest discover` | 102 | 203 | |
| Test files run in CI | 12 of 19 | 19 of 19 plus the new suites (ubuntu job); hook tests 0 to 2 | real CI not run |
| MCP tests | 15 of 16 | 18 of 18 | |
| Route oracles primary at 1 | 31 of 39 | 31 of 39 | unchanged (engines and descriptions unchanged since baseline) |
| Union collisions undeclared at 0.75 | 0 | 0 | |
| Duplicate skill names | 27 | 27 | engine-side |
| Union metadata characters | 290,189 | 290,189 | budget 60,000; engine-side |
| Engine Eval Readiness, stand-in / strict | 37.4 / 19.4 | 37.4 / 25.4 | strict T1 is now 3 of 5 (drift check still fails, pytest `NOT_ASSESSED`) |

No baseline measure is worse. The drift count rose only because new rules were added; the individual defects existed at baseline.

## 5. Currentness of external claims (access date 2026-10-31, review 2026-11-27)

"Read" means this cycle read the primary source; "reported" means a delegated read-only agent read it and its result was recorded but not
re-read here.

| Claim | Source | Dated | Support | Detail |
|---|---|---|---|---|
| Current MCP specification is `2026-07-28`; negotiation per request, optional `server/discover` | modelcontextprotocol.io specification, versioning page (read) | page shows no date | Supported (read) | The package states no spec version; the pinned SDK (1.30.0) predates this revision. The agent reports SDK 1.32.2 still declares `2025-11-25` as its latest protocol constant (read from the published tarball, reported) |
| `@modelcontextprotocol/sdk` latest 1.32.2 (2026-10-23); pin 1.30.0 (2026-07-27) | npm registry via `npm view` (read) | as shown | Contradicted: pin is stale and affected | Agent reports six advisories affect 1.30.0, all fixed by 1.32.0 (GitHub advisories API, reported) |
| `vitest` pin 4.1.11; `V4` tag 4.1.12; `latest` 5.0.5 | npm registry (read) | 2026-10-15 (reported) | Partial | Minor refresh available inside major 4; major 5 is new. `tsx` 4.23.15 and `yaml` 2.9.1 are `latest` (read) |
| TypeScript 7.0.2 and `@types/node` 26.6.6 are the latest majors; pins 5.9.2 and 24.3.0 | npm registry (reported) | 2026-07-08, 2026-10-28 | Partial | No action: a major upgrade needs its own cycle |
| Codex plugins: portable manifest is root `plugin.json`; `.codex-plugin/plugin.json` is a compatibility fallback; `interface` sits under `extensions.com.openai` | developers.openai.com/codex/plugins/build (read) | page shows no date | Partial | This package ships only `.codex-plugin/plugin.json` with a top-level `interface`; that is the fallback layout, and the same agent saw another Codex page that shows a top-level `interface`, so the two pages disagree. Migration is Peter's decision (`06`) |
| Claude Code plugin manifest, `${CLAUDE_PLUGIN_ROOT}` hooks, exit code 2 blocks, URL-object marketplace source with the `source: url` discriminator, `claude plugin validate` | code.claude.com plugin, marketplace and hooks pages (reported); local `claude plugin validate` (run) | page dates not shown | Supported | The suite marketplace uses the discriminator form. Local validator: valid, two warnings |
| Gemini CLI: `gemini-extension.json`, `GEMINI.md`, `commands/*.toml`; `project-instructions.md` is not documented; Antigravity CLI replaces Gemini CLI for some users from 18 June 2026 | geminicli.com docs (reported) | 14 May to 18 Jun 2026 | Partial | The package's Gemini adapter file name is not a documented context file; not changed |
| OpenCode: skills from `.opencode/skills/`, `.claude/skills/`, `.agents/skills/`; `AGENTS.md` rules; plugins are JS or TS modules | opencode.ai docs (reported) | 30 Oct 2026 | Partial | No manifest file is documented; the adapter's layout was not re-tested |
| Node.js LTS lines 22, 24 and 26 | nodejs.org release page (reported) | not shown | Supported | Local Node is 22.23.1; `engines` says `>=20` |

Not assessed: the Claude Code, Gemini and OpenCode pages were not read first-hand; no live install of any host adapter ran;
the Codex native install, a public marketplace submission and remote CI were not attempted.

## 6. NOT_ASSESSED

Real `pytest`; `jsonschema` schema validation (the stand-in for the handoff schema covers a subset); the PowerShell validators
(`validate-catalog.ps1`, adapter, install and security suites) and every Windows CI job; remote CI of the edited workflows; any
Tier 3 behavioural run; live-model routing; a Codex, Gemini or OpenCode install; the residual `npm audit` result after a lock refresh;
the `political` engine (not installed, not searched for).
