# M10-07 — SRS verifiable diagrams and design diagram standards: executor evidence

Executor scope: every M10-07 task in `C:\wamp64\www\srs-skills` (engine, `03-design-documentation` skills, scripts) plus the design-engine tasks AR-12 (T08) and AR-13 (T09) in `C:\wamp64\www\design-system-skills`, and the README / `validate_engine.py` repair in srs. Date: 29 September 2026. Zero spend: local tools only (Python 3.13.7, Node 24.8.0, Pandoc 3.9.0.2, the M10-01 pinned renderer and local Chrome). No commits, pushes, resets or branch changes. Not touched: srs `CLAUDE.md`/`AGENTS.md`/`.claude-plugin/`/`.skills-engine/`, design `CLAUDE.md`/`AGENTS.md`/`.claude-plugin/`, and every client workspace under `srs-skills/projects/` (GarageFlow was read only; the dry run used a scratch copy outside the repository).

Attribution line used in every file that borrows the Archify pattern (module docstrings of `engine/diagram_ir.py`, `engine/diagram_render.py`, `engine/checks/diagram_trace.py`, `engine/diagram_manifest.py`, `engine/baseline.py`, `engine/checks/baseline_delta.py`, `engine/findings.py`, the schema `$comment`, the authoring reference): "Pattern adapted from Archify (MIT, https://github.com/tt-a1i/archify, commit 0e4949f910a8e390bd3b4933883a4dcabad571be). Paraphrased; no schema, code or test text copied." Archify was not installed, vendored or run (AR-18 respected).

## Summary

