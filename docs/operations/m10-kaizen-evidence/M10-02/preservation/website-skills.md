# Preservation map — website-skills (M10-02-T02)

Contract: `docs/operations/claude-bridge-contract.md`. Pilot format: `design-system-skills.md`. Classification decided by the orchestrator's executor under Peter's delegated authority, 29 Sep 2026; reviewer ticks left open for the independent reviewer.

## Hashes and sizes

| File | Pre SHA-256 | Pre bytes | Post SHA-256 | Post bytes |
|---|---|---|---|---|
| `CLAUDE.md` | `bcdff4f356a70fc0de91742383f52b53cab12f985f58a7d68097a03df74bc070` | 21,323 (LF) | `245412aa1f0b13a791e97bdbf5f6fa2f67285fc911760b332345eb38d2dfd665` | 606 (LF) |
| `AGENTS.md` | `36796476f10f8121f3173a45e586e44c1a8d507a6db7b423e0bea9a4914b2b26` | 24,228 (CRLF working copy) | `fd0bbcd6710f5129b32be7af602b4b07807ef681403806562002aa9f583dd425` | 40,323 (LF) |

Router effective bytes (`CLAUDE.md` plus `@`-imported files): before 21,323 (no `@AGENTS.md` import; Claude loaded only `CLAUDE.md` and was told to read `AGENTS.md` separately); after 606 + 40,323 = 40,929. `AGENTS.md` was rewritten with LF endings; `git diff` shows content lines only (240 insertions, 0 deletions).

Moved blocks were copied verbatim unless noted. Long skill lists and code blocks are mapped per block because every row in the block has the same class; each listed path was checked and exists on disk.

## Sentence table

