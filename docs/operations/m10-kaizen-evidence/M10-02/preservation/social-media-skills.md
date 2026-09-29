# Preservation map — social-media-skills (M10-02-T02)

Contract: `docs/operations/claude-bridge-contract.md`. Pilot format: `design-system-skills.md`. Classification decided by the orchestrator's executor under Peter's delegated authority, 29 Sep 2026; reviewer ticks left open for the independent reviewer.

## Hashes and sizes

| File | Pre SHA-256 | Pre bytes | Post SHA-256 | Post bytes |
|---|---|---|---|---|
| `CLAUDE.md` | `68e47e0f5edea6d3fbbd767e9c2d6d1809a68e19b759347f1805c04166b8ab1c` | 21,416 (LF) | `4be682eada8ee84820ee525682781cd8f1a56ac8a30c20c30763e034536b5e9f` | 44 (LF) |
| `AGENTS.md` | `db192d0d74cbf8896d5522a9f0f2eb669ac14bd5cc0fb969569c003008559e8d` | 20,945 (CRLF working copy) | `465c2374f3edcf496430e9eb1be9ec594f2a0019acef46fd5cb9fe85a8f88f35` | 40,354 (LF) |

Router effective bytes (`CLAUDE.md` plus `@`-imported files): before 21,416 (the old `CLAUDE.md` had no `@AGENTS.md` import); after 44 + 40,354 = 40,398. Claude now loads the full runner-neutral router, which it previously did not. The byte growth is expected: the old `CLAUDE.md` was a second, mostly distinct router, and almost all of its content is doctrine that Codex never saw. Router slimming is out of scope here (CV-04, M10-08).

The pre-change `AGENTS.md` was a CRLF working copy; it was rewritten with LF endings, so `git diff` shows only content lines (196 insertions, 230 deletions across the two files).

## Method

The old `CLAUDE.md` was mostly its own router: 12 of its 15 content sections had no complete equivalent in `AGENTS.md`. Where a section added any detail not in `AGENTS.md`, the **whole section was moved verbatim** into a new `AGENTS.md` section, `## Engine conventions (moved from CLAUDE.md, M10-02)` (L204–396, before the design trigger block), with its `##` headings demoted to `###`. Sentences in a moved section that partly overlap existing `AGENTS.md` text are still classed doctrine-moved (the overlap is noted), because moving the whole section loses no nuance. Only sections or sentences with complete equivalents were dropped as duplicates. A mechanical check confirmed that every non-blank, non-rule line of the old `CLAUDE.md` except the title heading occurs verbatim in the new `AGENTS.md`, or is one of the duplicates listed below.

No Claude-mechanics sentences were found: the old `CLAUDE.md` carried no runner-specific loading instructions, and `AGENTS.md` L5–6 already tells Claude to skip the Codex-only section. The bridge therefore has no `## Claude-only notes` section and the manifest has no `claude_only_block`.

Headings are structural. The title `# social-media-skills — Project Conventions` is replaced by the bridge heading; section headings travel with their moved sections. `---` rules are dropped as formatting.

## Sentence table

Tables and lists are mapped per row group where all rows share one class, as stated in each row.

