# M10-10 executor evidence: design data, retrieval runtime and shared metrics

Executor scope: M10-10 T01–T09, T10 (runtime half) in `design-system-skills`, and T08 (UX-09) in
`chwezi-engine-agents`. The reference-document tasks (T10 reference, T11, T12 design side, T13, T14,
T15) were done by a forked executor; see `M10-10-references-evidence.md` in this folder.
Date: 29 September 2026. No git state was changed; all edits are unstaged.

Pre-existing dirty files at phase start: `pre-dirty-design.txt` (design tree was clean) and
`pre-dirty-agents.txt` (engine-agents had other executors' files; none were touched). Design
`AGENTS.md` shows as modified during this run: that is the M10-12 executor's edit, not this one.

## Summary of results

| Measure | Baseline | After |
|---|---|---|
| Catalogue records | 13 (all `original_synthesis`) | 66 (28 typography pairings, 6 palettes, 19 WCAG A/AA, 13 original) |
| Records with a citation | 0 | 53 |
| Banned or watchlisted faces in the catalogue | not checked | 0 (lint-enforced, read from the doctrine JSON) |
| Palette contrast failures | not checked | 0 of 56 computed pairs (light and dark) |
| Ranking | token overlap | BM25 (k1 1.5, b 0.75; tags x3, title x2, content x1) with calibrated abstention |
| Skills that name `design_query.py` | 0 | 4 |
| Held-out relevance (n = 16) | not measured | P@1 1.000, MRR@3 1.000, nDCG@3 0.968, negative abstention 1.000, typo recovery@3 1.000 |
| Mode enum | `{app, marketing}` | `{persuade, operate, read, experience}` with legacy aliases |

## T08 (UX-09): shared retrieval metrics — DONE

- Checked M10-03 first. `chwezi-engine-agents/scripts/lexical_routing.py` is a TF-IDF skill-routing
  index. It has no P@k, MRR, nDCG, abstention or BM25 code, and no other ranking-metric helper
  exists (`grep -rn "bm25|ndcg|reciprocal_rank|precision_at"` over engine-agents found nothing).
  So this task created the module, as the phase allows. The module header explains how it relates
  to `lexical_routing.py`, so the two are not duplicates.
- Added `scripts/lib/retrieval_metrics.py` (standard library only), which provides:
  - `precision_at_k`, `reciprocal_rank`, `mrr_at_k`, `dcg_at_k`, `ndcg_at_k` (graded), `abstention_rate`, `typo_recovery_at_k` and `mean`;
  - a `BM25` class with field boosts;
  - the vendoring rule in the header.
- Added `tests/test_retrieval_metrics.py`, where every metric is checked against at least 2 cases computed by hand.
- Vendored copy: `design-system-skills/engine/design_engine/retrieval_metrics.py`.
  - Header: `# vendored-from: chwezi-engine-agents@pending-M10-10-commit sha256:1829b5880310685e7ed8dd66673c6b1b01df7bfeb6cb8b7118e81f5ef3d9dd93`.
  - The hash is taken over the canonical file with line endings normalised to LF, so Git's autocrlf setting cannot change it.
  - The design harness and a pytest case both check that the file body matches the header hash.
- Command: `python -X utf8 -m pytest -q tests/test_retrieval_metrics.py` gave **12 passed**.
- Open item: once engine-agents is committed, replace `pending-M10-10-commit` in the design copy's header with the commit SHA. Changing only the header does not change the body hash.

## T01 (UX-01): doctrine lint — DONE

- `Catalog._validate` now calls `_lint_fonts`. Ban data comes from `doctrine/references/ai-slop-banned-fonts.json` every time a catalogue loads:
  - `hardBan`, `secondaryBan`, `monospaceBanned`, `hardBanFamilyPrefixes` and `conditionalPrimaryOnly`;
  - `watchlist`, treated as pending and therefore not usable.
- Slot rules for typography and google-fonts records:
  - A record with pairing slots needs `heading`, `body`, `group` and `use_case`, plus a record-level `licence`.
  - A record without slots must declare `content.kind: "guidance"`. The two existing records were marked this way.
  - Source Sans is allowed only in the `body` slot.
  - Group 07 records must state "never body" in `content.rules`.
- Any other field that names a banned family fails, unless that field is `must_not` or `avoid`.
- The matcher is a Python port of `hooks/lib/font-matcher.js` `bannedEntry`, checking in the same order: hard, prefix, secondary, mono.
- Shared vectors live in `tests/fixtures/font-matcher-vectors.json` (19 rows). They are consumed by:
  - the new Node test `tools/slop-detector/test/font-matcher-vectors.test.mjs`;
  - the pytest case `test_shared_font_matcher_vectors_match_python_lint`.
- Results:
  - `validate_design_catalog.py tests/fixtures/catalog/banned-heading.json` exits **1**: `FAIL: type-fixture-banned-heading: content.heading 'Inter' is banned by doctrine (hard)`.
  - A Source Sans 3 body under Spectral passes (pytest).
  - Heading "IBM Plex Sans Condensed" fails (exact hard-ban entry), and "IBM Plex Math" fails through the prefix (pytest).
  - A watchlisted heading fails (pytest).
- Deviation from the plan text: the phase says the watchlist is read from the M10-09 refresh record's machine table. M10-09 put that table into the JSON sidecar's `watchlist` array (7 entries), so the lint reads it from there. Nothing is hardcoded.

## T02 (UX-02): typography records — DONE (Peter to ratify the face list)

- There are 28 records, with at least 3 in each group from 01 to 08 (01:4, 02:4, 03:3, 04:4, 05:3, 06:3, 07:4, 08:3).
- Every record meets these conditions:
  - `evidence.source_type` is `human_authority`;
  - the citation is non-empty and names a `pairing-catalog.md` pairing ID or row, a `pairing-principles.md` core-move number (with the Bonneville principle numbers), or a `font-groups-and-usage.md` quick-chooser row;
  - `reviewed` is 2026-09-29 and `recheck_due` is 2027-09-29.
- Faces used (all pass the lint; none is banned or watchlisted):
  - Source Serif 4, Public Sans, Spectral, Libre Baskerville;
  - Andada Pro, Libre Caslon Text, Theano Didot, Alegreya, Alegreya Sans;
  - Bricolage Grotesque, Hanken Grotesk, Cabinet Grotesk, JetBrains Mono, Unbounded;
  - Atkinson Hyperlegible, Lexend, Bodoni Moda, Eczar;
  - Great Vibes, Caveat, Kalam, Sacramento (accent slot only).
- Faces excluded on purpose:
  - Syne (catalogue pairing A1 and the campaign default): on the watchlist.
  - Clash Display and Satoshi (P2): the phase's licence field allows OFL or SummitSoft only.
- Licences: OFL-1.1, except Cabinet Grotesk, which uses the ITF Free Font License (Fontshare): embedding is allowed, raw redistribution is not. That is recorded truthfully. No `fonts/` premium (SummitSoft) face was needed.
- The group 08 records adapt the pairing-catalog "workhorse" rows with a specific display face, because those rows have no pairing IDs:
  - Libre Baskerville over Public Sans;
  - Spectral over Atkinson Hyperlegible;
  - Andada Pro over Public Sans.
  These three are the newest combinations; Peter should check them first when he ratifies.
- No external specimen URLs were cited, so no DRE pass was needed for T02. Every citation points to an engine reference that already cites Bonneville, Segall or Vignelli.
- Checks:
  - `search "statutory report typography" --domain typography` returns `type-01-source-serif-public-sans` first.
  - `search "dashboard typography"` returns `type-04-public-sans-tabular-mono` first.

## T03 (UX-04): palette schema and contrast — DONE

- `content.tokens` must supply these pairs, and may carry a `dark` override block:
  - text pairs, at 4.5:1 or more: primary/on_primary, secondary/on_secondary, surface/on_surface, background/foreground, muted/on_muted, destructive/on_destructive;
  - non-text pairs, at 3:1 or more: border against surface, ring against background.
- Contrast uses WCAG 2.2 relative luminance (the sRGB threshold is 0.04045), computed with the standard library. The validator prints every ratio.
- An advisory list of framework-default hexes gives an AS1 WARN and never fails a record: Tailwind blue-500/600, indigo-500/600, violet-500/600, Bootstrap 5 primary and Material 2 baseline primary.
- Six palette records were added, each citing its source:
  - Maduuka institutional, light and dark, from `design-tokens-and-naming/examples/tokens.json`. The OKLCH primitives were converted to sRGB hex by a script.
  - KesiLex green, from `_themes.kesilex`.
  - Four monochrome ramps (forest, terracotta, ochre, ink) from `color-selection/scripts/palette_generator.py`, seeded with Maduuka primitives.
- Findings recorded in the records:
  - The source's `border.default` (neutral.300) is decorative, at about 1.4:1, so `border.strong` is used.
  - KesiLex `green.500` with neutral.0 falls below 4.5:1, so `green.700` is used.
  - In the dark theme, destructive is red.700 with neutral.0 (7.04:1). The source's red.500 with neutral.950 computed 4.04:1.
  - The generator's `semantic_palette()` returns Tailwind default hexes, so it was not used. Only its `monochromatic`/`complementary` outputs were.
- Checks:
  - `low-contrast-palette.json` exits **1** with `contrast on_primary/primary (light) is 3.45:1, below 4.5:1`.
  - pytest asserts 3.45, which was worked by hand: L(#8A8A8A) = 0.254120, and 1.05 / 0.304120 = 3.4526.
  - All 56 shipped pairs pass. The lowest is 4.59:1, for border against surface.

## T04 (UX-08): lifecycle — DONE

- `replacement_id` is required on a deprecated record and must resolve to an active record. It is rejected on any record that is not deprecated.
- `recheck_due` is taken from `evidence.recheck_due` when present. Otherwise the policy default applies: reviewed + 365 days for human authority, + 90 days for original synthesis.
- The validator gained `--as-of YYYY-MM-DD` and prints `WARN stale: <id> recheck_due <date>`.
- `style-legacy-flat.replacement_id` is `style-feature-first-hierarchy`. `search(..., include_deprecated=True)` returns `successor`.
- Checks:
  - pytest covers a missing or unresolvable replacement.
  - `--as-of 2027-12-01` printed 66 WARN lines. The 13 original records fall due on 2026-12-19; the new records on 2026-12-28 or 2027-09-29.
  - `--as-of 2026-09-30` prints none.

## T05 (UX-05): BM25 and calibration — DONE_WITH_LIMITATIONS

- `Catalog.search` and `Catalog.route` now use the vendored `BM25` (k1 1.5, b 0.75; boosts tags 3, title 2, content 1). Content is indexed by value, not by key.
- The index is cached per (source, revision, record count).
- Typo recovery maps an unknown query token (4 or more characters) to the closest vocabulary token using `difflib`, with cutoff 0.82.
- The output adds `calibration_version`, plus per-result `score` and `coverage`. The existing strict abstention still works; "quantum telescope" with `--strict` exits 2 with `abstained: true`.
- `data/retrieval-calibration.json` (`2026-10-v1`) was fitted only on the calibration split, by `tests/eval_catalog_relevance.py --calibrate`:
  - The coverage minimum is 0.34 (the phase default).
  - Every per-domain floor fitted to **0.0**. With the coverage minimum alone, calibration negative abstention was already 1.00, and unfloored it was 0.50. The fitting rule picks the lowest floors that meet the target, so every floor is zero.
  - The floors mechanism works and is tested, but no floor does any work at present. That is the limitation.
- `test_design_engine_runtime.py` passes. One original assertion had to change: `len(records) == 13` became `>= 60`, because T02, T03 and T09 add records by design. The other 8 original tests pass unchanged.
- `design_query.py search "dashboard"` output contains `calibration_version`.
- `decisions.py` no longer raises when one domain abstains. It records `abstained_domains` and prints ABSTAINED in Markdown. This is what T07's persist refusal depends on.

## T06 (UX-06): relevance harness — DONE_WITH_LIMITATIONS

- `tests/eval_catalog_relevance.py` has 40 cases in `tests/fixtures/catalog-relevance/cases.json`:
  - 24 calibration and 16 held-out (60 % / 40 %);
  - 11 negative, 5 typo, and 24 graded positive.
  - Held-out cases carry `inspect_for_tuning: false`.
- Metrics come from the vendored shared module.
- `baseline.json` stores the floors plus LF-normalised SHA-256 fingerprints of the catalogue, the calibration file, `catalog.py` and `cases.json`.
  - It is labelled "provisional regression gate".
  - Floors are the first held-out values minus 0.02, rounded down: P@1 0.98, MRR@3 0.98, nDCG@3 0.94, negative abstention 0.98, typo recovery@3 0.98.
- Results (`relevance-run.txt`, `relevance-metrics.json`):
  - calibration: P@1 1.000, MRR@3 1.000, nDCG@3 0.907, negative abstention 1.000, typo recovery@3 1.000;
  - held-out: P@1 1.000, MRR@3 1.000, nDCG@3 0.968, negative abstention 1.000, typo recovery@3 1.000;
  - **PASS**.
- Fingerprint check: appending one space to `design-catalog.json` gave `FAIL: fingerprint mismatch for ['data/design-catalog.json']` (exit 2). The file was then restored from a backup.
- Limitations:
  - The cases were judged by the same executor who wrote the records, so the perfect scores reflect author-set queries.
  - The second-reviewer re-judgement is **open**. The baseline is a regression gate only, not a quality target.

## T07 (UX-03): `scripts/design_query.py` and skill wiring — DONE

- The CLI has three subcommands:
  - `search`, which prints JSON and exits 2 when `--strict` abstains;
  - `design-system --brief`, which prints JSON and/or Markdown;
  - `persist`, which refuses a decision with any abstained domain (exit 3, nothing written) unless `--accept-abstention "<who>: <reason>"` is given. The accepted abstention is recorded in the saved file.
- A "Catalogue query" subsection was added under Workflow in four skills. It carries the paraphrased query contract (one dominant intent, 2–5 terms, retry once with a synonym, never persist unverified output). Descriptions are unchanged. The four skills:
  - `font-selection-and-pairing`;
  - `color-system-and-palette`;
  - `design-tokens-and-naming`;
  - `design-engine-and-product-improvement`.
- Checks:
  - `grep -l design_query.py skills/*/*/SKILL.md` returns 4 files.
  - `python scripts/design_query.py search "dashboard typography"` (without `-X utf8`) exits 0 with JSON.
  - Routing smoke without flags is identical before and after, byte for byte (`routing-smoke-before.txt` against `routing-smoke-after-noflags.txt`): precision@1 94 %, precision@3 100 %, owned negatives 21/21.
  - With the CI flags `--min-rank1 92 --lint-fixtures` it passes, with 0 fixture-lint findings.
  - `validate_engine.py --baseline` passes: 101/101 skills.

## T09 (UX-07): WCAG records and the pre-launch checklist — DONE

- 19 `ux` records, one for each A or AA success criterion named in `doctrine/references/wcag-2.2-criteria.md`:
  - 1.1.1, 1.4.3, 1.4.4, 1.4.10, 1.4.11, 1.4.12, 1.4.13;
  - 2.1.1, 2.2.2, 2.3.1, 2.4.3, 2.4.7, 2.4.11, 2.5.7, 2.5.8;
  - 3.2.6, 3.3.7, 3.3.8, 4.1.2.
- Excluded:
  - AAA criteria: 2.3.3, 2.4.12, 2.4.13, 3.3.9;
  - 4.1.1, which the file notes as obsolete;
  - "3.3.x", which is not a single criterion and was not invented.
- Each record has `sc`, `level`, `platform`, `do`, `dont`, `severity`, `code_good`, `code_bad` and `doctrine_ref`. The levels follow the W3C WCAG 2.2 Recommendation.
- `pre-launch-qa-checklist.md` Gate B gained a "Code-level checks" table (Check, SC, Platform, Good, Bad) with 15 code-checkable rows. The file grew from 156 to 181 lines.
- Checks:
  - A pytest cross-check parses the doctrine file and asserts exactly one record per A/AA criterion.
  - `search "target size" --domain ux` returns `ux-wcag-2-5-8` first, with the 24x24 CSS px rule and the 44x44 pt iOS / 48x48 dp Android note.

## T10 (IM-10): runtime half — DONE

- `decisions.py`:
  - `MODES = persuade, operate, read, experience`;
  - `app` maps to `operate` and `marketing` to `persuade`;
  - the brief carries `mode` and, only when a legacy value was given, `mode_alias_from`;
  - an unknown mode raises `DecisionError`;
  - the default is now `operate` (previously `app`, the same meaning).
- `persistence.load_project` normalises at read time and never rewrites the stored file.
- Checks:
  - 6 parametrised pytest cases cover app, marketing, persuade, operate, read and experience; an unknown mode is rejected.
  - A fixture project saved with `"mode": "marketing"` loads as `persuade` with `mode_alias_from: "marketing"`, and its bytes are unchanged.
  - The reference half is in the references evidence file.

## Full verification run (design-system-skills)

| Command | Result |
|---|---|
| `validate_engine.py --baseline tests/quality-baseline.json` | PASS: 101/101; 6 report-only byte warnings, the same set as before |
| `routing_smoke_test.py` (and with `--min-rank1 92 --lint-fixtures`) | PASS; output identical before and after |
| `validate_route_existence.py` | PASS, 0 findings |
| `validate_design_catalog.py data/design-catalog.json` | PASS, 66 records, 56 contrast pairs printed |
| `... --as-of 2027-12-01` | PASS with 66 stale warnings |
| `... banned-heading.json` / `... low-contrast-palette.json` | exit 1 / exit 1, as expected |
| `tests/eval_catalog_relevance.py` | PASS (numbers above) |
| `python -X utf8 -m pytest -q -p no:cacheprovider` | 139 passed |
| `design_query.py search` (four phase queries) | see `design-query-outputs.txt`; strict "quantum telescope" exits 2 and abstains |
| `node --test tools/slop-detector/test/` | 117 tests: 116 pass, 1 skipped, 0 fail |
| `node tools/slop-detector/cli.mjs --validate-registry`; `node hooks/test-banned-font-gate.js` | PASS; 45/45 |
| engine-agents `pytest tests/test_retrieval_metrics.py` | 12 passed |
| dev engine F13 schema validation | NOT_ASSESSED: outside this executor's repo scope (see open items) |

## Decisions taken under delegated authority (orchestrator, for Peter, 29 September 2026)

- Watchlisted faces count as "pending", so no catalogue record may encode them. Syne pairings are therefore excluded.
- Only the Cabinet Grotesk record uses a non-OFL licence, and it is labelled truthfully. The Fontshare P2 pairing was left out.
- The coverage minimum was kept at the phase default, 0.34. The per-domain floors fitted to 0.
- The pre-launch checklist platform and code pairs were added as a single table in Gate B, rather than as new columns in every checklist row. The perennial rows are checkbox lists, not table rows.

## Open items

1. **Dev engine F13 note (part of T12), not done.** It is outside this executor's scope. Proposed change: in `C:\wamp64\www\chwezi-dev-engine\benchmarks\solution-selection\fixtures.json`, on fixture F13, add `"acceptance_notes": ["Design-side evidence: design-system-skills/skills/00-cross-cutting-ops-qa-a11y/accessibility-wcag-2-2-compliance/references/native-control-sufficiency.md"]` without changing the oracles. Then run the schema validation named in `docs/updates/2026-09-20-solution-selection-implementation.md`.
2. Replace `pending-M10-10-commit` in the vendored header with the engine-agents commit SHA once that commit exists.
3. A second reviewer should re-judge the relevance cases. Until then the floors remain provisional.
4. Peter ratifies: the typography faces and pairings (28 records; the three group 08 combinations are the newest), the six palettes, and the visitor-modes and native-control doctrine.
5. `data/design-catalog.json` was re-serialised with `json.dumps(indent=2)`, so the diff also reformats the 13 original records. Their content is unchanged apart from `kind: guidance` on two records and `replacement_id` on one.
