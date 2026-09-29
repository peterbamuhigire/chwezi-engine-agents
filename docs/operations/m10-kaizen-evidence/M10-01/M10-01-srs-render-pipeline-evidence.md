# M10-01 — SRS render pipeline evidence (T09–T12)

Executor scope: `C:\wamp64\www\srs-skills` and its git-ignored client workspaces under `projects/` (T11 only). Date: 29 September 2026. Zero spend: only free local tools and a free npm install. No commits, pushes or branch changes. `srs-skills/AGENTS.md` and `CLAUDE.md` were not touched.

Attribution: the build-guard and render-receipt ideas are adapted from tt-a1i/archify (MIT, https://github.com/tt-a1i/archify, commit `0e4949f910a8e390bd3b4933883a4dcabad571be`), paraphrased; no Archify code was copied. The attribution line sits in `scripts/render_diagrams.py`, `scripts/check_docx_diagrams.py`, `engine/figures.py` and every `render-manifest.json`.

## Summary

| Task | Status | One line |
|---|---|---|
| M10-01-T09 | DONE | Pinned local renderer (`@mermaid-js/mermaid-cli` 12.0.0, lockfile, local Chrome, dead-proxy offline), `scripts/render_diagrams.py`, wired into `scripts/build-doc.sh` before Pandoc; fixture: 2 PNG + 2 SVG + 2 `word/media/` entries; malformed block exits 1 with no `.docx` |
| M10-01-T10 | DONE | `scripts/check_docx_diagrams.py` guard, called at the end of `build-doc.sh`; `--scan projects --exclude _kaizen,render-runs` → 691 files, 18 hits before T11, 0 after; clean/dirty unit tests |
| M10-01-T11 | DONE_WITH_LIMITATIONS | All 10 documents and 8 export copies (plus the second KraalCode copy) regenerated; originals quarantined; `export/BUILD-LOG.md` in 7 projects. Client re-issue NOT_ASSESSED (awaiting Peter, external release). One source edited after delivery (AcademiaPro ERD) and one source repaired for Mermaid syntax (GarageFlow HLD) — see T11 |
| M10-01-T12 | DONE | `phase06.infra_has_ir_diagram` now needs an incident-response figure (existing image or recorded rendering); new `phase03.design_docs_have_figures` for HLD/LLD; `engine/figures.py` `FIGURE_PROVIDERS` extension point for the M10-07 IR sidecar; coverage 95.83 %; sabotage control still fails |

## T09 — renderer spike and render step

### Spike (time-boxed; about 1.5 hours)

| Option | Local? | Result |
|---|---|---|
| (a) `@mermaid-js/mermaid-cli` 12.0.0 pinned in `scripts/diagram-render/package.json` + `package-lock.json` (204 packages, all from registry.npmjs.org), `PUPPETEER_SKIP_DOWNLOAD=1`, local Chrome via `PUPPETEER_EXECUTABLE_PATH` | Yes | **Chosen.** Renders all diagram kinds the SRS skills use (flowchart/graph, sequence, erDiagram). One browser session per document (`render.mjs` batches jobs). About 15–30 s per document |
| (b1) `pandoc-mermaid-filter` / `mermaid-filter` (npm) | Yes | Wraps the same mermaid-cli + Puppeteer; no gain; less control over captions, alt text, ppi and fonts. Not taken |
| (b2) Self-hosted Kroki | Would be | Needs Docker; Docker is not installed. Not taken |
| (b3) PlantUML (Java 21 present) | Yes | Different diagram language; would mean rewriting every client diagram. Not taken |
| (b4) `mermaid-py`, mermaid.ink, kroki.io | No | Hosted renderers — **forbidden**; not used |

- Install (the only network step): `npm install` with `PUPPETEER_SKIP_DOWNLOAD=1` — 204 packages, no browser download. `npm ci --offline` from the lockfile then reinstalled all 204 packages from the local cache with no network.
- `npm audit --omit=dev` first reported 6 high advisories, all via transitive `lodash-es@4.17.23` (mermaid → chevrotain). Fixed with an `overrides` pin `lodash-es: 4.18.1` in `package.json`; `npm audit` → **0 vulnerabilities**.
- Offline by construction: `render.mjs` launches Chrome with `--proxy-server=http://127.0.0.1:9 --proxy-bypass-list=<-loopback>`, so any request not served from local files goes to a dead proxy. The fixture and all 10 client documents rendered under this setting, which shows that no network access is needed after the one-time install.
- Versions recorded in each manifest: mermaid-cli 12.0.0, mermaid 12.0.0, puppeteer 25.12.0; browser `C:\Program Files\Google\Chrome\Application\chrome.exe`.

### Font (Public Sans) — findings and substitution record

- Config: `scripts/diagram-render/render-config.json` → `diagram_font_family: "Public Sans"`, fallback `sans-serif`. Checked at render time against `design-system-skills/doctrine/references/ai-slop-banned-fonts.json` (hardBan, prefix bans, secondaryBan, monospaceBanned) plus Mermaid's own defaults (Trebuchet MS, Verdana, Arial, Recursive Variable); a bare generic family is refused.
- **Public Sans is not installed system-wide** on this machine (`C:\Windows\Fonts` and the per-user font folder hold no Public Sans). It is present at `design-system-skills/fonts/08-body-ui-workhorses/public-sans/PublicSans-VF.ttf` (OFL). The render step loads that file with `@font-face` (inlined as a data URI, because mermaid-cli's file interceptor does not serve `.ttf`), and embeds the same face in every SVG. A headless-Chrome probe (`document.fonts.load` + `check`) runs before rendering and fails the build if the face does not resolve; every manifest records `"headless_chrome_probe": {"family": "Public Sans", "facesLoaded": 1, "resolved": true}`. If the file is missing the build stops (exit 3); the face is never silently substituted.
- Spike findings that the guard now catches:
  1. Mermaid **drops a `themeVariables.fontFamily` value that contains quote characters**; the first render therefore fell back to `"trebuchet ms", verdana, arial`. The family list is now written unquoted (`Public Sans, sans-serif`, valid CSS).
  2. Mermaid 12 applies the face only through a CSS variable scoped to a selector that matches nothing, so **flowchart HTML labels rendered in the browser's default serif (Times New Roman)** although the SVG declared Public Sans. Fixed by a `themeCSS` rule that pins the face on every element; confirmed visually on the PNGs.
  3. `render_diagrams.py` now fails a figure when the SVG's primary face is anything other than the approved face or a generic, or when the universal font rule is missing.
- Init directive injected into every block from the one config value: `%%{init: {"theme": "neutral", "themeVariables": {"fontFamily": "Public Sans, sans-serif"}}}%%` (placed after a block's YAML front-matter when one exists). Theme `neutral` (greyscale) was chosen for print documents; AR-12 in M10-07 sets the final diagram typography standard.
- Substitution record: no substitution occurred. Public Sans is the face used in every rendered figure.

### Figure insertion, resolution, evidence

- Figure form: `![Figure N — <caption>](_figures/<doc>-<n>.png){width=<in>in fig-alt="<alt>"}`. The phase file's example says `{width=100%}`; Pandoc's DOCX writer did not honour a percentage width in testing (a 1×1 px image came out at 1 pt), so the width is written in inches equal to the body measure (6.25 in from `templates/reference.docx` margins), reduced when a tall figure would exceed 8 in.
- Alt text from `%% alt: …` in the block, otherwise from the nearest heading (section numbers stripped) with a `WARNING` on stderr; caption from `%% caption: …`, otherwise the heading. `scripts/diagram-render/figure-alt.lua` moves the alt text into Word's image description (`wp:docPr descr`), while the caption stays below the figure (`ImageCaption` style). Verified in the fixture `.docx`.
- Pandoc reader changed from `-f gfm` to `-f gfm+attributes+implicit_figures` (needed for width and captions). Pandoc lays the figure out at 5.83 in in the current template, so the recorded ppi (computed at 6.25 in) is a lower bound.
- PNG scale = ceil(300 × printed width / SVG width), minimum 2, maximum 12. All fixture and client figures: 303–794 ppi (list in the T11 report).
- `render-manifest.json` in `<doc-dir>/_figures/` (P18 `render-review-manifest.json` convention): per figure the source file, block index, source-block SHA-256, PNG/SVG SHA-256, pixel size, printed width, ppi, caption, alt text and alt source; per document the renderer versions, browser, font family, font file SHA-256 and probe result.
- Stitching: `render_diagrams.py` joins the section files in manifest or alphabetical order (as Pandoc did), reading them with `utf-8-sig` so a BOM in a later file cannot leave `﻿# Heading` in the body (found on KampusPad `threat-model.md`).

### Acceptance commands

```text
bash scripts/build-doc.sh engine/tests/fixtures/diagram_render/valid/design FixtureDesign
  render_diagrams: 2 figure(s) rendered; manifest …/valid/design/_figures/render-manifest.json
  Scanned 1 .docx file(s); 0 contain Mermaid source.
  Built: engine/tests/fixtures/diagram_render/valid/FixtureDesign.docx      exit 0
  _figures: FixtureDesign-1.png, -1.svg, -2.png, -2.svg
  word/media: rId9.png, rId13.png (2 entries); docPr descr = the alt texts; captions "Figure 1 — System context", "Figure 2 — Incident response flow"
bash scripts/build-doc.sh engine/tests/fixtures/diagram_render/malformed/design FixtureMalformed
  ERROR: 01-broken.md block 1 (figure 1): Parse error on line 2: …
  ERROR: diagram rendering failed; no .docx was written                     exit 1
```

The same two builds run as `engine/tests/test_diagram_figures.py::test_build_doc_renders_fixture_and_rejects_malformed` (skipped automatically where the renderer, browser, font, Pandoc or `reference.docx` is absent — for example GitHub CI, which does not run `npm ci`). Linux runtime behaviour: NOT_ASSESSED (Windows only).

## T10 — post-build guard

- `scripts/check_docx_diagrams.py`: reads `word/document.xml` text and exits 1 on `sequenceDiagram`, `flowchart <dir>`, `graph <dir>`, `erDiagram`, `C4Context|C4Container|C4Component|C4Deployment`, `classDiagram`, `stateDiagram(-v2)`. It needs a direction after `flowchart`/`graph`, so prose such as "a flowchart shows" does not trip it (the phase file's `flowchart ` pattern would). `--scan` skips `~$` lock files, the `--exclude` names and any `.trash-*` quarantine folder; exit 2 on usage or read errors. Called at the end of `build-doc.sh`.
- Before T11: `python -X utf8 scripts/check_docx_diagrams.py --scan projects --exclude _kaizen,render-runs` → `Scanned 691 .docx file(s); 18 contain Mermaid source.`, 30 diagram headers, every hit `media=0` — the same 691/18 as the Archify report (`M10-01-srs-T10-scan-before.json`).
- After T11: `Scanned 691 .docx file(s); 0 contain Mermaid source.`, exit 0 (`M10-01-srs-T10-scan-after.json`).
- Unit tests (`engine/tests/test_diagram_figures.py`): clean vs dirty fixture `.docx`, scan with excludes/quarantine/lock files and JSON report, usage and bad-zip errors.

## T11 — regeneration of the 18 files

Driver: a scratchpad script (not committed) — `build-doc.sh` itself for build-doc.sh documents; for project-builder documents, that builder's Pandoc options and post-processor with the render step in front. Every original was copied to `.trash-<timestamp>/<name>.docx.quarantined` beside it **before** being overwritten. The `.quarantined` suffix stops the projects' `export-docs.ps1` (which copies every `*.docx` recursively) from re-exporting a dirty original. Nothing was deleted. All 19 quarantined copies (the 18 originals plus a second copy of GarageFlow Design from a failed first attempt) re-scan as containing Mermaid source, which confirms that they are the delivered originals.

| Document (under `srs-skills/projects/`) | Builder used | Figures (ppi) | Text check against the delivered file |
|---|---|---|---|
| `Ogma-Library/Ogma-Library_DeploymentOps_v2.1_2026-08-13.docx` (+ export) | `scripts/build_docx.py` options (`--toc --number-sections`, title) + `postprocess_docx.py` | 1 (346) | only the Mermaid code paragraph replaced |
| `Medic8/03-design-documentation/Medic8_ERD.docx` | `build-doc.sh` | 1 (794) | only the Mermaid code paragraph replaced |
| `Kulima/03-design-documentation/Kulima_DatabaseDesign.docx` (+ export) | `build-doc.sh` | 1 (603) | only the Mermaid code paragraph replaced |
| `Kulima/03-design-documentation/Kulima_HLD.docx` (+ export) | `build-doc.sh` | 1 (568) | only the Mermaid code paragraph replaced |
| `Kulima/export/Kulima_OperationsReadiness.docx` (export only) | `build-doc.sh` on `06-deployment-operations/` (alphabetical; first heading matches), output moved into `export/` | 1 (578) | only the Mermaid code paragraph replaced |
| `KraalCode/06-deployment-operations/KraalCode_Infrastructure.docx` (+ `04-infrastructure-docs/` copy + export) | `build-doc.sh` on `04-infrastructure-docs/` | 1 (371) | only the Mermaid code paragraph replaced |
| `KampusPad/03-design-documentation/KampusPad_Design_v1.1.docx` (+ export) | `build-docx.ps1` Build-Docx options + `postprocess_docx.py --version 1.1` | 4 (404, 657, 615, 725) | Mermaid paragraphs replaced; the delivered file had a pre-filled TOC cache, the rebuilt file has the TOC field (Word fills it on open) |
| `GarageFlow/03-design-documentation/GarageFlow_Design_v1.0.docx` (+ export) | no project builder found; Pandoc `markdown` over the sorted `*.md` files, no TOC (heading order and curly quotes match the delivered file) | 4 (658, 524, 338, 507) | only the 4 Mermaid code paragraphs replaced |
| `GarageFlow/06-deployment-operations/GarageFlow_Operations_v1.0.docx` (+ export) | as above | 1 (303) | only the Mermaid code paragraph replaced |
| `AcademiaPro/03-design-documentation/AcademiaPro_ERD.docx` | `build-doc.sh` | 2 (678, 527) | **source edited after delivery**: the rebuilt file also carries the AI Module Layer (section 4.8, a second ERD block), similarity 0.91 |

Every regenerated file has at least one `word/media/` entry per former diagram header (media 0 → 1, 1, 1, 1, 1, 1, 4, 4, 1, 2). SHA-256 before and after for each file and each export copy are in `M10-01-srs-T11-regeneration-report.json` and in each project's `export/BUILD-LOG.md` (KraalCode, Medic8, AcademiaPro, Kulima, KampusPad, GarageFlow, Ogma-Library). The evidence copy leaves out text samples, because client content stays out of this public repository.

Decisions under delegated authority (orchestrator under Peter's delegated authority, 29 Sep 2026):

1. **Version labels unchanged.** File names and in-document versions stay as delivered; the version increment belongs to the re-issue, which is an external release awaiting Peter. Client re-issue: **NOT_ASSESSED (awaiting Peter's approval)**.
2. **Export copies refreshed by targeted copy**, not by running each project's `export-docs.ps1`. That script re-copies every `.docx` in the project, which would have touched unrelated deliverables. The effect on the 8 affected copies is the same.
3. **GarageFlow HLD source repair.** Two sequence-diagram messages contained a bare `;`, which Mermaid 12 reads as a statement break, so the build (correctly) refused to render them. Each `;` was written as the Mermaid entity `#59;`, which renders as `;`, so the wording is unchanged. The original is at `GarageFlow/03-design-documentation/01-high-level-design/.trash-20260929-m10-01-T11/hld.md.quarantined`.
4. **AcademiaPro ERD rebuilt from the current source**, which now includes post-delivery content. It is not reconstructed from the old `.docx` (per the risk table). Flagged for Peter before any re-issue.

No document had missing source Markdown, so there are no `NOT_ASSESSED (source absent)` entries.

## T12 — gate change

- `engine/figures.py` (new): a figure is an image reference whose target exists (relative to the document or workspace root; remote URLs ignored), or a Mermaid block whose rendering is recorded in a `_figures/render-manifest.json` with the same source-block SHA-256 and whose PNG still exists (stale or deleted renders do not count). `FIGURE_PROVIDERS` is the documented extension point where M10-07 (AR-03 completion) registers the IR-sidecar provider.
- `engine/gates/phase06.py`: `_IR_DIAGRAM_RE` (which accepted the words `mermaid|plantuml`) is replaced. The infrastructure document must mention incident response **and** carry a figure whose label, target or diagram text is about it (incident, IR, escalation).
- `engine/gates/phase03.py`: new check `phase03.design_docs_have_figures`. Each HLD/LLD document (directory or file under `03-design-documentation/` whose name carries `hld|lld|high-level-design|low-level-design`) needs at least one figure. Clause: ISO/IEC/IEEE 42010:2011 §5.6 (architecture models); row added to `docs/standards-clause-registry.md`.
- Documentation: `docs/deterministic-gate-phase03.md` and `-phase06.md` updated.
- Knock-on: the seeded demo and the clean-project CLI test referenced `./ir.png` without the file existing, which the old regex accepted. `scripts/seed_demo_project.py` now writes a valid 1×1 placeholder PNG (labelled synthetic in a comment, like the demo's placeholder screenshots), and `test_cli.py` writes the file.
- Tests: a Mermaid-only fixture fails `infra_has_ir_diagram`; an existing rendered figure passes; stale render, missing PNG, dangling or remote image, unlabelled image and the provider extension point are covered, as are the phase03 fail/pass/silent cases.

## Verification run (29 Sep 2026, Windows 11, Python 3.13.7, Node 24.8.0, Pandoc 3.9.0.2)

| Command | Result |
|---|---|
| `python -m pytest` (repo config: `engine/tests`, `--cov-fail-under=90`) | **298 passed, 2 skipped** (pre-existing skips: `test_doctor` PATH, empty examples set); coverage **95.83 %** (`engine/figures.py` 100 %, `phase06.py` 100 %, `phase03.py` 97 %) |
| `python -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | exit 0; 159 active, 1 template, failure counts {} |
| `python -X utf8 scripts/routing_smoke_test.py` | 54/54, precision 1.000 |
| `python -m engine validate-skills` | SKILLS OK |
| `python scripts/seed_demo_project.py` + `python -m engine validate projects/_demo-hybrid-regulated` | ENGINE CONTRACT: PASS |
| same with `--break-something` | exit 1 (negative control still fails as designed) |
| `python -X utf8 scripts/source_ingestion_guardrail.py` | findings: 0 |
| `python -X utf8 scripts/validate_engine.py` | **FAIL — pre-existing, outside this scope**: `README.md` lacks `projects/<ProjectName>/`, `docs/hybrid-operating-model.md`, `docs/regulated-evidence-model.md` (the committed HEAD README already lacks all three, after the 2026-09-28 README refresh). The one new finding this work introduced (clause-registry row for the new check) was fixed |
| `python -X utf8 scripts/check_docx_diagrams.py --scan projects --exclude _kaizen,render-runs` | 691 scanned, 0 with Mermaid source |
| `bash -n scripts/build-doc.sh` | syntax OK |
| `npm audit --omit=dev` (scripts/diagram-render) | 0 vulnerabilities |

## Open items

- Client re-issue of the 10 documents (and version increments): Peter (external release). AcademiaPro ERD carries post-delivery content; confirm first.
- Peter's ratification of the T12 gate semantics (listed in the phase exit criteria).
- `validate_engine.py` README failures (pre-existing): owner is whoever maintains the README (it was not touched here).
- Authoring guidance: the SRS design skills should ask for `%% alt: …` and `%% caption: …` comments in Mermaid blocks. Every client figure used the heading fallback (warnings logged). This needs skill text edits, left for M10-07 (diagram IR, AR-12/AR-14) to avoid overlapping another executor's files.
- Large ERDs (Medic8, 46 entities) render legibly at high ppi but are dense at body width; a landscape-page option is an M10-07 layout concern.
- CI: `.github/workflows/engine.yml` has no Node step, so the render integration test is skipped in CI; the guard and gate tests run there.