| ID | Source line | Sentence (abridged) | Class | Destination | Reviewer |
|---|---|---|---|---|---|
| S01 | 5 | Engine is the Chwezi digital marketing and advertising consultancy engine; skills produce every lifecycle document and agency OS | doctrine-moved | AGENTS.md §Engine conventions › Purpose and scope boundary, L210 (overlaps §Purpose L62; lifecycle list is extra) | [ ] |
| S02 | 7 | Scope boundary: plans, specifies, writes, audits, reports across paid search, social, display, audio, outdoor, DR | doctrine-moved | same, L212 | [ ] |
| S03 | 7 | Spending, live ad-account changes, publishing or contacting people need explicit, action-specific client authority | doctrine-moved | same, L212 (overlaps L62; "action-specific" is extra) | [ ] |
| S04 | 7 | Handoffs: design, website via journey handoff, proposal, business-plan, accounting, research | doctrine-moved | same, L212 | [ ] |
| S05 | 7 | Skills generate text documents, plans, specifications and slide outlines — not code, builds or finished designs | doctrine-moved | same, L212 (overlaps Working Rules L170) | [ ] |
| S06 | 11–13 | Roadmap lives in `docs/plans/2026-04-14-…/00-roadmap-index.md` | doctrine-moved | §Engine conventions › Active Roadmap, L216–218 (Working Rules L174 names only the folder) | [ ] |
| S07 | 15 | Treat the roadmap as the controlling sequence for major improvements | doctrine-moved | same, L220 | [ ] |
| S08 | 15 | Target end-state is a world-class, market-adaptive engine, not an East Africa-only library | doctrine-moved | same, L220 | [ ] |
| S09 | 21 | Every blog/article/thought-leadership piece is researched with digital-research-engine before drafting | doctrine-moved | §Engine conventions › Blog & Article Research, L224 | [ ] |
| S10 | 21 | Never write a blog post from assumed knowledge alone | doctrine-moved | same, L224 | [ ] |
| S11 | 21 | Examples, statistics and cited research come from a live research wave with credit to original authors | doctrine-moved | same, L224 | [ ] |
| S12 | 23 | Engine location and "locate the repo rather than skip research" | doctrine-moved | same, L226 | [ ] |
| S13 | 24 | Method: research-orchestration, one agent per cohort, orchestrator synthesises | doctrine-moved | same, L227 | [ ] |
| S14 | 25 | Article SEO/SERP standard: three-wave study, approved search tool, record queries, no invented volumes, bilingual intent | doctrine-moved | same, L228 (8 sentences, moved verbatim as one bullet) | [ ] |
| S15 | 26 | Attribution mandatory; name researchers; mark UNVERIFIED; never fabricate a citation | doctrine-moved | same, L229 (4 sentences) | [ ] |
| S16 | 27 | Output: weave credits; close with "Sources & the researchers worth crediting"; N2 reference example | doctrine-moved | same, L230 (2 sentences) | [ ] |
| S17 | 33–45 | Naming-conventions table (11 rows: prefix, category, examples) | doctrine-moved | §Engine conventions › Naming Conventions, L234–246 (overlaps Routing Rules L115–128; examples and `01-`–`04-` onboarding band are extra) | [ ] |
| S18 | 51 | Skills sit in thematic subdirectories; canonical path `skills/<category>/<skill-name>/SKILL.md` | doctrine-moved | §Engine conventions › Skill Categories, L250 (overlaps §Purpose L76) | [ ] |
| S19 | 53–70 | Skill-categories table (16 rows: category and contents) | doctrine-moved | same, L252–269 (AGENTS.md L76 lists names only; contents are extra) | [ ] |
| S20 | 72 | Reference skills by full path in docs and prompts | doctrine-moved | same, L271 | [ ] |
| S21 | 78 | Binding contract is the authoring standard; use the template for new skills | doctrine-moved | §Engine conventions › Authoring Rules, L275 (overlaps Maintenance L198; "binding" wording kept) | [ ] |
| S22 | 80 | Rule 1: portable entrypoint, directory-matching name, single-line `Use when`, no README/CHANGELOG in skill folders | doctrine-moved | same, L277 | [ ] |
| S23 | 81 | Rule 2: no skills at `skills/` root; add a category only when none fits | doctrine-moved | same, L278 | [ ] |
| S24 | 82 | Rule 3: 500-line hard limit; references linked with a note on when to read | doctrine-moved | same, L279 (overlaps Working Rules L167) | [ ] |
| S25 | 83 | Rule 4: British English throughout, with example spellings; never American | doctrine-moved | same, L280 (overlaps Working Rules L169; examples extra) | [ ] |
| S26 | 84 | Rule 5: imperative language | doctrine-moved | same, L281 | [ ] |
| S27 | 85 | Rule 6: composition contracts list | doctrine-moved | same, L282 | [ ] |
| S28 | 86 | Rule 7: read-only analysis by default; listed actions need explicit authority | doctrine-moved | same, L283 | [ ] |
| S29 | 87 | Rule 8: release gates incl. repository tests and per-skill validation; failure counts empty | doctrine-moved | same, L284 (overlaps Maintenance L199; extra gates) | [ ] |
| S30 | 93 | Two ai-marketing skills enforce no AI slop | doctrine-moved | §Engine conventions › Anti-AI-Slop Quality Gate, L288 | [ ] |
| S31 | 95 | `anti-ai-slop` mandatory in real time; ship-gate on every output; alongside `ai-content-humaniser` | doctrine-moved | same, L290 (overlaps Baseline Skills L102 and How To Execute L145; "alongside humaniser" extra) | [ ] |
| S32 | 96 | `ai-slop-audit` after each major iteration; F blocks; auto-runs on review requests; A/B/C/F report | doctrine-moved | same, L291 (overlaps L103, L145) | [ ] |
| S33 | 98 | Shared evidence base and merged banned list; preserve named citations verbatim; no unsourced statistics | doctrine-moved | same, L293 | [ ] |
| S34 | 104 | Default Uganda/East Africa market; affects examples, penetration data, pricing, culture, audience | doctrine-moved | §Engine conventions › Default Country Context, L297 (overlaps Default Context L80) | [ ] |
| S35 | 106 | Replace assumptions for another market; make market assumptions explicit where material | doctrine-moved | same, L299 (overlaps L86, L173) | [ ] |
| S36 | 108–118 | Platform-defaults table for Uganda/EA (7 rows incl. WhatsApp and Facebook evidence caveats, registers MK-02, MK-03, WA-01) | doctrine-moved | same, L301–311 | [ ] |
| S37 | 124 | Apply frameworks where relevant; cite on first use | doctrine-moved | §Engine conventions › Strategic Frameworks, L315 | [ ] |
| S38 | 126–137 | Framework list (12 items: POEM … Channel choice) | doctrine-moved | same, L317–328 | [ ] |
| S39 | 139–148 | Key references list (9 items) | doctrine-moved | same, L330–339 | [ ] |
| S40 | 152 | Do not create book-extraction folders, summaries or extraction files | doctrine-moved | §Engine conventions › Book extractions…, L343 (overlaps Working Rules L171) | [ ] |
| S41 | 152 | Book knowledge lands only as task-oriented skill content with short citation; paraphrase; quotes ≤ 25 words | doctrine-moved | same, L343 (25-word limit and reference types are extra) | [ ] |
| S42 | 152 | `source_ingestion_guardrail.py` fails any file under a book-extraction path | doctrine-moved | same, L343 (overlaps L171) | [ ] |
| S43 | 154 | Reference files must not be single-book digests … cite as Author (Year) *Title*, Publisher (5 sentences) | duplicate | AGENTS.md Working Rules L172 (identical text) | [ ] |
| S44 | 158 | Deck outlines use this structured markdown format; every slide entry follows it | doctrine-moved | §Engine conventions › Deck outline format, L347 | [ ] |
| S45 | 160–169 | Slide-entry template (code block) | doctrine-moved | same, L349–358 | [ ] |
| S46 | 171 | Output is paste-ready into PowerPoint, Canva or Google Slides; no .pptx generated | doctrine-moved | same, L360 | [ ] |
| S47 | 177 | Listed skills should be referenced, not duplicated | doctrine-moved | §Engine conventions › Existing Skills, L364 | [ ] |
| S48 | 179–190 | Existing-skills table (10 rows) | doctrine-moved | same, L366–377 (overlaps Baseline Skills L97–108; blog-writer, blog-idea-generator, LinkedIn company pages and advertising entry rows are extra). Hard-coded list kept rather than marked obsolete, to avoid needing an obsolete tick | [ ] |
| S49 | 196–200 | Out-of-scope list (5 items incl. legal advice / pre-lawyer term sheet) | doctrine-moved | §Engine conventions › Out of Scope, L381–385 (overlaps L170; legal item extra) | [ ] |
| S50 | 204–211 | Upgrade priority order (6 items) | doctrine-moved | §Engine conventions › Upgrade Priority, L389–396 | [ ] |
| S51 | 213–231 | Design trigger block `v2` | duplicate | AGENTS.md L398–416 (text between markers compared: identical) | [ ] |

