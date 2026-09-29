# Preservation map — srs-skills (M10-02-T02)

Contract: `docs/operations/claude-bridge-contract.md`. Classification decided by the orchestrator's executor under Peter's delegated authority, 29 Sep 2026; reviewer ticks left open for the independent reviewer. Only `CLAUDE.md`, `AGENTS.md` and `.skills-engine/engine-manifest.yaml` were edited (another executor holds srs `scripts/`, `engine/` and `docs/`).

## Hashes and sizes

| File | Pre SHA-256 (working copy) | Pre bytes | Post SHA-256 | Post bytes |
|---|---|---|---|---|
| `CLAUDE.md` | `db46ab6844a955f384ddf80882110b3cfda5bd2a712c9fee3a8f5fdeece8bd88` | 33,849 (CRLF) | `4be682eada8ee84820ee525682781cd8f1a56ac8a30c20c30763e034536b5e9f` | 44 (LF) |
| `AGENTS.md` | `a518d0040bc7435ccf976b080399216e35a912a384a4f6f44a24a3429c94c536` | 21,330 (CRLF) | `fc39674072854e889b293ef04d7cf8d4947aa356c9a1fcd943b7e6ef77021811` | 49,688 (LF) |

Index blobs at `HEAD` (`15422d7`): `CLAUDE.md` `ba4f23b391ce4d2e64284364139040e28734abd1d34c58369ac01396fa37769d`, `AGENTS.md` `aec47b836e5c092dd17574bb21fc4a92076ce82fed85171adb12d4496f194440`.

Router effective bytes (`CLAUDE.md` plus `@`-imported files): before 33,849 (no `@AGENTS.md` import; Claude loaded `CLAUDE.md` only); after 44 + 49,688 = 49,732. Claude now loads the whole runner-neutral router, and Codex gains the SRS protocols it previously lacked.

No Claude-only section: every runner-mechanics statement is already in `AGENTS.md` (Codex-only section gated at `AGENTS.md` L5–6; "read the matching SKILL.md directly" in §Skill Families and in the moved Directory Logic bullet). `claude_only_block` is therefore omitted from the manifest.

Mechanical check: every non-blank `CLAUDE.md` line was searched for verbatim in the new `AGENTS.md`; the 29 lines not found verbatim are all accounted for below as duplicate, structural heading, or near-verbatim adjustment.

## Edits to existing `AGENTS.md` text made false by the conversion

| Line (old) | Old | New |
|---|---|---|
| L61 | "Preserve the existing Claude Code workflow defined in CLAUDE.md." | "…now held in this file; CLAUDE.md is a thin bridge that imports it (portfolio bridge contract, M10-02)." |
| L67 | "see the 'Skill Categories' section in `CLAUDE.md`" | "see the 'Skill Categories' section below" |
| L177–178 | "`CLAUDE.md` remains the Claude-specific root protocol and should not be replaced by this file." / "`AGENTS.md` provides Codex-facing baseline behavior and repository routing." | "`AGENTS.md` is the single runner-neutral root protocol…" / "`CLAUDE.md` is a thin bridge (`@AGENTS.md`)…; do not add doctrine to it." |

## Sentence table

Headings are structural and are replaced by the bridge heading or by the same heading in `AGENTS.md`. Where a list or table is uniformly classified it is mapped as one row group, stated in the row. New `AGENTS.md` sections were inserted after §Compatibility Notes and before §Finance & Accounting Trigger, in the original `CLAUDE.md` order.

