# Changelog

## Unreleased - Engine renames (29 September 2026)

- `srs-skills` is now `chwezi-sdlc-documentation` and `design-system-skills` is now
  `chwezi-design-engine` (GitHub repositories and local folders). Catalogue ids and paths,
  shared-asset paths, eval cases and fixtures (065 and 073 renamed), routing ownership and
  baseline keys, plugin eval folders, scripts, tests, MCP server tests, CI checkouts and live
  docs follow the new names; engine tours and the skill graph were regenerated.
- Suite marketplace entries renamed: `srs` is now `sdlc-documentation` and `design-system` is
  now `design-engine`, pointing at the new repository URLs.
- Design trigger block marker is now `<!-- chwezi-design-engine:trigger v4 -->`;
  `render_host_files.py` and the shared-asset register follow it.
- Dated records (Kaizen logs, M10 evidence, execution logs, plans, rejected-change ledger rows)
  keep the old names as written.

## Unreleased - M10-12 context contract, engine tours and skill graph

- Added the `PROJECT.md` project context contract
  (`docs/operations/project-context-contract.md`), its schema
  (`schemas/project-context.schema.json`), template
  (`templates/project-context/PROJECT.md`) and the read-only
  `scripts/project_context_doctor.py` with seeded fixtures;
  `validate-contracts.py` now validates a Markdown instance's front matter.
- Added one identical project-context read rule to every engine's `AGENTS.md`
  and to this package's `AGENTS.md`; the orchestrator pre-fills the craft
  brief from `PROJECT.md` when present.
- Added `scripts/skill_fanin.py` (inbound links, mentions, aliases, router and
  fixture references per active skill) and `scripts/generate_engine_tour.py`
  with committed tours for all twelve repositories under `docs/engine-tours/`.
- Added the report-only skill graph (`scripts/skill_graph.py`,
  `docs/skill-graph/skill-graph.json`), kept after the spike found defects no
  existing guardrail reports; it is never a routing input or a gate.
- MCP server: read-only `engine_tour` and `query_skill_graph` tools with tests.
- Added `scripts/skill_usage_scan.py` (local-only; tool calls only; refuses
  output inside a repository), a lifecycle map in `README.md` and the UA-11
  orientation case `077-orientation-dev-tour` (execution `NOT_ASSESSED`).

## Unreleased - 2026-09-24 Kaizen

- Added `scripts/validate-no-book-extractions.py`, a path-based portfolio
  copyright guard (banned `book-extractions/`, `extracted-books/`,
  `book-study/` folders and book-digest file names; domain-topic
  `*-extraction.md` files in skill `references/`/`templates/`/`examples/`
  pass; other exceptions via `catalog/content-integrity-allowlist.txt`;
  git-ignored working data out of scope), with tests. Wired into `CLAUDE.md`,
  the Claude Code adapter, the maintainer and validator instructions, and the
  portfolio craft standard.
- Added cross-engine handoff boundaries to the orchestrator (SRS, dev, design,
  research, finance ownership and sequence) and eval case
  `021-route-product-build-handoff`.
- Added a senior-practitioner bar and content-integrity section to the
  portfolio craft standard; requirements floor now demands buildable,
  implementation-free requirements.
- Fixed `validate-portfolio-craft.ps1`: accepts the 2026-09-20 README layout
  (capability section within the first four H2s) and reports every failure
  instead of stopping at the first.
- Catalog: `digital-research-skills` repository corrected to its GitHub name
  `digital-research-skills`; `windows-admin-engine-skills` integration status
  set to `pending` because its `.skills-engine/engine-manifest.yaml` does not
  exist.
- Evals 007 and 018 now target `chwezi-dev-engine` (renamed from
  `skills-web-dev` on 2026-09-20). README restores the coordination-card links
  required by `validate-kaizen-cards.py` and fixes the engineering plugin label.

## 1.0.0 - 2026-08-26

- Added a model-neutral canonical core with stable handoff, maintenance, and
  validation contracts.
- Added Codex, Claude Code, Gemini CLI, OpenCode, generic, and MCP adapters.
- Added capability negotiation, staged managed installers, fork discovery,
  path and mutation controls, and deterministic cross-host evaluations.
- Added release guides, CI gates, provenance metadata, and checksum policy.
