# Kaizen 2026-09-24 — SRS, design, engineering and coordination engines

Scope: `srs-skills`, `design-system-skills`, `chwezi-dev-engine`, `chwezi-engine-agents`, plus the
portfolio-wide book-extraction sweep (which also touched `digital-research-engine`).

Goal: every artefact these engines help produce must read, look and work like the output of a
senior human professional, to an Apple-grade bar for quality, security and UI/UX. Requirements
say what success means (SRS), engineering says how to build safely (dev), design says how the
experience looks, behaves and is evaluated (design).

## Book-extraction retirement (all engines scanned)

| Engine | Found | Action |
| --- | --- | --- |
| srs-skills | `book-extractions/` (15 files), 2 digest docs | Knowledge folded into task references; `git rm`; guardrail + 7 tests |
| chwezi-dev-engine | `book-extractions/` (21 files), book-derived plan content | 19 removed, 2 title-only records moved to `docs/game-dev-analysis/`; UX material folded into design engine; guardrail extended |
| design-system-skills | `docs/book-study/` (9 files) | Removed; repo-wide guard with tests |
| digital-research-engine | `extracted-books/` (3 files), `book-study-2026-08.md` | Folded, removed; `scripts/check_no_book_extractions.py` |
| other eight engines | none (business-plan "juice-extraction" etc. are domain topics) | No change |

Every affected engine's `AGENTS.md` and `CLAUDE.md` now carries a "Never store book extractions"
rule. This package adds `scripts/validate-no-book-extractions.py` (portfolio check, path-based,
allowlist in `catalog/content-integrity-allowlist.txt`). Final result: `roots=12 findings=0`.

## Book ingestion (35 titles; one input file was empty)

Knowledge entered only as paraphrased, task-oriented references with original, mostly Ugandan
worked examples and dated currentness notes. A 12-word-shingle overlap scan of every changed file
against the source texts found no verbatim passages (max 9 incidental shingles, spread across
unrelated books — stock phrases).

- SRS: opportunity and product-risk evidence gate, outcome roadmap and objective trace chain,
  AI eval-set and graduation requirements, AI business-case addendum, human-AI collaboration
  requirements, agent security and oversight requirements, experiment validity requirements,
  solution design views and controls, data contract / data quality / governance requirements,
  API interface requirements, delivery pipeline requirements, final requirements quality gate.
- Design: action-cycle and discoverability audit, error prevention and recovery patterns,
  low-literacy / low-bandwidth / emerging-market design, cultural adaptation, field research in
  low-resource settings, human-AI trust calibration, experiment-aware design evaluation, site
  planning and page types, modern CSS capability baseline, mobile-web patterns, style-era
  vocabulary, perceived performance for streaming and navigation.
- Engineering: API style selection, JSON payload and schema design, OWASP API Top 10 controls,
  APIs for agents and data (MCP 2026-07-28), LLM/agent threat-control map, least-privilege tool
  and MCP security, LLM pattern catalogue, agent governance, performance engineering procedure,
  AI-generated code review gate, algorithmic impact review, large-scale React/TS, React Native
  release checklist, GitHub Pages deployment, Actions security hardening, supply-chain provenance,
  IaC selection, rollout selection, Python version policy, pandas 3 reshaping, notebooks to
  production, FTI ML architecture, data contracts (ODCS v3.2.0), catalog and lineage
  (OpenLineage), accessibility testing (automated and manual).

Sources (concept inputs only): Cagan *Inspired*; Khan *AI Product Management*; Ximenes *Strategic
Software Engineering*; Marchiotto *Adopting AI for Business Transformation*; Thompson *Designing
Digital Solutions*; Nassery *Next-Level A/B Testing*; Wu & Liang *Human-AI Interaction and
Collaboration*; Norman *The Design of Everyday Things*; Lahiri, Prabhu et al. *Innovative
Solutions*; Plumley *Website Design and Development*; LaGrone *Web Design Blueprints*; Yang
*Building User Interfaces for Modern Web Applications*; McNeil *The Web Designer's Idea Book*
(vols 2 and 3); Dynowski & Dulak *Learning API Styles*; Johnson *Practical JSON Design and Usage*;
Day *APIs for AI and Data Science*; Fernandez *Patterns of Application Development Using AI*;
Borges & Campbell *AI Security Engineering*; Hodjat & Blondeau *The Agentic Enterprise*; Osmani
*Web Performance Engineering in the Age of AI*; Oliveira *AI Strategies for Web Development*;
Dormehl *The Formula*; Fusco *Large Scale Apps with React and TypeScript*; Bin Uzayr *Mastering
React Native* and *Mastering GitHub Pages*; Brikman *Fundamentals of DevOps and Software
Delivery*; Laster *Learning GitHub Actions*; Jones *Driving Data Quality with Data Contracts*;
Olesen-Bagneux *The Enterprise Data Catalog* (both titles); Chen *Pandas for Everyone*; Nelson
*Software Engineering for Data Scientists*; Jolowicz *Hypermodern Python Tooling*; Dowling
*Building Machine Learning Systems with a Feature Store*.

## Per-engine findings and fixes

