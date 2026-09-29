# Preservation map — digital-research-engine (M10-02-T02)

Contract: `docs/operations/claude-bridge-contract.md`. Pilot format: `design-system-skills.md`. Classification decided by the orchestrator's executor under Peter's delegated authority, 29 Sep 2026; reviewer ticks left open for the independent reviewer.

## Hashes and sizes

| File | Pre SHA-256 | Pre bytes | Post SHA-256 | Post bytes |
|---|---|---|---|---|
| `CLAUDE.md` | `b1c60b511772d2069e5a8bd187ea3840186b6a3d4d551f40cd67550760e25993` | 11,435 (LF) | `2029f55f80e20417e1b7359a5d2fd94b124813b657a7f58c5e79417f300a0ef2` | 889 (LF) |
| `AGENTS.md` | `6ab87b7e2077e81b5edcedc4c3a855ff290edcf304e92c6804e8737adf537497` | 14,395 (CRLF working copy) | `857dcbcfeec81d70a9f18dcc6b379594e02bbfdc64f0b09060930b3f8ab90f1b` | 19,568 (LF) |

Router effective bytes (`CLAUDE.md` plus `@`-imported files): before 11,435 (the old `CLAUDE.md` had no `@AGENTS.md` import); after 889 + 19,568 = 20,457. Claude now loads the full runner-neutral router, which it previously did not.

`AGENTS.md` was a CRLF working copy; it was rewritten with LF endings (git diff shows content lines only). The design trigger block (source lines 145–163) and the book-extraction section (source lines 15–25) were compared line by line with the `AGENTS.md` copies and are identical.

One existing `AGENTS.md` sentence was edited because the conversion made it false: "See also — `CLAUDE.md` — the Claude-Code-specific equivalent" now reads "`CLAUDE.md` — thin Claude Code bridge that imports this file (portfolio bridge contract, M10-02)". No other existing `AGENTS.md` text was changed.

## Sentence table

Headings are structural. Each carried section keeps its heading in `AGENTS.md` (Skill priority order, File-write conventions, Scope-exclusion discipline, When the user asks for elaboration, Proposal-output trigger) or maps to an existing one; "Standard research workflow" content lands under the new "Research wave discipline" section beside the existing "Standard workflow".

