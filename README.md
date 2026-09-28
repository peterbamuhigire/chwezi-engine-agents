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

## References

- [Chwezi Engine Agents source repository](https://github.com/peterbamuhigire/chwezi-engine-agents)
- [Engine orchestration contract](core/instructions/engine-orchestrator.md)
- [Engine registry](catalog/engines.yaml)
- [Portfolio craft standard](docs/operations/portfolio-craft-standard-2026-09-04.md)
- [Shared installer source](scripts/install-engine.js)
