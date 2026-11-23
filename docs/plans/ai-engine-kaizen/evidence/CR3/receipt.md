# CR3 README release evidence

**Criterion:** AC-CR3

**Tested README revision:** `b9005a848a87d530ec260a869f187f6fb3020304`

**Date/platform:** 2026-11-23, Windows local disposable checkout; Python and pytest available.

**Scope:** README and docs in the `ai-kaizen-readme` worktree. No sibling repository, external provider, host plugin installation, push or publication was included.

## Checks

- `python -B -X utf8 scripts/readme_metrics.py --check README.md` — exit 0. Metrics: 8,327 words; 25 H2 headings; one contents list; first command at line 20; longest section 1,289 words; 16 long lines; maximum line length 481; mean sentence length 12.6; Flesch reading ease 56; 229 bullets; 118 table rows. Configured limits met.
- `python -B -X utf8 scripts/check_readme_preservation.py . e9adbe7ca9de9c6c238999067f932b79a6c4d7d5 b9005a848a87d530ec260a869f187f6fb3020304` — exit 0. Of 81 prior links, 0 lost; all 59 commands retained; 5 tracked inbound heading links and 24 in-page anchors resolve.
- Local Markdown link review — 159 local targets; files and directory destinations resolved; no missing targets or heading fragments. The route/link review distinguishes an unavailable directory target from a file.
- `python -B -X utf8 scripts/validate-contracts.py --schema schemas/handoff.schema.json --instance tests/fixtures/valid-handoff.yaml` — `PASS` on the documented ordinary-handoff fixture. This is shape validation, not evidence acceptance.
- `evals/runners/run-contract-evals.py --route-oracles` — 77/77 fixture oracles passed, process exit 1 because eleven sibling engines were unavailable. Live route behavior is `NOT ASSESSED`; the non-AI IFRS example remains explicitly a proxy.
- Disposable quick-start checkout at the tested README revision `b9005a848a87d530ec260a869f187f6fb3020304`: `python -B -X utf8 -m pytest -p no:cacheprovider tests -q` — exit 0; 377 passed, 6 skipped, 24 subtests passed, 50 deprecation warnings. The tests ran in 161.95 seconds.
- In the same disposable checkout, `scripts/render_host_files.py --check --engines-root <empty-engines>` — exit 1: one missing canonical shared design trigger block and eleven sibling engines `NOT_ASSESSED`. This is the expected limitation of a standalone checkout without sibling engines, not a passing drift check.
- Native `python -B auto-agents/plan_contract.py docs/plans/ai-engine-kaizen/readme.contract.json --root .` currently reports the task metadata structurally valid and all three criteria pending. Final completion metadata is committed with this receipt and rerun before Jidoka recovery.

## Independent first-use result

The owner reports that an independent reader used the README task table, replayed `evals/cases/replay_ai_journeys.py`, and accepted the classifier and coding journeys. The reader also ran the documented schema-validation example on `tests/fixtures/valid-handoff.yaml` and observed `PASS`. The walkthrough is in [CR2](../CR2/walkthrough.md); case requirements and expected results are recorded in the [casebook](../../casebook.md).

**Output record:** This receipt summarizes stdout from the commands above; no separate machine report was retained. Fixture digests are in the [CR1 inventory](../CR1/claim-inventory.md) and [CR2 walkthrough](../CR2/walkthrough.md).

## Limitations

The quick-start pytest result is local synthetic/repository coverage, not hosted or production evidence. The drift check cannot assess shared assets or routes owned by missing sibling engines. The route-oracle exit 1 remains a limitation even though all local fixture oracles passed. Deprecation warnings are recorded, not suppressed. No public result reproduces private Development packets or runtime details.
