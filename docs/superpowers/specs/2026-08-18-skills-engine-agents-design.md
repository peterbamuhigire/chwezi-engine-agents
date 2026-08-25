# Skills Engine Agents Design

**Status:** Approved for implementation

## Goal

Create a portable Codex plugin that coordinates and maintains the ten local skills engines without embedding machine-specific paths or duplicating the engines' domain instructions.

## Decisions

- The repository is a standalone Codex plugin named `skills-engine-agents`.
- Agent definitions live in the plugin's `agents/` directory.
- Engine identity is discovered from the current Git checkout, repository name, and local `AGENTS.md`; the plugin does not require `C:\wamp64\www`.
- The canonical engine catalog stores repository names, router files, and safe validation commands.
- The initial release contains three agents: orchestration, maintenance, and validation.
- Existing engine repositories remain independently usable. Installing this plugin is optional.
- The plugin performs read-only inspection by default. Pulls, commits, pushes, and other writes require an explicit user request.

## Components

1. `.codex-plugin/plugin.json` — valid plugin metadata and UI-facing description.
2. `agents/engine-orchestrator.md` — selects applicable engines and produces handoff packets.
3. `agents/engine-maintainer.md` — checks remotes, pulls safely, and reports drift or dirty trees.
4. `agents/engine-validator.md` — maps an engine to its documented validation commands and reports evidence.
5. `catalog/engines.yaml` — portable ten-engine registry using canonical repository names and relative commands.
6. `scripts/discover-engine.ps1` — resolves the current engine from a local Git checkout.
7. `scripts/validate-catalog.ps1` — validates catalog completeness and repository paths.
8. `scripts/install.ps1` — installs or links the plugin into the user's personal Codex plugin location.
9. `README.md` — installation, distribution, fork, usage, and safety documentation.
10. `docs/distribution.md` — public-directory, workspace-directory, and local distribution paths.

## Portability and forks

The plugin never assumes a fixed checkout root. A contributor may clone one engine, fork it, rename its parent directory, and still use the plugin. Discovery first checks the current Git remote and repository basename, then reads `AGENTS.md`. If no catalog entry matches, the agents remain available for generic inspection but do not invent validation commands.

## Safety and failure behavior

- Dirty working trees are reported and not modified by maintenance actions.
- Non-fast-forward updates are reported as blocked rather than merged automatically.
- Missing tools or validation scripts are reported as `not assessed`.
- Unknown engines are reported explicitly with the current repository and branch.
- The maintainer never deletes files, resets branches, or force-pushes.

## Validation

- The plugin manifest is validated with the local plugin validator.
- The catalog validator checks all ten engine IDs, unique repository names, router paths, and command fields.
- PowerShell scripts are parsed before release.
- Git status and the final commit are inspected before publication.
