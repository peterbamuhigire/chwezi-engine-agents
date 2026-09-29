# Preservation maps — existing bridges aligned to the portfolio contract (M10-02-T02)

proposal-skills, chwezi-accounting-doctrine and windows-admin-engine-skills already imported `@AGENTS.md` but used three different preambles. Each is aligned to `docs/operations/claude-bridge-contract.md`. Classification decided by the M10-02 executor under Peter's delegated authority, 29 Sep 2026; reviewer ticks left open. Pre hashes are working-tree bytes before the edit.

## proposal-skills

| File | Pre SHA-256 | Pre bytes | Post SHA-256 | Post bytes |
|---|---|---|---|---|
| `CLAUDE.md` | `8dde854fbd7459f91ceb9a0aed22ec31ab45ef7590ed78b04c8ef918bf23f245` | 244 | `4be682eada8ee84820ee525682781cd8f1a56ac8a30c20c30763e034536b5e9f` | 44 |
| `AGENTS.md` | `c5ca7d1e4bdb7d161a7b7d52f713527c9ace1c65a1be64f83b9495022b699325` | 30,521 (CRLF) | `e339fd57e93f47de8ad242da5ea4177fbe412c29bf8e2325f0e1b5275afbb48f` | 30,516 (LF) |

| ID | Source line | Sentence (abridged) | Class | Destination | Reviewer |
|---|---|---|---|---|---|
| P01 | 1 | Heading `# CLAUDE.md` | structural | replaced by contract heading | [ ] |
| P02 | 3 | This is the Claude Code discovery bridge for proposal-skills | doctrine-moved | AGENTS.md, paragraph after "This repository is a dual-compatible skill system…" ("`CLAUDE.md` is only the Claude Code discovery bridge that imports this file") | [ ] |
| P03 | 4–5 | Canonical, model-neutral rules and routing remain in AGENTS.md, README.md, skills/SKILL.md | doctrine-moved | same paragraph, verbatim | [ ] |
| P04 | 5 | Keep this file free of duplicated policy | doctrine-moved | same paragraph ("keep it free of duplicated policy") | [ ] |
| P05 | 7 | `@AGENTS.md` | kept | bridge | [ ] |

Counts: doctrine-moved 3, duplicate 0, Claude-mechanics 0, obsolete 0. **Lost: 0.** Router effective bytes: 244 + 30,521 = 30,765 before; 44 + 30,516 = 30,560 after.

## chwezi-accounting-doctrine

| File | Pre SHA-256 | Pre bytes | Post SHA-256 | Post bytes |
|---|---|---|---|---|
| `CLAUDE.md` | `aee39974a4b7186ded762652cb8430935000b200d9e676983f9e585085c039d1` | 187 | `4be682eada8ee84820ee525682781cd8f1a56ac8a30c20c30763e034536b5e9f` | 44 |
| `AGENTS.md` | `0d37c911a7959f557c4d85e473da817a0c9b1cbbc63c270e79c8491be7e30d05` | 6,835 (CRLF) | `ad308e53a4c4720b978f8f7673c4c2e64f50ef3114d1fb755f719c8a18067802` | 8,683 (LF) |

| ID | Source line | Sentence (abridged) | Class | Destination | Reviewer |
|---|---|---|---|---|---|
| A01 | 1 | Heading `# Claude Code bridge` | structural | replaced by contract heading | [ ] |
| A02 | 3 | `@AGENTS.md` | kept | bridge | [ ] |
| A03 | 5 | The canonical instructions live in `AGENTS.md` | duplicate | AGENTS.md §Working rules ("Keep canonical instructions model-neutral… Runner-specific instructions belong only in a thin adapter") and the "model-neutral discovery and operating entry point" paragraph | [ ] |
| A04 | 5–6 | Keep this Claude-specific file thin so doctrine does not drift between runners | duplicate | AGENTS.md §Working rules, same bullet | [ ] |

Counts: duplicate 2, doctrine-moved 0, Claude-mechanics 0, obsolete 0. **Lost: 0.**

Other `AGENTS.md` additions in this repository (not moves from `CLAUDE.md`):
- `## Never store book extractions` — portfolio doctrine localised (the coordination package already binds every engine: "Never store book extractions in any engine or in this package"); the accounting router had no statement of it. Decided under Peter's delegated authority, 29 Sep 2026.
- The design trigger block `v2` at the end of `## Handoff` (M10-02-T06).

Router effective bytes: 187 + 6,835 = 7,022 before; 44 + 8,683 = 8,727 after.

## windows-admin-engine-skills

