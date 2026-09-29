# M10-13 — Cross-engine extensions: executor evidence

Executor scope: every M10-13 task (T01–T06) in `proposal-skills`, `business-plan-skills`, `chwezi-accounting-doctrine`, `digital-research-engine`, plus register rows and evidence in `chwezi-engine-agents`. `srs-skills` was consumed (commands run), never edited. Date: 29 September 2026. Zero spend: local tools only (Python 3.13, PyYAML 6.0.2, Pandoc 3.9.0.2, the M10-01 pinned renderer with local Chrome/Edge) and free web desk research for T05. No git state changes.

Evidence location note: the phase file proposed `docs/operations/my-10-kaizen-evidence/M10-13/`; the location actually defined by M10-00 is `docs/operations/m10-kaizen-evidence/M10-13/`, used here.

## Summary

| Task | Status | One line |
|---|---|---|
| T01 (AR-15, BL-13b) | DONE | Renderer home confirmed as `srs-skills` (`scripts/render_diagrams.py`, `scripts/build-doc.sh`, `python -m engine diagrams …`); hand-off paragraph recorded once and used verbatim in T02 and T06; `--help` of all 7 commands exits 0 |
| T02 (AR-15) | DONE_WITH_LIMITATIONS | Proposal reference + 1-line link; validators pass; synthetic `.docx` has 2 captioned figures, 0 diagram-source matches, font check `PASS` ×2. Routing fixture NOT added (concurrency rule) — hand-off below; the 8 pt legibility of the 10-step workflow figure at body width is not met |
| T03 (UX-13) | DONE | Read-only lookup + 13 tests; all acceptance outputs match; register byte-identical; finance validators pass. Peter's acknowledgement of the payroll-skill link is recorded below under delegated authority |
| T04 (UA-14) | NOT_ASSESSED | Not run: zero-spend rule. Decision record written; settings/CLAUDE.md/DRE status hashes identical before and after |
| T05 (BL-13a) | DONE_WITH_LIMITATIONS | Scan record + 57 register rows (15 → 72); verdicts study 23 / borrow idea 2 / ignore 29 / block 3; ten Kaizen repos re-checked (all at pins); register schema PASS; currency gate 0 findings. 27 candidates triage-only |
| T06 (BL-13b) | DONE_WITH_LIMITATIONS | Business-plan reference + 3 one-line links; validators pass; synthetic Gantt with PPDA award as blocking milestone rendered to PNG + SVG, font check `PASS`. Limitation: Mermaid Gantt canvas is 8,064 px wide, so labels are illegible at the portrait body measure (renderer hand-off below) |

---

## T01 — renderer home and hand-off paragraph

- Outcome (a) of the phase notes: the renderer lives in `srs-skills`. `catalog/engines.yaml` key verified: `id: srs-skills`, `path: srs-skills` (released_commit `905b9a4`). srs HEAD at execution: `360854a`.
- Hand-off paragraph (single source): `M10-13-T01-figure-rendering-handoff.md`. Inserted by script, byte-for-byte, into both consumer references.
- `--help` transcript: `M10-13-T01-help-transcript.txt` — `render_diagrams.py`, `check_docx_diagrams.py`, `engine diagrams`, `diagrams validate|generate|manifest|verify-manifest`: 7 × exit 0. `build-doc.sh` has no `--help`; its usage lines are recorded.
- Findings recorded in the paragraph (discovered while proving it):
  1. `engine diagrams validate` needs a workspace with an `_context/` directory (`WorkspaceNotFoundError` otherwise).
  2. IR `srs_section` fields must match `^[0-9]+(\.[0-9]+)*$`; proposals and plans use their own section number.
  3. `build-doc.sh` given an MSYS path (`/c/wamp64/...`) built a `.docx` with the figures replaced by descriptions (Pandoc `[WARNING] Could not fetch resource`), yet the post-build guard passed because no Mermaid source survived. Relative or Windows paths work. **Hand-off to the srs owner:** convert `DOC_DIR` with `cygpath -m` before `--resource-path`, and make the guard fail when a rendered figure is missing from `word/media/`.
- Copying check: no renderer, schema or generator code exists in `proposal-skills` or `business-plan-skills` (only Markdown was added).

## T02 — proposal technical-approach figures

