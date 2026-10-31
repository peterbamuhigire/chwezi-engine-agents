# Chwezi Engine Agents

Chwezi Engine Agents is the coordination package for the Chwezi skills portfolio. It routes a task to the smallest set of engines that owns it and records the handoff between them.

It also keeps every engine's registry entry, plugin manifests, host bridge files and validators consistent. It holds no domain doctrine. Each of the eleven domain engines stays the only source of its own skills.

It is for people who maintain one or more Chwezi engine checkouts, and for teams that need the same routing, installation and checks across several engines. The domain engines install and work without it.

## At a glance

- **Twelve repositories.** The catalogue ([`catalog/engines.yaml`](catalog/engines.yaml)) lists eleven public domain engines. This package makes twelve.
- **One skill and four workflows.** The skill is `rules-distill`. The workflows are the engine orchestrator, the engine maintainer, the engine validator and the capability negotiator.
- **Tests.** The package suite gives `352 passed, 3 skipped` with pytest (exit 0), measured on 2026-10-31.
- **Drift check.** `render_host_files.py --check` exits 1 with 30 findings: 19 sit in the engines and 11 are pin lag. See [Open findings](#open-findings).
- **Hygiene check.** This package alone exits 0 with 0 findings. Across the portfolio it finds 14 in four repositories.
- **Score.** 48.09 out of 100 (raw and capped) on 31 October 2026, against a target of 95. One critical finding, F-01, is open.

## Start here

1. Install the coordinator in Claude Code. The plugin works without any other engine.

   ```text
   /plugin marketplace add peterbamuhigire/chwezi-engine-agents
   /plugin install chwezi-suite@chwezi
   ```

   Host adapters, the standalone installer and the manual route are under [Install and update](#install-and-update).
2. Check a clone. This needs Python 3.11 or later, `PyYAML`, `jsonschema` and `pytest`.

   ```sh
   git clone https://github.com/peterbamuhigire/chwezi-engine-agents.git
   cd chwezi-engine-agents
   python3 -X utf8 -m pytest -p no:cacheprovider tests -q
   ```

   Expect `352 passed, 3 skipped` and exit 0. The three skips need sibling engine folders; see [Validation](#validation).
3. Run the read-only drift check against your engine checkouts. `<folder>` is a folder that holds them; repeat the flag for a second folder.

   ```sh
   python3 -X utf8 scripts/render_host_files.py --check --engines-root <folder>
   ```

   On 2026-10-31 it exits 1 with 30 findings. [Open findings](#open-findings) explains each group.

## Contents

- [What it is and who runs it](#what-it-is-and-who-runs-it)
- [Find the right tool](#find-the-right-tool)
- [How it works](#how-it-works)
- [What is inside](#what-is-inside)
- [Install and update](#install-and-update)
- [Validation](#validation)
- [Portfolio](#portfolio)
- [Lifecycle map](#lifecycle-map)
- [Contracts and governance](#contracts-and-governance)
- [Quality and improvement](#quality-and-improvement)
- [Open findings](#open-findings)
- [Decisions waiting for the maintainer](#decisions-waiting-for-the-maintainer)
- [Date-triggered gates across the portfolio](#date-triggered-gates-across-the-portfolio)
- [What the October 2026 kaizen improved](#what-the-october-2026-kaizen-improved)
  - [Correctness fixes](#kept-changes-correctness-fixes)
  - [New checks](#kept-changes-new-checks)
  - [Documentation and README work](#kept-changes-documentation-and-readme-work)
  - [Scores and measures](#scores-and-measures)
- [References](#references)
- [Contributing, author and licence](#contributing-author-and-licence)

## What it is and who runs it

The package has eight functions:

- routing and handoff between engines;
- the engine catalogue;
- shared installation and manifest generation;
- portfolio drift control;
- contract and behavioural evaluation;
- a Model Context Protocol (MCP) server with six tools, one of them an approval-gated fast-forward pull;
- deterministic engine tours and skill-graph reports;
- a destructive-command safety hook.

A maintainer runs it on a workstation that holds several engine checkouts. CI runs a subset of the same checks.

It follows these standards:

- JSON Schema 2020-12 for every contract and catalogue schema, and Semantic Versioning for releases.
- The Model Context Protocol for its server, and the plugin formats of Claude Code, Codex, Gemini CLI and OpenCode.
- The OWASP Application Security Verification Standard (ASVS) 5.0 path-handling controls, as a design analogue in its plugin threat model.

Its outputs are:

- engine handoff records, validated against [`core/contracts/handoff.yaml`](core/contracts/handoff.yaml);
- installed engine files with an ownership manifest, and generated plugin manifests;
- validator and drift-check evidence;
- contract and Tier-3 behavioural evaluation reports;
- engine tours in Markdown and JSON, and a report-only skill graph with a fan-in report;
- explicit `NOT_ASSESSED` records wherever a check cannot run.

It does not hold domain skills, and it writes to an engine only when you ask. `git pull --ff-only` needs an explicit request on a clean `main`. `--render` writes a closed list of derived fields.

## Find the right tool

| I want to | Use |
|---|---|
| Decide which engines own a task | [`catalog/engines.yaml`](catalog/engines.yaml) and the [engine orchestrator](core/instructions/engine-orchestrator.md) |
| See whether the engines drifted from the shared rules | `python3 -X utf8 scripts/render_host_files.py --check --engines-root <folder>` |
| Scan every public repository for settings files, keys and workstation paths | `python3 -X utf8 scripts/check_public_hygiene.py --engines-root <folder>` |
| Compare the shared hook files in every engine | `python3 -X utf8 scripts/check_hook_copies.py --engines-root <folder>` |
| Refresh the `released_commit` pins | `python3 -X utf8 scripts/refresh_released_commits.py --write --engines-root <folder>` |
| Install one engine without the plugin system | `node scripts/install-engine.js install --engine <path-to-engine> --scope user --dry-run` |
| Check the catalogue against its schema | `python3 -X utf8 scripts/validate-contracts.py --schema schemas/engine-catalog.schema.json --instance catalog/engines.yaml` |
| Read a generated tour of an engine | [`docs/engine-tours/`](docs/engine-tours/) |
| Find principles that recur across an engine's skills | the [`rules-distill`](skills/rules-distill/SKILL.md) skill |
| Measure how readable a README is | `python3 -X utf8 scripts/readme_metrics.py --check README.md` |
| Check that a README rewrite lost no link, command or anchor | `python3 -X utf8 scripts/check_readme_preservation.py . main <branch>` |

Every command above only reads, except `refresh_released_commits.py --write` (it edits the pins in `catalog/engines.yaml`) and an `install-engine.js` run without `--dry-run`. [`docs/operations/package-tools-reference.md`](docs/operations/package-tools-reference.md) describes every tool group in full.

## How it works

- **The catalogue.** [`catalog/engines.yaml`](catalog/engines.yaml) holds each engine's id, repository, folder, router, manifest and declared validators. Catalogue paths are folder names, not locations.
- **The locator.** [`scripts/lib/engine_roots.py`](scripts/lib/engine_roots.py) finds each checkout from repeatable `--engines-root` folders and the `CHWEZI_ENGINES_ROOT` variable. It matches the catalogue `path`, repository, id or `aliases` (former folder names).
- **Missing engines.** A missing or ambiguous engine is `NOT ASSESSED`, never a pass.
- **The orchestrator.** It picks the smallest set of engines for a task. It records ownership, sequence, evidence boundaries, blockers and the next action in a handoff record.
- **The checks.** Each check reads the engines and reports. A check that cannot run exits 3. Write actions are separate flags and refuse when an engine is dirty or off `main`.
- **The safety rules.** [`core/policies/safety-boundaries.md`](core/policies/safety-boundaries.md) is binding: read-only by default, approval for writes, and the destructive-command hook in `hooks/`.

## What is inside

### Skill

| Category | Skill | What it does |
|---|---|---|
| Maintenance | [`rules-distill`](skills/rules-distill/SKILL.md) | Scans one engine's skills for principles that recur in two or more skills and are absent from `rules/`. Proposes promotions for explicit approval; never edits `rules/` itself. |

Count: Maintenance 1. Total: **1 active `SKILL.md`**. Domain skills live only in the eleven engine repositories.

### Coordination workflows

| Workflow | Canonical instruction | What it does | Output contract |
|---|---|---|---|
| Engine orchestrator | [`engine-orchestrator.md`](core/instructions/engine-orchestrator.md) | Selects the smallest relevant set of engines and records ownership, sequence, evidence boundaries, blockers and next action. | [`handoff.yaml`](core/contracts/handoff.yaml) |
| Engine maintainer | [`engine-maintainer.md`](core/instructions/engine-maintainer.md) | Inspects status, branch and upstream; permits only an approved `git pull --ff-only` on a clean `main`. | [`maintenance-result.yaml`](core/contracts/maintenance-result.yaml) |
| Engine validator | [`engine-validator.md`](core/instructions/engine-validator.md) | Runs only the validator commands declared in the catalogue; missing evidence is `NOT_ASSESSED`. | [`validation-result.yaml`](core/contracts/validation-result.yaml) |
| Capability negotiator | [`capability-negotiator.md`](core/instructions/capability-negotiator.md) | Records which host capabilities are present and which degraded mode applies. | [`capability-profile.schema.json`](schemas/capability-profile.schema.json) |

Codex wrappers for the first three are in [`agents/`](agents/). Other host adapters are in [`adapters/`](adapters/).

### Tools by function

| Function | Main tools | In short |
|---|---|---|
| Registry | [`catalog/engines.yaml`](catalog/engines.yaml), [`validate-contracts.py`](scripts/validate-contracts.py) | Engine ids, paths, routers and declared validators; schema checks for every YAML or JSON instance. |
| Discovery | [`discover-engine.ps1`](scripts/discover-engine.ps1), [`detect-capabilities.py`](scripts/detect-capabilities.py) | Finds the Git root, catalogue entry and router for a path; detects host capabilities without changing anything. |
| Install and packaging | [`install.sh`](scripts/install.sh), [`install-engine.js`](scripts/install-engine.js), [`generate-plugin-manifest.js`](scripts/generate-plugin-manifest.js) | Install, update and remove the package or one engine with ownership records; generate plugin manifests. |
| Drift control | [`render_host_files.py`](scripts/render_host_files.py), [`catalog/shared-assets.yaml`](catalog/shared-assets.yaml) | Checks bridge files, invariants, versions, hooks, shared-asset copies, pin lag and router wording in every repository. |
| Portfolio hygiene | [`check_public_hygiene.py`](scripts/check_public_hygiene.py), [`catalog/hygiene-policy.yaml`](catalog/hygiene-policy.yaml) | Read-only scan for settings files, key files, credential-shaped strings and workstation paths. Never prints a secret. |
| Shared hook files | [`check_hook_copies.py`](scripts/check_hook_copies.py) | Compares every engine and installed plugin copy of four hook files with this package's canonical copy. |
| Release pins | [`refresh_released_commits.py`](scripts/refresh_released_commits.py) | Reports, or with `--write` refreshes, each engine's `released_commit` pin. Refuses when an engine is dirty or off `main`. |
| Routing evaluation | [`lexical_routing.py`](scripts/lexical_routing.py), [`validate-routing-baseline.py`](scripts/validate-routing-baseline.py) | A lexical routing index, cross-engine ownership oracles and a ratchet that only raises routing floors. |
| Contract and behavioural evaluation | [`run-contract-evals.py`](evals/runners/run-contract-evals.py), [`run_behavioural_eval.py`](scripts/run_behavioural_eval.py) | 77 deterministic cases; a Tier-3 runner whose zero-spend gate refuses model calls unless allowed. |
| Orientation | [`generate_engine_tour.py`](scripts/generate_engine_tour.py), [`skill_graph.py`](scripts/skill_graph.py) | Deterministic engine tours and a report-only skill graph that is never a routing input. |
| MCP server | [`mcp-server/`](mcp-server/) | Six tools. The pull tool needs a confirmation token; no tool accepts a command string from the model. |
| Safety | [`hooks/destructive-bash-gate.js`](hooks/destructive-bash-gate.js), [`hooks/hooks.json`](hooks/hooks.json) | A `PreToolUse` gate that blocks destructive shell and Git commands. |
| README quality | [`readme_metrics.py`](scripts/readme_metrics.py), [`check_readme_preservation.py`](scripts/check_readme_preservation.py) | Measure readability against the limits in the [README standard](docs/operations/readme-standard-2026-10-31.md); report links, commands and anchors a rewrite lost. |

The remaining groups (portfolio contracts, skill metadata and integrity, project context, usage scan, portfolio baseline) are in the [full tool reference](docs/operations/package-tools-reference.md).

### Coordination cards

These three cards are checked by `scripts/validate-kaizen-cards.py`:

- [`agentic-h2-readiness-card.md`](docs/operations/agentic-h2-readiness-card.md): H2 readiness and agentic-literacy card.
- [`three-horizon-ai-adoption-card.md`](docs/operations/three-horizon-ai-adoption-card.md): three-horizon adoption and frontier card.
- [`task-runbook-and-integration-evidence.md`](docs/operations/task-runbook-and-integration-evidence.md): task runbook and integration evidence card.

## Install and update

**Prerequisites**, taken from the adapter guides and scripts:

- Git, and Windows PowerShell 5.1 or 7+, or a POSIX shell.
- Python 3.11 or later for the validators, evaluators and drift checker. Python 3.14 was used for the 31 October 2026 measurements.
- Node.js 20 or later for the shared installer, the safety hook and the MCP server. The MCP server also needs npm.
- `PyYAML` for the Python checks, `jsonschema` for the contract validators, and `pytest` for the test suite. [Validation](#validation) says which check needs what.

Commands use `python3`. On a Windows host, `python` or `py -3` stands in.

### Claude Code plugin marketplace

Add the suite marketplace, then install the coordinator, a domain engine, or both. Each plugin installs fully on its own; the coordinator is optional.

```text
/plugin marketplace add peterbamuhigire/chwezi-engine-agents
/plugin install chwezi-suite@chwezi
/plugin install sdlc-documentation@chwezi
```

Marketplace plugin names: `chwezi-suite`, `sdlc-documentation`, `business-plan`, `website`, `social`, `linux`, `proposal`, `engineering`, `accounting`, `design-engine`, `research` and `windows-admin`.

The `chwezi-suite` plugin ships the `rules-distill` skill and the destructive-command hook. Set the plugin option `hooks_enabled` to `false` to keep the skill without hook enforcement.

### Host adapters

The adapters cover Codex, Claude Code, Gemini CLI, OpenCode, a generic host and MCP. From a clone, install the coordination package for one host.

The installer writes `.skills-engine-agents-install.json`. It refuses an unmanaged non-empty destination. It refuses to overwrite locally modified files unless `-Force` is given after review.

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

- `update.sh` calls `install.sh` directly, and the committed file mode of `install.sh` is 100644. On a fresh clone `update.sh` exits 126 with `Permission denied`.
  - Run `sh scripts/install.sh --host <host> --destination <folder>` instead.
  - Over a managed copy that exits 0. Over a locally modified file it refuses (exit 1) unless `--force` is given after review.
- `uninstall.sh --force` removed every managed file (exit 0) and left the empty folders behind.

Codex reads the package through `.codex-plugin/plugin.json`. The plugin name `skills-engine-agents` is kept on purpose; see [Decisions waiting for the maintainer](#decisions-waiting-for-the-maintainer).

Host-specific steps are in [`docs/adapters/`](docs/adapters/) and the publication routes in [`docs/distribution.md`](docs/distribution.md).

### Standalone engine install

This route needs no plugin system. The shared installer copies one engine's skills, and its agents, commands and hooks where present, into user scope (`~/.claude`) or project scope (`.claude`). It records a content hash for every file it writes.

```sh
node scripts/install-engine.js install --engine <path-to-engine> --scope user --dry-run
node scripts/install-engine.js install --engine <path-to-engine> --scope project
node scripts/install-engine.js doctor
node scripts/install-engine.js uninstall --engine <engine-name>
```

### MCP server (optional)

Build it, then copy [`mcp-server/.mcp.json.example`](mcp-server/.mcp.json.example) into the host's MCP configuration. Use real paths and a host-generated confirmation token.

```powershell
cd mcp-server
npm ci
npm test
npm run build
```

`npm ci` needs network access to the npm registry. On 2026-10-31 (Node.js 22.23.1) in a clean copy:

- `npm ci --ignore-scripts` exited 0 and `npm run build` exited 0.
- `npm test` passed 18 of 18 tests in 6 files.
- `npm audit` reports 13 vulnerabilities in the locked dependencies. That is the open finding F-01 under [Open findings](#open-findings).

### Manual route

Clone `https://github.com/peterbamuhigire/chwezi-engine-agents.git` and read [`AGENTS.md`](AGENTS.md). Claude Code reads it through `CLAUDE.md`.

Resolve the engine from [`catalog/engines.yaml`](catalog/engines.yaml), then read that engine's own router before any of its `SKILL.md` files. Skills are read directly; they are not registered with a host's native skill tool.

## Validation

Run every command from the package root. Results were measured on 2026-10-31 on Fedora, in scratch copies of this package (`PYTHONDONTWRITEBYTECODE=1`, `-p no:cacheprovider`).

The rows that read the engines were re-run after the engines merged their README work, so they read each engine's `main` of that day. The npm rows need network access and are from the earlier run the same day.

### Set-up

Engines are found through `CHWEZI_ENGINES_ROOT` (folders separated by `:` on POSIX and `;` on Windows) or a repeated `--engines-root`. A renamed checkout is found through its catalogue `aliases`, so no symlink is needed.

A few checks still take `--workspace-root` (marked "workspace" below). That folder has children named by the catalogue `path`, such as `chwezi-sdlc-documentation` and `chwezi-dev-engine`, with this package linked as `chwezi-engine-agents`.

- The research engine's catalogue path is `digital-research-engine`, which differs from its repository name.
- Where checkouts keep other folder names, build the folder from symlinks.

```sh
export CHWEZI_ENGINES_ROOT=<folder-with-engines>:<second-folder-with-engines>
WS=<folder-of-catalogue-named-links>
```

### Dependencies

- Python 3.11 or later with `PyYAML` (every Python check).
- `jsonschema` for `validate-contracts.py` and `project_context_doctor.py`. Both exit 3 (`NOT ASSESSED`) when it is absent.
- `pytest` for the test suite. `python3 -m pytest` fails with "No module named pytest" where it is absent.
- Node.js 20 or later for the hook tests, the marketplace check and the MCP server, plus npm and network access for `npm ci` and `npm audit`.
- PowerShell (`pwsh`) for every `.ps1` suite, and the Claude Code command-line tool for `claude plugin validate`.
- Versions used for the figures below: Python 3.14.8, PyYAML 6.0.3, jsonschema 4.26.0, pytest 9.0.3, Node.js 22.23.1, Claude Code 2.1.316.

A check that needs a sibling engine that is absent exits 3 with `NOT_ASSESSED`. For example, `validate-no-book-extractions.py` with no workspace folder reports 11 of 12 roots not assessed.

### Commands and results

| Command | Needs | Result on 2026-10-31 |
|---|---|---|
| `python3 -X utf8 -m pytest -p no:cacheprovider tests -q` | pytest, PyYAML, jsonschema | 352 passed, 3 skipped (note 1) |
| `python3 -X utf8 -m unittest discover -s tests -p 'test_*.py'` | PyYAML | Not a substitute for pytest: 293 tests ran, 2 failures and 8 errors, all environmental (note 2) |
| `python3 -X utf8 scripts/render_host_files.py --check` | PyYAML | Exit 1, 30 findings, 0 not assessed (note 3) |
| `python3 -X utf8 scripts/check_public_hygiene.py` (`--repo .` for this package alone) | PyYAML, git | Exit 1, 14 findings in four repositories; this package alone exits 0 with 0 findings (note 4) |
| `python3 -X utf8 scripts/check_hook_copies.py` | none beyond Python | Exit 0: 11 engine repositories and 8 installed plugin copies, 76 files, 0 differences (note 5) |
| `python3 -X utf8 scripts/refresh_released_commits.py` (check mode) | git | Exit 1: 11 engines, 11 not at HEAD, 5 to 9 commits behind. It exited 0 when the pins were refreshed in `f1e4565` (note 6) |
| `python3 -X utf8 scripts/validate-contracts.py --schema schemas/engine-catalog.schema.json --instance catalog/engines.yaml` | PyYAML, jsonschema | Exit 0. The same command with `schemas/adapter-manifest.schema.json` passes for each of the six `adapters/*/adapter.yaml` |
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
| `bash -n scripts/install.sh scripts/update.sh scripts/uninstall.sh` | bash | Exit 0 (syntax only; see the `update.sh` finding under Install and update) |
| `cd mcp-server && npm ci && npm run build && npm test` | Node.js, npm, network | Exit 0 at each step, 18 of 18 tests. `npm audit` exits 1 with 13 vulnerabilities (open finding F-01) |
| `claude plugin validate .` | Claude Code | Exit 0 with two warnings (note 7) |
| `python3 -X utf8 scripts/readme_metrics.py --check README.md` | none beyond Python | Exit 0: the six absolute limits are met by this README |
| `python3 -X utf8 scripts/check_readme_preservation.py . HEAD HEAD` | git | Exit 0: every `README.md` anchor linked in the repository and every in-page link resolves |

Notes on the table:

1. The three skips look for sibling folders named `chwezi-dev-engine` and `chwezi-design-engine` next to this package (`tests/test_run_behavioural_eval.py`, `tests/test_validate_rule_markers.py`). With those siblings present: 355 passed, 0 skipped. The two README tools added 90 tests to the 262 before them.
2. The failures are environmental: eight tests need `jsonschema`, two files import `pytest`, and the pytest-style files collect no tests. The count was 203 tests with the same 2 failures and 8 errors before the README tools.
3. Nineteen findings sit in the engines: 17 `shared-asset-unregistered-variant`, 1 `shared-asset-byte-drift` and 1 `plugin-exclusion-stale`. The other 11 are `released-commit-lag`. The count is the same through `--engines-root`, `CHWEZI_ENGINES_ROOT` and `--workspace-root`. [Open findings](#open-findings) names each one.
4. The 14 findings are Linux 11, dev engine 1, accounting 1 and design 1. There is no credential-shaped string.
5. The check also reads the host plugin folder (`~/.claude/plugins` by default; `--plugins-dir` overrides).
6. With `--write` it exits 2 and writes nothing when any engine is dirty or not on `main`. That was confirmed the same day against engine checkouts that held uncommitted files.
7. The warnings are: a root `CLAUDE.md` is not loaded as plugin context, and there is no plugin icon. `--strict` exits 1 on them.

### Not run on this host

These checks are `NOT_ASSESSED`:

- Every PowerShell suite, because there is no `pwsh`:
  - `tests/validate_catalog.ps1`, the three scripts in `tests/adapters/`, `tests/install/*.ps1`, `tests/security/*.ps1` and `tests/test_capability_fallbacks.ps1`;
  - `evals/runners/run-host-smoke-tests.ps1`;
  - `scripts/validate-portfolio-craft.ps1` and `scripts/validate-prompt-capability.ps1`, which take `-WorkspaceRoot` and carry a Windows default.
- The remote CI workflows (`.github/workflows/`).
- Any Tier 3 behavioural run. Paid model calls need `--allow-model-calls` and the maintainer's authority.
- Live-model routing, and a native install into Codex, Gemini CLI or OpenCode.

## Portfolio

Twelve public repositories make up the portfolio: the eleven domain engines in [`catalog/engines.yaml`](catalog/engines.yaml) and this package. Repository names were checked against the GitHub API on 2026-10-31.

- Three engines were renamed on GitHub while the checkouts on the maintainer's workstation kept their old folder names.
- The research engine's earlier name `digital-research-skills` now only redirects to `chwezi-research-engine`. It stays the research engine's catalogue id.
- The catalogue records each former folder name as an alias. The `origin` remote of a renamed checkout may still carry the old URL, which GitHub redirects.
- The dev and Linux engines sit in Claude Code's user skills folder on that workstation and the other nine in a separate engines folder. `--engines-root` and `CHWEZI_ENGINES_ROOT` take both.

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

About the scores:

- They are the pass-2 figures of 31 October 2026, read from each repository's `docs/kaizen/2026-10-engine-kaizen-pass-2/05-final-report.md`.
- Raw is the mean of the ten dimensions that engine rated (eleven for this package), as the report prints it. Capped is `min(raw, 65)`, the Portfolio Kaizen Standard's reporting ceiling. The cap binds only for Linux.
- They are reviewer judgements against named evidence, not audits. None reaches the 95 target.
- Linux's later lab wave (`docs/kaizen/2026-10-linux-lab-wave/05-final-report.md` in that repository) raised its raw mean to 77.9, still 65.0 capped.
- The SDLC report also prints 45 under a stricter initial cap set for the first cycle, whereas the Standard's cap gives 55.68.
- Each engine's own README keeps its open findings and its calendar. This package's summary of those calendars is under [Date-triggered gates across the portfolio](#date-triggered-gates-across-the-portfolio).

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
- [Hook canonical copy](docs/operations/hook-canonical-copy.md), [supply-chain policy](docs/security/supply-chain-policy.md), the [README standard](docs/operations/readme-standard-2026-10-31.md) and the [documentation index](docs/README.md).

## Quality and improvement

The package follows the Portfolio Kaizen Standard: measure, change, check and record. The published score is capped at 65 out of 100, and the plan targets 95. The evidence is in these folders:

- [`docs/kaizen/2026-10-engine-kaizen/`](docs/kaizen/2026-10-engine-kaizen/), 29 October 2026: scope, baseline scorecard and backlog. The cycle stopped after its second commit and has no final report.
- [`docs/kaizen/2026-10-engine-kaizen-pass-2/`](docs/kaizen/2026-10-engine-kaizen-pass-2/), 31 October 2026: scope and evidence, baseline scorecard, backlog, experiment log, validation record, final report and next cycle. Raw logs are under `evidence/`.
- [`docs/kaizen/2026-10-readme-kaizen/`](docs/kaizen/2026-10-readme-kaizen/readme-kaizen-record.md), 31 October 2026: the README readability cycle. It publishes no score.

Earlier audits, execution logs and plans are indexed in [`docs/README.md`](docs/README.md). What the cycle changed, with the commit and the check behind each change, is under [What the October 2026 kaizen improved](#what-the-october-2026-kaizen-improved).

**Latest published score.** Pass 2 ([final report](docs/kaizen/2026-10-engine-kaizen-pass-2/05-final-report.md)): raw 48.09 out of 100 (529 over eleven dimensions), published `min(raw, 65)` = 48.09. The frozen pass-2 baseline was 44.18.

- The 29 October scorecard printed a mean of 46.82, but its rows sum to 505, which is 45.91. That cycle has no final score.
- The 95 target is not met, and the open critical finding F-01 overrides the aggregate.
- The score is the cycle owner's judgement against named evidence, not an independent audit.

## Open findings

- **F-01, vulnerable MCP lockfile (critical, escalated).** `npm audit` in `mcp-server/` reports 13 vulnerabilities (6 moderate, 6 high, 1 critical) on 2026-10-31, the same count as on 29 October.
  - The pass-2 report records the critical entry (`proxy-addr`) as transitive and behind the HTTP transport that the stdio server does not import.
  - `zod`, also flagged, is used by the SDK at run time. Its exposure was not assessed.
  - The SDK pin 1.30.0 is behind 1.32.2. The fix is an `npm install` of two minor versions, which needs the maintainer's authority. The exact commands and the acceptance check are in [`06-next-cycle.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/06-next-cycle.md).
  - The MCP server is optional. Nothing else in the package depends on it.
- **The drift check exits 1 with 30 findings.** Re-run on 2026-10-31 as `python3 -X utf8 scripts/render_host_files.py --check --engines-root <folder> --engines-root <folder>`. Nineteen are engine-side.
  - 17 `shared-asset-unregistered-variant`: `routing_smoke_test.py` in six engines, `rules/common/core.md` in four, the `skill-writing` skill in five, and the design engine's `generate-plugin-manifest.js` and `install-engine.js`.
  - 1 `shared-asset-byte-drift` (the design engine's `install.sh`) and 1 `plugin-exclusion-stale` (the business-plan manifest's `country-context/*`).
  - There were 16 variants when pass 2 closed. The 17th is the social-media engine's `rules/common/core.md`, edited in `3075062` on 31 October after that.
  - Each variant needs a content review before its hash is registered with an owner and a reason in [`catalog/shared-assets.yaml`](catalog/shared-assets.yaml), after the last engine wave. The order is in `06-next-cycle.md`.
  - The other 11 are `released-commit-lag`: every pin is 5 to 9 commits behind its engine's HEAD, now that the engines have merged their README work. That is the pin rule working.
  - The lag clears when the pins are refreshed again with `scripts/refresh_released_commits.py --write`, after every engine is clean and on `main`.
  - The portfolio-drift CI job runs this check and the hygiene check, so it fails while either exits 1.
- **The hygiene check exits 1 with 14 findings in four repositories.**
  - Linux has 11: a tracked `.claude/settings.local.json` and ten live path lines.
  - The dev engine has 1 (a tracked `.claude/settings.local.json`) and the design engine has 1 (a path in `doctrine/design-doctrine.md` line 161).
  - Accounting has 1: 45 path lines in dated records against a ceiling of 44.
  - It found no credential-shaped string. A tracked file stays in public history after it is removed from the tree. Removing it from history needs a rewrite and force-push, which is the maintainer's decision.
- **Script defects found while documenting.** They are recorded in [`07-docs-followups.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/07-docs-followups.md).
  - `scripts/update.sh` exits 126 on a fresh clone (see Install and update).
  - CI runs neither `tests/security/install-engine-ownership.test.js` (it passes locally) nor the two `tests/security/install-*-preservation.ps1` scripts.
- **Not established.** No remote CI run of the edited workflows, no PowerShell run, no native install in a host, no Tier 3 behavioural run and no live-model routing. Routing figures are a lexical proxy.
- **Open work in the pass-2 backlog** ([`06-next-cycle.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/06-next-cycle.md)):
  - ten more scripts still need `--workspace-root` instead of the engine locator;
  - the release chain: plugin manifests read 1.1.0, `release/manifest.json` and the MCP package read 1.0.0, tag `v1.1.0` exists, `release.yml` still names `skills-engine-agents`, and there is no provenance manifest or signing;
  - the Codex layout and the Gemini adapter file name;
  - no routing fixtures for the coordinator's one skill;
  - 27 duplicate skill names and union skill metadata of 290,189 characters against a 60,000 budget (engine-side figures taken from the pass-2 evidence, not re-measured here).

## Decisions waiting for the maintainer

The full table, with defaults, is in [`06-next-cycle.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/06-next-cycle.md).

1. Authorise the MCP lockfile refresh for F-01 (default: the critical finding stays open).
2. Pin policy: keep allowance 0, so the drift check fails after any engine commit on a workstation, or set a standing `--pin-lag-max` (default: 0; skipped in shallow CI clones).
   - The pins were refreshed to the engines' `main` commits in `f1e4565` on 31 October and the check read 0 lag at those commits.
   - It read 11 findings later the same day, once the engines had moved.
3. Keep the Codex identity `skills-engine-agents` and the `.codex-plugin/` fallback layout, or migrate to a root `plugin.json` (default: unchanged).
4. Public history: dev and Linux still track `.claude/settings.local.json` (SDLC and design repaired the tree only). Removing it needs a rewrite and force-push (default: no rewrite).
5. Whether the hygiene policy may name the workstation account in a public repository (default: as is).
6. One version for the package: plugin manifests 1.1.0, `release/manifest.json` and the MCP package 1.0.0 (default: unchanged).
7. Retire or renew the two overdue documents: `portfolio-craft-standard-2026-09-04.md` (review 2026-10-04) and `domain-prompt-compilation-contract-2026-09-16.md` (review 2026-10-16) (default: both stay overdue).
8. Add a per-validator platform field to the catalogue schema (default: not added).

## Date-triggered gates across the portfolio

No check in this package reads the calendar.

- The only date logic is `project_context_doctor.py --today`, which compares a project's own `review_due`. That was searched in `scripts/`, `evals/`, `hooks/` and `mcp-server/src/`.
- Review dates written into documents and registers here are read by no validator. Examples are 2026-12-29 in `catalog/shared-assets.yaml` and the two overdue reviews above.

The engines are different. Their source-register gates fail on a date unless the sources are re-read first. The rows below come from each engine's README "Quality and improvement" section on `main`.

- The first failing date of each was confirmed on 2026-10-31 by running that engine's validator with a later date in a scratch clone.
- The exceptions are the design engine (see its row) and the proposal and business-plan engines. They have no such option and are as their READMEs state.
- Counts assume nothing is re-verified in between.

| Date | Engine | What happens |
|---|---|---|
| Already failing | Social media | `check_source_freshness.py` exits 1: five quarantined records stay `NOT_ASSESSED` until their primary text is read. Its CI job fails with it. |
| Already failing | Business plan | `refresh_evidence_register.py --check` exits 1: four register rows overdue (UBOS, KNBS, UNBS and the Bank of Uganda supervision page). |
| 2026-11-04 | Dev engine | `check_source_register.py` and its CI step first exit 1 on five records (Next.js release, support policy, upgrade guide and security notices). 2026-11-03 passes. |
| 2026-11-06 | Windows administration | `check_source_register.py` exits 1 with one finding: the policy review date 2026-11-05 has passed. 39 findings from 2026-11-11, when 35 URL rows pass the 90-day interval. |
| 2026-11-08 | Social media | Further records start to lapse: one on 2026-11-08, 20 by 2026-11-29 and 90 by 2026-12-30, on top of the five quarantined. |
| 2026-11-17 | Accounting Doctrine | The NSSF entry passes its recheck date. `tools/source_register_integrity.py` exits 1 (`INT-008`), two tests fail and the lookup tool refuses final use for NSSF. 2026-11-16 passes. |
| 2026-11-30 | Digital Research | The register gate exits 1 in `validate_source_currency.py`, `validate_engine.py` and CI: 11 findings, starting with four OpenAI platform records. 2026-11-29 passes. 13 findings from 2026-12-01. |
| 2026-11-30 | SDLC documentation | `validate_source_register.py` exits 1 with three findings (OpenAI plugin schema, OpenAI archive limit, Claude marketplace). 2026-11-29 passes. |
| 2026-12-01 | Proposal | `validate_skills.py` and `check_source_currency.py` exit 1 for all 14 register records. The gate passes through 2026-11-30, as the engine's README states; neither script has a date option. |
| 2026-12-01 | Website | `validate-source-registers.py` exits 1 with 8 findings (the October standards register, three of its claims and four standards-table rows). `validate-search-doctrine.py` follows from 2026-12-06. 2026-11-30 passes. |
| 2026-12-01 | Linux | The CI step "Check bounded hygiene regressions" (`kaizen_metrics.py`) fails on ten source rows with a review-by date of 2026-11-30. 2026-11-30 passes. |
| 2026-12-01 | Business plan | Two more rows become overdue, six in all; 15 by 2027-01-30. |
| 2026-12-20 | Design engine | Warnings only: `validate_design_catalog.py` lists 13 catalogue records as stale and exits 0. No design validator fails on a date. |

Notes on the calendar:

- The five quarantined social-media records are `UG-DPPR-2021`, `UG-COPYRIGHT-2026`, `KE-DP-GENERAL-2021`, `RW-DPP-2021` and `ITU-INTERNET-USAGE`.
- The design engine's next review dates (2026-12-29 font watchlist, 2027-01-27 full re-audit) are read by no validator, as its README states. That was not re-run here.
- Later batches (2027-01-27 to 2027-03-30 and beyond, in every engine except design) are in each engine's README.
- Re-audit dates written in the evidence rather than enforced include this package's own on 2026-11-13, Windows on 2026-11-05, Linux on 2026-11-07, research on 2026-11-27 and most others on 2026-11-30.

## What the October 2026 kaizen improved

Two cycles ran on this package. The 29 October cycle froze a baseline and a backlog and stopped. The 31 October cycle (pass 2) kept nine backlog items, reverted none and escalated one critical finding.

The root cause, from [`02-improvement-backlog.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/02-improvement-backlog.md): the portfolio's own checks assumed one Windows workspace folder with catalogue folder names. On any other layout most of them could not run, so drift went unseen.

The fix was a shared engine locator, then one check per recurring drift class. Each check has a control that fails when the check is broken.

How to read the figures:

- Every hash was confirmed on `main` with `git show --stat`.
- Every "re-measured" figure was run again on 2026-10-31 in a scratch copy against the engines at their pinned `main` commits.
- Figures marked "evidence" come from [`03-experiment-log.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/03-experiment-log.md) or [`04-validation-record.md`](docs/kaizen/2026-10-engine-kaizen-pass-2/04-validation-record.md). They were not re-measured.
- Real CI never ran on any of this (no push), and no PowerShell suite ran.

The changes follow in four parts: [correctness fixes](#kept-changes-correctness-fixes), [new checks](#kept-changes-new-checks), [documentation and README work](#kept-changes-documentation-and-readme-work), and [scores and measures](#scores-and-measures).

## Kept changes: correctness fixes

- **CI and the supply-chain policy disagreed with the release workflow (K8, `6763854`).**
  - CI skipped 7 of 19 Python test files and every hook test. `docs/security/supply-chain-policy.md` claimed a provenance manifest, checksum verification and a publication gate that no workflow had.
  - Now the ubuntu job runs every Python test file and both hook tests. It also scans this package for settings files, key files, credential-shaped strings and host paths.
  - The portfolio job adds the hook-copy and hygiene checks. The release workflow calls the validate workflow first. The policy lists what is not yet true.
  - Check: the workflow YAML was parsed and each added command replayed locally (exit codes in `evidence/k8-ci-local-replay.txt`). The workflows themselves have not run.
- **The MCP validation tool reported a validator that could not start as a failure (K7, `0267684`).**
  - An exit code of 126 or 127 from a declared validator came back as `FAIL`. The discovery test asserted branch `main`, so it failed on any other branch.
  - Exit 126 and 127 are now `NOT ASSESSED`, and the test compares with the checkout's own branch.
  - MCP tests: 15 of 16 before (evidence), 18 of 18 after (re-measured). The two new tests fail against the old `engine-validation.ts` (evidence).
- **`skill_graph.py` crashed on a linked layout, and most portfolio scripts needed a hand-built workspace (K1, `eb8dae1`, `9329a82`).**
  - It raised a `ValueError` on any checkout outside one workspace folder.
  - The new locator finds engines through repeatable `--engines-root`, `CHWEZI_ENGINES_ROOT` and catalogue `aliases` for the four renamed engines. The drift check takes `--engines-root`.
  - Tests: 13 locator tests and 5 drift-layout tests (re-counted: 13 in `tests/test_engine_roots.py`).
  - On the real two-parent layout the drift check gave the same output as the hand-built symlink workspace (evidence: 37 findings each way). Today the three routes all give 30 findings (re-measured).
  - The graph script exits 0 where it crashed (evidence: 1,105 nodes, 12,035 edges). Ten more scripts still need `--workspace-root`.
- **This package's router, one adapter note and one script default carried workstation paths (K6, `d4450f7`).**
  - Package-side machine-path findings: 7 before (evidence), 0 after (`check_public_hygiene.py --repo .`, re-measured).
  - The Windows-only defaults in two PowerShell scripts are allow-listed in `catalog/hygiene-policy.yaml` with a written reason, not fixed. Editing PowerShell cannot be checked without `pwsh`.
- **Two suite marketplace counts were stale (K9, `f099c75`).** The business-plan and design-engine entries now read 137 and 102. `generate-plugin-manifest.js --check-marketplace`: 21 ok and 2 drift before (evidence), 23 ok and 0 drift after (re-measured).
- **A published figure did not match its own rows.** The 29 October scorecard printed a mean of 46.82 over rows that sum to 505, which is 45.91. The pass-2 report states the corrected comparison, 45.91 to 48.09 raw. This corrects the record (`dc743e3`); it is not a score gain.

## Kept changes: new checks

Each check was added with a control: a case built to fail.

- **Public-repository hygiene (K2, `5d7dbc8`, `2259900`).** `scripts/check_public_hygiene.py` and `catalog/hygiene-policy.yaml` scan tracked files for per-user settings files, `.env` and key files, credential-shaped strings and workstation paths. Record ceilings only fall, and output is redacted.
  - 26 tests. Seven single-line mutations were each caught, one only after a test was added (evidence).
  - The first live run found 26 findings in 7 repositories, two of them tracked `.claude/settings.local.json` files in public repositories (evidence).
  - Today it finds 14 in four (re-measured), because engines repaired some. It found no credential-shaped string at either run.
- **Canonical hook copy and installed copies (K3, `0d539fa`).** `scripts/check_hook_copies.py` and `docs/operations/hook-canonical-copy.md` name this package as the source of four hook files. They compare all eleven engine copies and the installed plugin copies.
  - 13 tests, five mutations caught (evidence).
  - Re-measured: 11 repositories and 8 installed copies, 76 files, 0 differences.
- **`released_commit` pins (K4, `2af312e`, applied in `f1e4565`).** Pins lagged 11 of 11 engines by 28 to 51 commits with no check (evidence).
  - `scripts/refresh_released_commits.py` writes the pins. It refuses, and writes nothing, if an engine is dirty, missing or off `main`. The drift check reports the lag.
  - 21 tests on throw-away repositories, six mutations caught (evidence).
  - `f1e4565` changed the eleven pin lines only (`git show --stat`). The check then exited 0 with 0 engines behind (re-measured at those commits).
  - A `--write` run against the live catalogue by mistake during testing was restored with `git restore` and not committed (evidence).
- **Catalogue validators against engine manifests (K5, `608f466`).** Ten manifest commands (website six, Windows three, proposal one) were missing from the catalogue.
  - Two rules now fail on a catalogue validator whose script is absent and on a manifest command the catalogue lacks. Both read 0 after the refresh.
  - 8 tests, four mutations caught (evidence).
- **Path-free router wording and a renderer (K6, `d4450f7`).** `templates/agents-blocks/` holds one wording for three managed router sentences. The rules `router-host-path` and `router-former-name` flag workstation paths and pre-rename names in router files. `--render-router-blocks` rewrites the legacy form.
  - The rule flagged exactly the accounting (2 lines) and social (3 lines) routers. The renderer was idempotent on scratch copies.
  - Those engines then applied it in their own documentation waves (their commits `f405a5b` and `830f154`). The drift check now reports no router finding (re-measured).
  - 14 tests, five mutations caught (evidence).
- **Tests.** 101 new `unittest` tests for the six checks (evidence). 73 sit in four new files (re-counted: 13, 26, 13 and 21).
  - `unittest discover` collected 102 tests at baseline and 203 after (evidence).
  - A real pytest run at the pass-2 close gave 262 passed and 3 skipped, or 265 passed with sibling folders present (re-measured). The baseline had no pytest on this host, so seven pytest-style files ran only through a labelled stand-in.

## Kept changes: documentation and README work

- **The router and the changelog teach the new checks (`903243e`).** The router names the locator, the hygiene and hook-copy checks, the pin script and the renderer. The changelog records the pass.
- **Evidence discipline.** The baseline was frozen before any change (`39ee3a1`) and the backlog was selected from it (`c887dfa`). The experiment log, validation record, final report, next-cycle file and raw logs followed (`dc743e3`, `4b9a30e`, `3dde18e`).
- **The documentation wave** (`ce48567` to `c9d155b`, now on `main`) added the validation table with dependencies, the portfolio table, the calendar, a documentation index and the follow-ups file. It removed stale statements, measured the installer and found the `update.sh` defect listed under Install and update.
- **README readability (31 October 2026).** A scoped cycle, recorded in [`readme-kaizen-record.md`](docs/kaizen/2026-10-readme-kaizen/readme-kaizen-record.md). It published no score.
  - `scripts/readme_metrics.py` and `scripts/check_readme_preservation.py` became package tools with 90 new tests. Forty-seven one-line mutations were each caught.
  - [`readme-standard-2026-10-31.md`](docs/operations/readme-standard-2026-10-31.md) sets the shared structure, limits and preservation rules for every README in the portfolio, with measured results for the eleven engines.
  - This README gained a front door, a contents list and plain-English prose. The tool table went to [`package-tools-reference.md`](docs/operations/package-tools-reference.md) and the reference lists to [`references.md`](docs/references.md).

## Scores and measures

| Measure | Before | After | Source |
|---|---:|---:|---|
| Raw score, eleven dimensions | 44.18 (pass-2 baseline); 45.91 on 29 October, corrected | 48.09 | final report |
| Published, `min(raw, 65)` | 44.18; 45.91 | 48.09 | final report |
| Drift check findings | 21 engine-side | 19 at the pinned commits; 30 in a live re-run (19 plus 11 pin lag) | evidence; re-measured |
| Hygiene findings | none measurable | 14 in four repositories (26 in seven on the first run) | evidence; re-measured |
| Pin lag | 11 of 11 engines | 0 of 11 at the pinned commits; 11 of 11 in a live re-run, 5 to 9 commits | evidence; re-measured |
| Suite marketplace drift | 2 | 0 | evidence; re-measured |
| Hook copies differing | not checked for installed copies | 0 of 76 files | re-measured |
| MCP tests | 15 of 16 | 18 of 18 | evidence; re-measured |
| Engine Eval Readiness, strict | 19.4 | 25.4 | evidence |

At the pass-2 close the drift check read 37 findings, 16 of them newly visible through the new rules.

Not counted as improvements: F-01 (open), the 17 unregistered shared-asset variants (engine-side, listed above), and anything that needs a CI run or a PowerShell host.

The pass-2 changes also make pre-existing defects visible, so the drift and hygiene checks exit 1 until the engines are reconciled. That is the intended signal.

## References

The sources this package cites are listed in [`docs/references.md`](docs/references.md). The page holds 12 repositories from which methods were adapted, 13 groups of standards and official sources, and 6 entries under websites and articles. No books are cited.

All adaptations are paraphrased or re-implemented; no text or code is copied. The [third-party skill register](docs/security/third-party-skill-register.json) records a further 60 repositories screened by desk review on 29 Sep 2026 as sources of ideas. Nothing from them was installed.

The lifecycle map above names its one adapted source, addyosmani/agent-skills (MIT, commit `2686b62`). The [source repository](https://github.com/peterbamuhigire/chwezi-engine-agents) is on GitHub.

## Contributing, author and licence

- **Contributing:** read [`CONTRIBUTING.md`](CONTRIBUTING.md) before you change a script, a contract or a workflow. It lists the checks to run and the rules for AI agents.
- **Editing a README:** follow the [README standard](docs/operations/readme-standard-2026-10-31.md) and run the two README checks first (see [Find the right tool](#find-the-right-tool)).
- **Author:** Peter Bamuhigire.
- **Licence:** MIT. See [`LICENSE`](LICENSE).
