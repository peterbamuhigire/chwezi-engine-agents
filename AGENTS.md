# AGENTS.md - chwezi-engine-agents (Skills Engine Agents)

<!-- MODEL-ROUTING-BLOCK v2 2026-11-10 -->
## Model classes and token discipline (Claude Code, Codex and any runner; mandatory)
Name a class here, never a model version. The owner's routing file maps classes to current models (Knowledge Bank, Development, Anthropic Models: `model-routing.json`; handoff AM-01), so a model upgrade needs no edit in this repository.
- **Classes:** **M Mundane** (fastest and cheapest; mechanical work with a clear right answer); **N Normal** (default; executes an approved plan); **X Expert** (strongest standard class; plans, judges, hard debugging, final review); **S Special occasion** (premium class above X; rare; only through the seven-test gate, AM-01 s5, including approved billing). A new model is classified by relative price and vendor positioning (AM-01 s1.1). With no S class available, X is the ceiling.
- **Escalate one class, on a trigger only:** two failed acceptance checks; an undecidable choice; unreviewed money, tenant, security or legal work. Drop back after the hard step.
- **Tokens, both runners:** start-up files at most 8,000 tokens and `AGENTS.md` at most 32 KiB (Codex stops at its byte cap); one task per session, clear or new thread between tasks, compact near 80%; plan to a file, execute in a fresh session (resume a plan from its small `RESUME.md` only); read the router section then one `SKILL.md`, search instead of loading; consult only the engine whose domain matches the task; subagents and tools return summaries, cap tool output (`tool_output_token_limit`), disable unused MCP tools; stable prefix first, no instruction edits mid-session; parallel agents only with a written budget; non-interactive runs for bulk (Batch API only with an approved API budget); effort medium by default, high needs a reason, the maximum needs approval.
- **Class S case for this repository (E-07, AM-02):** one controlled trial of the advisor and orchestrator patterns on a real task, compared with an X-led run. Everything else: X plans, N executes, M for mechanical work.
- **Monthly Kaizen, first step:** Anthropic currency check (AM-01 s8) and the token-budget lint; record `Anthropic currency check YYYY-MM-DD: no change|changed`.
<!-- /MODEL-ROUTING-BLOCK -->


Coordination and maintenance layer for the eleven catalogued domain skills
engines. This file is the runner-neutral router for this package; `CLAUDE.md`
is a thin bridge that imports it (portfolio bridge contract,
`docs/operations/claude-bridge-contract.md`). The primary router is
[`README.md`](README.md); host adapters live under `adapters/` (for example
[`adapters/claude-code/CLAUDE.md`](adapters/claude-code/CLAUDE.md) and
[`adapters/codex/`](adapters/codex/)).

How to use this package:

1. Resolve the engine for the current task from `catalog/engines.yaml`
   (catalogue paths are folder names, not locations: find each checkout through the active
   engine-routing table, `--engines-root` or `CHWEZI_ENGINES_ROOT`; former folder names are
   catalogue `aliases`).
2. Read that engine's own `AGENTS.md` (falling back to `CLAUDE.md` or
   `README.md`) before loading any of its `SKILL.md` files.
3. Use the three workflows in `agents/` — `engine-orchestrator`,
   `engine-maintainer`, `engine-validator` — by reading their definitions
   directly. Canonical instructions live in `core/instructions/`.

Project context: if the working project root holds a `PROJECT.md` with `project_schema: 1`, read it before planning. It points to this engine's own context sources and never replaces them.

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
  `python3 -X utf8 scripts/validate-no-book-extractions.py --workspace-root <folder>`
  (path-based; the folder holds the engines under their catalogue paths; domain
  topics such as a skill's `references/juice-extraction.md` pass; other
  exceptions need a reasoned line in `catalog/content-integrity-allowlist.txt`).

Engine count: the catalog holds eleven public domain engines; with this
package that makes twelve Chwezi repositories. Private personal engines stay
out of the catalog, the marketplace, and every public document.

Cross-engine handoffs: SRS defines what success means, the dev engine how to
build it safely, design how it looks, behaves, and is evaluated, research what
is currently true, and finance what happens to money. See
`core/instructions/engine-orchestrator.md`.

Host-specific material: `README.md` and `docs/adapters/` document installation per
host (Codex reads `.codex-plugin/plugin.json`); each applies to the host it names
only. Claude Code reads this file through `CLAUDE.md`.