Files: `proposal-skills/skills/pipeline/06-methodology/references/technical-approach-figures.md` (new); `proposal-skills/skills/pipeline/06-methodology/SKILL.md` (+1 line in References; 358 → 359 lines).

Commands (from `proposal-skills`):

| Command | Result |
|---|---|
| `python -X utf8 scripts/validate_skills.py --baseline quality-baseline.json` | 115 active skills, 0 findings |
| `python -X utf8 scripts/routing_smoke_test.py` | 25 fixtures, top-three precision 100.0 % |
| `python -X utf8 scripts/proposal_fixture_check.py` | PASS |
| `python -X utf8 scripts/encoding_link_gate.py` | 0 findings; encoding, local links, sibling routes PASS |

Synthetic sample (`T02-sample-proposal/`, fictional client, built with the hand-off commands from `srs-skills`): `engine diagrams validate` → `DIAGRAMS: PASS (1 figure(s) validated)`; `generate` → PASS; `build-doc.sh ../chwezi-engine-agents/.../T02-sample-proposal/technical-approach Sample_Technical_Proposal` → 2 figures rendered, guard "0 contain Mermaid source"; `verify-manifest` → PASS.

- `word/media/`: `rId9.png` (113,702 B), `rId13.png` (62,083 B) — 2 images.
- `grep -Ec "flowchart|graph TD|C4Context" word/document.xml` → 0.
- Captions in `document.xml`: "Figure 1 — Proposed solution context", "Figure 2 — Delivery workflow and approval gates".
- `Sample_Technical_Proposal.figures.json`: FIG-001 and fig-2, `font_family: Public Sans`, `font_substitution_check: PASS` for both.
- PNG sizes 3356×548 and 4068×428 px at 6.25 in → 537 and 651 ppi.
- SHA-256: `.docx` `943daf2c…9375944`; manifest `d1ed3a63…a0956`.

Limitations:
- **Routing fixture not added.** The brief forbids editing routing fixtures while M10-03 works on them. Hand-off for the M10-03/orchestrator: add to `proposal-skills/tests/fixtures/routing-fixtures.json` `{"id": "technical-approach-figures", "kind": "positive", "prompt": "Write the technical approach and methodology for this ICT tender with a delivery workflow figure", "expected": "skills/pipeline/06-methodology"}`. Checked against a scratch copy of the fixture file using the repo's own scorer: PASS (06-methodology ranked 2nd). Two figure-first wordings ("Add figures to the methodology section…", "Methodology section needs a delivery phases diagram…") FAILED (top three were SaaS/AI skills); that is a routing gap for M10-03 to judge, not fixed here.
- The 10-node delivery-workflow figure's labels fall below 8 pt at the 6.25 in measure (4068 px canvas). The reference now tells authors to split workflows of more than about seven steps; the sample itself was not re-drawn.
- Proof is on a synthetic sample only.

## T03 — finance effective-date lookup

Files: `chwezi-accounting-doctrine/tools/source_register_lookup.py` (new); `tests/test_source_register_lookup.py` (new, 13 tests); `skills/08-tax-and-statutory/tax-statutory-source-register-and-country-packs/SKILL.md` (+1 line, decision rule 9); `skills/04-subledgers-and-operations/payroll-and-statutory-postings-east-africa/SKILL.md` (+1 line under decision rule 3).

Semantics as specified: state permission read from `schema.yaml` `state_machine` (no hard-coded list; a test flips `draft` to `true` in a temp schema and the result follows); jurisdiction → folder found from the entries (`UG`→`uganda`, `IF`→`ifrs`); half-open dated intervals; undated entries returned as candidates with "effective date NOT_ASSESSED"; `verified-with-caveat` (whose schema value is a string, not `true`) is refused with the caveat text; recheck overdue, stale, superseded and `NOT_CAPTURED` archive warnings; exit 0/3/2 (1 = unreadable register). `--as-of` defaults to today (UTC). PyYAML only; no writes; no network.

Verbatim outputs: `M10-13-T03-finance-lookup-transcript.txt`. Key lines (`--as-of 2026-09-29`):

