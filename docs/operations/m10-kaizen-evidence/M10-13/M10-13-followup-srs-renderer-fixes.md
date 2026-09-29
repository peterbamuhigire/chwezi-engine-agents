# M10-13 follow-up — srs renderer fixes (evidence)

Bounded follow-up to the defects in `M10-13-cross-engine-extensions-evidence.md` (T01 finding 3, T02/T06 limitations and hand-offs). Date: 29 September 2026. Zero spend: local tools only (Python 3.13, Pandoc 3.9.0.2, the pinned renderer `@mermaid-js/mermaid-cli` 12.0.0 with local Chrome). No git state changes; all edits unstaged. Client workspaces under `srs-skills/projects/` were read only (scan).

## Summary

| Item | Status | One line |
|---|---|---|
| 1. `build-doc.sh` MSYS path | DONE | `--resource-path` now gets `cygpath -m` of the doc directory; defect reproduced before the fix, new test builds from a `/c/...` path with both figures embedded |
| 2. Missing-figure guard | DONE | `check_docx_diagrams.py` now fails when a render manifest's PNG is not embedded (SHA-256) or a figure caption has no image above it; `build-doc.sh` passes the manifest explicitly; 4 new tests |
| 3. Gantt width and colours | DONE | Gantt jobs get `useWidth` 720 px, 13 px labels, neutral token colours, no today line; T06 sample re-rendered at 720 px (PNG 2160 × 840, 345 ppi), smallest label about 8.1 pt at 6.25 in; design reference gained §3a Gantt |
| 4. Proposal routing fixture | DONE | `technical-approach-figures` added; smoke 26/26, ranked 2nd; baseline count 25 → 26 |

## 1. `build-doc.sh` given an MSYS path

Reproduction before the fix (scratch copy of `engine/tests/fixtures/diagram_render/valid/design`, path passed as `/c/Users/.../repro/design`): Pandoc printed `[WARNING] Could not fetch resource _figures/Repro-1.png: replacing image with description` (×2), the old guard printed `0 contain Mermaid source`, and `word/media/` was empty.

Cause: Pandoc is a native Windows program; MSYS converts a path argument but not a path inside a `;`-separated list, so `--resource-path=.;/c/...` was unreadable.

Fix (`scripts/build-doc.sh`): a `native_path` helper runs `cygpath -m` when `cygpath` exists (Git Bash, MSYS2, Cygwin) and returns the path unchanged elsewhere; `--resource-path` and the guard's `--render-manifest` use `DOC_DIR_NATIVE`.

Test: `engine/tests/test_diagram_figures.py::test_build_doc_accepts_msys_path` builds the valid fixture from a `/c/...` path, asserts exit 0, no `Could not fetch resource` in stderr, and that both manifest PNG hashes are in `word/media/`. Skipped where the renderer, browser, Pandoc or (on Windows) `cygpath` is absent. Note: the renderer tests are skipped when pytest runs from PowerShell, because `shutil.which("bash")` then finds WSL bash in `System32`; they run from Git Bash (as below).

## 2. Missing-figure guard

`scripts/check_docx_diagrams.py` now runs three checks per `.docx`:

