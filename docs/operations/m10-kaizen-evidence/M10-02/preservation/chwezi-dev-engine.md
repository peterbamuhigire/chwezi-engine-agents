# Preservation map — chwezi-dev-engine (M10-02-T01 bridge alignment)

Contract: `docs/operations/claude-bridge-contract.md`. Classification decided by the M10-02 executor under Peter's delegated authority, 29 Sep 2026; reviewer ticks left open.

The dev engine already had a thin bridge. The only change is that the duplicated `## Never store book extractions` section, which the dev test used to allow, leaves the bridge because the portfolio contract treats it as doctrine that belongs in `AGENTS.md`.

## Hashes and sizes

| File | Pre SHA-256 (working tree) | Pre bytes | Post SHA-256 | Post bytes |
|---|---|---|---|---|
| `CLAUDE.md` | `d499f8aba2d733799c25199524b787b1296808ded2545101c16f659fd7c95843` | 1,037 | `4be682eada8ee84820ee525682781cd8f1a56ac8a30c20c30763e034536b5e9f` | 44 |
| `AGENTS.md` | `7e077a6e0babe5d093a994d225000f0e55270e011003441982c974f51a166be6` | 15,194 (CRLF working copy) | unchanged | 15,194 |

Router effective bytes: before 1,037 + 15,194 = 16,231; after 44 + 15,194 = 15,238.

## Sentence table

| ID | Source line | Sentence (abridged) | Class | Destination | Reviewer |
|---|---|---|---|---|---|
| D01 | 1–3 | Bridge heading and `@AGENTS.md` | kept | bridge | [ ] |
| D02 | 5 | Heading `## Never store book extractions` | duplicate | AGENTS.md L91 | [ ] |
| D03 | 7–9 | Book extractions, summaries, chapter notes never stored (folders, `*-extraction.md`) | duplicate | AGENTS.md L93–96 | [ ] |
| D04 | 9 | Keeping them infringes copyright | duplicate | AGENTS.md L96–97 | [ ] |
| D05 | 9–12 | Knowledge enters only as paraphrased skill content and `references/` with short citation | duplicate | AGENTS.md L97–101 (superset: adds anti-patterns, task organisation) | [ ] |
| D06 | 12 | Verbatim quotations rare and under 25 words | duplicate | AGENTS.md L101–102 | [ ] |
| D07 | 12–13 | Never cite a local ebook path or shadow-library file name | duplicate | AGENTS.md L102 | [ ] |
| D08 | 13–14 | Staging notes live outside the repository, never linked | duplicate | AGENTS.md L102–103 | [ ] |
| D09 | 14–16 | `source_ingestion_guardrail.py` (also run by `skill_catalog_guardrails.py`) fails on folder, file or link | duplicate | AGENTS.md L106–110 (superset: adds ebook-path citation) | [ ] |
| D10 | 16–17 | Plan and audit documents may name books but not store content | duplicate | AGENTS.md L110–111 | [ ] |

Counts: duplicate 9, doctrine-moved 0, Claude-mechanics 0, obsolete 0. **Lost: 0.**

Test alignment: `tests/test_engine_control_plane.py` `BRIDGE_ALLOWED_SECTION` changed from `## Never store book extractions` to `## Claude-only notes`, with a 25-line limit and a new test proving the book-extraction section is now rejected in the bridge.
