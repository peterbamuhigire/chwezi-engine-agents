# Preservation map — business-plan-skills (M10-02-T02)

Contract: `docs/operations/claude-bridge-contract.md`. Pilot format: `design-system-skills.md`. Classification decided by the executor under Peter's delegated authority, 29 Sep 2026; reviewer ticks left open for the independent reviewer.

## Hashes and sizes

| File | Pre SHA-256 | Pre bytes | Post SHA-256 | Post bytes |
|---|---|---|---|---|
| `CLAUDE.md` | `825f1a20f94a8e63f105ee517714a4fcb22f5bd0424b02d41e175490a2a09086` | 19,781 (CRLF working copy) | `f139502a2e31ad71897c144e142930e503d368b2f6088bb69a959042e4e3ce12` | 222 (LF) |
| `AGENTS.md` | `6bfea5e9f53aacf4809643ce8b91d9da1ff57e30235db699f3698d8adc543e35` | 23,812 (CRLF working copy) | `37b4abd0171476eed22b66ada21cfa4b7433dfadadd1fad05aac8d9f4cb5d0a7` | 38,154 (LF) |

Router effective bytes: before 19,781 (the old `CLAUDE.md` had no `@AGENTS.md` import); after 222 + 38,154 = 38,376. Claude now loads the full runner-neutral router. Both pre files were CRLF working copies of LF blobs and were rewritten with LF; `git diff AGENTS.md` shows 136 insertions and 0 deletions — no existing `AGENTS.md` sentence was changed.

## Method

Large uniform blocks (the skill-category list, the methodology list, the currency, multi-country, source-referencing and anti-slop sections) were moved verbatim as whole blocks; each row below covers one bullet or sentence unless it names a line range, in which case every sentence in the range has the same class and destination. Structural headings are recreated in `AGENTS.md` where their block moved, or dropped where the block is a duplicate.

## Sentence table

