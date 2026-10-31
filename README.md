# Chwezi Engine Agents

Chwezi Engine Agents is the coordination and shared-tooling package for the Chwezi skills portfolio of eleven independently installable domain engines: requirements, business plans, websites, digital marketing, Linux administration, proposals, engineering, accounting, design, research and Windows administration. It routes a task to the smallest set of engines that owns it, records the handoff between them, and keeps every engine's registry entry, plugin manifests, host bridge files and validators consistent. Its functions are routing and handoff, the engine catalogue, shared installation and manifest generation, portfolio drift control, contract and behavioural evaluation, a read-only Model Context Protocol (MCP) server, deterministic engine tours and skill-graph reports, and a destructive-command safety hook. It holds no domain doctrine; each engine remains the only source of its own skills.

The package follows JSON Schema 2020-12 for every contract and catalogue schema, Semantic Versioning for releases, the Model Context Protocol for its server, and the host plugin formats documented by Claude Code, Codex, Gemini CLI and OpenCode; its plugin threat model uses OWASP ASVS 5.0 path-handling controls as a design analogue. Its outputs are engine handoff records validated against `core/contracts/handoff.yaml`, installed engine files with an ownership manifest, generated plugin manifests, validator and drift-check evidence, contract and Tier-3 behavioural evaluation reports, engine tours in Markdown and JSON, a report-only skill graph and fan-in report, and explicit `NOT_ASSESSED` records wherever a check cannot run. It is for people who maintain one or more Chwezi engine checkouts, and for teams that need consistent routing, installation and validation across several engines. Domain engines install and work without it.

## Installation