| ID | Source line | Sentence (abridged) | Class | Destination | Reviewer |
|---|---|---|---|---|---|
| S01 | 3 | Operating instructions for Claude Code working inside this engine | duplicate | AGENTS.md L65 ("Operating instructions for Codex and other agent runtimes…"), now loaded by Claude through the bridge | [ ] |
| S02 | 7 | Do not hallucinate; nothing appears unless traceable to a real source | duplicate | AGENTS.md §The one rule, L69 (superset: adds "claim") | [ ] |
| S03 | 9 | This is enforced by the `source-evaluation` skill | doctrine-moved | AGENTS.md §The one rule, L73 | [ ] |
| S04 | 9 | Read source-evaluation SKILL.md and evidence-discipline.md before research | duplicate | AGENTS.md L71 | [ ] |
| S05 | 9 | Hard-constraint clause must appear verbatim in every sub-agent prompt | duplicate | AGENTS.md L71 | [ ] |
| S06 | 11 | Strike sub-agent content that violates evidence discipline | doctrine-moved | AGENTS.md §The one rule, L73 | [ ] |
| S07 | 11 | Don't paper over; log in `EVIDENCE-AUDIT.md`, adjust next prompt | doctrine-moved | AGENTS.md §The one rule, L73 | [ ] |
| S08 | 15–16 | Book extractions/summaries/chapter notes never stored (folders, files) | duplicate | AGENTS.md §Never store book extractions (identical) | [ ] |
| S09 | 17 | Keeping them infringes copyright | duplicate | same (identical) | [ ] |
| S10 | 17–20 | Book knowledge enters only as paraphrased task-oriented content with citation | duplicate | same (identical) | [ ] |
| S11 | 20 | Verbatim quotations rare and under 25 words | duplicate | same (identical) | [ ] |
| S12 | 21 | Staging notes live outside the repository | duplicate | same (identical) | [ ] |
| S13 | 22–24 | `check_no_book_extractions.py` fails on extraction folder or link | duplicate | same (identical) | [ ] |
| S14 | 24–25 | Research-technique extraction files are methods, not book extractions | duplicate | same (identical) | [ ] |
| S15 | 29 | Workflow triggered by "research X", "find pain points of Y", "do another pass" | doctrine-moved | AGENTS.md §Research wave discipline, intro | [ ] |
| S16 | 31 | Plan the waves: one sub-agent per cohort | duplicate | AGENTS.md §Standard workflow step 3 ("For each cohort: dispatch a research sub-task"); also restated in Claude-only bullet 1 | [ ] |
| S17 | 31 | Use `Agent` tool, `subagent_type: content-marketing:search-specialist` (or `general-purpose`) | Claude-mechanics | Claude-only block, bullet 1 | [ ] |
| S18 | 32 | Brief each agent self-contained; they don't see conversation history | doctrine-moved | AGENTS.md §Research wave discipline, bullet 1 | [ ] |
| S19 | 33–37 | Brief includes goal/scope/out-of-scope, themes, sources, deliverable shape, verbatim clause | doctrine-moved | same bullet (list joined into one sentence) | [ ] |
| S20 | 38 | Run in parallel where independent | doctrine-moved | AGENTS.md §Research wave discipline, bullet 2 | [ ] |
| S21 | 38 | Multiple `Agent` tool calls in one message | Claude-mechanics | Claude-only block, bullet 2 | [ ] |
| S22 | 39 | Background mode (`run_in_background: true`) for waves > 2 minutes | Claude-mechanics | Claude-only block, bullet 3 | [ ] |
| S23 | 40 | Never read sub-agent transcripts with the shell tool — overflow context | Claude-mechanics | Claude-only block, bullet 4 | [ ] |
| S24 | 40 | Use the structured `<result>` block in the completion notification | Claude-mechanics | Claude-only block, bullet 4 | [ ] |
| S25 | 41 | Verify before merging: spot-check 10% stats, 5 quotes, all court/statute citations | doctrine-moved | AGENTS.md §Research wave discipline, bullet 3 | [ ] |
| S26 | 42 | Run critical reasoning before synthesis or final drafting | duplicate | AGENTS.md §Standard workflow step 5 | [ ] |
| S27 | 43 | Write outputs to cohort research/analysis/opportunities; append when merging Wave-2 | doctrine-moved | AGENTS.md §Research wave discipline, bullet 4 (paths also in §Output paths) | [ ] |
| S28 | 44 | Cross-cohort synthesis via `mind-mapping-and-synthesis`, orchestrator only | duplicate | AGENTS.md §Standard workflow step 6 | [ ] |
| S29 | 45 | Word doc via `research-output-formats` → `professional-word-output` or `python-document-generation` | doctrine-moved | AGENTS.md §Research wave discipline, bullet 5 (step 8 lacked `professional-word-output`) | [ ] |
| S30 | 46 | Run `ai-slop-audit` before delivering any report or `.docx` | doctrine-moved | AGENTS.md §Research wave discipline, bullet 6 | [ ] |
| S31 | 46 | Output reads as a professional human researcher's: sourced, authored judgement, varied structure, counter-case | doctrine-moved | same bullet | [ ] |
| S32 | 46 | Grade F blocks delivery until fixed | doctrine-moved | same bullet (step 9 carries a shorter form) | [ ] |
| S33 | 50 | "For any non-trivial task:" (priority order intro) | doctrine-moved | AGENTS.md §Skill priority order | [ ] |
| S34 | 52 | `anti-ai-slop` real-time, every output, every time | doctrine-moved | same, item 0 (verbatim) | [ ] |
| S35 | 52 | Quality counterpart to evidence-discipline: sourced report can still read as slop | doctrine-moved | same, item 0 | [ ] |
| S36 | 52 | Apply continuously while writing | doctrine-moved | same, item 0 | [ ] |
| S37 | 52 | Run `ai-slop-audit` after each major iteration; grade F blocks progression | doctrine-moved | same, item 0 | [ ] |
| S38–S46 | 53–61 | Priority items 1–9 (evidence-discipline … research-output-formats last) | doctrine-moved | same, items 1–9 (verbatim; nine rows uniformly classified) | [ ] |
| S47 | 65 | Append, don't overwrite; `# Pass 2 — Gap-fill addendum` headers | doctrine-moved | AGENTS.md §File-write conventions (verbatim) | [ ] |
| S48 | 66 | Never delete a sourced claim without logging in `EVIDENCE-AUDIT.md` | doctrine-moved | same | [ ] |
| S49 | 67 | Mark gaps explicitly; "no source found" is valid, filler is not | doctrine-moved | same | [ ] |
| S50 | 68 | Date every research file at the top | doctrine-moved | same | [ ] |
| S51 | 69 | List sources by tier in `sources.md` | doctrine-moved | same | [ ] |
| S52 | 73 | Hard exclusion set by the user (intro) | doctrine-moved | AGENTS.md §Scope-exclusion discipline (verbatim) | [ ] |
| S53 | 75 | Restate it verbatim in every sub-agent brief | doctrine-moved | same | [ ] |
| S54 | 76 | If a sub-agent returns it, filter before writing files | doctrine-moved | same | [ ] |
| S55 | 77 | Track the exclusion in the project `README.md` | doctrine-moved | same | [ ] |
| S56 | 81 | Default reflex: find a new source | doctrine-moved | AGENTS.md §When the user asks for elaboration (verbatim) | [ ] |
| S57 | 81 | Alternatives: restate source more thoroughly, or acknowledge the gap | doctrine-moved | same | [ ] |
| S58 | 81 | Never embellish with plausible-sounding additions | doctrine-moved | same | [ ] |
| S59 | 85 | `Agent` — for every research wave | Claude-mechanics | Claude-only block, bullet 5 | [ ] |
| S60 | 86 | `WebFetch` — URL verification, statistic re-check, abstract retrieval | Claude-mechanics | Claude-only block, bullet 5 | [ ] |
| S61 | 87 | `Read` — cross-checking draft outputs | Claude-mechanics | Claude-only block, bullet 5 | [ ] |
| S62 | 88 | `Write` / `Edit` — for the markdown corpus | Claude-mechanics | Claude-only block, bullet 5 | [ ] |
| S63 | 89 | `Grep` — duplicate citations across cohorts (triangulation) | Claude-mechanics | Claude-only block, bullet 5 | [ ] |
| S64 | 93 | Avoid `Bash`-based tail of sub-agent output files | Claude-mechanics | Claude-only block, bullet 4 | [ ] |
| S65 | 94 | Avoid direct `.docx` editing — markdown canonical, Word generated | doctrine-moved | AGENTS.md §File-write conventions, last bullet | [ ] |
| S66 | 98 | Every project lives under `projects/<project-id>/` | doctrine-moved | AGENTS.md §Project structure invariants, bullet 1 | [ ] |
| S67 | 99 | Kernel project required files and folders | duplicate | AGENTS.md §Project structure invariants (identical list) | [ ] |
| S68 | 100 | Cohort sub-project required files and folders | duplicate | same (identical list) | [ ] |
| S69 | 101 | Final report is `projects/<project-id>/report-v<N>-<date>.docx` | duplicate | AGENTS.md §Output paths | [ ] |
| S70 | 105 | Use these commands for project-managed work | doctrine-moved | AGENTS.md §Kernel commands, intro | [ ] |
| S71 | 107–114 | Kernel steps doctor, new-project, sync, status, validate, assemble, pack | duplicate | AGENTS.md §Kernel commands 1–7 (identical) | [ ] |
| S72 | 109 | Run `00-meta-initialization` and complete `_context/` (step 3) | doctrine-moved | AGENTS.md §Kernel commands, intro ("After step 2, … before `sync`") | [ ] |
| S73 | 118 | Discover active skills from filesystem; proposal engine not in catalogue; no README inventory | duplicate | AGENTS.md §Skill authoring and release gates (identical) | [ ] |
| S74 | 119 | Follow skill-authoring standard; start from template | duplicate | same (identical) | [ ] |
| S75 | 120 | Preserve the 59-skill catalogue | duplicate | same (identical) | [ ] |
| S76 | 121 | Run the three release validators | duplicate | same (identical) | [ ] |
| S77 | 122 | Run canonical `quick_validate.py`; unavailable check is not assessed | duplicate | same (identical) | [ ] |
| S78 | 126 | Proposal outputs (full list incl. "other persuasive document") route final drafting to proposal-skills | doctrine-moved | AGENTS.md §Proposal-output trigger (section moved verbatim; Standard workflow step 7 carries a shorter list) | [ ] |
| S79 | 128 | Parent router path | doctrine-moved | same (also in step 7) | [ ] |
| S80 | 129 | Section sub-skills `pipeline\01-cover-letter\` through `10-financial-proposal\` | doctrine-moved | same | [ ] |
| S81 | 130 | Cross-cutting families: domain-delivery, strategy-positioning, writing-content | doctrine-moved | same | [ ] |
| S82 | 131 | Load the profiles router before drafting | doctrine-moved | same (also in step 7) | [ ] |
| S83 | 132 | Language standards: British English; East African tone; day-month-year dates; proposal gates | doctrine-moved | same; recorded as the `british-english` invariant | [ ] |
| S84 | 134 | Proposal engine evolves in its own repository | doctrine-moved | same | [ ] |
| S85 | 136 | Research corpus is input to proposal pipeline; output to `05-output/`; export chain | doctrine-moved | same | [ ] |
| S86 | 140 | See also: `AGENTS.md` — Codex / generic-agent equivalent of this file | obsolete | False after conversion: `AGENTS.md` is now the single router that `CLAUDE.md` imports, not an equivalent; the reciprocal `AGENTS.md` line was corrected. Needs Peter's tick. | [ ] |
| S87 | 141 | See also: `PROJECT_BRIEF.md` — engine mission & direction | duplicate | AGENTS.md §See also ("engine mission") | [ ] |
| S88 | 142 | See also: source-evaluation SKILL.md + evidence-discipline.md | duplicate | AGENTS.md §The one rule, L71 | [ ] |
| S89 | 143 | See also: proposal-skills standalone engine | duplicate | AGENTS.md §Proposal-output trigger (S78, S84) | [ ] |
| S90 | 145–163 | Design trigger block v2 (markers and body) | duplicate | AGENTS.md trigger block (identical between markers) | [ ] |

## Counts

S38–S46 count as nine sentences, so the table covers 90 sentences.

| Class | Rows | Count |
|---|---|---|
| duplicate | S01, S02, S04, S05, S08–S14, S16, S26, S28, S67–S69, S71, S73–S77, S87–S90 | 27 |
| doctrine-moved | S03, S06, S07, S15, S18–S20, S25, S27, S29–S58, S65, S66, S70, S72, S78–S85 | 51 |
| Claude-mechanics | S17, S21–S24, S59–S64 | 11 |
| obsolete | S86 | 1 |
| lost | — | 0 |

Lost: 0.

## Invariants recorded (`.skills-engine/engine-manifest.yaml`)

- `british-english`: "Language standards: British English; East African professional tone; day-month-year dates"
- `book-extraction-ban`: "Book extractions, book summaries and chapter-by-chapter notes must never be stored in this"
- `not-assessed`: "Missing source, locator, currentness, reviewer, or product evidence is `NOT ASSESSED`, never a pass."
- `no-hallucination` (engine-specific): "**Do not hallucinate.** No claim, statistic, quote, name, court case, statute, organisation, or URL"

`claude_only_block` holds the five Claude-only bullets; the rendered bridge equals `CLAUDE.md` byte for byte (checked).

## Verification (engine root, 29 Sep 2026)

- `python -X utf8 scripts/skill_contract_validator.py --baseline tests/skill-engine/quality-baseline.json` → 59 active, 59 fully compliant, exit 0
- `python -X utf8 scripts/routing_smoke_test.py` → 29/29, top-3 precision 1.000, exit 0
- `python -X utf8 scripts/validate_engine.py` → exit 0 (runs routing smoke test, book-extraction check, `engine doctor`, engine unit tests)
- `python -X utf8 tests/agent-integration/test_digital_research_agent_contract.py` → PASS
- `engine/cli.py` doctor only requires `CLAUDE.md` to exist (still true); `engine/scaffold.py` writes per-project `CLAUDE.md` files and is unaffected.
