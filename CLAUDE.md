# CLAUDE.md - chwezi-engine-agents (Skills Engine Agents)

Coordination and maintenance layer for the eleven catalogued domain skills
engines. The primary router is [`README.md`](README.md); the Claude Code
adapter is [`adapters/claude-code/CLAUDE.md`](adapters/claude-code/CLAUDE.md).

How to use this package under Claude Code:

1. Resolve the engine for the current task from `catalog/engines.yaml`
   (paths are relative to `C:\wamp64\www\` on this machine).
2. Read that engine's own `CLAUDE.md` (falling back to `AGENTS.md` or
   `README.md`) before loading any of its `SKILL.md` files.
3. Use the three workflows in `agents/` — `engine-orchestrator`,
   `engine-maintainer`, `engine-validator` — by reading their definitions
   directly; they are not registered with Claude Code's native `Skill` tool.
   Canonical instructions live in `core/instructions/`.

Safety boundaries (binding):

- Read-only by default. `git pull --ff-only` only after an explicit user
  request in this session; skip dirty or diverged repositories; never reset,
  delete, merge manually, or force-push.
- Unavailable validation commands are reported as `NOT ASSESSED`, never
  treated as a pass.
- Writes, submissions, external messages, and publication require explicit
  user approval in this session.
- Never store book extractions in any engine or in this package: no
  `book-extractions/`, `extracted-books/`, `book-study/` folders, no
  `*-book-extraction.md`, book summaries, or chapter-by-chapter notes. Book
  knowledge enters only as paraphrased, task-oriented skill content with a
  short `Sources` line. Check with
  `python -X utf8 scripts/validate-no-book-extractions.py` (path-based; domain
  topics such as a skill's `references/juice-extraction.md` pass; other
  exceptions need a reasoned line in `catalog/content-integrity-allowlist.txt`).

Engine count: the catalog holds eleven public domain engines; with this
package that makes twelve Chwezi repositories. Private personal engines stay
out of the catalog, the marketplace, and every public document.

Cross-engine handoffs: SRS defines what success means, the dev engine how to
build it safely, design how it looks, behaves, and is evaluated, research what
is currently true, and finance what happens to money. See
`core/instructions/engine-orchestrator.md`.

Note: `README.md` documents Codex-specific installation and a
`~/.codex/...` validator path; those apply to the Codex host only and are
not expected to exist on this machine for Claude Code use.
