# Chwezi Engine Agents

Chwezi Engine Agents is the coordination and shared-tooling package for the Chwezi skills portfolio of eleven independently installable domain engines: requirements, business plans, websites, digital marketing, Linux administration, proposals, engineering, accounting, design, research and Windows administration. It routes a task to the smallest set of engines that owns it, records the handoff between them, and keeps every engine's registry entry, plugin manifests, host bridge files and validators consistent. Its functions are routing and handoff, the engine catalogue, shared installation and manifest generation, portfolio drift control, contract and behavioural evaluation, a read-only Model Context Protocol (MCP) server, deterministic engine tours and skill-graph reports, and a destructive-command safety hook. It holds no domain doctrine; each engine remains the only source of its own skills.

The package follows JSON Schema 2020-12 for every contract and catalogue schema, Semantic Versioning for releases, the Model Context Protocol for its server, and the host plugin formats documented by Claude Code, Codex, Gemini CLI and OpenCode; its plugin threat model uses OWASP ASVS 5.0 path-handling controls as a design analogue. Its outputs are engine handoff records validated against `core/contracts/handoff.yaml`, installed engine files with an ownership manifest, generated plugin manifests, validator and drift-check evidence, contract and Tier-3 behavioural evaluation reports, engine tours in Markdown and JSON, a report-only skill graph and fan-in report, and explicit `NOT_ASSESSED` records wherever a check cannot run. It is for people who maintain one or more Chwezi engine checkouts, and for teams that need consistent routing, installation and validation across several engines. Domain engines install and work without it.

## Installation

Prerequisites, taken from the adapter guides and scripts: Git; Windows PowerShell 5.1 or 7+, or a POSIX shell; Python 3.11 or later for the validators, evaluators and drift checker; Node.js 20 or later for the shared installer, the safety hook and the MCP server (npm is also needed for the MCP server).

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

Codex reads the package through `.codex-plugin/plugin.json` (plugin name `skills-engine-agents`). Host-specific steps are in [`docs/adapters/`](docs/adapters/) and the publication routes in [`docs/distribution.md`](docs/distribution.md).

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
| Drift control | [`render_host_files.py`](scripts/render_host_files.py), [`catalog/shared-assets.yaml`](catalog/shared-assets.yaml) | Checks every public repository's `CLAUDE.md` bridge, canary invariants, version consistency, model-ID corruption, byte-order marks, hook configuration and shared-asset copies; `--render` writes only a closed list of derived fields. |
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