**srs-skills.** IEEE 830 cited as current in ~25 places → ISO/IEC/IEEE 29148:2018 (830 clause
numbers retained only as the section-layout contract). ISO/IEC 25010:2011 → 2023 (nine
characteristics, coverage map). WCAG 2.1 → 2.2. API spec generation moved from OpenAPI 3.0.3 to
3.1.2 with JSON Schema 2020-12 and RFC 9457 errors; rate-limit headers are a recorded decision
(IETF draft). OWASP LLM categories → 2025 IDs plus Agentic Applications 2026. EU AI Act timeline
reference incl. Digital Omnibus (Reg. (EU) 2026/1744). UX path had no design handoff and
prescribed a banned font — fixed. Attribute-mapping description realigned with its body.
New final quality gate (G1–G11) linked from PRD and core SRS skills. Stray empty `%SystemDrive%`
directory removed.

**design-system-skills.** Completed and reviewed the carried-over uncommitted change set (four new
skills conform; 101/101 compliant). APCA was presented as "the WCAG 3 method" in 11 files — the
WCAG 3 Working Draft does not name it; now a design aid only. `prefers-reduced-motion` was listed
as AA; it is SC 2.3.3 (AAA) and is kept as a house rule. "7 ± 2" working-memory claims replaced
(Cowan: about four chunks). WCAG 2.1 → 2.2 AA in 13+ files. Quality gate now labels every item
`HEURISTIC`, `MEASURED` or `NOT_ASSESSED`; only measured evidence may say "conforms". CI moved to
current action majors and now installs pytest.

**chwezi-dev-engine.** 126 files had `compatible_with: [Codex, codex]` (find/replace corruption
of `claude-code`) plus 11 prose corruptions — restored. Control-plane and approval validators
still expected `skills-web-dev` — corrected to `chwezi-dev-engine`. Eight source registers cited
local ebook paths — replaced with author/title. 88 stale GitHub Actions pins updated (checkout
v7 etc.; Node 22/24). PHP supported-branch baseline, ISO/IEC 27001:2022 control numbering and
OWASP Top 10:2025 confirmed. Nine new routing fixtures.

**chwezi-engine-agents.** Portfolio book-extraction validator + tests; cross-engine handoff
boundary table and eval 021; "senior-practitioner bar" in the craft standard; portfolio-craft
validator no longer depends on a stale README heading and reports all failures; catalog: research
engine repository set to its real GitHub name (`digital-research-skills`), Windows engine
integration set to `pending` (manifest never committed); stale `skills-web-dev` in evals fixed.

## Validator evidence (final run, 2026-09-24)

| Engine | Command | Result |
| --- | --- | --- |
| srs | `validate_skill_engine.py --baseline` | active 159, failure counts `{}` |
| srs | `routing_smoke_test.py` | 54/54, top-3 precision 1.000 |
| srs | `source_ingestion_guardrail.py` | findings: 0 |
| srs | `validate_engine.py` / `engine validate-skills` | exit 0 / SKILLS OK |
| srs | `pytest tests engine/tests` | 285 passed, 2 skipped, coverage 95.55% |
| design | `validate_engine.py --baseline` | skills=101 fully_compliant=101 |
| design | `routing_smoke_test.py` | 68 fixtures, p@1 85%, p@3 100% |
| design | route existence / cross-engine routes | PASS / PASS |
| design | delivery evidence manifest | PASS (all stages NOT ASSESSED) |
| design | `pytest tests` | 99 passed |
| dev | `skill_catalog_guardrails.py --report-only` | active 185 / cap 200, findings: 0 |
| dev | `source_ingestion_guardrail.py` | findings: 0 |
| dev | `routing_smoke_test.py` | p@1 160/166 (96%), p@3 166/166, failures 0 |
| dev | control plane / approval adapters | PASS / PASS |
| dev | `pytest tests` | 129 passed, 3 skipped |
| agents | contracts, kaizen cards, lifecycle, budget, no-book-extractions | all PASS (roots=12 findings=0) |
| agents | catalog / portfolio craft / prompt capability (PowerShell) | PASS |
| agents | `pytest tests` | 14 passed |
| research | `validate_engine.py` | exit 0 |

## Unresolved and evidence limits

- `chwezi-dev-engine` has 185 active skills: under the 200 cap, above the 150–170 target. The
  overage predates this cycle (14 skills added 2026-09-20). Candidate merges (owner decision):
  `council` + `santa-method`; `strategic-compact` and `parallel-execution-optimizer` into
  `coding-agent-optimization`; `verification-loop` into `world-class-engineering`.
- EU AI Act primary text (EUR-Lex) could not be retrieved; dates rest on the European Commission
  page plus secondary sources. OWASP "LLM Top 10 2026" IDs not yet mapped.
- MCP 2026-07-28 semantics, Claude prefill removal, TypeScript 7 and React 19.3 details were
  verified from official pages by the working agents but not independently re-read at review.
- 29148 clause numbers, ISO/IEC 25012 review status and Uganda PDPO regulator pages: NOT_ASSESSED.
- No rendered, device or assistive-technology proof was produced for any design guidance:
  NOT_ASSESSED. No downstream project has yet been generated with the updated SRS templates.
- Input limits: *Enterprise Architecture for Digital Business* (Hazra & Unhelkar) was a 0-byte
  file — NOT_ASSESSED. The file labelled as McNeil's mobile idea book is volume 2 of *The Web
  Designer's Idea Book*. Several early releases contained only one or two chapters.
- digital-research-engine still holds author-named references (e.g. `forsyth-reports-proposals.md`,
  `morley-*.md`) that should be reviewed for single-book digest structure in a later cycle.
- Windows engine needs `.skills-engine/engine-manifest.yaml` before its catalog status returns
  to `available`. `scripts/discover-engine.ps1` fails on Windows PowerShell 5.1 without
  `-CatalogPath` (pre-existing).