| ID | Source line | Sentence (abridged) | Class | Destination | Reviewer |
|---|---|---|---|---|---|
| S01 | 1–3 | `# CLAUDE.md`; "This file provides guidance to Claude Code…" | duplicate | Replaced by bridge heading `# Claude Code repository memory` (same function) | [ ] |
| S02 | 7 | Skills library built from `SKILL.md` files for static websites from markdown and assets | duplicate (part) | AGENTS.md §Purpose L69 ("portable skill library for building websites") | [ ] |
| S03 | 7 | "…from markdown content and assets. It is not a standalone application." | doctrine-moved | AGENTS.md §Purpose, new sentence "It teaches agents to build static websites from markdown content and assets; it is not a standalone application." ("Claude" made runner-neutral) | [ ] |
| S04 | 9 | Referenced from global engine-routing table; Claude Code and Codex resolve checkout and consume skills directly | doctrine-moved | AGENTS.md §Purpose (verbatim) | [ ] |
| S05 | 11–17 | Portable agency system with five explicit layers (qualification … governance) | doctrine-moved | AGENTS.md §Purpose (verbatim list) | [ ] |
| S06 | 19 | Premium is the default commercial standard | duplicate | AGENTS.md §Baseline Rules "Premium is the default commercial standard for this website engine" | [ ] |
| S07 | 19 | Must be delivered as credible business asset: strategy, world-class content, SEO/GEO, premium UX, conversion architecture … post-launch improvement | doctrine-moved | AGENTS.md §Baseline Rules, new bullet after the Premium bullet (verbatim; carries GEO, conversion architecture, post-launch improvement absent from AGENTS.md) | [ ] |
| S08 | 19 | If brief cannot support it: paid discovery, smaller premium scope, or no-bid/no-build | duplicate | AGENTS.md §Baseline Rules Premium bullet | [ ] |
| S09 | 23 | `SKILL.md` is the concise execution layer | duplicate | AGENTS.md L73, §Quality Expectations "Keep `SKILL.md` concise" | [ ] |
| S10 | 24 | Skills under `skills/<category>/<skill-name>/SKILL.md` across 11 categories | duplicate | AGENTS.md §Purpose L72 | [ ] |
| S11 | 25 | Exact acknowledgement line below first heading, never in frontmatter | duplicate | AGENTS.md §Baseline Rules L84 | [ ] |
| S12 | 26 | `references/` holds detailed material incl. `legacy-guidance.md` | duplicate | AGENTS.md L74 and L85 | [ ] |
| S13 | 27 | `scripts/` holds deterministic helpers | duplicate | AGENTS.md L75 | [ ] |
| S14 | 28 | AGENTS.md provides routing and quality rules; Claude must read its runner-agnostic doctrine (list) and apply it in full | Claude-mechanics | Claude-only block bullet 1 ("Apply `AGENTS.md` in full, including its runner-agnostic doctrine"); the import now loads all listed sections | [ ] |
| S15 | 28 | Skip only the explicitly Codex-only sections (e.g. "Codex-only model setup") | Claude-mechanics | Claude-only block bullet 1 | [ ] |
| S16 | 30 | Claude-specific projects may point here; not dependent on `.claude/skills/` or any nested submodule path | doctrine-moved | AGENTS.md §Purpose (verbatim; AGENTS.md L77 had only the `.claude/skills/` part) | [ ] |
| S17 | 32–34 | Every blog/article must be researched with digital-research-engine before drafting; never from assumed knowledge; real sources, credit authors | doctrine-moved | AGENTS.md new §Blog & Article Research — Always Use the Digital Research Engine (verbatim, heading kept) | [ ] |
| S18 | 36 | Engine location: resolve from routing table; canonical checkout path; no retired alias | doctrine-moved | same section (verbatim) | [ ] |
| S19 | 37 | Method: `research-orchestration/SKILL.md`, multi-agent wave, orchestrator synthesises | doctrine-moved | same section (verbatim) | [ ] |
| S20 | 38 | Article SEO/SERP standard: three-wave study, top five results, approved API, record query data, no invented volumes, bilingual intent | doctrine-moved | same section (verbatim) | [ ] |
| S21 | 39 | Attribution mandatory; UNVERIFIED marking; never fabricate; "Sources & the researchers worth crediting" block | doctrine-moved | same section (verbatim) | [ ] |
| S22 | 41 | Root contains docs plus `docs/`, `skills/`, `projects/`; operational dirs stay at root | duplicate | AGENTS.md §Purpose L77 (last sentence) | [ ] |
| S23 | 43–61 | §Repository Structure / Skill Categories: 11 categories with counts and skill names; always use full categorised path | doctrine-moved | AGENTS.md new §Repository Structure (verbatim; the `**`category/`** (N)` format is kept because the registry validator parses it — see open item) | [ ] |
| S24 | 63–84 | Core Build Skills annotated list | doctrine-moved | AGENTS.md §Repository Structure (verbatim) | [ ] |
| S25 | 86–92 | Enforcement Skills (Phase 10) list | doctrine-moved | same (verbatim) | [ ] |
| S26 | 94–105 | Operating Discipline Skills (Phase 11) list and Phase 11 additions | doctrine-moved | same (verbatim; overlaps AGENTS.md §Governance but adds "60-question exam") | [ ] |
| S27 | 107–116 | Authority Skills (Phase 12) and Phase 12 additions (licence mix) | doctrine-moved | same (verbatim; licence composition absent elsewhere) | [ ] |
| S28 | 118–123 | Canonical scripts, configs, CI pipeline path | doctrine-moved | same (verbatim; `install-canonical-ci.sh`, `metadata-audit.sh`, `post-deploy-smoke.sh`, `rollback.sh` absent elsewhere) | [ ] |
| S29 | 125–145 | Support And Audit Skills list | doctrine-moved | same (verbatim) | [ ] |
| S30 | 147–151 | External Skill Set: proposal-skills resolved from routing table | doctrine-moved | same (verbatim) | [ ] |
| S31 | 153–166 | Skill Execution Order: website build skills are sequential (10 steps) | doctrine-moved | AGENTS.md new §Skill Execution Order (verbatim) | [ ] |
| S32 | 168 | `website-builder` orchestrates the sequence from language setup, content, assets | doctrine-moved | same (verbatim) | [ ] |
| S33 | 170 | Cross-cutting skills apply throughout instead of owning one artefact | doctrine-moved | same (verbatim) | [ ] |
| S34 | 172–180 | Five agency engine layers (commercial … governance) | doctrine-moved | AGENTS.md new §Current Agency Engine Layers (verbatim) | [ ] |
| S35 | 182–191 | Plugin guidance: Claude Code `/plugin` install commands | Claude-mechanics | Claude-only block bullet 2 (verbatim commands) | [ ] |
| S36 | 193 | Use plugins where they materially improve output | Claude-mechanics | Claude-only block bullet 2 | [ ] |
| S37 | 197–198 | Every project inherits the 15-step pipeline via `install-canonical-ci.sh` | duplicate | AGENTS.md §Enforcement and Quality Gates L205–206 | [ ] |
| S38 | 199–202 | Pipeline order is fixed: install → … → rollback-ready | doctrine-moved | AGENTS.md §Enforcement and Quality Gates (verbatim) | [ ] |
| S39 | 204 | Any gate failure blocks deploy | doctrine-moved | same (verbatim) | [ ] |
| S40 | 204–206 | Thresholds live in the two configs and are non-negotiable; adjustments need a decision entry | doctrine-moved (first half) / duplicate (decision entry, AGENTS.md L207–208) | same | [ ] |
| S41 | 208–209 | Full reference: three deploy references | doctrine-moved | same (verbatim) | [ ] |
| S42 | 213–218 | Hard expectations: zero unnecessary JS; self-hosted assets; distinctive outputs; source content from docs; mobile-first/multilingual; privacy/terms as trust infrastructure | doctrine-moved | AGENTS.md new §Hard Repository Expectations (verbatim) | [ ] |
| S43 | 219 | Run `skill-safety-audit` when a skill changes materially | duplicate | AGENTS.md §Safety L260 (identical) | [ ] |
| S44 | 220 | Update top-level docs when operating model changes | doctrine-moved | §Hard Repository Expectations (verbatim) | [ ] |
| S45 | 221 | Canonical SKILL.md structure in `docs/doc-style-guide.md` | doctrine-moved | same | [ ] |
| S46 | 222 | July 2026 contract in `docs/skill-authoring-standard.md`; start from template | doctrine-moved | same (overlaps §Baseline Rules L89; "July 2026" detail kept) | [ ] |
| S47 | 223 | Run contract validator against baseline and routing smoke test; baseline accepts no findings; top three | doctrine-moved | same (overlaps L90; baseline file and top-three rule absent elsewhere) | [ ] |
| S48 | 224 | Acknowledgement line directly under first heading without duplicating it | doctrine-moved | same (overlaps L84; "without duplicating" detail kept) | [ ] |
| S49 | 225 | Canonical names in `glossary.md`; renames follow deprecation policy | doctrine-moved | same | [ ] |
| S50 | 226–227 | Every project ships through canonical CI; not installed and green = not shipped | doctrine-moved | same | [ ] |
| S51 | 228–238 | Thresholds set against conservative Slow-4G/3G stress profile; figures; NOT_ASSESSED sources; lab gates block, field p75 decides; INP from field data | doctrine-moved | same (verbatim; partly overlaps §Enforcement Africa calibration bullet) | [ ] |
| S52 | 239–240 | `perf-gate.sh` enforces every budget category via route-weight-budget and html-perf-lint | doctrine-moved | same | [ ] |
| S53 | 244–257 | Direct-response copy: use `long-form-sales-copy`; three procedure groups | doctrine-moved | AGENTS.md new §Direct-Response Copy for Sales Pages (verbatim) | [ ] |
| S54 | 259–267 | Working procedures live in named references (sales letter, funnels, offers, price strategy, premium selling, pricing page, headlines/ethics filter) | doctrine-moved | same (verbatim) | [ ] |
| S55 | 269–272 | Brand-level messaging uses SB7 brandscript worksheet as upstream foundation | doctrine-moved | same (verbatim) | [ ] |
| S56 | 276–277 | Book extractions, summaries and raw book text never stored | duplicate | AGENTS.md §Rules L36–37 | [ ] |
| S57 | 277 | Books are durable concept inputs only | duplicate | AGENTS.md §Mandatory Digital Research currentness gate L61 | [ ] |
| S58 | 277–281 | Turn method into task-oriented reference (procedure, checklist, template, decision rules, phrase bank) in original words; cite author, year, title, publisher; quotes under 25 words and rare | doctrine-moved | AGENTS.md §Rules, new paragraph after the book rule (near-verbatim) | [ ] |
| S59 | 281 | Put volatile claims through the currentness gate | duplicate | AGENTS.md §Rules L39 | [ ] |
| S60 | 281–284 | Former `book-extractions/` removed 2026-09-24; map in retirement record | doctrine-moved (date) / duplicate (map path, AGENTS.md L40–41) | AGENTS.md §Rules new paragraph | [ ] |
| S61 | 285–286 | `source_ingestion_guardrail.py` rejects files in four named directories | doctrine-moved | AGENTS.md §Rules new paragraph (verbatim) | [ ] |
| S62 | 288–306 | Design trigger block v2 | duplicate | AGENTS.md L264–282 (compared: identical between markers) | [ ] |
| S63 | 307–316 | Relocated design skills block | duplicate | AGENTS.md L283–292 (compared: identical) | [ ] |