- UG `paye` 2026-08-15 → `UG-PAYE-RATES`, `state: draft`, `final_use_allowed: false`, warnings `["draft: not for final output", "archive snapshot not captured"]`, exit 3.
- UG `paye` 2026-05-15 → match `candidates`, `UG-PAYE-RATES-THROUGH-2026-06-30`, `final_use_allowed: false`, warnings `["superseded", "effective date NOT_ASSESSED", "recheck overdue", "archive snapshot not captured"]`, exit 3.
- UG `no-such-register` → exit 2. (Also: UG `nssf` 2026-08-15 → `verified-current`, exit 0.)

| Command | Result |
|---|---|
| `python -m unittest discover -s tests -p "test_*.py"` | Ran 20 tests, OK (13 new) |
| `tools/check-source-register.ps1` (Windows PowerShell 5.1; `pwsh` not installed) | state: pass; 11 entry files; 1 verified-current |
| `check-links.ps1` / `check-skill-contracts.ps1` / `check-mojibake.ps1` / `check-frontmatter-yaml.ps1` | pass / pass (108 skills, 40/40 blockers) / pass / pass |
| SHA-256 of every file under `doctrine/source-register` before vs after | identical (diff empty) |
| `git status --porcelain doctrine/source-register` | empty |

Decision under delegation: the phase requires Peter's acknowledgement before the payroll-skill link merges (it touches the P02 tax path). Recorded: "acknowledged by orchestrator under Peter's delegated authority, 29 Sep 2026"; the link only adds a stop condition (exit 3 = hard stop) and changes no register content. Attribution line to UI UX Pro Max is in the tool's docstring.

## T04 — Understand Anything sandbox pilot (UA-14)

Status: **NOT_ASSESSED** — "not run: zero-spend rule; owner approval for spend not given". The pilot's measures are all produced by model calls, so it cannot run under the zero-spend rule; install alone measures nothing, so nothing was installed.

File: `digital-research-engine/docs/continuous-improvement/understand-knowledge-sandbox-pilot-2026-09.md` (dated at execution). Every measure is `NOT_ASSESSED` with reason; verdict: no adoption; re-entry condition stated (spend approval + UA-01 reversal trigger).

Hashes (before at session start / after at close):

| Item | Before | After |
|---|---|---|
| `~/.claude/settings.json` | `110aee8a…90a4be` | `110aee8a…90a4be` (identical) |
| `~/.claude/CLAUDE.md` | `70965424…c0866` | `70965424…c0866` (identical) |
| DRE `git status --porcelain` output | `39479f02…0c36a0c` | `01c8d2cf…e30b33` |

The DRE status hashes differ only for reasons outside T04: at the start the status held one modification by another phase (`scripts/routing_smoke_test.py`), which that phase committed during this session (DRE HEAD moved to `05c3b9b`); at the end the status lists exactly the two new records `docs/continuous-improvement/ecosystem-scan-2026-Q4.md` (T05) and `understand-knowledge-sandbox-pilot-2026-09.md` (this record). With those two excluded the status is empty. No live engine file was changed by T04. No plugin installed, nothing to uninstall, no sandbox to quarantine.

## T05 — BL-13a first quarterly ecosystem scan (from AC-04)

**Status:** DONE_WITH_LIMITATIONS. 27 of the 47 new candidates were triaged only (GitHub API metadata, file tree, README install lines); their outbound hosts and overlap are `NOT_ASSESSED` and each such register row says "Triage only". The 20 fully screened candidates and the 10 Kaizen re-check rows carry every field the acceptance criterion requires.

**Procedure followed:** `chwezi-dev-engine/skills/sdlc-meta/skill-engine-audit/references/ecosystem-scan-and-intake.md` (seven steps), run as a DRE research wave (`research-orchestration`, with `skill-safety-audit` as the safety lens). Desk review only: nothing installed, cloned or executed. GitHub REST API through `gh` (free), web pages and one arXiv abstract. Zero spend.

**Files changed**
- `digital-research-engine/docs/continuous-improvement/ecosystem-scan-2026-Q4.md` (new): sources, method, security-feed summary, verdict totals, marketplace re-check, screened table (S01–S20), triaged table (T01–T27), re-check of the ten Kaizen repositories, candidate backlog, register diff, hand-offs, next scan date.
- `chwezi-engine-agents/docs/security/third-party-skill-register.json`: 57 rows appended (15 → 72); `scope` gained one sentence; no existing row changed.
- `chwezi-engine-agents/docs/operations/m10-kaizen-evidence/M10-13/ecosystem-scan-2026-Q4-sources.json` (new): 11 sources and 9 claims for the currency gate.

