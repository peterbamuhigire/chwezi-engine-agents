# Chwezi Engine Agents

`chwezi-engine-agents` is the coordination and shared tooling layer for the Chwezi skills suite. It routes work to independently installable engines, keeps their registry and plugin manifests aligned with their skill trees, provides shared install and validation tools, and distributes a destructive-command safety hook. It does not replace domain engines or provide their specialist doctrine.

The package is for people maintaining one or more Chwezi engine checkouts and teams that need consistent routing, installation, and validation. Its outputs include engine handoffs, installed skill/plugin files, generated manifests, validator evidence, and documented `NOT ASSESSED` results when a check cannot run. The coordination contract assigns requirements, engineering, design, research, and finance questions to their respective engines.

## Installation

For Claude Code, add the suite marketplace and install the coordinator or only the domain plugins you need:

```text
/plugin marketplace add peterbamuhigire/chwezi-engine-agents
/plugin install chwezi-suite@chwezi
```

For a local checkout or another supported host, install an engine with Node.js 18 or later:

```sh
node scripts/install-engine.js install --engine <path-to-engine>
```

The shared installer also supports project/user scope, dry-run, doctor, update, and uninstall modes. Review its help and the target paths before choosing a scope. Domain engines can be installed on their own; the coordinator is optional.

## Capabilities

| Category | Included capability | Source |
|---|---|---|
| Routing and handoffs | Selects the smallest relevant engines and records ownership, sequence, evidence boundaries, blockers, and next action. | [`core/instructions/engine-orchestrator.md`](core/instructions/engine-orchestrator.md) |
| Engine registry | Records engine IDs, repository/check-out paths, router files, manifests, and declared validator commands for the eleven registered domain engines. | [`catalog/engines.yaml`](catalog/engines.yaml) |
| Install and packaging | Installs and removes an engine, generates plugin manifests from discovered skill trees, and protects unmanaged or modified destination files by default. | [`scripts/`](scripts/) |
| Validation | Runs declared contract, lifecycle, catalog, runtime-budget, and portfolio checks; missing evidence remains `NOT ASSESSED`. | [`scripts/`](scripts/) |
| Safety and shared rules | Distributes a Bash destructive-command gate and provides a skill for proposing recurring principles for shared rules. | [`hooks/`](hooks/), [`skills/rules-distill/`](skills/rules-distill/) |
| Coordination standards | Defines evidence expectations and craft practices for cross-engine work. | [`docs/operations/`](docs/operations/) |
| Project context | `PROJECT.md` contract (durable truth and pointers to each engine's own context) with a read-only doctor. | [`docs/operations/project-context-contract.md`](docs/operations/project-context-contract.md), [`scripts/project_context_doctor.py`](scripts/project_context_doctor.py) |
| Orientation and structure | Deterministic engine tours, skill fan-in report and a report-only skill graph; the MCP server serves tours read-only (`engine_tour`). | [`docs/engine-tours/`](docs/engine-tours/), [`scripts/generate_engine_tour.py`](scripts/generate_engine_tour.py), [`scripts/skill_fanin.py`](scripts/skill_fanin.py), [`scripts/skill_graph.py`](scripts/skill_graph.py) |
| Usage evidence | Local-only count of `SKILL.md` reads from session tool calls; output stays outside every repository. | [`scripts/skill_usage_scan.py`](scripts/skill_usage_scan.py) |

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
| DEFINE | Requirements (`srs-skills`) | `srs-skills:01-strategic-vision/`, `srs-skills:02-requirements-engineering/fundamentals/before/02-elicitation-toolkit/` |
| PLAN | Engineering and design documentation | `chwezi-dev-engine:skills/execution-plan-scripts/`, `srs-skills:03-design-documentation/` |
| BUILD | Engineering; websites | `chwezi-dev-engine:skills/sdlc-meta/world-class-engineering/`, `website-skills:skills/orchestration/website-builder/` |
| VERIFY | Engineering; design | `chwezi-dev-engine:skills/sdlc-meta/world-class-engineering/references/verification-loop.md`, `design-system-skills:skills/00-cross-cutting-ops-qa-a11y/visual-product-slop-audit/` |
| REVIEW | Engineering | `chwezi-dev-engine:skills/sdlc-meta/git-collaboration-workflow/` |
| SHIP | Engineering; websites; servers | `chwezi-dev-engine:skills/devops-cloud/deployment-release-engineering/`, `website-skills:skills/launch-ops/deploy/`, `linux-skills:linux-sysadmin/` |

Cross-cutting overlays join any stage, alongside the owner and never instead of it: finance
(`chwezi-accounting-doctrine:skills/`) wherever money moves, design
(`design-system-skills:skills/`) wherever an output's appearance changes, and research
(`digital-research-skills:skills/`) for current or uncertain claims.[^commercial]

[^commercial]: Commercial work comes before DEFINE: proposals (`proposal-skills:skills/`),
    business plans (`business-plan-skills:skills/pipeline/00-plan-assembly/`) and marketing
    (`social-media-skills:skills/pipeline/06-digital-marketing-strategy/`).

The one-screen lifecycle idea is adapted from addyosmani/agent-skills (MIT,
https://github.com/addyosmani/agent-skills, commit `2686b62`).

## References

- [Chwezi Engine Agents source repository](https://github.com/peterbamuhigire/chwezi-engine-agents)
- [Engine orchestration contract](core/instructions/engine-orchestrator.md)
- [Engine registry](catalog/engines.yaml)
- [Portfolio craft standard](docs/operations/portfolio-craft-standard-2026-09-04.md)
- [Shared installer source](scripts/install-engine.js)