1. Mermaid source in the visible text (unchanged).
2. **Missing figure:** every PNG a render manifest lists for the document (key = `.docx` stem) must be embedded in `word/media/` byte for byte (SHA-256; Pandoc embeds PNGs unchanged, checked on 4 regenerated client files). Manifests: `--render-manifest` (repeatable), or discovered: `<stem>.figures.json` beside the `.docx`, `_figures/render-manifest.json` at or below the `.docx` folder and, in `--scan`, anywhere in the same top-level project folder (export copies). Pass when one listing manifest is fully embedded; a manifest without hashes falls back to a count check.
3. **Figure placeholder:** an `ImageCaption` paragraph whose preceding paragraph holds no `w:drawing`/`w:pict`/`w:object` (Pandoc's "replacing image with description"). Needs no manifest.

Exit 1 on either failure; output lines `MISSING-FIGURE` and `FIGURE-PLACEHOLDER`; JSON report gains `manifest_checked` and `missing`. The old guard on the pre-fix reproduction `.docx` now gives 2 × `MISSING-FIGURE` + 2 × `FIGURE-PLACEHOLDER`, exit 1.

Tests added: `test_check_docx_fails_when_manifest_figure_not_embedded` (good / fetch-failed / stale image), `test_check_docx_placeholder_without_manifest`, `test_check_docx_discovers_manifests` (build-doc layout, export copy, `figures.json`, malformed manifest), `test_check_docx_manifest_helpers`.

### Client-document scan (read only)

`python -X utf8 scripts/check_docx_diagrams.py --scan projects --exclude _kaizen,render-runs`:

```
FIGURE-PLACEHOLDER projects\GarageFlow\08-end-user-documentation\GarageFlow_UserDocs_v1.0.docx caption='Garage Manager App home screen — screenshot pending first build' (no image above the caption)
FIGURE-PLACEHOLDER projects\GarageFlow\export\GarageFlow_UserDocs_v1.0.docx caption='Garage Manager App home screen — screenshot pending first build' (no image above the caption)
Scanned 691 .docx file(s); 0 contain Mermaid source.
Figure check: 18 .docx file(s) matched a render manifest; 2 missing rendered figures.
```

- Mermaid-source hits: **0** (unchanged).
- The 18 regenerated client `.docx` files from M10-01-T11 (Ogma-Library ×2, Medic8, Kulima DB ×2, Kulima HLD ×2, Kulima Operations export, KraalCode ×3, KampusPad ×2, GarageFlow Design ×2, GarageFlow Operations ×2, AcademiaPro) all matched a render manifest and all pass: every figure is embedded. None newly fails. (The "19" in M10-01 counts the quarantined originals, which sit in `.trash-*` and are skipped.)
- **Investigated, not weakened:** the 2 hits are GarageFlow user documentation (original and export copy), not regenerated diagram documents. `08-end-user-documentation/user-manual.md` line 3 references `screenshots/manager-home.png`, which does not exist, so Pandoc wrote the alt text in place of the picture. This is a real defect in a delivered file that the old guard could not see. Because the scan now exits 1, anyone running the scan as a pass/fail gate will see it fail until the screenshot is supplied or the image line is removed from the source. Client workspace not touched.

## 3. Gantt width and colours

Cause: Mermaid sizes a Gantt chart to its container (the renderer's 4,000 px viewport), so T06's chart was drawn 3,984 px wide (PNG 8,064 px). Also found: author or injected `%%{init}%%` directives containing `'` are dropped whole, because Mermaid turns every `'` into `"` before parsing the directive as JSON, so CSS cannot go in a directive.

Fix:
- `scripts/diagram-render/render-config.json` gains a `gantt` block: `mermaid` (`useWidth` 720, `fontSize`/`sectionFontSize` 13, `barHeight` 24, `barGap` 6, `leftPadding` 150, `rightPadding` 40, `axisFormat` `%d %b` default), `axis_font_px` 13, `today_marker_off`, and `theme_variables` mapped to neutral document tokens (task `#F4F4F4`/`#5A5A5A`, critical `#D8D8D8` with an `#1A1A1A` border, active `#F7F7F7`, done white, grid `#D8D8D8`, text `#1A1A1A`; no red).
- `scripts/render_diagrams.py`: `diagram_type()`, `gantt_settings()`, `gantt_min_label_pt()`, `gantt_css()`, `mermaid_config()`. For Gantt blocks the injected directive carries the `gantt` settings and colours (no quotes), the job gets its own `mermaidConfig` (settings, colours, base font CSS plus axis-label size and grid rule CSS), and `todayMarker off` is inserted unless the author set `todayMarker` (a printed plan must not depend on the build date). Other diagram types are unchanged (same directive, same shared config).
- `scripts/diagram-render/render.mjs`: uses `job.mermaidConfig` when present, else the shared config.
- Test: `test_render_gantt_width_colours_and_today_marker` (includes `gantt_min_label_pt(cfg) >= 8.0` and no `'` in the directive).

Design engine (edit limited to the permitted file): `design-system-skills/skills/13-presentations-and-documents/docx-report-and-document-formatting/references/diagram-visual-standards.md` gained **§3a Gantt charts**: role → token table, critical path by darker tint plus heavier border (never colour alone), fixed drawing width, no today line, short axis dates, split or landscape when 8 pt cannot be held. §3 had no Gantt guidance; the brand `Accent` is not defined by the doctrine, so the neutral tint is the default and `Accent` tint is named as the option where a document sets one.

### T06 sample re-render

Copy of `T06-sample-gantt/` source rebuilt with `bash scripts/build-doc.sh <scratch>/implementation Sample_Plan_Timeline` (unchanged Mermaid source; the author's `axisFormat %b %Y` and `tickInterval 1month` are kept). Outputs in `followup-T06-gantt-rerender/`.

| Measure | Before (T06) | After |
|---|---|---|
| SVG viewBox width | 3,984 | 720 (viewBox `0 0 720 280`) |
| PNG | 8,064 × 488 px | 2,160 × 840 px |
| ppi at 6.25 in | 1,290 | 345 (≥ 300) |
| Smallest label printed | 11 px × 450 pt / 3,984 px ≈ 1.2 pt | 13 px × 450 pt / 720 px ≈ 8.1 pt |
| Critical bars | `#d42` red | `#D8D8D8` fill, `#1A1A1A` 2 px border |
| Today line | drawn | off |
| Font check | PASS | PASS (Public Sans) |
| Guard | 0 Mermaid source | 0 Mermaid source; 1 figure matched manifest, 0 missing |

SHA-256: PNG `5404c544ba27bb3c516a49c68ded33a1ba355531e01dccfd9fd25281f6b18089`; SVG `e6adebd7…`; `.docx` `029de22b…`; `figures.json` `1c955f42…`; `render-manifest.json` `c98d8abc…`. Visual check of the PNG: title, both section labels, all six task labels and the four month ticks read clearly; outside-bar labels cross the light grid rules without collision.

## 4. Proposal routing fixture

`proposal-skills/tests/fixtures/routing-fixtures.json`: added `{"id": "technical-approach-figures", "kind": "positive", "prompt": "Write the technical approach and methodology for this ICT tender with a delivery workflow figure", "expected": "skills/pipeline/06-methodology"}` after `methodology`. `quality-baseline.json` `routing_fixture_count` 25 → 26 (the validator fails on a count mismatch).

Result: `PASS technical-approach-figures … top3=skills/meta/kaizen-improvement-system, skills/pipeline/06-methodology, skills/domain-delivery/giz-eu-local-procurement-response`. Ranked 2nd; `kaizen-improvement-system` ranks 1st on this wording (worth a look by the routing owner; not changed here).

## Commands and results

| Repo | Command | Result |
|---|---|---|
| srs-skills (Git Bash) | `python -m pytest` | 432 passed, 2 skipped (pre-existing: `test_doctor` PATH case, empty example set); coverage 96.86 % (≥ 90) |
| srs-skills | `python -m pytest engine/tests/test_diagram_figures.py --no-cov` | 28 passed (renderer and both build-doc tests ran) |
| srs-skills | `python -X utf8 scripts/validate_engine.py` | `ENGINE CONTRACT: PASS`, exit 0 |
| srs-skills | `python -X utf8 scripts/routing_smoke_test.py` | 55/55, top-3 1.000, precision@1 47/55; owned negatives 16 (13 pass, 0 fail, 3 not assessed cross-engine); exit 0 |
| srs-skills | `check_docx_diagrams.py --scan projects --exclude _kaizen,render-runs` | 691 scanned, 0 Mermaid source; 18 matched manifests, all pass; 2 placeholders in GarageFlow UserDocs (above); exit 1 |
| proposal-skills | `routing_smoke_test.py` | 26 fixtures, top-three 100.0 %, exit 0 |
| proposal-skills | `validate_skills.py --baseline quality-baseline.json` | 115 active, 0 findings, exit 0 (after baseline 26) |
| proposal-skills | `proposal_fixture_check.py` / `encoding_link_gate.py` / `unittest discover -s tests` | PASS / 0 findings / 52 tests OK |
| design-system-skills | `python -X utf8 scripts/validate_engine.py` | exit 0 (pre-existing report-only byte warnings only) |

## Open items

- GarageFlow UserDocs: missing screenshot `screenshots/manager-home.png` (source and delivered `.docx` + export copy). Owner decision: supply the screenshot and rebuild, or remove the image line.
- Proposal routing: `kaizen-improvement-system` outranks `06-methodology` for the figure wording (still top three).
- Linux behaviour of `native_path` (no `cygpath`, path unchanged): NOT_ASSESSED (Windows only).