| ID | Source line | Sentence (abridged) | Class | Destination | Reviewer |
|---|---|---|---|---|---|
| S01 | 1 | `# AI Assistant Protocol: SRS-Skills` (title) | duplicate (structural) | replaced by bridge heading | [ ] |
| S02 | 5 | You are an expert Systems Architect … IEEE-compliant skills … high-fidelity SRS | doctrine-moved | AGENTS.md §Project Mission (verbatim) | [ ] |
| S03 | 9 | Repository Root: this directory holds root docs and repository-level folders | duplicate | AGENTS.md §Skill Families ("Root directories are reserved…") | [ ] |
| S04 | 10 | Engineering skills live in Chwezi Dev Engine (URL, checkout, layout); consult router; read SKILL.md; use for methodology selection… | doctrine-moved | AGENTS.md §Directory Logic & Pathing (verbatim; URL and "use these skills for…" absent from §Skill Families) | [ ] |
| S05 | 11 | Finance is the Chwezi Accounting Doctrine (URL, checkout); resolve via global registry | doctrine-moved | AGENTS.md §Directory Logic & Pathing (verbatim; URL and registry resolution absent elsewhere) | [ ] |
| S06 | 12 | Domain knowledge in `/domains/`; read the domain `INDEX.md` | doctrine-moved | AGENTS.md §Directory Logic & Pathing (verbatim; INDEX.md step absent from §Skill Families) | [ ] |
| S07 | 13 | Project workspace `projects/<ProjectName>/` (untracked, gitignored); all client docs built there | doctrine-moved | AGENTS.md §Directory Logic & Pathing (verbatim) | [ ] |
| S08 | 14 | Context source of truth is `projects/<ProjectName>/_context/` | duplicate | AGENTS.md §Pathing Model (same sentence) | [ ] |
| S09 | 15 | Output destination for section files and final `.docx` | doctrine-moved | AGENTS.md §Directory Logic & Pathing (verbatim) | [ ] |
| S10 | 16 | DOCX export contract: `export/`, `export-docs.ps1`, `export-docs.sh`; run export after build | duplicate | AGENTS.md §Pathing Model (same three paths and the copy-to-`export/` step) | [ ] |
| S11 | 17 | Skill files MUST use canonical paths; legacy aliases only inside alias-block comments; enforced by `python -m engine validate-skills` | doctrine-moved | AGENTS.md §Directory Logic & Pathing (verbatim; alias-block rule absent from §Pathing Model) | [ ] |
| S12 | 18 | `templates/reference.docx` is the Pandoc Word style reference | doctrine-moved | AGENTS.md §Directory Logic & Pathing (verbatim) | [ ] |
| S13 | 19 | `scripts/build-doc.sh` stitches `.md` into `.docx` | doctrine-moved | AGENTS.md §Directory Logic & Pathing (verbatim) | [ ] |
| S14 | 21–34 | New Project Protocol: trigger sentence and steps 1–10 (incl. `superpowers:brainstorming`, hybrid heuristic, Uganda signals, duplicate "5." numbering) | doctrine-moved (row group, 12 sentences) | AGENTS.md §New Project Protocol — VERBATIM, wording untouched for M10-08 SP-01 | [ ] |
| S15 | 38 | Hybrid methodology → invoke `hybrid-synchronization` between Phase 02 sign-off and Phase 07 | doctrine-moved | AGENTS.md §Hybrid Cross-Cutting Trigger (verbatim) | [ ] |
| S16 | 38 | Kernel blocks Phase 07 until `hybrid` gate passes | doctrine-moved | AGENTS.md §Hybrid Cross-Cutting Trigger (verbatim) | [ ] |
| S17 | 42–47 | Build Document Protocol: trigger and steps 1–5 | doctrine-moved (row group, 6 sentences) | AGENTS.md §Build Document Protocol (verbatim) | [ ] |
| S18 | 51–54 | `[DOMAIN-DEFAULT]` blocks: pre-populated, marked, sourced, reviewed by consultant | doctrine-moved (row group, 4 sentences) | AGENTS.md §Domain Injection Protocol (verbatim) | [ ] |
| S19 | 55 | Never silently removed by Claude — only the consultant removes them | doctrine-moved (near-verbatim) | AGENTS.md §Domain Injection Protocol: "by the assistant (Claude or any other runner)" so the rule binds every runner | [ ] |
| S20 | 59 | Principle 1: map to README standards; quality judged against ISO/IEC/IEEE 29148:2018; IEEE 830 layout only; 1233/E1340 supporting | doctrine-moved | AGENTS.md §Core Engineering Principles (verbatim); invariant `iso-29148` | [ ] |
| S21 | 60 | Principle 2: never hallucinate; flag gaps in `_context/` | doctrine-moved | AGENTS.md §Core Engineering Principles (verbatim; partial overlap with §Quality Bar "Do not invent missing requirements") | [ ] |
| S22 | 61–65 | Principles 3–7: stimulus-response, ISO/IEC/IEEE 24765 terms, LaTeX and active voice, minimum length, vague-adjective prohibition with ISO 25010/25023/IEEE 982 | doctrine-moved (row group, 5 principles) | AGENTS.md §Core Engineering Principles (verbatim) | [ ] |
| S23 | 67 | `## Premium Default` (heading) | duplicate (structural) | content carried in AGENTS.md §Quality Bar | [ ] |
| S24 | 69 s1 | This SRS engine is for premium, world-class systems work | duplicate | AGENTS.md §Quality Bar ("Premium, world-class quality is the default for this engine.") | [ ] |
| S25 | 69 s2 | Do not generate commodity-grade requirements, vague low-cost specifications, or documents intended to justify weak products | doctrine-moved | AGENTS.md §Quality Bar, new bullet (verbatim) | [ ] |
| S26 | 69 s3 | Sub-premium brief → narrow to premium deliverable or flag poor fit | duplicate | AGENTS.md §Quality Bar ("treat it as a poor-fit engagement. Recommend narrowing scope…") | [ ] |
| S27 | 71 | Premium requirements must make value visible through packaging, UX, buyer proof… | duplicate | AGENTS.md §Quality Bar (identical sentence) | [ ] |
| S28 | 73 | Premium requirements are specific, verifiable, outcome-linked, operationally realistic… | doctrine-moved | AGENTS.md §Quality Bar, new bullet (verbatim) | [ ] |
| S29 | 74 | For executive/enterprise/affluent/luxury/high-ticket contexts invoke `07-premium-product-positioning` before PRD/SRS finalisation | doctrine-moved | AGENTS.md §Quality Bar, new bullet (verbatim; "before PRD/SRS finalisation" and context list differ from the existing bullet) | [ ] |
| S30 | 75 | Premium is not marketing language; it appears as measurable quality, trust, onboarding… requirements | doctrine-moved | AGENTS.md §Quality Bar, new bullet (verbatim) | [ ] |
| S31 | 79 | PRIME methodology (Kodukula & Vinueza, 2024); never skip Inspect and Modify | doctrine-moved | AGENTS.md §Skill Execution Workflow (verbatim) | [ ] |
| S32 | 81–85 | Workflow steps 1–5: Initialization, Analysis (PIF, glossary gaps), Synthesis, Human Review Gate, Validation | doctrine-moved (row group, 5 steps) | AGENTS.md §Skill Execution Workflow (verbatim) | [ ] |
| S33 | 89 | Refer to README.md and PROJECT_BRIEF.md for the eight-phase skill flow | doctrine-moved | AGENTS.md §Full Skill Suite (verbatim) | [ ] |
| S34 | 93 | Categories belong to the external engineering-catalog engine, not this repo; include the category segment when routing | doctrine-moved | AGENTS.md §Skill Categories (verbatim) | [ ] |
| S35 | 95–113 | 17-row category table (`ai` … `security`) describing the Chwezi Dev Engine | doctrine-moved (row group, 17 rows) | AGENTS.md §Skill Categories (verbatim). The plan's obsolete candidate was examined: the 17 rows match the 17 directories under `chwezi-dev-engine/skills/` today, the table is explicitly labelled as describing that engine, and `AGENTS.md` §Skill Families already pointed to it. It is not false today, so it was moved, not marked obsolete. Retiring it in favour of the dev engine's own README is a later slimming decision (CV-04, M10-08) | [ ] |
| S36 | 115 | To locate a skill, resolve the dev engine, inspect `skills/<category>/`, read `<skill-name>/SKILL.md` | doctrine-moved | AGENTS.md §Skill Categories (verbatim) | [ ] |
| S37 | 119–124 | Use the authoring standard and template; release requires both zero-debt checks (two commands) | duplicate | AGENTS.md §Skill Authoring and Release Gate (standard, template, both commands) | [ ] |
| S38 | 126 s1 | Do not waive a finding through the baseline | duplicate | AGENTS.md §Skill Authoring ("The baseline is zero debt, not a waiver.") | [ ] |
| S39 | 126 s2 | Update routing fixtures when a trigger or neighbour boundary changes; run anti-slop audit on changed human-facing content | doctrine-moved | AGENTS.md §Skill Authoring and Release Gate, new bullet (verbatim) | [ ] |
| S40 | 130–139 | Book-extraction ban: folders, file names, copyright, paraphrase rule, citation and currentness note, <25-word quotes, staging outside, guardrail behaviour, plans may name books | duplicate (row group, 6 sentences) | AGENTS.md §Never store book extractions (superset: more folder names, same rule, guardrail and plan allowance); invariant `book-extraction-ban` | [ ] |
| S41 | 143–146 | Before admitting any standard edition, law, capability, version or metric threshold into a skill **or generated requirement**, follow the currentness gate; books are concept inputs only | doctrine-moved | AGENTS.md §Mandatory Digital Research currentness gate, appended paragraph (verbatim; extends the gate from Kaizen work to generated requirements) | [ ] |
| S42 | 150–153 | Uganda compliance skills: `uganda-dppa-compliance`, `dpia-generator`, when to invoke | doctrine-moved (row group, 3 sentences) | AGENTS.md §Compliance Skills (Uganda Domain) (verbatim) | [ ] |
| S43 | 157–162 | Uganda DPPA fail tags (5 tags) | doctrine-moved (row group) | AGENTS.md §Compliance Fail Tags (Uganda) (verbatim) | [ ] |
| S44 | 166–199 | Documentation & Writing Standards: scope sentence; Three-Emphasis Rule; List Formatting; Heading Standards; Numbers; Markdown Syntax; Acronyms and Glossary | doctrine-moved (row group, 24 sentences) | AGENTS.md §Documentation & Writing Standards and its six sub-sections (verbatim) | [ ] |
| S45 | 203 | Prohibited: subjective adjectives without IEEE-982.1 metric | doctrine-moved | AGENTS.md §Prohibited Actions (verbatim) | [ ] |
| S46 | 207–212 | Anti-AI-Slop Quality Gate: `28-anti-ai-slop` real-time gate; `29-ai-slop-audit` after each iteration, grade F blocks; verified-evidence list | doctrine-moved (row group, 4 paragraphs) | AGENTS.md §Anti-AI-Slop Quality Gate (MANDATORY) (verbatim; far more detail than the §Skill Authoring and §Quality Bar bullets) | [ ] |
| S47 | 216 | Project workspaces are local and gitignored; never `git add -f`; never commit `templates/reference.docx`; commit scope | doctrine-moved | AGENTS.md §Git Commit Protocol for Projects (verbatim) | [ ] |
| S48 | 220–225 | IEEE 1012 evaluation framework: correctness, consistency, completeness, verifiability | doctrine-moved (row group, 4) | AGENTS.md §V&V SOP / IEEE 1012 Evaluation Framework (verbatim) | [ ] |
| S49 | 227–231 | Audit Execution Loop (Skill 08): traceability, logic scrutiny, conflict resolution | doctrine-moved (row group, 3) | AGENTS.md §V&V SOP / Audit Execution Loop (verbatim) | [ ] |
| S50 | 235 | `[CONTEXT-GAP]` → consult dev engine `context-gap-fillers.md` | doctrine-moved | AGENTS.md §V&V SOP / Filling Context Gaps (verbatim) | [ ] |
| S51 | 239–248 | Failure protocols and six V&V fail tags | doctrine-moved (row group, 8) | AGENTS.md §V&V SOP / Failure Protocols (verbatim) | [ ] |
| S52 | 252–254 | Quality constraints: formal tone; Integrity Level/Baseline/Anomaly records (ISO/IEC 15504); SOP is Skill 08 contract | doctrine-moved (row group, 3) | AGENTS.md §V&V SOP / Quality Constraints (verbatim) | [ ] |
| S53 | 258–272 | Project registries: required files, `engine sync`, editable fields, five kernel failure conditions | doctrine-moved (row group, 8) | AGENTS.md §V&V SOP / Project Registries (verbatim) | [ ] |
| S54 | 276–281 | Governance artifacts: ADR catalog, CIA, baselines, waivers (≤ 90 days), sign-off ledger, evidence pack | doctrine-moved (row group, 6) | AGENTS.md §V&V SOP / Governance Artifacts (verbatim) | [ ] |
| S55 | 285–286 | Update docs/CHANGELOG.md; keep DEPENDENCIES.md current | doctrine-moved (row group, 2) | AGENTS.md §Documentation Maintenance (verbatim) | [ ] |
| S56 | 287 | Reference README.md, CLAUDE.md and other root docs in change tickets | doctrine-moved (near-verbatim) | AGENTS.md §Documentation Maintenance: "README.md, AGENTS.md (imported by the CLAUDE.md bridge), and other root docs" — CLAUDE.md no longer carries the protocol | [ ] |
| S57 | 292–315 | Finance & Accounting Trigger: trigger list, five steps, `finance-module-audit` auto-run | duplicate (row group) | AGENTS.md §Finance & Accounting Trigger (identical list and steps; the only differences — GitHub link and "resolve through the global engine registry" — are carried by S05) | [ ] |
| S58 | 318–336 | Design trigger block `v2` | duplicate | AGENTS.md trigger block (text between the markers compared: identical) | [ ] |

