# Preservation map — design-system-skills (M10-02-T02 pilot)

Contract: `docs/operations/claude-bridge-contract.md`. Classification decided by the orchestrator's executor under Peter's delegated authority, 29 Sep 2026; reviewer ticks left open for the independent reviewer and Peter's pilot ratification.

## Hashes and sizes

| File | Pre SHA-256 | Pre bytes | Post SHA-256 | Post bytes |
|---|---|---|---|---|
| `CLAUDE.md` | `1c73164838f269164b07fdf3c014e849a184fe0c157a16c37d06a679cb58982a` | 4,093 (LF) | `d7dbf48536b73c69aa22adfa68d7b0c168796360f4a4dea2012e22c74986f0d0` | 212 (LF) |
| `AGENTS.md` | `3b76e5f90c9c6a7dab8bbb4155b3799cb4e3e0d78da04ec8951b73ca49bc5e21` | 9,570 (CRLF working copy; index is LF) | `021307bce491a774e63f8910621bbaf055e9a826effcc132e8f780740d688524` | 11,277 (LF) |

Router effective bytes (`CLAUDE.md` plus `@`-imported files): before 4,093 (the old `CLAUDE.md` had no `@AGENTS.md` import, so Claude loaded only it); after 212 + 11,277 = 11,489. Claude now loads the full runner-neutral router, which it previously did not.

The pre-change `AGENTS.md` was a CRLF working copy of an LF index blob; it was rewritten with LF endings, so `git diff` shows only the content lines changed (26 insertions, 2 deletions).

## Sentence table

Headings (`# CLAUDE.md — …`, `## Routing …`, `## Never store book extractions`, `## Font folder contract`, `## When invoked from another engine`) are structural and are replaced by the bridge heading or by the matching `AGENTS.md` section. The one heading with meaning, "The one rule that overrides convenience", is carried as S16a.

| ID | Source line | Sentence (abridged) | Class | Destination | Reviewer |
|---|---|---|---|---|---|
| S01 | 3–6 | Cross-cutting design engine; default presentation source in addition to domain engine, like finance | doctrine-moved | AGENTS.md §Relationship to other engines, L123–126 (verbatim) | [ ] |
| S02 | 8 | Skills are NOT on the native skill-discovery path | Claude-mechanics | Claude-only block (CLAUDE.md, `claude_only_block`) | [ ] |
| S03 | 8–9 | Read the `SKILL.md` files directly; do not use the `Skill` tool | Claude-mechanics | Claude-only block; also duplicate-of AGENTS.md L87–88 | [ ] |
| S04 | 13 | Read `doctrine/design-doctrine.md` first (anti-slop charter + map) | doctrine-moved | AGENTS.md §Protocol L84 (parenthetical "first (anti-slop charter + map)" added) | [ ] |
| S05 | 14–15 | Glob `skills/**/SKILL.md` fresh every time; route by frontmatter description | duplicate | AGENTS.md L85–86 | [ ] |
| S06 | 15 | Do not rely on any hardcoded skill list | duplicate | AGENTS.md L86 ("never a cached list") | [ ] |
| S07 | 15–16 | The README table is a hint only | duplicate | AGENTS.md L87 | [ ] |
| S08 | 16–17 | This makes newly added skills appear with no registration step | duplicate | AGENTS.md L86–87 ("picked up with zero registration") | [ ] |
| S09 | 18 | Apply the doctrine references in `doctrine/references/` | duplicate | AGENTS.md L89 | [ ] |
| S10 | 19–20 | Skill authoring/catalogue maintenance: apply authoring standard, run both quality commands | duplicate | AGENTS.md L92–94 and §Skill-engine release commands | [ ] |
| S11 | 24 | Never use a banned AI-slop font as primary typeface (path) | duplicate | AGENTS.md L98 | [ ] |
| S12 | 25–26 | Hard ban list: Inter … IBM Plex (all faces), bare system stacks alone | duplicate | AGENTS.md L98–100 (identical list) | [ ] |
| S13 | 26–27 | Secondary ban list: Space Grotesk … Nunito Sans | duplicate | AGENTS.md L100–101 | [ ] |
| S14 | 27–28 | Roboto Mono, IBM Plex Mono banned as monospace; Source Sans 3 paired body only | duplicate | AGENTS.md L101 | [ ] |
| S15 | 28–29 | State the chosen typeface(s) and reason before producing any artifact | duplicate | AGENTS.md L102 | [ ] |
| S16a | 22 (heading) | The banned-font rule overrides convenience | doctrine-moved | AGENTS.md §Hard rules L103 | [ ] |
| S16 | 29–30 | If the anti-slop checklist cannot be met, say so and ask; never fall back to Inter/system stack | doctrine-moved | AGENTS.md §Hard rules L103–104 (verbatim) | [ ] |
| S17 | 34–35 | Book extractions, summaries, chapter notes never stored (folders, `*-extraction.md`) | duplicate | AGENTS.md L36–37 (identical) | [ ] |
| S18 | 35–36 | Keeping them infringes copyright | duplicate | AGENTS.md L37–38 | [ ] |
| S19 | 36–38 | Book knowledge enters only as paraphrased skill content and `references/` with short citation | duplicate | AGENTS.md L38–40 | [ ] |
| S20 | 38 | Verbatim quotations stay rare and under 25 words | duplicate | AGENTS.md L40 | [ ] |
| S21 | 38–39 | Staging notes live outside the repository, never linked from skills | duplicate | AGENTS.md L40–41 | [ ] |
| S22 | 39–40 | `validate_engine.py` fails on extraction folder or links; plan/audit docs may name books | duplicate | AGENTS.md L41–42 | [ ] |
| S23 | 44–47 | Eight `fonts/` folders are fixed team taxonomy, not preference; names listed | doctrine-moved | AGENTS.md §Hard rules L109–111 (verbatim, with folder names) | [ ] |
| S24 | 47–48 | On a new device or after a taxonomy pull, ensure all eight directories exist | duplicate | AGENTS.md L106–107 | [ ] |
| S25 | 48–50 | Members may curate different font files but must not rename or replace categories | doctrine-moved | AGENTS.md §Hard rules L111–112 (verbatim) | [ ] |
| S26 | 54–57 | Named domain engines hand off here when work touches how an artifact looks (listed concerns) | doctrine-moved | AGENTS.md §Relationship to other engines L128–131 (verbatim) | [ ] |
| S27 | 57 | Content and structure stay in the domain engine; presentation comes here | doctrine-moved | AGENTS.md L131 (verbatim) | [ ] |
| S28 | 59–61 | Advertising creative arrives as a brief; returns concepts etc. under the handoff-contract path | doctrine-moved | AGENTS.md L133–135 (verbatim) | [ ] |
| S29 | 62 | Strategy, copy, legal release and measurement stay with the marketing engine | doctrine-moved | AGENTS.md L136 (verbatim) | [ ] |