**Sources (fixed):** ComposioHQ/awesome-claude-skills at `be2a406907db` (unchanged since the pin); anthropics/skills at `33375500bcea` (12 commits after `fa0fa64`; new folders `academy-guide` and `discernment-nudge`); Peter's five configured marketplaces (read-only); GitHub topic search `agent-skills` and `claude-code`, top 30 each by stars, pushed on or after 2026-07-01 (60 results, 54 unique); security feeds: Snyk ToxicSkills (5 Feb 2026: 534 of 3,984 skills, 13.4 %, critical; 76 confirmed malicious), CSA research note (6 May 2026), SkillSieve arXiv 2604.06550 (v3 27 Jul 2026), NVIDIA/SkillSpector.

**Verdicts (57 new rows):** study 23, borrow_idea 2, ignore 29, block 3 (screened 20: 11/2/6/1; triaged 27: 3/0/23/1; Kaizen re-check 10: 9/0/0/1).
- Blocks: `virgiliojr94/book-to-skill` (no-book-extractions rule); `asgeirtj/system_prompts_leaks` (leaked third-party text; the CC0 declaration cannot licence it); `ComposioHQ/awesome-claude-skills` as an installable plugin (its setup command carries instruction-override text and writes an API key into `~/.mcp.json`; it stays a read-only scan source).

**Borrow-idea candidates (next Kaizen; none implemented):**
1. NVIDIA/SkillSpector (Apache-2.0, commit 88312190c7c6): cross-check `skill-safety-gate.md` against the scanner's 17 categories. Owner: chwezi-dev-engine.
2. anthropics/skills `discernment-nudge` (Apache-2.0 folder licence, commit 33375500bcea): after a substantive research answer, give the reader two or three concrete questions to check facts and assumptions. Owner: digital-research-engine.

**Re-check of the ten Kaizen repositories:** all ten default-branch HEADs equal the pinned or studied commit (Superpowers `8ca22db`, Ponytail `e3ba2aa`, UI UX Pro Max `09170ee`, Graphify `d6eaa8a`, Caveman `2fd153c`, Addy `2686b62`, Understand Anything `b05cc3b`, Awesome `be2a406`, Archify `0e4949f`, Impeccable `114ea1d`). No licence changes. Upstream movement: Superpowers `dev` branch 277 commits ahead of main (`b1f8774`, 27 Sep); Impeccable tagged `engine-v0.1.7` at `6dd107f` on 29 Sep, 59 commits ahead of main; Graphify advisory GHSA-pcc4-rvhr-2pr8 (high, 27 Sep 2026; `graphifyy < 0.9.70`) — the pinned 0.9.71 is past the fix and Graphify remains rejected at P06. No advisories for the other nine.

**Commands and results**
- `python -X utf8 scripts/validate-contracts.py --schema schemas/third-party-skill-register.schema.json --instance docs/security/third-party-skill-register.json` (chwezi-engine-agents) → `PASS`. Negative check on a scratch copy with one verdict `safe_to_install` → `FAIL … not one of ['study', 'borrow_idea', 'ignore', 'block']`, exit 2.
- `python -X utf8 scripts/validate_source_currency.py ../chwezi-engine-agents/docs/operations/m10-kaizen-evidence/M10-13/ecosystem-scan-2026-Q4-sources.json --as-of 2026-09-29` (DRE) → `findings: 0`, `PASS: metadata/date checks only; claim support NOT ASSESSED`, exit 0.
- DRE `skill_contract_validator.py --baseline tests/skill-engine/quality-baseline.json` → 59 active skills, 59 fully compliant, exit 0.
- DRE `routing_smoke_test.py` → 29/29 top-3 (lexical proxy); precision@1 25/29; owned negatives 9 (pass 7, fail 0, not assessed 2); exit 0.
- DRE `validate_engine.py` → exit 0 (routing smoke, no-book-extractions, engine doctor, 37 unit tests OK).