Portfolio drift control: `python3 -X utf8 scripts/render_host_files.py --check
--engines-root <folder>` (or `--workspace-root <folder>`) checks every public
repository's `CLAUDE.md` bridge,
canary invariants, version consistency, model-ID corruption, BOMs, hook
configuration and the shared-asset register (`catalog/shared-assets.yaml`).
It is read-only; `--render --engine <path>` writes only the closed list of
derived fields named in the script.

Portfolio checks find engines through `scripts/lib/engine_roots.py` (repeatable
`--engines-root`, `CHWEZI_ENGINES_ROOT`, catalogue `aliases` for former folder
names), so they run on any layout; a missing or ambiguous engine is `NOT ASSESSED`.
`--check` also reports `released_commit` lag, catalogue validators that do not exist
or that an engine manifest declares and the catalogue lacks, and workstation paths or
former engine names in router files. `--render-router-blocks --engine <path>` rewrites
only the legacy host-path form of three router sentences from `templates/agents-blocks/`.
Other read-only checks: `scripts/check_public_hygiene.py` (tracked local settings, env
and key files, credential-shaped strings, host paths; policy in
`catalog/hygiene-policy.yaml`), `scripts/check_hook_copies.py` (the shared hook files;
canonical copy and procedure in `docs/operations/hook-canonical-copy.md`).
`scripts/refresh_released_commits.py --write` refreshes the pins and refuses when an
engine is dirty, missing or off `main`.

Tests and validators: `README.md` section "Validation" lists each command, what it needs
(PyYAML, `jsonschema`, `pytest`, Node.js, `pwsh`, network access) and its measured result
on 2026-10-31; the test suite is `python3 -X utf8 -m pytest -p no:cacheprovider tests`.
Open findings, decisions and the portfolio calendar of date-triggered gates are in the
sections "Open findings", "Decisions waiting for the maintainer" and "Date-triggered gates
across the portfolio" of `README.md`; evidence is in `docs/kaizen/`.

README quality: before you edit any Chwezi `README.md`, read
`docs/operations/readme-standard-2026-10-31.md` (structure, limits, preservation rules).
`python3 -X utf8 scripts/readme_metrics.py --check README.md` measures a README against the
limits, and `python3 -X utf8 scripts/check_readme_preservation.py <repo> <base> <new>` reports
the links, commands and heading anchors that a rewrite lost between two git revisions. Both
are read-only; exit 3 means NOT ASSESSED.
`python3 -X utf8 scripts/check_readme_contract.py --engines-root <folder>` checks that each engine README keeps `## Capabilities`
or `## Capability map` among its first four H2 headings (the rule of `scripts/validate-portfolio-craft.ps1`, on any host).

<!-- chwezi-design-engine:trigger v4 -->
### Design / typography / UI/UX (cross-cutting — consult IN ADDITION)

Any work touching how an artifact LOOKS — font/typeface choice, type scale, colour, layout/grid,
visual identity, web/desktop/mobile UI screens, or the visual formatting of a DOCX/PPTX/PDF/XLSX
— routes to the **`chwezi-design-engine`** engine, the single home for ALL design/UI/UX skills
and the anti-AI-slop doctrine.

**Resolve its location on THIS device from the active runner's global engine-routing table or
`AGENTS.md`** — never assume an absolute path; it varies per machine. Then read its
`README.md` → `doctrine/design-doctrine.md` → glob `skills/**/SKILL.md` fresh and route by
frontmatter (read SKILL.md directly, not via the Skill tool). Content and structure stay in THIS
engine; presentation comes from chwezi-design-engine. Hard rule: never use a banned AI-slop font
as primary type — hard ban: Inter, Geist, Roboto, Open Sans, Lato, Arial, Fraunces, IBM Plex (all
faces); secondary ban: Space Grotesk, Instrument Serif, Instrument Sans, Poppins, Montserrat, Nunito, Nunito Sans, Newsreader, Cormorant (all cuts), Crimson Pro, Plus Jakarta Sans, DM Sans, Outfit, Playfair Display, Lora, Space Mono;
Roboto Mono and IBM Plex Mono are banned as monospace choices; Source Sans 3 only as a paired
body face; no bare system stacks alone. State the chosen typeface and reason before producing
any artifact.
<!-- /chwezi-design-engine:trigger -->
