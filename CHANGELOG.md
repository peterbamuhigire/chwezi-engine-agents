# Changelog

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