**Decisions under delegated authority (29 Sep 2026):** two screening depths (full screen for skill-shaped, engine-relevant candidates; labelled triage for applications, harnesses, gateways and out-of-domain packs); the ten Kaizen source repositories added as register rows; CC BY-NC 4.0 treated as ideas-only; every new row `review_after` 2026-12-29; next scan first week of January 2027, owner: engine maintainer.

**Open items and hand-offs**
- Supply-chain register owner: the `claude-code-workflows` marketplace (wshobson/agents) was last refreshed locally on 19 Mar 2026; ten of its plugins are enabled and upstream is now at `156b7a5e7a8b`. Not edited here (outside T05 scope).
- Triaged rows must be fully screened before any becomes a borrowing candidate.
- No new reference was written in T05, so no routing case is needed.

## T06 — business-plan figure reference

Files: `business-plan-skills/skills/pipeline/00-plan-assembly/references/plan-figures.md` (new); one-line links in `skills/pipeline/00-plan-assembly/SKILL.md` (248 → 249), `skills/pipeline/13-implementation-timeline/SKILL.md` (301 → 302), `skills/meta-pitch/pitch-deck/SKILL.md` (341 → 342). All ≤ 500 lines.

| Command | Result |
|---|---|
| `python -X utf8 scripts/validate_skill_engine.py --baseline docs/quality/skill-quality-baseline.json` | 137 active skills, 137 fully compliant |
| `python -X utf8 scripts/routing_smoke_test.py --threshold 1.0` | 61/61 (100.0 %) |
| `python -X utf8 -m unittest discover -s tests -p "test_*.py"` | Ran 62 tests, OK (one pre-existing content warning about `skills/demo/references/digest.md`, not blocking) |
| `python -X utf8 scripts/routing_link_check.py` | 7 surfaces, 0 failures |

Synthetic Gantt (`T06-sample-gantt/`): Mermaid `gantt` with the Contracts Committee award as a `milestone, crit` task that the standstill/signature task starts `after`, critical path marked `crit`. `build-doc.sh` → 1 figure rendered, guard 0 Mermaid source, figures manifest written; `verify-manifest` PASS; `font_substitution_check: PASS`, `font_family: Public Sans`; PNG 8064×488 px (1,290 ppi at 6.25 in) plus SVG. SHA-256: `.docx` `cf72727c…f91c5`; manifest `4452cf01…d032619`.

Limitations and hand-off:
- **Legibility.** The renderer strips author `%%{init}%%` lines and Mermaid's Gantt draws on a fixed wide canvas, so at the portrait body measure the labels are far below 8 pt. The reference tells authors to use a landscape page or split by phase and keep the full schedule as a table. **Hand-off to the srs owner (M10-07):** set a Gantt width and font size in the renderer's injected init directive (for example `gantt.useWidth`) so Gantt figures meet the 8 pt rule.
- Mermaid's neutral theme colours `crit` bars red; colour tokens for Gantt are not covered by `diagram-visual-standards.md` §3 (design-engine hand-off, M10-09 owns that area).
- No routing fixture added (concurrency rule). Optional hand-off case for business-plan: prompt "Render the implementation Gantt with the PPDA award as a blocking gate", expected `skills/pipeline/13-implementation-timeline` (not run against the scorer).
- Proof is on a synthetic sample only.

---

## Exit-criteria check

1. Validators for touched engines: proposal, finance, business-plan pass (above); DRE validators pass (T05 section).
2. No renderer, schema or generator code in `proposal-skills` or `business-plan-skills`: only `.md` files added/changed.
3. Finance register folder byte-identical: yes.
4. Live DRE working tree unchanged by T04: T04 installed nothing; the only DRE changes are the two new records under `docs/continuous-improvement/`.
5. Attribution lines present (T02, T06 references; T03 tool docstring; T04 record; T05 scan record); no third-party text copied.

## Pre-existing dirty files (not touched by this executor)

- `proposal-skills`: `skills/language/language-standards/SKILL.md`.
- `digital-research-engine`: `scripts/routing_smoke_test.py`.
- `chwezi-engine-agents`: many M10-03 files (`evals/`, `scripts/`, `tests/`, `schemas/`, `.claude-plugin/marketplace.json`, `CONTRIBUTING.md`, `docs/distribution.md`, workflow).
- `srs-skills`: M10-03 files (routing fixtures, validators, several `SKILL.md`); this executor ran srs commands but wrote nothing inside `srs-skills`.