## Consequential `AGENTS.md` edit (not a `CLAUDE.md` sentence)

`AGENTS.md` L80 read "Extends the guidance in `CLAUDE.md` with runner-neutral operations and the Codex adapter, kept for dual-compat tooling." After the conversion that statement is false (`CLAUDE.md` no longer carries guidance). It was replaced with "This file is the single runner-neutral router and doctrine for the engine; `CLAUDE.md` is a thin bridge that imports it (portfolio bridge contract, M10-02)." Recorded for the reviewer. [ ]

## Manifest additions (`.skills-engine/engine-manifest.yaml`)

- `claude_only_block`: the two-line Claude-only body above (byte-equal to the `CLAUDE.md` section body).
- `invariants`: `book-extraction-ban`, `not-assessed`, `banned-font-primary` (all verified present in post-change `AGENTS.md`).
- `invariant_exemptions`: `british-english` — no British English output rule exists in the design router; adding one would be new doctrine.
- Design is the owner of the trigger block, so it carries no `design-trigger` copy in its own `AGENTS.md`.

## Counts

| Class | Count |
|---|---|
| duplicate | 18 (S05–S15, S17–S22, S24; S03 is also present in AGENTS.md but is counted as mechanics) |
| doctrine-moved | 10 (S01, S04, S16a, S16, S23, S25–S29) |
| Claude-mechanics | 2 (S02, S03) |
| obsolete | 0 |

Total sentences: 30 (S01–S29 plus S16a). **Lost: 0.**

## Regression (run from the engine root, 29 Sep 2026)

- `python -X utf8 scripts/validate_engine.py --baseline tests/quality-baseline.json` → `skills=101 fully_compliant=101`, exit 0.
- `python -X utf8 scripts/routing_smoke_test.py` → `routing fixtures=68 precision@1=85% precision@3=100%`, exit 0 (routing reads skills, not routers; unchanged).
- `python -X utf8 tests/agent-integration/test_design_agent_contract.py` → `PASS: design-system-skills agent contract`.
- `python -X utf8 -m pytest tests -q -p no:cacheprovider` → 99 passed.
- No script or test in `scripts/` or `tests/` reads `CLAUDE.md`.
