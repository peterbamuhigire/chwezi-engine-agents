# AGENTS.md - chwezi-engine-agents (Skills Engine Agents)

Coordination and maintenance layer for the eleven catalogued domain skills
engines. This file is the runner-neutral router for this package; `CLAUDE.md`
is a thin bridge that imports it (portfolio bridge contract,
`docs/operations/claude-bridge-contract.md`). The primary router is
[`README.md`](README.md); host adapters live under `adapters/` (for example
[`adapters/claude-code/CLAUDE.md`](adapters/claude-code/CLAUDE.md) and
[`adapters/codex/`](adapters/codex/)).

How to use this package:

1. Resolve the engine for the current task from `catalog/engines.yaml`
   (paths are relative to `C:\wamp64\www\` on this machine).
2. Read that engine's own `AGENTS.md` (falling back to `CLAUDE.md` or
   `README.md`) before loading any of its `SKILL.md` files.
3. Use the three workflows in `agents/` — `engine-orchestrator`,
   `engine-maintainer`, `engine-validator` — by reading their definitions
   directly. Canonical instructions live in `core/instructions/`.

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

Host-specific material: `README.md` documents Codex-specific installation and a
`~/.codex/...` validator path; those apply to the Codex host only. Claude Code
reads this file through `CLAUDE.md`.

Portfolio drift control: `python -X utf8 scripts/render_host_files.py --check
--workspace-root ..` checks every public repository's `CLAUDE.md` bridge,
canary invariants, version consistency, model-ID corruption, BOMs, hook
configuration and the shared-asset register (`catalog/shared-assets.yaml`).
It is read-only; `--render --engine <path>` writes only the closed list of
derived fields named in the script.

<!-- design-system-skills:trigger v2 -->
### Design / typography / UI/UX (cross-cutting — consult IN ADDITION)

Any work touching how an artifact LOOKS — font/typeface choice, type scale, colour, layout/grid,
visual identity, web/desktop/mobile UI screens, or the visual formatting of a DOCX/PPTX/PDF/XLSX
— routes to the **`design-system-skills`** engine, the single home for ALL design/UI/UX skills
and the anti-AI-slop doctrine.

**Resolve its location on THIS device from the active runner's global engine-routing table or
`AGENTS.md`** — never assume an absolute path; it varies per machine. Then read its
`README.md` → `doctrine/design-doctrine.md` → glob `skills/**/SKILL.md` fresh and route by
frontmatter (read SKILL.md directly, not via the Skill tool). Content and structure stay in THIS
engine; presentation comes from design-system-skills. Hard rule: never use a banned AI-slop font
as primary type — hard ban: Inter, Geist, Roboto, Open Sans, Lato, Arial, Fraunces, IBM Plex (all
faces); secondary ban: Space Grotesk, Instrument Serif, Poppins, Montserrat, Nunito, Nunito Sans;
Roboto Mono and IBM Plex Mono are banned as monospace choices; Source Sans 3 only as a paired
body face; no bare system stacks alone. State the chosen typeface and reason before producing
any artifact.
<!-- /design-system-skills:trigger -->
