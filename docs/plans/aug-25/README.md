# Universal Multi-Host Skills Engine Agents Plan

This directory is the executable plan for extending `skills-engine-agents` from a Codex-only plugin into a model-neutral coordination package with host adapters, portable tools, optional MCP integration, and explicit integration contracts in all ten skills-engine repositories.

The master overview is [universal-multi-host-agents-plan.md](./universal-multi-host-agents-plan.md). The files below are the phase-level implementation documents. Each phase is independently reviewable and contains its own files, interfaces, tasks, tests, evidence requirements, failure handling, and commit checkpoint.

## Phase files

1. [Phase 1 — Compatibility baseline](./phase-01-compatibility-baseline.md)
2. [Phase 2 — Canonical core](./phase-02-canonical-core.md)
3. [Phase 3 — Schemas and contracts](./phase-03-schemas-contracts.md)
4. [Phase 4 — Capability negotiation](./phase-04-capability-negotiation.md)
5. [Phase 5 — Codex adapter](./phase-05-codex-adapter.md)
6. [Phase 6 — Claude Code adapter](./phase-06-claude-code-adapter.md)
7. [Phase 7 — Gemini, OpenCode, and generic adapters](./phase-07-other-host-adapters.md)
8. [Phase 8 — MCP server](./phase-08-mcp-server.md)
9. [Phase 9 — Installation and fork discovery](./phase-09-installation-and-forks.md)
10. [Phase 10 — Security and permission controls](./phase-10-security-controls.md)
11. [Phase 11 — Cross-host/model evaluation](./phase-11-evaluation-suite.md)
12. [Phase 12 — Release documentation and operations](./phase-12-release-operations.md)
13. [Phase 13 — Engine integration and public distribution](./phase-13-engine-integration-publication.md)

## Execution rules

- All work stays on `main` unless the user explicitly requests a branch.
- Complete phases in order. Phases 5–7 may run in parallel only after Phases 1–4 have produced stable contracts.
- Commit each implementation phase separately with the commit message specified in that phase file.
- Keep the ten engine repositories independent. Their routers and `SKILL.md` files remain the domain source of truth.
- Treat unavailable tools, dependencies, provider access, and host capabilities as `NOT ASSESSED`; never treat them as a pass.
- Before every commit, run the phase’s checks, `git diff --check`, and a staged-diff review.
- Before public release, run the full release gate in Phase 12 and the ten-engine publication gate in Phase 13.

## Required final evidence

The implementation is ready for release only when the evidence packet includes:

- compatibility matrix and host/provider boundary;
- validated canonical contracts and schemas;
- adapter smoke-test reports;
- installation, update, uninstall, and fork-discovery reports;
- security and mutation-gate reports;
- cross-host/model evaluation report;
- ten engine integration manifests and engine release references;
- release archive, checksums, provenance manifest, and developer installation guides.