## Counts

| Class | Count |
|---|---|
| duplicate | 2 (S43, S51) |
| doctrine-moved | 49 |
| Claude-mechanics | 0 |
| obsolete | 0 |
| **Lost** | **0** |

## One `AGENTS.md` sentence added (not moved)

The new section opens with one framing sentence: "The sections below were moved verbatim from the former `CLAUDE.md` when it became the thin bridge (portfolio bridge contract, M10-02). They bind every runner." It records provenance; it changes no rule.

## Manifest

`.skills-engine/engine-manifest.yaml` gained `invariants:` (no `claude_only_block`, no exemptions):

- `british-english`: "Use British English throughout unless the target market or requested language requires otherwise." (Working Rules)
- `book-extraction-ban`: "Never store book extractions or book summaries in this repository (owner rule, 2026-09-23)." (Working Rules)
- `not-assessed`: "Missing source, rights, platform, render, approval, or performance evidence is `NOT ASSESSED`, never a pass." (Portfolio Craft Contract)

## Checks (engine root, 29 Sep 2026)

| Command | Result |
|---|---|
| `python -X utf8 scripts/validate_skill_engine.py --baseline quality-baseline.json` | `skills=191 compliant=191 failures=0`, exit 0 |
| `python -X utf8 scripts/routing_smoke_test.py` | `routing fixtures=56 passed=56 top_3_precision=1.000`, exit 0 |
| `python -X utf8 scripts/check_source_freshness.py` | `PASS (63 records within review windows; … claim support NOT ASSESSED)`, exit 0 |
| `python -X utf8 tests/agent-integration/test_social_media_agent_contract.py` | `PASS`, exit 0 |
| `python -X utf8 -m pytest tests -q` | 29 passed, 1 failed. The failure is `test_all_repository_markdown_links_resolve_or_are_external`, on `projects/maduuka-2026-09/node_modules/idb-keyval/README.md`, an ignored (`!!`) local folder. It is unrelated to this change. `test_active_routes_do_not_advertise_absent_deck_taxonomy`, which reads `CLAUDE.md` and `AGENTS.md`, passes |