| Task | Status | One line |
|---|---|---|
| T01 (AR-04) | DONE | `engine/registry/schemas/diagram-ir.schema.json` (draft 2020-12, closed, 7 kinds, per-kind roles, `trace`, `evidence`, `semantic_checks`) + `engine/diagram_ir.py`; 3 valid and 4 invalid fixtures fail with `schema/<keyword>` and JSON-pointer subjects |
| T02 (AR-04) | DONE | `engine/diagram_render.py` + `diagrams generate`; golden trace table byte-identical; every `.mmd` starts with the Public Sans init directive; two runs give identical SHA-256 |
| T03 (AR-05) | DONE | `engine/checks/diagram_trace.py`, registered in `phase03` as `phase03.diagram_trace`; each of 9 negative fixtures raises exactly its code; valid fixture clean |
| T04 (AR-08) | DONE | `Finding` gains keyword-only `code`, `subject`, `evidence`, `supported_fixes`; reporters emit them only when present; golden SARIF/Markdown/JUnit from HEAD reproduced byte for byte |
| T05 (AR-09) | NOT DONE — outside assigned scope | engine-agents `schemas/validation-result.schema.json` extension was not in this executor's scope (srs + design only); orchestrator to assign |
| T06 (AR-06) | DONE | HLD Steps 3, 4, 5, 7, 11, LLD Steps 3–5 and 9, database-design Step 4 rewritten; new `references/diagram-ir-authoring.md`; `%% alt:` / `%% caption:` guidance (M10-01 hand-over) added |
| T07 (AR-07) | DONE | `diagram_elements` in snapshots; `baseline diff` and `BaselineDeltaCheck` report added/removed/changed/moved; legacy snapshot loads |
| T08 (AR-12) | DONE_WITH_LIMITATIONS | `diagram-visual-standards.md` + links + ban-side evidence paragraph; human typographic authority for Public Sans *by name* is NOT_ASSESSED (escalated to Peter); Peter's ratification pending |
| T09 (AR-13) | DONE (enablement awaits Peter's exact-diff approval) | hook widened to `.svg`/`.mmd`/`.json`; 14 new cases; 32/32 pass |
| T10 (AR-14) | DONE | `<OutputName>.figures.json`, `diagrams manifest`, `diagrams verify-manifest`, candidate freezing in `generate` and in the renderer |
| T11 (AR-04/05/14) | DONE_WITH_LIMITATIONS | pilot validates, renders and verifies; full `engine validate` of the partial fixture still fails on pre-existing, unrelated phase gates (see T11); GarageFlow dry run recorded |
| Extra | DONE | srs README references added; `validate_engine.py` no longer requires the canonical path in the thin `CLAUDE.md` bridge (orchestrator instruction); `validate_engine.py` exits 0 |
| Extra | DONE | `%% alt:` / `%% caption:` authoring guidance (M10-01 open item) in the HLD reference, LLD Step 3 and LLD `logic.prompt` |

## Design decisions taken during execution (all within the phase file's notes)

- **Layout on disk.** IR lives in `<doc-dir>/diagrams/*.ir.json`; derived output in `<doc-dir>/_generated/` (`FIG-nnn.mmd`, `trace-table.md`, `.validated.json`, `.generated.json`). A section embeds a figure with `<!-- diagram-ir: FIG-nnn -->` and the trace table with `<!-- diagram-ir: trace-table -->`; `scripts/render_diagrams.py` expands the markers at build time. This keeps `build-doc.sh`'s stitching unchanged.
- **Line-ending-safe hashes.** `core.autocrlf=true` and no `.gitattributes` in srs: a Windows checkout would turn LF into CRLF and change raw SHA-256. IR, Mermaid and trace-table hashes are therefore SHA-256 of the text with CRLF normalised to LF (`text_sha256`); any other one-byte change still changes the hash (tested). Binary PNG/DOCX use raw SHA-256.
- **Edge ids required.** The phase file allows optional relationship ids (Archify). Stable ids are needed for the T07 delta, so `edges[].id` is required in `schema_version` 1.
- **Registry field for "in scope".** `_registry/identifiers.yaml` has no scope or deferral field (schema checked: `id`, `kind`, `defined_in`, `title`, `links`); every FR entry is treated as in scope, recorded in the module docstring. Without a registry file the check uses the identifiers in the project's Markdown and emits one INFO `diagram/registry-absent` finding.
- **Additional codes** beyond the T03 list, all for malformed IR: `diagram/invalid-json`, `diagram/duplicate-id`, `diagram/duplicate-figure-id`, `diagram/candidate-not-validated` (T10), `diagram/stale-generated`, `diagram/unknown-figure` (renderer expansion), `diagram/registry-absent` (INFO), `diagram/baseline-delta` (INFO, T07).
- **Class diagrams** have no IR kind in `schema_version` 1 (the phase's seven kinds). LLD Step 3 keeps Mermaid `classDiagram` with `%% alt:`/`%% caption:`.
- **No drop shadows.** Mermaid's `neutral` theme adds a drop-shadow filter to nodes, which the T08 standard forbids. `render_diagrams.theme_css()` now adds `* { filter: none !important; }` (checked visually on the pilot PNGs).
- **Hook fallback handling.** In `.svg`/`.mmd` the generic quoted-literal matcher is not used, so a banned face named only as a *fallback* warns on stderr instead of blocking (phase note T09); `.json` inspects only the `fontFamily` key.

## T01 — IR schema and loader

Files: `engine/registry/schemas/diagram-ir.schema.json`, `engine/diagram_ir.py`, `engine/tests/fixtures/diagram_ir/{valid/context,sequence,state}.ir.json`, `engine/tests/fixtures/diagram_ir/invalid/{unknown-property,invalid-element-id,malformed-trace-id,missing-alt-text}.ir.json`, `engine/tests/test_diagram_ir.py`.

- Root closed at every level; `schema_version` const 1; `meta.figure_id` `^FIG-[0-9]{3}$`; `alt_text` minLength 20; `owner_document`/`source_documents` reject absolute, drive-letter, backslash and `..` paths; element ids `^[a-z][a-z0-9_-]{0,47}$`; trace `^[A-Z]{2,5}(-[A-Z0-9]{1,8})*-[0-9]{3,5}$` (shape only); roles per kind via `if/then`; `attributes` only on `erd`; `order`+`kind` required on sequence messages, `cardinality` on ERD edges.
- `python -m pytest engine/tests/test_diagram_ir.py -q` → 20 passed. Invalid fixtures: `schema/additionalProperties` at `/nodes/1` (evidence names `colour`), `schema/pattern` at `/nodes/1/id`, `schema/pattern` at `/nodes/1/trace/0`, `schema/required` at `/meta`.

## T02 — generator and `diagrams generate`

Files: `engine/diagram_render.py`, CLI `diagrams generate`, `engine/tests/fixtures/diagram_ir/golden/healthcare-trace-table.md`, `engine/tests/test_diagram_render.py`.

- `context`/`component`/`deployment`/`dataflow` → `flowchart LR` with subgraphs for boundaries; `sequence` → `sequenceDiagram`; `state` → `stateDiagram-v2`; `erd` → `erDiagram` with entity aliases and `PK`/`FK`. Label text is escaped with Mermaid entity codes (`#59;` etc.).
- `DIAGRAM_FONT_STACK = "Public Sans, sans-serif"`, cites `diagram-visual-standards.md`; a test pins it equal to `scripts/diagram-render/render-config.json`.
- Pilot outputs, two runs (SHA-256 identical): `FIG-001.mmd e65dc7f3…cfe5`, `FIG-002.mmd a7369cce…9f36`, `FIG-003.mmd 1205d080…ec03`, `trace-table.md 0d372a4c…806b`, `.generated.json f28abdec…fcc5`.
- Render check of kinds not in the pilot: an `erd` and a `dataflow` IR built through `build-doc.sh` in a scratch project rendered correctly (`artefacts/erd-render-check.png`: Public Sans, `DECIMAL(19,4)`, `||--o{`).
- `pytest engine/tests/test_diagram_render.py` → 7 passed.

## T03 — `DiagramTraceCheck`

Files: `engine/checks/diagram_trace.py`, `engine/gates/phase03.py` (check 9), fixtures `engine/tests/fixtures/diagram_trace/{base,cases/*}`, `engine/tests/test_diagram_trace.py`, `docs/standards-clause-registry.md` (row `phase03.diagram_trace`, ISO/IEC/IEEE 42010:2011 §5.6), `docs/deterministic-gate-phase03.md`, `scripts/validate_engine.py` (explicit id).

| Negative fixture | Codes produced (exactly) | Severity |
|---|---|---|
| unknown-trace-id | `diagram/unknown-trace-id` | HIGH |
| uncovered-requirement | `diagram/uncovered-requirement` | MEDIUM |
| unexpected-root | `diagram/unexpected-root` | HIGH |
| unexpected-terminal | `diagram/unexpected-terminal` | HIGH |
| required-edge | `diagram/required-edge` | HIGH |
| required-path | `diagram/required-path` | HIGH |
| dead-end-state | `diagram/dead-end-state` | HIGH |
| unmapped-sequence | `diagram/unmapped-sequence` | MEDIUM |
| unknown-edge-endpoint | `diagram/unknown-edge-endpoint` | HIGH |
| valid | none | — |

Every finding carries `supported_fixes` containing the guard wording "without removing the requirement or the semantic check" (asserted by test). `pytest engine/tests/test_diagram_trace.py` → 17 passed.

## T04 — `Finding` fields and reporters

Files: `engine/findings.py`, `engine/gates/_shared.py` (`attach_clause` now uses `dataclasses.replace`, so the new fields survive clause attachment), `engine/reporters/{markdown,sarif,junit}.py`, `engine/tests/test_findings.py`, golden files `engine/tests/fixtures/findings_golden/report.{md,sarif.json,junit.xml}` (generated from the HEAD `905b9a4` reporter code in a scratch copy).

- Markdown: `Code | Subject | Supported fixes` columns appear only when a finding carries a diagnostic field; SARIF: `ruleId` = code when present, `properties` = `gateId`, `subject`, `evidence`, `supportedFixes`; JUnit: ` [code]` message suffix.
- All pre-existing tests pass unchanged; legacy findings serialise byte-identically to the HEAD goldens.

## T06 — skills

Files: `03-design-documentation/01-high-level-design/SKILL.md` (276 → 272 lines), `…/references/diagram-ir-authoring.md` (new), `…/logic.prompt`; `02-low-level-design/SKILL.md` (281 → 264), `logic.prompt`; `04-database-design/SKILL.md` (264 → 263), `logic.prompt`.

- Step 11 now embeds `<!-- diagram-ir: trace-table -->`; no hand-typed table. The C4Context/graph TD examples are replaced by a minimal IR example.
- Degraded mode: author IR anyway, mark `[V&V-FAIL: diagram IR not validated]`, report `NOT_ASSESSED`.
- `grep -n "diagram-ir.schema.json" 03-design-documentation/01-high-level-design/SKILL.md` → lines 86, 94, 140.
- `python -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` → 159 active, failure counts `{}`; `python -X utf8 scripts/routing_smoke_test.py` → 54/54, precision 1.000; `python -m engine validate-skills` → SKILLS OK. No new skill (catalogue stays at 159).

## T07 — baseline delta

Files: `engine/baseline.py`, `engine/checks/baseline_delta.py` (new INFO finding `phase09.baseline_delta.diagram_delta`, code `diagram/baseline-delta`, when `_registry/baselines.yaml` declares `previous`; registry row added), `engine/cli.py` (`baseline diff` prints the diagram section only when non-empty), fixture `engine/tests/fixtures/diagram_baseline/` (v1, v2, legacy snapshots plus their IR sources), `engine/tests/test_diagram_baseline.py`.

```text
python -m engine baseline diff engine/tests/fixtures/diagram_baseline v1 v2
Added: 0 / Removed: 0 / Modified: 0
Diagram elements (reports what changed; infers no impact or risk):
  Added: 0   Removed: 1  - FIG-001#auditor   Changed: 0   Moved: 1  > FIG-001#clerk
```

Legacy snapshot (no `diagram_elements` key) loads and diffs. 6 tests pass.

## T08 — diagram visual standards (design engine)

Files: `skills/13-presentations-and-documents/docx-report-and-document-formatting/references/diagram-visual-standards.md` (new), `…/SKILL.md` (Workflow step 6 and References), `…/references/tables-and-figures.md` (one bullet), `doctrine/references/ai-slop-banned-fonts.md` (one paragraph in the evidence-basis section only).

- Typeface: applies the existing formal-document mapping (Source Serif 4 → Public Sans) — Public Sans for labels, JetBrains Mono for code identifiers only. Pairing structure cited to Bonneville via `pairing-principles.md`; Public Sans by name rests on Peter's 29 Sep 2026 house ruling. **`font-groups-and-usage.md` records no typographer, foundry or literature citation for the Public Sans mapping, so the typographic authority is recorded as NOT_ASSESSED and escalated to Peter** (not invented).
- Ban-side evidence entry: Mermaid default stack `trebuchet ms, verdana, arial, sans-serif` (`theme-default.js` line 36, accessed 29 Sep 2026), evidence only. Trebuchet MS and Verdana were **not** added to the JSON ban list — ratification item for Peter.
- UA-13 coordination: the reference names the data-visualisation references folder as UA-13's home; no link to a not-yet-existing file.
- Pilot checklist run (reviewer judgement by the executor, recorded as such): `artefacts/PilotHLD-{1,2,3}.png` — labels in Public Sans (probe `resolved: true`, SVG font check passed, manifest `font_substitution_check: PASS`), neutral greys, no emphasis colour, no shadows after the `filter:none` rule, sentence-case labels, 303+ ppi PNG plus SVG with embedded face, numbered caption and alt text from `meta.alt_text` in the `.docx`. Colour-token mapping is approximated by Mermaid's `neutral` theme (greys), not by project tokens: DONE_WITH_LIMITATIONS.
- `python -X utf8 scripts/validate_engine.py --baseline tests/quality-baseline.json` → exit 0 (101/101 compliant; pre-existing report-only byte warnings); `routing_smoke_test.py` → 68 fixtures, precision@3 100 %, exit 0; `validate_route_existence.py` → PASS, findings 0 (`artefacts/design-verify.txt`).

## T09 — banned-font hook

Files: `hooks/banned-font-gate.js`, `hooks/test-banned-font-gate.js`.

- `RELEVANT_EXTENSIONS` += `.svg`, `.mmd`, `.json`. New matcher for SVG `font-family="…"`/`'…'`, CSS `font-family:` stacks inside SVG/Mermaid (quoted stacks included), and `fontFamily` keys (JSON, escaped-quote and single-quoted directive forms). First family decides; banned fallbacks in `.svg`/`.mmd` warn on stderr. `.json` inspects only the `fontFamily` key. Ban list still read only from `ai-slop-banned-fonts.json`.
- `node hooks/test-banned-font-gate.js` → **32/32 passed** (18 pre-existing unchanged + 14 new, including `font-family="Arial"` in `.svg`, `"fontFamily":"Inter"` inside `%%{init}%%` in `.mmd`, `"fontFamily": "Roboto"` in `.json`, JetBrains Mono and Public Sans allowed, fallback warnings asserted on stderr).
- The pilot's real SVG, `.mmd` and IR files pass the hook (exit 0).
- Enablement in the plugin needs Peter's exact-diff approval (phase §9); not enabled or changed elsewhere by this work.

## T10 — figure manifest and candidate freezing

Files: `engine/diagram_manifest.py`, CLI `diagrams manifest` / `diagrams verify-manifest`, `scripts/build-doc.sh` (one manifest call after the `.docx` guard), `scripts/render_diagrams.py` (marker expansion, candidate check, IR fields in `render-manifest.json`, `filter:none`), `engine/figures.py` (IR provider registered in `FIGURE_PROVIDERS`), `engine/tests/test_diagram_manifest.py`, `.gitignore` additions for build outputs.

- One byte changed in a fixture IR without re-validating → `diagrams generate` exits 1 with `diagram/candidate-not-validated`; `build-doc.sh` also refuses (tested end to end).
- One byte changed after the build (IR, PNG or `.mmd`) → `verify-manifest` exits 1 naming the figure (`FIG-001`, `FIG-003`, `FIG-002`); an untouched rebuild verifies clean (tested end to end with the real renderer).
- Pilot manifest: `artefacts/PilotHLD.figures.json` (3 figures, renderer `@mermaid-js/mermaid-cli` 12.0.0, font Public Sans, `font_substitution_check: PASS`, `state: local-review-export`, `artifact_sha256` map of 13 paths).

## T11 — pilot and dry run

Pilot files: `engine/tests/fixtures/healthcare_admissions/03-design-documentation/01-high-level-design/{hld.md, diagrams/context.ir.json, diagrams/intake-retry-sequence.ir.json, diagrams/intake-lifecycle-state.ir.json, _generated/*}` and `engine/tests/fixtures/healthcare_admissions/.gitignore`. Synthetic content only.

- `python -m engine diagrams validate engine/tests/fixtures/healthcare_admissions` → `DIAGRAMS: PASS (3 figure(s) validated)`; `generate` → PASS; `bash scripts/build-doc.sh …/01-high-level-design PilotHLD` → 3 figures, 0 Mermaid source in `.docx`, manifest written; `verify-manifest` → PASS.
- `python -m engine validate engine/tests/fixtures/healthcare_admissions` → **still FAIL, on pre-existing gates unrelated to diagrams** (the fixture is a partial behavioural fixture with no phase 04–09 artefacts: `phase01.canonical_inputs_present`, `phase03.architecture_decisions_recorded`, `phase03.security_threat_model_present`, `phase04.*`, `phase05.*`, `phase06.*`, `phase07.*`, `phase08.*`, `phase09.*`). With the IR present the diagram check adds only one INFO finding (`diagram/registry-absent`; the fixture has no identifier registry), `phase03.design_docs_have_figures` is satisfied by the IR provider, and the six previous `phase03.requirements_have_design_evidence` findings are cleared by the generated trace table. The literal acceptance "validate passes" is therefore NOT met for reasons outside M10-07; recorded as a limitation rather than filling the fixture with unrelated artefacts.
- Dry run (GarageFlow HLD, scratch copy outside `projects/`; source `projects/GarageFlow/03-design-documentation/01-high-level-design/hld.md` SHA-256 `d7321bc4…ef2`, read only). Three figures transcribed to IR without adding design content: §1 system context (as `component`, 18 nodes, 22 edges), §4.2 MoMo request-to-pay (`sequence`, 9 messages), §3.5 payment state machine (`state`). Findings (`artefacts/M10-07-T11-dryrun-code-counts.json`; no client text in the public evidence):

| Code | Count | Reviewer judgement (executor, recorded as judgement) |
|---|---|---|
| `diagram/unknown-trace-id` (HIGH) | 11 | **Not a document defect.** All are `EI-nnn` external-interface ids, which are genuine SRS identifiers but are not in `engine.idscan.KIND_PREFIXES`. Engine gap; adding `EI` changes `sync`/registry behaviour for every workspace, so it is handed off (M10-08/M10-14) rather than changed here |
| `diagram/unmapped-sequence` (MEDIUM) | 1 | **False positive.** FR-108 is a stimulus-response requirement, but GarageFlow writes FRs as `**FR-108 Title.** … shall …`, which `stimulus_response.py`'s pattern (`**FR-nnn**` then text) does not recognise. Engine gap, handed off |
| `diagram/uncovered-requirement` (MEDIUM) | 169 | **Expected, not a defect.** Only 3 of the document's figures were converted; the HLD's component table (not IR) carries most FR mappings |
| Semantic checks (required paths/edges, dead ends, terminals) | 0 | The state machine and the sequence satisfied every declared check |

True document defects found by `diagram/*` codes: **0**. Limitations found: IR `sequence` cannot express Mermaid `alt`/`loop` blocks (the alternative webhook/polling branches became ordered messages); self-messages are allowed. Under the value gate's no-change clause (zero true defects), Peter decides whether the hand table is adequate; the pilot shows the generated table and figure checks work.

## Extra — srs README and `validate_engine.py`

- `README.md`: new "Project workspaces and operating models" section naming `projects/<ProjectName>/`, `docs/hybrid-operating-model.md`, `docs/regulated-evidence-model.md` (both files verified present).
- `scripts/validate_engine.py`: `validate_root_pathing()` checks `README.md` and `AGENTS.md` only (the thin `@AGENTS.md` `CLAUDE.md` bridge from M10-02 imports the text); explicit ids for `phase03.diagram_trace` and `phase09.baseline_delta.diagram_delta`.
- `python -X utf8 scripts/validate_engine.py` → `ENGINE CONTRACT: PASS`, exit 0.

## Verification run (29 Sep 2026)

| Command (srs-skills) | Result |
|---|---|
| `pip install -c requirements-ci.txt -e ".[dev]"` | exit 0 |
| `python -m pytest --cov=engine --cov-fail-under=90` | **367 passed, 2 skipped** (pre-existing skips); coverage **96.54 %** (M10-01 baseline 298 passed, 95.83 %); includes both real-renderer end-to-end builds |
| `python -X utf8 scripts/validate_engine.py` | PASS, exit 0 |
| `python -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | exit 0, 159 active, failure counts {} |
| `python -X utf8 scripts/routing_smoke_test.py` | 54/54, precision 1.000 |
| `python -m engine validate-skills` | SKILLS OK |
| `python scripts/seed_demo_project.py` + `python -m engine validate projects/_demo-hybrid-regulated` | PASS |
| same with `--break-something` | exit 1 (negative control fails as designed) |
| `python -X utf8 scripts/source_ingestion_guardrail.py` | findings 0 |
| `python -m engine diagrams validate / generate engine/tests/fixtures/healthcare_admissions` | PASS / PASS |
| `python -m engine diagrams verify-manifest …/healthcare_admissions/03-design-documentation/01-high-level-design` | PASS |
| `python -X utf8 scripts/check_docx_diagrams.py --scan projects --exclude _kaizen,render-runs` | 691 scanned, 0 with Mermaid source |
| `bash -n scripts/build-doc.sh` | OK |

Design-system-skills: see T08/T09 (`artefacts/design-verify.txt`). chwezi-engine-agents `validate-contracts.py`: NOT_ASSESSED (T05 not in scope).

## Open items for the orchestrator / Peter

1. **T05 (AR-09)** not executed — engine-agents schema slice needs an owner. The finding shape it should mirror is in `engine/diagram_ir.py` (`code`, `subject`, `evidence`, `supported_fixes`) and the `--json` output of `diagrams validate`.
2. **Shared file:** `design-system-skills/doctrine/references/ai-slop-banned-fonts.md` was already modified (uncommitted `<!-- rule:font.ban.* -->` anchors from another executor) when T08 ran. The T08 change is one paragraph inserted after the "…source-verification pass (2026-06-21)." line; the other executor's 16 anchors were intact afterwards. Stage both together or check the merge. `design-system-skills/README.md` and `scripts/validate_engine.py` were also dirty from another executor and were not touched here.
3. **Peter's ratification:** T08 doctrine (diagram typography and the ban-side entry); the NOT_ASSESSED typographic authority for Public Sans; whether to add Trebuchet MS / Verdana to the JSON ban list; exact-diff approval before the widened T09 hook is relied on in the plugin.
4. **Hand-offs:** `EI` prefix recognition and `**FR-nnn Title.**` stimulus-response recognition (dry-run false positives) → M10-08/M10-14; `diagram/uncovered-requirement` ratchet → M10-14; IR `sequence` has no `alt`/`loop` — consider a `schema_version` 2 fragment construct; class-diagram IR kind not in v1.
5. **CI:** `.github/workflows/engine.yml` still has no Node step, so the two real-renderer tests skip in GitHub CI (unchanged from M10-01); all other new tests run there.
