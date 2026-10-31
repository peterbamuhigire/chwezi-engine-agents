# Documentation index

This folder holds the contracts, policies, evidence and generated reports of the coordination package. The package overview, installation, validation commands, the quality status and an account of what the October 2026 kaizen improved ([README](../README.md#what-the-october-2026-kaizen-improved)) are in the [README](../README.md); the runner-neutral router is [`AGENTS.md`](../AGENTS.md). Records dated before 31 October 2026 keep the names and paths they were written with (for example `srs-skills` and `design-system-skills` for the engines now called `chwezi-sdlc-documentation` and `chwezi-design-engine`).

## Current contracts and policies

| Path | What it holds |
|---|---|
| [`architecture/`](architecture/) | [Compatibility contract](architecture/compatibility-contract.md), [host, model and capability matrix](architecture/host-model-capability-matrix.md) and [ADR-001, hosts versus models](architecture/decision-records/ADR-001-hosts-versus-models.md). |
| [`adapters/`](adapters/) | One installation guide per host: [Claude Code](adapters/claude-code.md), [Codex](adapters/codex.md), [Gemini CLI](adapters/gemini-cli.md), [OpenCode](adapters/opencode.md), [generic](adapters/generic.md) and [MCP](adapters/mcp.md). |
| [`distribution.md`](distribution.md) | Versioning, release and publication routes. |
| [`runtime-skill-budget.md`](runtime-skill-budget.md) | How to run the runtime skill metadata budget validator and what its default limits are. |
| [`security/`](security/) | [Permission model](security/permission-model.md), [threat model](security/threat-model.md), [plugin and installer threat model](security/plugin-threat-model.md), [supply-chain policy](security/supply-chain-policy.md) with its [register](security/supply-chain-register.json) and the [third-party skill register](security/third-party-skill-register.json); `sbom/` holds the MCP server's software bill of materials. |
| [`schemas/`](schemas/) | The system administration activity record schema. |
| [`operations/`](operations/) | Operating contracts and records. Contracts: [Claude bridge](operations/claude-bridge-contract.md), [portfolio craft standard](operations/portfolio-craft-standard-2026-09-04.md), [skill lifecycle and invocation](operations/skill-lifecycle-and-invocation.md), [project context](operations/project-context-contract.md), [portable links rule](operations/portable-links-rule.md), [upgrade policy](operations/upgrade-policy.md), [incident runbook](operations/incident-runbook.md) and [hook canonical copy](operations/hook-canonical-copy.md). The three coordination cards checked by `scripts/validate-kaizen-cards.py` are [H2 readiness](operations/agentic-h2-readiness-card.md), [three-horizon adoption](operations/three-horizon-ai-adoption-card.md) and [task runbook and integration evidence](operations/task-runbook-and-integration-evidence.md). |

The domain prompt compilation contract and the portfolio craft standard carry review dates (2026-09-16 and 2026-09-04 files, review 2026-10-16 and 2026-10-04) that have passed; see the decisions in the [README](../README.md#quality-and-improvement).

## Improvement records

| Path | What it holds |
|---|---|
| [`kaizen/2026-10-engine-kaizen-pass-2/`](kaizen/2026-10-engine-kaizen-pass-2/) | The 31 October 2026 cycle: scope and evidence, baseline scorecard, backlog, experiment log, validation record, [final report](kaizen/2026-10-engine-kaizen-pass-2/05-final-report.md), [next cycle](kaizen/2026-10-engine-kaizen-pass-2/06-next-cycle.md), [documentation follow-ups](kaizen/2026-10-engine-kaizen-pass-2/07-docs-followups.md) and raw logs under `evidence/`. |
| [`kaizen/2026-10-engine-kaizen/`](kaizen/2026-10-engine-kaizen/) | The 29 October 2026 cycle: scope, baseline scorecard and backlog. It stopped after its second commit and has no final report. |
| [`audits/2026-09-29-m10-reaudit/`](audits/2026-09-29-m10-reaudit/) | The 29 September 2026 measured re-audit ([executive summary](audits/2026-09-29-m10-reaudit/00-executive-summary.md), [master scorecard](audits/2026-09-29-m10-reaudit/09-master-scorecard.md), [roadmap](audits/2026-09-29-m10-reaudit/10-roadmap-to-world-class.md)). |
| `operations/kaizen-2026-*.md`, `operations/m10-kaizen-execution-2026-09-29.md`, `operations/skills-kaizen-execution-2026-09-26.md` | Dated kaizen and execution records from September 2026; `operations/m10-kaizen-evidence/` and `operations/skills-kaizen-evidence/` hold their evidence. |
| [`operations/engine-renames-2026-09-29.md`](operations/engine-renames-2026-09-29.md) | Evidence for the 29 September 2026 engine renames. |
| [`updates/`](updates/) | [Coordinator MCP dependency security follow-up](updates/2026-09-28-mcp-dependency-security-follow-up.md) (28 September 2026). |
| [`plans/aug-25/`](plans/aug-25/README.md), [`superpowers/`](superpowers/) | The August 2026 multi-host plan (13 phases) and the original design and plan. Historical; the implementation has moved on. |

## Generated reports

| Path | What it holds |
|---|---|
| [`engine-tours/`](engine-tours/) | A Markdown and a JSON tour for each of the twelve repositories, written by `scripts/generate_engine_tour.py` and read by the MCP server's `engine_tour` tool. |
| [`skill-graph/skill-graph.json`](skill-graph/skill-graph.json) | The report-only skill graph from `scripts/skill_graph.py`. It is never a routing input. |