| ID | Source line | Sentence (abridged) | Class | Destination | Reviewer |
|---|---|---|---|---|---|
| S01 | 5 | Collection of Claude Code skills for generating bankable business plans | duplicate | AGENTS.md §Purpose L63 (dual-surface suite for bankable plans) | [ ] |
| S02 | 5 | Active skills live under `skills/<category>/<skill-name>/SKILL.md`; self-contained with optional `references/` | doctrine-moved | AGENTS.md §Current Layout L83 (verbatim; AGENTS L67 only gave `skills/<skill-name>/`) | [ ] |
| S03 | 7 | Also read `AGENTS.md` and `README.md` for runner-agnostic doctrine this file does not duplicate | Claude-mechanics | Claude-only block (README part); the `AGENTS.md` part is now the `@AGENTS.md` import | [ ] |
| S04 | 7 | Skip only the explicitly Codex-only sections (e.g. "Codex-only model setup") | Claude-mechanics | Claude-only block | [ ] |
| S05 | 9 | Root holds project documentation plus `docs/`, `skills/`, `projects/` | duplicate | AGENTS.md L81 | [ ] |
| S06 | 9 | Keep `docs/`, `.git`, `tools/` and non-skill operational directories at root | duplicate | AGENTS.md L81 (AGENTS also names `projects/`) | [ ] |
| S07 | 13 | Skills grouped into categories; use `skills/<category>/<skill-name>/` paths; bare names valid | doctrine-moved | AGENTS.md §Skill Categories L87 | [ ] |
| S08 | 15–37 | Category list (23 bullets incl. 7 `advisory-deliverables` sub-bullets; `meta-finance/` appears twice in the source, both kept) | doctrine-moved | AGENTS.md §Skill Categories L89–111 (verbatim) | [ ] |
| S09 | 41–43 | Naming conventions (3 bullets) | doctrine-moved | AGENTS.md §Naming Conventions L115–117 | [ ] |
| S10 | 47 | Every active skill follows the July 2026 contract in `skill-writing` and its template | duplicate | AGENTS.md L136 + L138–141 | [ ] |
| S11 | 48 | Frontmatter: directory name, one-line `Use when` ≤ 350 chars, portable metadata | duplicate | AGENTS.md L136 | [ ] |
| S12 | 49 | Skills declare triggers, inputs, outputs, evidence, workflow, decisions, quality, five anti-patterns, permissions, degraded mode, references | duplicate | AGENTS.md L136 | [ ] |
| S13 | 50 | Audit/review skills read-only; mutation, publishing, spending, destructive action, certification need explicit authority | doctrine-moved | AGENTS.md §Canonical Authoring Standard, "Additional authoring rules" (AGENTS L136 had only the read-only half) | [ ] |
| S14 | 51 | Keep `SKILL.md` ≤ 500 lines and use British English | doctrine-moved | same list (British English for skills was only "where natural" in AGENTS L168) | [ ] |
| S15 | 52 | Run zero-debt validator and routing smoke test before release; see `CONTRIBUTING.md` | duplicate | AGENTS.md §Verification (validator, smoke test, zero debt, `CONTRIBUTING.md`) | [ ] |
| S16 | 53 | Route full plans through `business-plan-orchestrator`; `00-plan-assembly` only for final packaging; validate release bundle | doctrine-moved | "Additional authoring rules" (the "only for final packaging" limit was implicit in AGENTS) | [ ] |
| S17 | 54 | Validate source register, apply sector gates, run formula-map auditor on XLSX | duplicate | AGENTS.md §Default Baseline (country-market register, sector gates, `formula_map.py`) | [ ] |
| S18 | 55 | `meta-investment-committee-red-team` only after complete pack; simulation is not approval | doctrine-moved | "Additional authoring rules" ("simulation is not approval" absent from AGENTS) | [ ] |
| S19 | 59–74 | Key Methodologies (16 bullets: Rogoff, On Target, SMART, phrase bank, business-model scoring, evidence class, King, AI section, digital transformation, website, retail, pricing, direct response, commercial system, business-case test, critical thinking) | doctrine-moved | AGENTS.md §Plan Content Doctrine › Key Methodologies (verbatim) | [ ] |
| S20 | 78 | Book extractions, summaries and raw source text never stored; former folder removed 2026-09-23 | duplicate | AGENTS.md §Book extractions and source text | [ ] |
| S21 | 78 | Books are durable concept inputs; paraphrase into `references/` with brief citation | duplicate | same section | [ ] |
| S22 | 78 | `source_ingestion_guardrail.py` blocks any `book-extractions/` path | duplicate | same section ("fails on any `book-extractions/` path") | [ ] |
| S23 | 82–87 | When Generating Plan Content (6 bullets) | doctrine-moved | AGENTS.md §Plan Content Doctrine › When Generating Plan Content (verbatim; bullets 5–6 overlap Core Rules but carry extra detail) | [ ] |
| S24 | 91–98 | Currency and Localisation (UGX default, dated FX rule, 4 cost sub-bullets, regulators, institutions) | doctrine-moved | › Currency and Localisation (verbatim) | [ ] |
| S25 | 102–119 | Multi-Country Plans (country-context use, 6 numbered replacements, universal frameworks list, Uganda default, new-country template) | doctrine-moved | › Multi-Country Plans (Non-Uganda) (verbatim) | [ ] |
| S26 | 123–125 | Source Referencing (3 bullets) | doctrine-moved | › Source Referencing (verbatim) | [ ] |
| S27 | 130–151 | Anti-AI-Slop Quality Gate (skill locations; `anti-ai-slop` mandatory in real time, scope, order, verify-before-emit; `ai-slop-audit` cadence, F blocks, auto-run triggers, graded report) | doctrine-moved | AGENTS.md §Anti-AI-Slop Quality Gate (verbatim; AGENTS Task Routing/Core Rules held only the summary) | [ ] |
| S28 | 155–168 | Finance & Accounting Trigger scope list | duplicate | AGENTS.md §Finance & Accounting Trigger (identical) | [ ] |
| S29 | 170–176 | Trigger steps 1–5 | duplicate | same section (AGENTS says "corresponding finance skill" and numbers the last step 6; content identical) | [ ] |
| S30 | 178 | `finance-module-audit` auto-runs on any system with a finance element | duplicate | same section (identical) | [ ] |
| S31 | 181–199 | Design trigger block v2 | duplicate | AGENTS.md trigger block (text between markers byte-identical after CRLF normalisation; checked with `diff`) | [ ] |

## Counts

| Class | Rows | Notes |
|---|---|---|
| duplicate | 17 | S01, S05, S06, S10–S12, S15, S17, S20–S22, S28–S31 (+ S03's `AGENTS.md` half) |
| doctrine-moved | 12 | S02, S07–S09, S13, S14, S16, S18, S19, S23–S27 (block rows cover 70+ bullets/sentences) |
| Claude-mechanics | 2 | S03 (README half), S04 |
| obsolete | 0 | |
| **Lost** | **0** | |

## Checks after conversion (engine root, exit codes)

- `validate_skill_engine.py --baseline docs/quality/skill-quality-baseline.json`: exit 0 (fully compliant 137).
- `routing_smoke_test.py --threshold 1.0`: exit 0, 61/61 top-three (100.0%).
- `tests/agent-integration/test_business_plan_agent_contract.py`: PASS.
- `routing_link_check.py` (reads `CLAUDE.md` and `AGENTS.md`; moved paths are now checked in `AGENTS.md`): 7 surfaces, 0 failures before and after.
- `pytest tests`: 61 passed, 1 failed — `test_runtime_orchestration_guidance.py::test_contract_is_linked_and_has_required_controls` asserts `README.md` names `runtime-agnostic-orchestration-2026-09-07.md`; `README.md` was not touched, so this failure predates the conversion (README rewrite, commit `27c2c9b`).