Prerequisites, taken from the adapter guides and scripts: Git; Windows PowerShell 5.1 or 7+, or a POSIX shell; Python 3.11 or later for the validators, evaluators and drift checker (3.14 was used for the 31 October 2026 measurements); Node.js 20 or later for the shared installer, the safety hook and the MCP server (npm is also needed for the MCP server). The Python checks need `PyYAML`, the contract validators also need `jsonschema`, and the test suite needs `pytest`; [Validation](#validation) says which check needs what. Commands below use `python3`; on a Windows host `python` or `py -3` stands in.

**Claude Code (plugin marketplace).** Add the suite marketplace, then install the coordinator, a domain engine, or both. Each plugin installs fully on its own; the coordinator is optional.

```text
/plugin marketplace add peterbamuhigire/chwezi-engine-agents
/plugin install chwezi-suite@chwezi
/plugin install sdlc-documentation@chwezi
```

Marketplace plugin names: `chwezi-suite`, `sdlc-documentation`, `business-plan`, `website`, `social`, `linux`, `proposal`, `engineering`, `accounting`, `design-engine`, `research` and `windows-admin`. The `chwezi-suite` plugin ships the `rules-distill` skill and the destructive-command hook; set the plugin option `hooks_enabled` to `false` to keep the skill without hook enforcement.

**Host adapters (Codex, Claude Code, Gemini CLI, OpenCode, generic, MCP).** From a clone, install the coordination package for one host. The installer writes `.skills-engine-agents-install.json`, refuses an unmanaged non-empty destination, and refuses to overwrite locally modified files unless `-Force` is given after review.

```powershell
.\scripts\install.ps1 -Host codex -Destination "$env:USERPROFILE\plugins\skills-engine-agents"
.\scripts\install.ps1 -Host claude-code -Destination .claude\skills-engine-agents
.\scripts\update.ps1 -Destination "$env:USERPROFILE\plugins\skills-engine-agents"
.\scripts\uninstall.ps1 -Destination "$env:USERPROFILE\plugins\skills-engine-agents" -Force
```

```sh
sh scripts/install.sh --host codex --destination "$HOME/.local/share/skills-engine-agents"
sh scripts/update.sh --destination "$HOME/.local/share/skills-engine-agents"
sh scripts/uninstall.sh --destination "$HOME/.local/share/skills-engine-agents" --force
```

The PowerShell forms were not run on the Linux workstation used for the October 2026 pass (no `pwsh`), so they are `NOT_ASSESSED` there. The `sh` forms were run on 2026-10-31 against a scratch destination, with two findings:

- `update.sh` calls `install.sh` directly, and the committed file mode of `install.sh` is 100644, so on a fresh clone `update.sh` exits 126 with `Permission denied`. Run `sh scripts/install.sh --host <host> --destination <folder>` instead. Over a managed copy it exits 0; over a locally modified file it refuses (exit 1) unless `--force` is given after review.
- `uninstall.sh --force` removed every managed file (exit 0) and left the empty folders behind.

Codex reads the package through `.codex-plugin/plugin.json` (plugin name `skills-engine-agents`, kept on purpose; see the decisions under [Quality and improvement](#quality-and-improvement)). Host-specific steps are in [`docs/adapters/`](docs/adapters/) and the publication routes in [`docs/distribution.md`](docs/distribution.md).

**Standalone engine install (without the plugin system).** The shared installer copies one engine's skills, and its agents, commands and hooks where present, into user scope (`~/.claude`) or project scope (`.claude`), recording a content hash for every file it writes:

```sh
node scripts/install-engine.js install --engine <path-to-engine> --scope user --dry-run
node scripts/install-engine.js install --engine <path-to-engine> --scope project
node scripts/install-engine.js doctor
node scripts/install-engine.js uninstall --engine <engine-name>
```

**MCP server (optional).** Build it, then copy [`mcp-server/.mcp.json.example`](mcp-server/.mcp.json.example) into the host's MCP configuration with real paths and a host-generated confirmation token.

```powershell
cd mcp-server
npm ci
npm test
npm run build
```

`npm ci` needs network access to the npm registry. On 2026-10-31 (Node.js 22.23.1) `npm ci --ignore-scripts` in a clean copy exited 0, `npm run build` exited 0 and `npm test` passed 18 of 18 tests in 6 files. `npm audit` reports 13 vulnerabilities in the locked dependencies; that is the open finding F-01 under [Quality and improvement](#quality-and-improvement).

**Manual route.** Clone `https://github.com/peterbamuhigire/chwezi-engine-agents.git`, read [`AGENTS.md`](AGENTS.md) (Claude Code reads it through `CLAUDE.md`), resolve the engine from [`catalog/engines.yaml`](catalog/engines.yaml), then read that engine's own router before any of its `SKILL.md` files. Skills are read directly; they are not registered with a host's native skill tool.

## Capabilities

### Skills

| Category | Skill | What it does |
|---|---|---|
| Maintenance | [`rules-distill`](skills/rules-distill/SKILL.md) | Scans one engine's skills for principles that recur in two or more skills and are absent from `rules/`, and proposes promotions for explicit approval; never edits `rules/` itself. |

Count: Maintenance 1. Total: **1 active `SKILL.md`**. Domain skills live only in the eleven engine repositories.

### Coordination workflows

| Workflow | Canonical instruction | What it does | Output contract |
|---|---|---|---|
| Engine orchestrator | [`engine-orchestrator.md`](core/instructions/engine-orchestrator.md) | Selects the smallest relevant set of engines and records ownership, sequence, evidence boundaries, blockers and next action. | [`handoff.yaml`](core/contracts/handoff.yaml) |
| Engine maintainer | [`engine-maintainer.md`](core/instructions/engine-maintainer.md) | Inspects status, branch and upstream; permits only an approved `git pull --ff-only` on a clean `main`. | [`maintenance-result.yaml`](core/contracts/maintenance-result.yaml) |
| Engine validator | [`engine-validator.md`](core/instructions/engine-validator.md) | Runs only the validator commands declared in the catalogue; missing evidence is `NOT_ASSESSED`. | [`validation-result.yaml`](core/contracts/validation-result.yaml) |
| Capability negotiator | [`capability-negotiator.md`](core/instructions/capability-negotiator.md) | Records which host capabilities are present and which degraded mode applies. | [`capability-profile.schema.json`](schemas/capability-profile.schema.json) |

Codex wrappers for the first three are in [`agents/`](agents/); other host adapters are in [`adapters/`](adapters/).

### Tools and scripts by function

| Function | Tool | What it does |
|---|---|---|
| Registry | [`catalog/engines.yaml`](catalog/engines.yaml), [`validate-catalog.ps1`](scripts/validate-catalog.ps1), [`validate-contracts.py`](scripts/validate-contracts.py) | Holds engine IDs, paths, routers, manifests and declared validators; validates the catalogue and every YAML or JSON instance against its schema. |
| Discovery | [`discover-engine.ps1`](scripts/discover-engine.ps1), [`detect-capabilities.py`](scripts/detect-capabilities.py) | Identifies the Git root, catalogue entry and router for a path; detects local host capabilities without mutation. |
| Install and packaging | [`install.ps1`](scripts/install.ps1) / [`install.sh`](scripts/install.sh), `update`, `uninstall`, [`install-engine.js`](scripts/install-engine.js), [`generate-plugin-manifest.js`](scripts/generate-plugin-manifest.js), [`audit-managed-files.ps1`](scripts/audit-managed-files.ps1) | Installs, updates and removes the package or one engine with ownership records; generates plugin manifests from discovered skill trees; audits managed files. |
| Engine location | [`scripts/lib/engine_roots.py`](scripts/lib/engine_roots.py) | Finds an engine checkout from repeatable `--engines-root` folders, the `CHWEZI_ENGINES_ROOT` environment variable (a path-separator list) and, where a check asks for it, the folder that holds this package. It matches the catalogue `path`, repository, id or `aliases` (former folder names). A missing or ambiguous engine is `NOT ASSESSED`, never a pass. |
| Drift control | [`render_host_files.py`](scripts/render_host_files.py), [`catalog/shared-assets.yaml`](catalog/shared-assets.yaml), [`templates/agents-blocks/`](templates/agents-blocks/) | Checks every public repository's `CLAUDE.md` bridge, canary invariants, version consistency, model-ID corruption, byte-order marks, hook configuration, shared-asset copies, `released_commit` pin lag, catalogue validators against each engine's manifest, host paths and former engine names in router files, and stale plugin exclusions. `--render` writes only a closed list of derived fields; `--render-router-blocks --engine <path>` rewrites the legacy host-path form of three router sentences from the templates. |
| Portfolio hygiene | [`check_public_hygiene.py`](scripts/check_public_hygiene.py), [`catalog/hygiene-policy.yaml`](catalog/hygiene-policy.yaml) | Read-only scan of each repository's tracked files for per-user settings files, `.env` and key files, credential-shaped strings, and workstation or user-profile paths. Dated records are counted against ceilings that may only fall. Output never prints a matched secret. |
| Shared hook files | [`check_hook_copies.py`](scripts/check_hook_copies.py), [`docs/operations/hook-canonical-copy.md`](docs/operations/hook-canonical-copy.md) | Names this package's `hooks/` folder as the canonical copy of four files and compares every engine copy and every installed plugin copy against it, byte for byte with line endings normalised. |
| Release pins | [`refresh_released_commits.py`](scripts/refresh_released_commits.py), [`scripts/lib/released_commits.py`](scripts/lib/released_commits.py) | Reports, or with `--write` refreshes, the `released_commit` pin of every catalogue engine from the engine's HEAD. It refuses, and writes nothing, when an engine is dirty, missing, ambiguous or not on `main`. |
| Portfolio contracts | [`validate-portfolio-craft.ps1`](scripts/validate-portfolio-craft.ps1), [`validate-prompt-capability.ps1`](scripts/validate-prompt-capability.ps1), [`validate-kaizen-cards.py`](scripts/validate-kaizen-cards.py), [`validate-rule-markers.py`](scripts/validate-rule-markers.py) | Confirms the craft contract, domain prompt capability, coordination cards and doctrine rule markers across engines. |
| Skill metadata and content integrity | [`validate-skill-lifecycle.py`](scripts/validate-skill-lifecycle.py), [`validate-runtime-skill-budget.py`](scripts/validate-runtime-skill-budget.py), [`validate-no-book-extractions.py`](scripts/validate-no-book-extractions.py) | Checks lifecycle and invocation metadata, the skill metadata exposed to a runtime, and the ban on stored book extractions. |
| Routing evaluation | [`lexical_routing.py`](scripts/lexical_routing.py), [`validate-routing-baseline.py`](scripts/validate-routing-baseline.py), [`evals/routing/`](evals/routing/), [`scripts/lib/retrieval_metrics.py`](scripts/lib/retrieval_metrics.py) | Portfolio-wide lexical routing index, cross-engine ownership oracles and a ratchet that only raises routing floors; shared precision, MRR, nDCG and BM25 metrics. |
| Contract and behavioural evaluation | [`evals/runners/run-contract-evals.py`](evals/runners/run-contract-evals.py), [`run-host-smoke-tests.ps1`](evals/runners/run-host-smoke-tests.ps1), [`run_behavioural_eval.py`](scripts/run_behavioural_eval.py), [`evals/`](evals/) | Deterministic checks on 77 routing, acceptance, maintenance, validation, security and orientation cases; Tier-3 behavioural runner with arm isolation and a zero-spend gate that refuses model calls unless explicitly allowed. |
| Orientation and structure | [`generate_engine_tour.py`](scripts/generate_engine_tour.py), [`skill_fanin.py`](scripts/skill_fanin.py), [`skill_graph.py`](scripts/skill_graph.py), [`docs/engine-tours/`](docs/engine-tours/) | Deterministic engine tours, skill fan-in counts by provenance, and a report-only skill graph that is never a routing input. |
| Project context and usage | [`project_context_doctor.py`](scripts/project_context_doctor.py), [`skill_usage_scan.py`](scripts/skill_usage_scan.py), [`templates/project-context/`](templates/project-context/) | Read-only doctor for a project's `PROJECT.md` ([contract](docs/operations/project-context-contract.md)); local-only count of `SKILL.md` reads whose output stays outside every repository. |
| Portfolio baseline | [`kaizen_portfolio_snapshot.py`](scripts/kaizen_portfolio_snapshot.py) | Deterministic, read-only snapshot of skill files and working-tree state across the eleven engines. |
| MCP server | [`mcp-server/`](mcp-server/) | Exposes `discover_engine`, `inspect_engine`, `validate_engine`, `pull_engine_ff_only`, `engine_tour` and `query_skill_graph`; no tool accepts a command string from the model. |
| Safety | [`hooks/destructive-bash-gate.js`](hooks/destructive-bash-gate.js), [`hooks/hooks.json`](hooks/hooks.json), [`core/policies/safety-boundaries.md`](core/policies/safety-boundaries.md) | `PreToolUse` gate that blocks destructive shell and Git commands; binding read-only, approval and `NOT_ASSESSED` rules. |

Coordination cards (checked by `scripts/validate-kaizen-cards.py`):

- [`agentic-h2-readiness-card.md`](docs/operations/agentic-h2-readiness-card.md): H2 readiness and agentic-literacy card.
- [`three-horizon-ai-adoption-card.md`](docs/operations/three-horizon-ai-adoption-card.md): three-horizon adoption and frontier card.
- [`task-runbook-and-integration-evidence.md`](docs/operations/task-runbook-and-integration-evidence.md): task runbook and integration evidence card.

## Validation

Run every command from the package root. Engines are found through `CHWEZI_ENGINES_ROOT` (folders separated by `:` on POSIX and `;` on Windows) or a repeated `--engines-root`; a renamed checkout is found through its catalogue `aliases`, so no symlink is needed. A few checks still take `--workspace-root` (marked "workspace" below): a folder whose children are named by the catalogue `path`, such as `chwezi-sdlc-documentation`, `chwezi-dev-engine` and `digital-research-engine` (the research engine's catalogue path differs from its repository name), with this package linked as `chwezi-engine-agents`. Where checkouts keep other folder names, build that folder from symlinks.

```sh
export CHWEZI_ENGINES_ROOT=<folder-with-engines>:<second-folder-with-engines>
WS=<folder-of-catalogue-named-links>
```

**Dependencies.** Python 3.11 or later with `PyYAML` (every Python check); `jsonschema` (`validate-contracts.py` and `project_context_doctor.py`, which exit 3, `NOT ASSESSED`, when it is absent); `pytest` (the test suite; `python3 -m pytest` fails with "No module named pytest" where it is absent). Node.js 20 or later for the hook tests, the marketplace check and the MCP server, plus npm and network access for `npm ci` and `npm audit`. PowerShell (`pwsh`) for every `.ps1` suite. The Claude Code command-line tool for `claude plugin validate`. Versions used for the figures below: Python 3.14.8, PyYAML 6.0.3, jsonschema 4.26.0, pytest 9.0.3, Node.js 22.23.1, Claude Code 2.1.316.

Results were measured on 2026-10-31 on Fedora, in scratch copies of this package (`PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`), with the eleven engines at the `main` commits pinned in `catalog/engines.yaml`. A check that needs a sibling engine that is absent exits 3 with `NOT_ASSESSED`; for example `validate-no-book-extractions.py` with no workspace folder reports 11 of 12 roots not assessed.

| Command | Needs | Result on 2026-10-31 |
|---|---|---|
| `python3 -X utf8 -m pytest -p no:cacheprovider tests -q` | pytest, PyYAML, jsonschema | 262 passed, 3 skipped. The skips look for sibling folders named `chwezi-dev-engine` and `chwezi-design-engine` next to this package (`tests/test_run_behavioural_eval.py`, `tests/test_validate_rule_markers.py`); with a workspace folder that holds them: 265 passed, 0 skipped |
| `python3 -X utf8 -m unittest discover -s tests -p 'test_*.py'` | PyYAML | Not a substitute for pytest: 203 tests ran, 2 failures and 8 errors, all environmental (no `jsonschema` for 8 of them; two files import `pytest`), and the pytest-style files collect no tests |
| `python3 -X utf8 scripts/render_host_files.py --check` | PyYAML | Exit 1, 19 findings, 0 not assessed: 17 `shared-asset-unregistered-variant`, 1 `shared-asset-byte-drift` (the design engine's `install.sh`), 1 `plugin-exclusion-stale` (business-plan manifest). All are engine-side; the count was the same through `--engines-root`, `CHWEZI_ENGINES_ROOT` and `--workspace-root` |
| `python3 -X utf8 scripts/check_public_hygiene.py` (`--repo .` for this package alone) | PyYAML, git | Exit 1, 14 findings in four repositories (Linux 11, dev 1, accounting 1, design 1); no credential-shaped string; this package alone exits 0 with 0 findings |
| `python3 -X utf8 scripts/check_hook_copies.py` | none beyond Python | Exit 0: 11 engine repositories and 8 installed plugin copies, 76 files, 0 differences. It also reads the host plugin folder (`~/.claude/plugins` by default; `--plugins-dir` overrides) |
| `python3 -X utf8 scripts/refresh_released_commits.py` (check mode) | git | Exit 0: 11 engines, 0 not at HEAD. With `--write` it exits 2 and writes nothing when any engine is dirty or not on `main` (confirmed the same day against engine checkouts that held uncommitted files) |
| `python3 -X utf8 scripts/validate-contracts.py --schema schemas/engine-catalog.schema.json --instance catalog/engines.yaml` | PyYAML, jsonschema | Exit 0; exit 3 without `jsonschema`. The same command with `schemas/adapter-manifest.schema.json` passes for each of the six `adapters/*/adapter.yaml` |
| `python3 -X utf8 scripts/validate-no-book-extractions.py --workspace-root "$WS"` | workspace | Exit 0: 12 roots, 0 findings |
| `python3 -X utf8 scripts/validate-kaizen-cards.py` | none beyond Python | Exit 0, three cards valid |
| `python3 -X utf8 scripts/validate-routing-baseline.py` and `python3 -X utf8 scripts/validate-runtime-skill-budget.py --root skills` | PyYAML | Exit 0 each: the routing ratchet holds; this package's one skill exposes 255 metadata characters |
| `python3 -X utf8 scripts/validate-runtime-skill-budget.py --collisions --ownership evals/routing/ownership.yaml --workspace-root "$WS"` | workspace | Exit 0: 1,091 skills, 15 cross-engine pairs at 0.75 or above, 0 undeclared (a lexical proxy, not live routing) |
| `python3 -X utf8 scripts/validate-skill-lifecycle.py --root skills` | PyYAML | Exit 0, 0 findings |
| `python3 -X utf8 scripts/validate-rule-markers.py <design-engine>/doctrine/references/ai-slop-banned-fonts.md` | PyYAML | Exit 0: 29 markers, sidecar checked |
| `python3 -X utf8 evals/runners/run-contract-evals.py --cases evals/cases --route-oracles --workspace-root "$WS" --out <report.json>` | workspace | Exit 0, 77 of 77 assertions; the report goes where `--out` points |
| `node hooks/test-destructive-bash-gate.js` and `node hooks/test-plugin-hook-config.js` | Node.js | Exit 0: 61 of 61 and 7 of 7 |
| `node scripts/generate-plugin-manifest.js --check-marketplace --workspace-root "$WS"` | Node.js, workspace | Exit 0: 23 ok, 0 drift |
| `node --test tests/security/install-engine-ownership.test.js` | Node.js | Exit 0, 1 test passed. No workflow runs it |
| `bash -n scripts/install.sh scripts/update.sh scripts/uninstall.sh` | bash | Exit 0 (syntax only; see the `update.sh` finding under Installation) |
| `cd mcp-server && npm ci && npm run build && npm test` | Node.js, npm, network | Exit 0 at each step, 18 of 18 tests. `npm audit` exits 1 with 13 vulnerabilities (open finding F-01) |
| `claude plugin validate .` | Claude Code | Exit 0 with two warnings (a root `CLAUDE.md` is not loaded as plugin context; no plugin icon); `--strict` exits 1 on those warnings |

**Not run on this host (`NOT_ASSESSED`).** Every PowerShell suite, because there is no `pwsh`: `tests/validate_catalog.ps1`, the three scripts in `tests/adapters/`, `tests/install/*.ps1`, `tests/security/*.ps1`, `tests/test_capability_fallbacks.ps1`, `evals/runners/run-host-smoke-tests.ps1`, `scripts/validate-portfolio-craft.ps1` and `scripts/validate-prompt-capability.ps1` (both take `-WorkspaceRoot` and carry a Windows default). Also not run: the remote CI workflows (`.github/workflows/`), any Tier 3 behavioural run (paid model calls need `--allow-model-calls` and the maintainer's authority), live-model routing, and a native install into Codex, Gemini CLI or OpenCode.

## Portfolio

Twelve public repositories make up the portfolio: the eleven domain engines in [`catalog/engines.yaml`](catalog/engines.yaml) and this package. Repository names were checked against the GitHub API on 2026-10-31. Three engines were renamed on GitHub while the checkouts on the maintainer's workstation kept their old folder names, and the research engine's earlier name `digital-research-skills` now only redirects to `chwezi-research-engine`; it stays the research engine's catalogue id. The catalogue records each former folder name as an alias, and the `origin` remote of a renamed checkout may still carry the old URL, which GitHub redirects. The dev and Linux engines sit in Claude Code's user skills folder on that workstation and the other nine in a separate engines folder; `--engines-root` and `CHWEZI_ENGINES_ROOT` take both.

| Engine | GitHub repository | Catalogue id | Local folder (this workstation) | Raw | Capped |
|---|---|---|---|---:|---:|
| Accounting Doctrine | `chwezi-accounting-doctrine` | same | `chwezi-accounting-doctrine` | 58.2 | 58.2 |
| Digital Research | `chwezi-research-engine` | `digital-research-skills` | `chwezi-research-engine` | 59.5 | 59.5 |
| Dev engine | `chwezi-dev-engine` | same | `skills-web-dev` | 62.5 | 62.5 |
| Design engine | `chwezi-design-engine` | same | `design-system-skills` | 60.3 | 60.3 |
| SDLC documentation | `chwezi-sdlc-documentation` | same | `srs-skills` | 55.68 | 55.68 |
| Linux | `linux-skills` | same | `linux-skills` | 75.6 | 65.0 |
| Windows administration | `windows-admin-engine-skills` | same | `windows-admin-engine-skills` | 59.5 | 59.5 |
| Proposal | `proposal-skills` | same | `proposal-skills` | 61.4 | 61.4 |
| Business plan | `business-plan-skills` | same | `business-plan-skills` | 50.0 | 50.0 |
| Website | `website-skills` | same | `website-skills` | 62.9 | 62.9 |
| Social media | `social-media-skills` | same | `social-media-skills` | 60.0 | 60.0 |
| This package | `chwezi-engine-agents` | not catalogued | `chwezi-engine-agents` | 48.09 | 48.09 |

Scores are the pass-2 figures of 31 October 2026, read from each repository's `docs/kaizen/2026-10-engine-kaizen-pass-2/05-final-report.md`. Raw is the mean of the ten dimensions that engine rated (eleven for this package), as the report prints it; capped is `min(raw, 65)`, the Portfolio Kaizen Standard's reporting ceiling. The cap binds only for Linux. The figures are reviewer judgements against named evidence, not audits, and none reaches the 95 target. Two notes: Linux's later lab wave (`docs/kaizen/2026-10-linux-lab-wave/05-final-report.md` in that repository) raised its raw mean to 77.9, still 65.0 capped; and the SDLC report also prints 45 under a stricter initial cap set for the first cycle, whereas the Standard's cap gives 55.68. Each engine's own README keeps its open findings and its calendar; this package's summary of those calendars is under [Quality and improvement](#quality-and-improvement).

## Lifecycle map

One screen from idea to release. Each stage names its owning engine and an entry route
(`engine-id:path`); the owner answers its question once and hands the artefact on, as the
[orchestrator's handoff table](core/instructions/engine-orchestrator.md) sets out.

| Stage | Owner | Entry route |
|---|---|---|
| DEFINE | Requirements (`chwezi-sdlc-documentation`) | `chwezi-sdlc-documentation:01-strategic-vision/`, `chwezi-sdlc-documentation:02-requirements-engineering/fundamentals/before/02-elicitation-toolkit/` |
| PLAN | Engineering and design documentation | `chwezi-dev-engine:skills/execution-plan-scripts/`, `chwezi-sdlc-documentation:03-design-documentation/` |
| BUILD | Engineering; websites | `chwezi-dev-engine:skills/sdlc-meta/world-class-engineering/`, `website-skills:skills/orchestration/website-builder/` |
| VERIFY | Engineering; design | `chwezi-dev-engine:skills/sdlc-meta/world-class-engineering/references/verification-loop.md`, `chwezi-design-engine:skills/00-cross-cutting-ops-qa-a11y/visual-product-slop-audit/` |
| REVIEW | Engineering | `chwezi-dev-engine:skills/sdlc-meta/git-collaboration-workflow/` |
| SHIP | Engineering; websites; servers | `chwezi-dev-engine:skills/devops-cloud/deployment-release-engineering/`, `website-skills:skills/launch-ops/deploy/`, `linux-skills:linux-sysadmin/` |

Cross-cutting overlays join any stage, alongside the owner and never instead of it: finance
(`chwezi-accounting-doctrine:skills/`) wherever money moves, design
(`chwezi-design-engine:skills/`) wherever an output's appearance changes, and research
(`digital-research-skills:skills/`) for current or uncertain claims.[^commercial]

[^commercial]: Commercial work comes before DEFINE: proposals (`proposal-skills:skills/`),
    business plans (`business-plan-skills:skills/pipeline/00-plan-assembly/`) and marketing
    (`social-media-skills:skills/pipeline/06-digital-marketing-strategy/`).

The one-screen lifecycle idea is adapted from addyosmani/agent-skills (MIT,
https://github.com/addyosmani/agent-skills, commit `2686b62`).

## Contracts and governance

- [Engine orchestration contract](core/instructions/engine-orchestrator.md) and [handoff contract](core/contracts/handoff.yaml).
- [Compatibility contract](docs/architecture/compatibility-contract.md) and [host and model capability matrix](docs/architecture/host-model-capability-matrix.md).
- [Claude bridge contract](docs/operations/claude-bridge-contract.md) for every engine's `CLAUDE.md`.
- [Portfolio craft standard](docs/operations/portfolio-craft-standard-2026-09-04.md) and [skill lifecycle and invocation](docs/operations/skill-lifecycle-and-invocation.md).
- [Plugin threat model](docs/security/plugin-threat-model.md), [third-party skill register](docs/security/third-party-skill-register.json) and [third-party tool dispositions](docs/operations/third-party-tool-dispositions-2026-09-29.md).
- [Upgrade policy](docs/operations/upgrade-policy.md) and [incident runbook](docs/operations/incident-runbook.md).
- [Hook canonical copy](docs/operations/hook-canonical-copy.md), [supply-chain policy](docs/security/supply-chain-policy.md) and the [documentation index](docs/README.md).

## Quality and improvement

The package follows the Portfolio Kaizen Standard: measure, change, check and record; a published score capped at 65 out of 100; a plan that targets 95. The evidence is in [`docs/kaizen/2026-10-engine-kaizen/`](docs/kaizen/2026-10-engine-kaizen/) (29 October 2026: scope, baseline scorecard and backlog; the cycle stopped after its second commit and has no final report) and [`docs/kaizen/2026-10-engine-kaizen-pass-2/`](docs/kaizen/2026-10-engine-kaizen-pass-2/) (31 October 2026: scope and evidence, baseline scorecard, backlog, experiment log, validation record, final report and next cycle, with raw logs under `evidence/`). Earlier audits, execution logs and plans are indexed in [`docs/README.md`](docs/README.md).

**Latest published score.** Pass 2 ([final report](docs/kaizen/2026-10-engine-kaizen-pass-2/05-final-report.md)): raw 48.09 out of 100 (529 over eleven dimensions), published `min(raw, 65)` = 48.09. The frozen pass-2 baseline was 44.18. The 29 October scorecard printed a mean of 46.82, but its rows sum to 505, which is 45.91, and that cycle has no final score. The 95 target is not met, and the open critical finding F-01 overrides the aggregate. The score is the cycle owner's judgement against named evidence, not an independent audit.

**Open findings that matter to a user.**

- **F-01, vulnerable MCP lockfile (critical, escalated).** `npm audit` in `mcp-server/` reports 13 vulnerabilities (6 moderate, 6 high, 1 critical) on 2026-10-31, the same count as on 29 October. The pass-2 report records the critical entry (`proxy-addr`) as transitive and behind the HTTP transport that the stdio server does not import, and `zod`, also flagged, as used by the SDK at run time with its exposure not assessed. The SDK pin 1.30.0 is behind 1.32.2. The fix is an `npm install` of two minor versions, which needs the maintainer's authority; the exact commands and the acceptance check are in [`06-next-cycle.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/06-next-cycle.md). The MCP server is optional; nothing else in the package depends on it.
- **The drift check exits 1 with 19 findings, all engine-side.** Re-run on 2026-10-31 (`python3 -X utf8 scripts/render_host_files.py --check --engines-root <folder> --engines-root <folder>`): 17 `shared-asset-unregistered-variant` (`routing_smoke_test.py` in six engines, `rules/common/core.md` in four, the `skill-writing` skill in five, and the design engine's `generate-plugin-manifest.js` and `install-engine.js`), 1 `shared-asset-byte-drift` (the design engine's `install.sh`) and 1 `plugin-exclusion-stale` (the business-plan manifest's `country-context/*`). There were 16 variants when pass 2 closed; the 17th is the social-media engine's `rules/common/core.md`, edited in `3075062` on 31 October after that. Each variant needs a content review before its hash is registered with an owner and a reason in [`catalog/shared-assets.yaml`](catalog/shared-assets.yaml), after the last engine wave; the order is in `06-next-cycle.md`.
- **The hygiene check exits 1 with 14 findings in four repositories.** Linux 11 (a tracked `.claude/settings.local.json`, ten live path lines), dev engine 1 (a tracked `.claude/settings.local.json`), design engine 1 (a path in `doctrine/design-doctrine.md` line 161) and accounting 1 (45 path lines in dated records against a ceiling of 44). It found no credential-shaped string. A tracked file stays in public history after it is removed from the tree, and removing it from history needs a rewrite and force-push, which is the maintainer's decision.
- **Script defects found while documenting.** `scripts/update.sh` exits 126 on a fresh clone (see Installation). CI runs neither `tests/security/install-engine-ownership.test.js` (passes locally) nor the two `tests/security/install-*-preservation.ps1` scripts. These are recorded in [`07-docs-followups.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/07-docs-followups.md); this wave changed no script.
- **Not established.** No remote CI run of the edited workflows, no PowerShell run, no native install in a host, no Tier 3 behavioural run and no live-model routing. Routing figures are a lexical proxy.
- **Open work in the pass-2 backlog** ([`06-next-cycle.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/06-next-cycle.md)): ten more scripts still need `--workspace-root` instead of the engine locator; the release chain (plugin manifests read 1.1.0, `release/manifest.json` and the MCP package read 1.0.0, tag `v1.1.0` exists; `release.yml` still names `skills-engine-agents`; no provenance manifest or signing); the Codex layout and the Gemini adapter file name; no routing fixtures for the coordinator's one skill; 27 duplicate skill names and union skill metadata of 290,189 characters against a 60,000 budget (engine-side figures taken from the pass-2 evidence, not re-measured here).

**Decisions waiting for the maintainer** (full table in [`06-next-cycle.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/06-next-cycle.md)):

1. Authorise the MCP lockfile refresh for F-01 (default: the critical finding stays open).
2. Pin policy: keep allowance 0, so the drift check fails after any engine commit on a workstation, or set a standing `--pin-lag-max` (default: 0; skipped in shallow CI clones). The pins were refreshed to the engines' `main` commits in `f1e4565` on 31 October, so the check reads 0 lag until an engine moves.
3. Keep the Codex identity `skills-engine-agents` and the `.codex-plugin/` fallback layout, or migrate to a root `plugin.json` (default: unchanged).
4. Public history: dev and Linux still track `.claude/settings.local.json` (SDLC and design repaired the tree only); removing it needs a rewrite and force-push (default: no rewrite).
5. Whether the hygiene policy may name the workstation account in a public repository (default: as is).
6. One version for the package: plugin manifests 1.1.0, `release/manifest.json` and the MCP package 1.0.0 (default: unchanged).
7. Retire or renew the two overdue documents, `portfolio-craft-standard-2026-09-04.md` (review 2026-10-04) and `domain-prompt-compilation-contract-2026-09-16.md` (review 2026-10-16) (default: both stay overdue).
8. Add a per-validator platform field to the catalogue schema (default: not added).

### Date-triggered gates across the portfolio

No check in this package reads the calendar (searched `scripts/`, `evals/`, `hooks/` and `mcp-server/src/`; the only date logic is `project_context_doctor.py --today`, which compares a project's own `review_due`). Review dates written into documents and registers here, such as 2026-12-29 in `catalog/shared-assets.yaml` and the two overdue reviews above, are read by no validator. The engines are different: their source-register gates fail on a date unless the sources are re-read first. The rows below are gathered from each engine's README "Quality and improvement" section on `main`; the first failing date of each was confirmed on 2026-10-31 by running that engine's validator with a later date in a scratch clone (design excepted, see its row; proposal and business plan have no such option and are as their READMEs state). Counts assume nothing is re-verified in between.

| Date | Engine | What happens |
|---|---|---|
| Already failing | Social media | `check_source_freshness.py` exits 1: five quarantined records (`UG-DPPR-2021`, `UG-COPYRIGHT-2026`, `KE-DP-GENERAL-2021`, `RW-DPP-2021`, `ITU-INTERNET-USAGE`) stay `NOT_ASSESSED` until their primary text is read; its CI job fails with it |
| Already failing | Business plan | `refresh_evidence_register.py --check` exits 1: four register rows overdue (UBOS, KNBS, UNBS and the Bank of Uganda supervision page) |
| 2026-11-04 | Dev engine | `check_source_register.py` and its CI step first exit 1: five records (Next.js release, support policy, upgrade guide and security notices); 2026-11-03 passes |
| 2026-11-06 | Windows administration | `check_source_register.py` exits 1 (one finding: the policy review date 2026-11-05 has passed); 39 findings from 2026-11-11, when 35 URL rows pass the 90-day interval |
| 2026-11-08 | Social media | Further records start to lapse: one on 2026-11-08, 20 by 2026-11-29, 90 by 2026-12-30 (on top of the five quarantined) |
| 2026-11-17 | Accounting Doctrine | The NSSF entry passes its recheck date: `tools/source_register_integrity.py` exits 1 (`INT-008`), two tests fail and the lookup tool refuses final use for NSSF; 2026-11-16 passes |
| 2026-11-30 | Digital Research | The register gate exits 1 in `validate_source_currency.py`, `validate_engine.py` and CI: 11 findings, starting with four OpenAI platform records; 2026-11-29 passes. 13 findings from 2026-12-01 |
| 2026-11-30 | SDLC documentation | `validate_source_register.py` exits 1: three findings (OpenAI plugin schema, OpenAI archive limit, Claude marketplace); 2026-11-29 passes |
| 2026-12-01 | Proposal | `validate_skills.py` and `check_source_currency.py` exit 1 for all 14 register records; the gate passes through 2026-11-30 (stated by the engine's README; neither script has a date option) |
| 2026-12-01 | Website | `validate-source-registers.py` exits 1 (8 findings: the October standards register, three of its claims and four standards-table rows); `validate-search-doctrine.py` follows from 2026-12-06; 2026-11-30 passes |
| 2026-12-01 | Linux | The CI step "Check bounded hygiene regressions" (`kaizen_metrics.py`) fails on ten source rows with a review-by date of 2026-11-30; 2026-11-30 passes |
| 2026-12-01 | Business plan | Two more rows become overdue, six in all; 15 by 2027-01-30 |
| 2026-12-20 | Design engine | Only warnings: `validate_design_catalog.py` lists 13 catalogue records as stale and exits 0. No design validator fails on a date; the next review dates (2026-12-29 font watchlist, 2027-01-27 full re-audit) are read by no validator (as the engine's README states; not re-run here) |

Later batches (2027-01-27 to 2027-03-30 and beyond, in every engine except design) are in each engine's README. Re-audit dates written in the evidence rather than enforced include this package's own on 2026-11-13, Windows on 2026-11-05, Linux on 2026-11-07, research on 2026-11-27 and most others on 2026-11-30.

## References

### Books

No books are cited in this repository.

### Repositories

Repositories from the my-10-kaizen study (29 Sep 2026) from which this package adapted methods. All adaptations are paraphrased or re-implemented; no text or code is copied.

- addyosmani/agent-skills — https://github.com/addyosmani/agent-skills — MIT — commit `2686b62`: the one-screen lifecycle map; the lexical routing tokeniser, stemmer, IDF and owner-outranks-self rule (`scripts/lexical_routing.py`); Tier-3 behavioural evaluation mechanics (`scripts/run_behavioural_eval.py`).
- DietrichGebert/ponytail — https://github.com/DietrichGebert/ponytail — MIT — commit `e3ba2aa`: canary-invariant and version-consistency checks (`scripts/render_host_files.py`); arm isolation and self-test discipline for behavioural runs; the honest-reporting structure of the behavioural report template.
- obra/superpowers — https://github.com/obra/superpowers — MIT — commit `8ca22db`: Windows hook failure modes recorded in the drift checker and Claude bridge contract.
- pbakaus/impeccable — https://github.com/pbakaus/impeccable — Apache-2.0 — commit `114ea1d`: the split between durable project truth and task detail, and the report-only doctor (`scripts/project_context_doctor.py`).
- Egonex-AI/Understand-Anything — https://github.com/Egonex-AI/Understand-Anything — MIT — commit `b05cc3b`: fan-in as an importance signal (`scripts/skill_fanin.py`); install rejected, see the tool dispositions.
- Graphify-Labs/graphify — https://github.com/Graphify-Labs/graphify — Apache-2.0 — commit `d6eaa8a`: provenance-tagged edges, the never-invent-an-edge rule and the shrink guard (`scripts/skill_graph.py`); host adoption rejected.
- JuliusBrussee/caveman — https://github.com/JuliusBrussee/caveman — skill text MIT — commit `2fd153c`: "measure before cutting" (`scripts/skill_usage_scan.py`); no BSL code used.
- nextlevelbuilder/ui-ux-pro-max-skill (UI UX Pro Max) — https://github.com/nextlevelbuilder/ui-ux-pro-max-skill — MIT — commit `09170ee`: BM25 defaults and calibration idea (`scripts/lib/retrieval_metrics.py`).
- ComposioHQ/awesome-claude-skills — https://github.com/ComposioHQ/awesome-claude-skills — no root licence — commit `be2a406`: red-flag patterns for imported setup text (`tests/fixtures/prompt-injection/red-flag-patterns.md`) and the seed list for the third-party skill register.
- tt-a1i/archify — https://github.com/tt-a1i/archify — commit `0e4949f`: reviewed; estate-wide install rejected (tool dispositions, D3). Its diagram ideas were adopted in `chwezi-sdlc-documentation`, not here.
- anthropics/skills — https://github.com/anthropics/skills — Apache-2.0 — commit `3337550`: the `mcp-builder` evaluation method used for the coordinator MCP tool-surface evaluation (`evals/mcp/coordinator-qa.yaml`).
- affaan-m/ECC — https://github.com/affaan-m/ECC — commit `d3b8a3e`: the ECC audit (20 Sep 2026) supplied the standalone install tier and scope choice (`scripts/install-engine.js`) and the deterministic-collection-plus-judgement split in `rules-distill`.

The [third-party skill register](docs/security/third-party-skill-register.json) records a further 60 repositories screened by desk review on 29 Sep 2026 as sources of ideas; nothing from them was installed.

### Standards and official sources

- JSON Schema, draft 2020-12 — https://json-schema.org/draft/2020-12/schema (all files in `schemas/`).
- Semantic Versioning (`MAJOR.MINOR.PATCH`), as applied in [`docs/distribution.md`](docs/distribution.md).
- Model Context Protocol — https://docs.anthropic.com/en/docs/mcp; `@modelcontextprotocol/sdk` 1.30.0 in `mcp-server/package.json`.
- OWASP Application Security Verification Standard (ASVS) 5.0 — https://owasp.org/projects/asvs, https://github.com/OWASP/ASVS/releases (path-handling analogue in the plugin threat model).
- Claude Code documentation — https://code.claude.com/docs/en/plugins, https://code.claude.com/docs/en/plugins-reference, https://code.claude.com/docs/en/plugins/manifest-reference, https://code.claude.com/docs/en/plugins/relevance, https://code.claude.com/docs/en/hooks, https://code.claude.com/docs/en/best-practices.
- Anthropic documentation — https://docs.anthropic.com/en/docs/claude-code/skills, https://docs.anthropic.com/en/docs/claude-code/memory, https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables.
- OpenAI Codex plugins — https://developers.openai.com/codex/plugins/; OpenAI API guides on prompt engineering, evals, safety best practices, models and changelog — https://developers.openai.com/api/docs/.
- Gemini CLI extension reference — https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md.
- OpenCode rules and skills — https://opencode.ai/docs/rules/, https://opencode.ai/docs/skills.
- Microsoft PowerShell guidance — https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-shouldprocess, https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/requesting-confirmation-from-cmdlets, https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/rules/useapprovedverbs.
- npm CLI v11 `npm audit` and `npm sbom` — https://docs.npmjs.com/cli/v11/commands/npm-audit/, https://docs.npmjs.com/cli/v11/commands/npm-sbom/.
- XDG Base Directory specification — https://specifications.freedesktop.org/basedir/latest/; .NET `Environment.SpecialFolder` — https://learn.microsoft.com/en-us/dotnet/api/system.environment.specialfolder.
- Official sources checked for other engines during portfolio Kaizen and recorded in this package's execution logs and the system-administration activity contract: IFRS 18; RFC 6797; OWASP ASVS; NIST SSDF 1.1; Uganda Revenue Authority PAYE and Income Tax Amendment Act 2026 pages; KCCA Local Service Tax; Google Search AI features guide; nginx, Apache httpd, Certbot, Debian, Ubuntu and Red Hat Enterprise Linux documentation; Windows Task Scheduler, Windows Update for Business and Active Directory audit-policy documentation.

### Websites and articles

- Robertson, S. and Zaragoza, H. (2009) "The Probabilistic Relevance Framework: BM25 and Beyond", *Foundations and Trends in Information Retrieval* 3(4) (cited in `scripts/lib/retrieval_metrics.py`).
- SEEK preprint, arXiv 2609.29803v1 — https://arxiv.org/abs/2609.29803v1 (source S17 in the 26 Sep 2026 Kaizen log).
- W3C Markup Validation Service user documentation — https://validator.w3.org/docs/users.html.
- DeepSeek API documentation — https://api-docs.deepseek.com/ (multi-host plan, Aug 2026).
- pytest cache documentation — https://docs.pytest.org/en/stable/how-to/cache.html.
- [Chwezi Engine Agents source repository](https://github.com/peterbamuhigire/chwezi-engine-agents).
