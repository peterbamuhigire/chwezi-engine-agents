# M10-10 — reference-document tasks: executor evidence

Scope: T10 (reference half), T11, T12 (design half), T13, T14, T15 in
`C:/wamp64/www/design-system-skills`. Code and data tasks (T01–T09, T10 runtime half) are recorded
in the parent executor's evidence file. Executed 29 September 2026. No git state changes.

## T10 (reference half) — DONE
- Added `doctrine/references/visitor-modes.md`: Persuade, Operate, Read, Experience; per surface,
  not per project; Chwezi worked examples (SRS portal, client website, dashboard product, campaign
  microsite); font **categories** only (Operate/Read: 04 or 08, never a bare system stack;
  Persuade/Experience: 03 or 06); density, motion and colour posture; runtime enum and legacy
  aliases (`app → operate`, `marketing → persuade`, `mode_alias_from`).
- Detector mapping stated honestly: all 49 rules in `tools/slop-detector/rules/registry.json` list
  all four modes, so no rule relaxes or tightens by mode today; the per-mode table is reviewer
  posture only. All rule IDs named were checked against the registry.
- Linked from `skills/14-conversion-and-web-page-patterns/landing-page-and-conversion-design/SKILL.md`
  and `skills/12-data-viz-and-dashboards/dashboard-and-data-product-design/SKILL.md` (one line
  each, References section; descriptions unchanged).
- Attribution: Impeccable (Apache-2.0, commit 114ea1d), framing only.

## T11 — DONE
- Added `skills/00-cross-cutting-ops-qa-a11y/design-critique-and-review-facilitation/references/refinement-verbs.md`:
  ten verbs, each with scope rule, reading per visitor mode, done-check and hand-off to `polish`;
  `colorize` accepted as command token for `colourise`; the `polish` done-check carries the
  paraphrase that a detector finding is defect evidence and a clean run is not proof of quality,
  pointing to `tools/slop-detector`. DOCX/PPTX review-comment section (Chwezi-original) with a
  ten-row table and three rules. Linked from the skill's References section.

## T12 (design half) — DONE; dev-engine F13 note NOT DONE (out of this executor's repo scope)
- Added `skills/00-cross-cutting-ops-qa-a11y/accessibility-wcag-2-2-compliance/references/native-control-sufficiency.md`:
  three-part approval rule (failed user task, AT test result recorded as MEASURED, design-system
  reason); date, color, file, dialog, details/summary, popover entries; memorable-date rule; F13
  counterexample (range + explained blackout dates); "not a universal rule" framing. Linked from
  SKILL.md References.
- Open item: the `acceptance_notes` reference on fixture F13 in
  `chwezi-dev-engine/benchmarks/solution-selection/fixtures.json` is not made here; the
  orchestrator should assign it.

## T13 — DONE
- Added `skills/12-data-viz-and-dashboards/data-visualization/references/relationship-diagrams-that-teach.md`:
  ten recommendations, each with a human-authority citation; Understand Anything appears only in
  the "why this matters" line as evidence of the problem.
- `data-visualization/SKILL.md`: one line added to References; 486 → 487 lines (cap 500).
- Reviewer grep: no AI-vendor or AI-tool source is cited as authority in the file.

## T14 — DONE
- `skills/09-design-systems-tokens-and-theming/measured-style-pack/SKILL.md`: added "Capture
  budget" and "Element-scope mode" subsections under Workflow, with attribution to anydesign
  (MIT, commit d81bd89 — retrieved from the GitHub API on 29 September 2026; latest commit
  d81bd8957a21c2d7fba8d2a8f4f60050d09368b5, "Release v0.6.0: token budget", licence SPDX MIT).
- `scripts/hedge-word-lint.js` path confirmed present.
- File trimmed to 20,419 bytes (273 lines) so it stays under the 20,480-byte report-only warning.

## T15 — DONE
- `THIRD_PARTY_NOTICES.md`: new section "M10-10 adoptions" with UI UX Pro Max (09170ee),
  Impeccable (114ea1d), Ponytail (e3ba2aa), Understand Anything (b05cc3b) and anydesign (d81bd89).
  `grep -c "09170ee\|114ea1d\|e3ba2aa\|b05cc3b" THIRD_PARTY_NOTICES.md` = **6** (≥ 4).