Structural headings (`## What This Repo Is`, `## Repo Model`, `## Book Sources Are Never Stored Here (owner rule, 2026-09-24)`, `## Plugin Guidance`, `## Canonical CI Pipeline (Phase 10)`) are replaced by the destination sections; their content is mapped above. The owner-rule date is already in AGENTS.md §Rules ("owner rule, 2026-09-24").

## Counts

| Class | Count |
|---|---|
| duplicate | 17 (S01, S02, S06, S08–S13, S22, S37, S43, S56, S57, S59, S62, S63; the duplicate halves of S40 and S60 are counted with their rows as doctrine-moved) |
| doctrine-moved | 42 |
| Claude-mechanics | 4 (S14, S15, S35, S36) |
| obsolete | 0 |
| lost | 0 |
| total rows | 63 |

Lost: 0. The plan's suggested "obsolete" candidate (hard-coded skill lists duplicating the filesystem) was not used: every listed path exists, the lists carry routing annotations found nowhere else, and the registry validator parses the category counts, so they were moved rather than retired.

## Invariants recorded (`.skills-engine/engine-manifest.yaml`)

- `book-extraction-ban`: "Book extractions, book summaries and raw book text must never be stored in this"
- `not-assessed`: "Missing browser, render, live, or stakeholder evidence is `NOT ASSESSED`, never a pass."
- `premium-default`: "Premium is the default commercial standard for this website engine."
- Exemption `british-english`: no British English output rule exists in the website router.

## Open item (needs the parent's action)

`scripts/validate-skill-registry.py` (L132–138) and `tests/test_kaizen_wave1_contracts.py` (L29) read category counts from `CLAUDE.md`. After the conversion they fail (`CLAUDE.md category counts {} != …`). The category list moved verbatim to `AGENTS.md`, so the fix is a two-line repoint to `AGENTS.md` in each file. A ready patch is at the executor scratchpad `website-repoint/website-registry-repoint.patch`; executing the patched sources against the live tree gives `registry valid: 62 skills` and the count test passes. Not applied, because validators are outside the fork's edit scope.

Decided under Peter's delegated authority, 29 Sep 2026.