## Counts

| Class | Rows | Notes |
|---|---|---|
| duplicate | 14 (S01, S03, S08, S10, S23, S24, S26, S27, S37, S38, S40, S57, S58; S01 and S23 are structural headings) | |
| doctrine-moved | 44 | includes near-verbatim adjustments S19 and S56 |
| Claude-mechanics | 0 | no Claude-only section needed |
| obsolete | 0 | the 17-row table was examined and moved (S35) |
| lost | 0 | |

Lost: 0.

## Invariants recorded (`.skills-engine/engine-manifest.yaml`)

- `book-extraction-ban`: "Book extractions, book summaries, chapter-by-chapter notes and book-by-book"
- `not-assessed`: "Missing execution, render, source, reviewer, or stakeholder evidence is `NOT ASSESSED`, never a pass."
- `iso-29148`: "Requirement quality is judged against ISO/IEC/IEEE 29148:2018 (individual and set characteristics;"
- Exemption `british-english`: no British English output rule exists anywhere in the SRS router (AGENTS.md, former CLAUDE.md, README.md, `rules/common/`); adding one would be new doctrine.

## Validators (run from the engine root, 29 Sep 2026)

| Command | Result |
|---|---|
| `python -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | pass: active skills 159, templates 1, failure counts `{}` |
| `python -X utf8 scripts/routing_smoke_test.py` | pass: 54/54 fixtures, top-3 precision 1.000 |
| `python -X utf8 tests/agent-integration/test_srs_agent_contract.py` | `PASS: srs-skills agent contract` |
| `python -X utf8 scripts/validate_engine.py` | FAIL (4 lines). Three README.md lines (`projects/<ProjectName>/`, `docs/hybrid-operating-model.md`, `docs/regulated-evidence-model.md`) pre-exist: README.md is unmodified. One line is caused by this conversion: `CLAUDE.md missing required text: projects/<ProjectName>/` — `validate_root_pathing()` (`scripts/validate_engine.py` L42) requires that string in `CLAUDE.md`. The text now lives in `AGENTS.md`, which the bridge imports. The fix is to drop `CLAUDE.md` from that list (or resolve `@` imports); the script is outside this executor's edit scope because another executor holds srs `scripts/`. |