| File | Pre SHA-256 | Pre bytes | Post SHA-256 | Post bytes |
|---|---|---|---|---|
| `CLAUDE.md` | `6eaa7d95e5bc87aeff1c149e8106330f6a983d91a1457bf3ce2dad04612c2352` | 1,480 | `852e12657b4661425f964c9e4d0ddafb6c3cc9462341228f08d0ccb06d13b673` | 250 |
| `AGENTS.md` | `ef092e5559abb7ed64dcd36e4671594c24cddf95174d8da41b6dfaa9253cb91c` | 9,911 (CRLF) | `8710fac2f06305b26b7eafed6a28470f39f5d39a709a314d02dab9b8cfef98e4` | 11,846 (LF) |

| ID | Source line | Sentence (abridged) | Class | Destination | Reviewer |
|---|---|---|---|---|---|
| W01 | 1 | Heading `# CLAUDE.md — … (router for Claude Code)` | structural | replaced by contract heading | [ ] |
| W02 | 3 | `@AGENTS.md` | kept | bridge | [ ] |
| W03 | 5–6 | `AGENTS.md` is the runner-neutral router and doctrine; Claude Code follows it in full | duplicate | AGENTS.md §Purpose ("canonical, runner-neutral engine") and Codex-only section ("Claude and other runners must skip it and retain … full engine capabilities") | [ ] |
| W04 | 6 | Skip only its "Codex-only model setup" section | Claude-mechanics | Claude-only block, bullet 1 | [ ] |
| W05 | 8 | How to use this engine under Claude Code (lead-in) | structural | — | [ ] |
| W06 | 10 | Read `AGENTS.md`, then `rules/common/core.md` for non-trivial tasks | duplicate | AGENTS.md §Rules | [ ] |
| W07 | 11 | Glob `skills/**/SKILL.md` and route by frontmatter `description` | doctrine-moved | AGENTS.md §Start here, step 6 ("Discovery fallback: …") | [ ] |
| W08 | 11–12 | Read `SKILL.md` directly; not registered with the native `Skill` tool | Claude-mechanics | Claude-only block, bullet 2 | [ ] |
| W09 | 13–14 | Every host, domain or fleet change is preview-first and approval-gated as the skill specifies | doctrine-moved | AGENTS.md §Start here, step 7 | [ ] |
| W10 | 14–15 | Missing host, lab, source, live or recovery evidence is `NOT ASSESSED` | doctrine-moved | AGENTS.md §Start here, step 7 (also PORTFOLIO CRAFT CONTRACT) | [ ] |
| W11 | 16 | Validate with the commands declared in `.skills-engine/engine-manifest.yaml` | doctrine-moved | AGENTS.md §Start here, step 8 | [ ] |
| W12 | 18 | Heading `## Never store book extractions` | duplicate | AGENTS.md §Never store book extractions | [ ] |
| W13 | 20–22 | Extractions, summaries, chapter notes never stored (folders, `*-extraction.md`) | duplicate | AGENTS.md §Never store book extractions, first sentence | [ ] |
| W14 | 22–24 | Knowledge enters as paraphrased skill content and `references/` files (procedures, checklists, decision rules) with citation (Author (Year) *Title*, Publisher) | doctrine-moved | AGENTS.md §Never store book extractions (appended) | [ ] |
| W15 | 24 | Verbatim quotations rare and under 25 words | doctrine-moved | same section | [ ] |
| W16 | 25 | Staging notes live outside the repository and are never linked from skills | doctrine-moved | same section | [ ] |
| W17 | 25–27 | The portfolio check fails if an extraction folder appears | duplicate | same section ("enforces this"; appended wording kept for strictness) | [ ] |

Counts: duplicate 6, doctrine-moved 7, Claude-mechanics 2, obsolete 0, structural 2 (plus the kept import). **Lost: 0.**

Other `AGENTS.md` addition: the design trigger block `v2` before `## Change discipline` (M10-02-T06).

Router effective bytes: 1,480 + 9,911 = 11,391 before; 250 + 11,846 = 12,096 after.

## Validators after the change (29 Sep 2026)

- proposal: `validate_skills.py --baseline quality-baseline.json` active skills 115, findings 0; `routing_smoke_test.py` 25 fixtures, top-three precision 100.0%; agent contract PASS.
- accounting: `tools/validate-doctrine.ps1 -Strict` all sections pass (router-map, accounting-invariants, negative controls: 0 findings); agent contract PASS.
- windows: `validate_engine.py` validated_skills=19 findings=0; `routing_smoke_test.py` 19 fixtures, 0 failures; `source_ingestion_guardrail.py` 0 findings; `unittest discover -s tests/python` 23 tests OK.