- `docs/continuous-improvement/design-catalog-provenance-2026-09-29.md`: appended a dated entry
  (the record's own rule: changes are new dated entries) noting the M10-10 idea adoptions; the
  "undetermined, attributed defensively" position is unchanged.
- Note: the UUPM line names `data/retrieval-calibration.json`, `tests/eval_catalog_relevance.py`
  and `scripts/design_query.py`, which the parent executor creates in T05–T07.

## DRE source evaluation (digital-research-engine `source-evaluation` credibility ladder)

| Claim used | Source | Tier | Confidence | Accessed (UTC) |
|---|---|---|---|---|
| Date input is for dates users know or can look up without a calendar | GOV.UK Design System, Date input, https://design-system.service.gov.uk/components/date-input/ | 1 (primary, government design standard) | high | 2026-09-29 |
| Ask for memorable dates with date input; calendar controls for near-future/recent-past or day-of-week needs; never JS-only calendar | GOV.UK Design System, Dates pattern, https://design-system.service.gov.uk/patterns/dates/ | 1 | high | 2026-09-29 |
| Date input: locale display, `yyyy-mm-dd` value, min/max/step, no per-date disabling, limited styling | MDN, https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/input/date | 2 (authoritative reference) | high | 2026-09-29 |
| Popover: top layer, light dismiss, non-modal; use dialog for modal | MDN, https://developer.mozilla.org/en-US/docs/Web/API/Popover_API | 2 | high (Baseline year not stated in the reference; summary tool reported 2025, unconfirmed) | 2026-09-29 |
| dialog/details behaviour | WHATWG HTML Living Standard (well-established; not re-fetched) | 1 | medium-high | 2026-09-29 |
| Layered drawing reduces crossings with ordered levels | Sugiyama, Tagawa, Toda 1981, IEEE TSMC 11(2):109–125, doi:10.1109/TSMC.1981.4308636 (Semantic Scholar record) | 2 (peer-reviewed) | high | 2026-09-29 |
| Node-link readability drops from ~50 nodes; matrices stay legible; node-link better only for path finding | Ghoniem, Fekete, Castagliola, IEEE InfoVis 2004 (ACM DL / LISN records) | 2 | high | 2026-09-29 |
| Overview first, zoom and filter, details on demand | Shneiderman 1996, IEEE Symposium on Visual Languages (dblp, ACM DL) | 2 | high | 2026-09-29 |
| Network idioms: node-link, adjacency matrix, containment; reduce idioms | Munzner 2014, A K Peters / CRC Press (publisher and course records) | 2 (scholarly book) | high | 2026-09-29 |
| Reorderable matrix, networks as a graphic class | Bertin, *Semiology of Graphics*, UW Press 1983 (French 1967; Esri Press 2010) | 2 | medium (edition facts verified; matrix-reordering content from established knowledge, not re-read) | 2026-09-29 |
| Layering and separation; small multiples | Tufte, *Envisioning Information*, Graphics Press 1990 (chapter titles verified) | 2 | high | 2026-09-29 |
| Integrating words and images | Tufte, *Beautiful Evidence*, Graphics Press 2006 | 2 | medium (not re-fetched) | 2026-09-29 |
| Gestalt grouping (proximity, connectedness, common region) | Ware, *Information Visualization: Perception for Design*, 4th ed., Morgan Kaufmann 2020 (Elsevier listing) | 2 | high | 2026-09-29 |
| anydesign commit and licence | GitHub API, repos/uxKero/anydesign | 1 | high | 2026-09-29 |

Verification trail: credibility ladder only (no Burke/Tudor audit needed for standards and
scholarly references). No AI-tool source supports any recommendation.

## Commands and results (design-system-skills)

- `python -X utf8 scripts/validate_engine.py --baseline tests/quality-baseline.json` → exit 0;
  `skills=101 fully_compliant=101`; 6 report-only byte warnings (same count as the pre-change run).
- `python -X utf8 scripts/validate_route_existence.py` → `PASS`, findings 0.
- `python -X utf8 scripts/routing_smoke_test.py --min-rank1 92 --lint-fixtures` (sanity only;
  final before/after diff is the parent's) → `precision@1=94% precision@3=100%
  owned_negatives=21/21`, fixture lint 0 findings. Unchanged from the pre-change run.
- Banned/watchlisted font scan (names read from `ai-slop-banned-fonts.json`: hardBan, prefixes,
  secondaryBan, monospaceBanned, watchlist) over the four new references and the edited
  measured-style-pack SKILL.md → 0 hits.

## Decisions under delegated authority
- Capture budget and element scope placed as `###` subsections under Workflow (not new `##`
  sections) to keep the skill's section contract intact.
- T15 attribution written to both `THIRD_PARTY_NOTICES.md` (acceptance target) and, as a dated
  entry, to the UX-15 provenance record.

## Open items
- Dev-engine F13 `acceptance_notes` (T12 second half) — assign to an executor with dev-engine scope.
- Doctrine-class ratification by Peter: visitor-modes reference and native-control approval rule.
