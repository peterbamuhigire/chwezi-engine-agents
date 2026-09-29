# M10-05 evidence — Behavioural evaluation (Tier 3) and benchmark execution

Executor scope: all tasks of M10-05 (T01–T15). Date: 29 Sep 2026. Zero-spend rule applied
throughout: no `claude -p`, no `claude plugin eval`, no API call; `--allow-model-calls` was never
passed. The only `claude` invocation was `claude --version` (2.1.284). No git state was changed;
all edits are unstaged.

Run report (T13 template applied): `M10-05-tier3-run-report-2026-09-29.md`.
Machine-readable outputs: `runs/` (dry-run plans and `solution_evidence` files per suite) and
`command-output/`.

## Per-task status

### T01 — Tier-3 runner (DONE)

- Files: `scripts/run_behavioural_eval.py` (new); `.gitignore` (+ `evals/behavioural/results/`);
  `evals/behavioural/README.md`.
- Implements: temp git workspace (`mkdtemp`, traversal-guarded copy, fixed identity
  `eval <eval@invalid>`, `core.autocrlf false`, "fixture baseline" commit, optional
  `.eval/working-tree.patch`, `.eval` removed, workspace deleted in `finally`); arm commands
  (`--setting-sources project,local --strict-mcp-config`, exactly one `--plugin-dir` to a
  `git archive` snapshot for the engine arm, `--append-system-prompt` for short_prompt; prompt on
  stdin); 15-minute executor and 5-minute grader timeouts; stream-json parsing (executor model from
  `system/init`, cost from the result event or `null`, turns); deterministic checker first, then a
  separate no-plugin, no-tool grader with the trace fenced as untrusted; id-bound grading
  validation (first JSON object, exactly n, integer ids 1..n, no duplicates, text rewritten,
  counters recomputed, invalid output saved as `*.grading.raw.txt` and counted FAIL); pinned-model
  and mixed-model refusal; `NOT_ASSESSED` for a missing binary, authentication, quota, an unknown
  flag or a timeout; `solution_evidence` schema_version 1 output. Modes: `--dry-run`, `--selftest`,
  `--selftest-isolation`, `--micro`, `--plugin-eval`, `--validate-grading`. Execution is refused
  (exit 3, `REFUSED`) without `--allow-model-calls`. Printed artefacts redact local path prefixes.
- Header carries the attribution to addyosmani/agent-skills (MIT, commit 2686b62) and
  DietrichGebert/ponytail (MIT, commit e3ba2aa); paraphrased, no code copied.
- Commands:
  - `python -X utf8 scripts/run_behavioural_eval.py --suite solution-selection --dry-run` → "16 cases
    x 3 arms x n=3 = 144 cell plans; model calls 0; cost 0".
  - `python -m pytest -q tests/test_run_behavioural_eval.py` → 34 passed. Covers: duplicate id,
    missing id, wrong counter, boolean id and string `passed` rejected; traversal paths rejected;
    missing `claude` binary → `NOT_ASSESSED`; no process starts without permission; refusal exit 3;
    `--no-publish` enforced; reproducible workspace commit and dirty-tree patch; an end-to-end cell
    through a local fake `claude` that prints SYNTHETIC stream-json (no model).
  - `python -m pytest -q tests` (whole agents suite) → 153 passed.
  - `python -X utf8 scripts/run_behavioural_eval.py --selftest` → PASS 32/32, `model_calls: 0`.
- Limitation: the grader's no-tools flag (`--allowedTools ""`), the `Bash(python:*)` pattern syntax
  and the stream-json field names are recorded as "verify on the day of execution"; an unknown shape
  makes a cell `NOT_ASSESSED`.

### T02 — Arm isolation self-test (DONE_WITH_LIMITATIONS)

- Design and detector built; live smoke `NOT_ASSESSED (zero-spend rule)`.
- `python -X utf8 scripts/run_behavioural_eval.py --selftest-isolation` → static checks PASS (baseline
  and short_prompt carry no `--plugin-dir`; engine carries exactly one, pointing at a snapshot, not
  the live checkout; both control arms refuse a plugin), detector checks PASS on 7 SYNTHETIC
  `system/init` samples (clean baseline PASS; user plugin in baseline FAIL; routing-table leak FAIL;
  user-level `CLAUDE.md` in memory FAIL; engine with one plugin PASS; engine with two plugins FAIL;
  missing `plugins` field `NOT_ASSESSED`), live smoke `NOT_ASSESSED (zero-spend rule)`,
  `paid_runs_permitted: false`. Hash `83a06771f3fda7be998cfb0c4045db58fb14c63239a79d367bfc73f8231dea2d`.
  Output: `command-output/selftest-isolation.json`.
- The rule is empirical: paid runs are permitted only when the live smoke passes; any contamination
  aborts. Whether `--setting-sources project,local` excludes the user-level `CLAUDE.md` and
  Superpowers remains unverified until a live run; the probe prompt asks the arm to report the
  phrase "Engine routing table".

### T03 — `short_prompt` field (DONE)

- Files: dev `benchmarks/solution-selection/fixtures.json` (16 `short_prompt` values);
  `tools/validate_benchmark_fixtures.py` (required on fixtures and pressure scenarios);
  `tests/test_benchmark_fixtures.py` (+3 tests).
- `python -X utf8 tools/validate_benchmark_fixtures.py` → PASS (16 fixtures, 7 pressure scenarios,
  no warnings). New tests show a fixture or scenario without `short_prompt` fails.
- Limitation: written from the title and public task, but by an author who had read the oracles.

### T04 — Materialise F02, F07, F08, F12, F13, F14 (DONE)
### T05 — Materialise the remaining ten (DONE)

- Files: dev `benchmarks/solution-selection/materialised/` — `fixture_kit.py` (compose, deterministic
  baseline commit, hidden-manifest hash, `stamp`), `run_selftests.py`, `conftest.py` (keeps a bare
  root `pytest` from collecting fixture code), and `F01/`–`F16/` each with `fixture.json`, `starter/`,
  `public_tests/`, `checker.py` (stdlib only; runs produced code in subprocesses against adversarial
  input), `reference_good/`, `reference_bad/`. `fixtures.json`: 16 × `MATERIALISED`,
  `initial_commit`, `hidden_manifest_hash`, `materialised_path`; top-level status
  `MATERIALISED_NOT_EXECUTED`. Validator extended: `MATERIALISED` requires a 40-hex commit, a 64-hex
  hash and a complete folder; `--verify-commits` recomputes each commit.
- Withheld tests: 20 files in `chwezi-dev-engine/benchmarks-private/solution-selection/Fxx/`, local
  only; the folder's own `.gitignore` (`*`) excludes it, so it is not part of any commit.
- Commands:
  - `python -X utf8 benchmarks/solution-selection/materialised/run_selftests.py` → PASS 16/16,
    `model_calls: 0` (2 min 52 s). Every good PASS, every bad FAIL, every bad reference passes its
    public tests, every unmodified starter FAILs except F15 (by design: the readable starter is the
    correct answer to the "compact code" counterexample).
  - `fixture_kit.py stamp --check` → PASS (no drift).
  - `validate_benchmark_fixtures.py --verify-commits` → PASS, 16 materialised.
  - dev `python -m pytest tests -q` → 207 passed, 3 skipped; `skill_catalog_guardrails.py
    --report-only` → 167 active SKILL.md (unchanged), 0 errors; `validate_engine_control_plane.py`
    PASS; `contract_gate.py --all` 0 errors; `routing_smoke_test.py --min-rank1 88 --lint-fixtures`
    0 failures; `node scripts/generate-plugin-manifest.js --engine . --check` current.
- Stack notes: F03, F09 and F16 use Node (checker exits 2 / `NOT_ASSESSED` without it); F16 uses
  the native `Intl.Segmenter` with a decision record; F09, F15 record manual AT/reviewer checks
  `NOT_ASSESSED`; F10's PostgreSQL leg `NOT_ASSESSED`.

### T06 — Execute the solution-selection suite (NOT_ASSESSED — zero-spend rule)

- `--dry-run --emit-evidence runs` → 144 cells planned; `tools/solution_evidence.py validate
  runs/solution-selection-evidence.json --root runs` → `NOT_ASSESSED`, no errors; `report` →
  `NOT_ASSESSED`, cost `NOT_ASSESSED`. No `grading.json` exists because no cell executed.

### T07 — Acceptance prompts (NOT_ASSESSED — zero-spend rule)

- Files: agents `evals/cases/065`–`076-accept-*.yaml` gain `last_run_date`, `last_run_reason` and
  `last_run_evidence` (`last_run` stays `NOT_ASSESSED`). 36 cells planned; evidence validates
  `NOT_ASSESSED`. First-skill hit rate per engine: `NOT_ASSESSED` for all 12 engines. First-skill
  detection (Skill tool call or `SKILL.md` read) is unit-tested on SYNTHETIC traces.
- Contract shape: `python -X utf8 evals/runners/run-contract-evals.py --cases evals/cases --out
  <scratch>/shape.json` → 76/76 PASS (100 %).

### T08 — Pressure scenarios (DONE for authoring; execution NOT_ASSESSED — zero-spend rule)

- Files: dev `benchmarks/solution-selection/pressure-scenarios.json` gains PS03–PS07; `fixtures.json`
  PS02 gains `not_assessed_reason`. PS02 was already taken (quality-bar guard, M10-04), so the
  phase's PS02–PS06 table maps to PS03 destructive Git (`git-collaboration-workflow`, rules/common
  security + destructive-bash gate), PS04 SRS shared-understanding gate (`02-elicitation-toolkit`,
  `decision-frontier-elicitation.md`), PS05 render evidence (`13-saas-billing-and-metering-spec`
  fallback rule), PS06 DRE currentness (`source-verification`), PS07 approval control plane
  (`ai-agent-tooling-and-hitl`). Seven scenarios in total, each with three combined pressures,
  forced A/B/C choice, `short_prompt` and deterministic `forbidden_trace_patterns` (PS06 uses the
  LLM grader via `grader_note`).
- 42 cells planned (2 arms × n=3); evidence validates `NOT_ASSESSED`. Scoring: a safety expectation
  counts only at 100 % of runs.

### T09 — Plugin evals (DONE for cases; execution NOT_ASSESSED — zero-spend rule)

- Files: agents `evals/plugin/README.md` and 11 cases under `evals/plugin/<engine id>/<case>/`
  (`prompt.md`, `graders/*.md`) for five families; `max_turns: 12`.
- Shape check PASS (11 cases). `--plugin-eval --engine <id>` for all 7 engines → shape PASS,
  `NOT_ASSESSED (zero-spend rule)`, every command carries `--no-publish`
  (`command-output/plugin-eval-*.json`).
- `experimental.evals` manifest keys: NOT ADDED (reported, per brief). The agents copy of
  `generate-plugin-manifest.js` spreads `...existingManifest`, so an added key would be preserved.
  Recommendation: do not add the key, because the cases live in chwezi-engine-agents and the wrapper
  passes an explicit `--eval-dir`; a per-engine `evals/plugin` folder does not exist.
  `node scripts/generate-plugin-manifest.js --engine . --check` (dev) → current.

### T10 — MCP tool-surface evaluation (DONE for authoring and answer freezing; model run NOT_ASSESSED)

- Files: dev `skills/ai/ai-agent-tooling-and-hitl/references/mcp-tool-surface-evaluation.md` (new,
  paraphrase with attribution to anthropics/skills mcp-builder, Apache-2.0, commit
  33375500bcea98d610eb30ce10ac4e59b89c390d) and a one-line link in that skill's `SKILL.md`; agents
  `evals/mcp/build_fixture_workspace.py`, `coordinator-qa.yaml` (10 pairs), `verify_answers.py`,
  `samples/` (SYNTHETIC traces).
- `python -X utf8 skills/sdlc-meta/skill-writing/scripts/quick_validate.py
  skills/ai/ai-agent-tooling-and-hitl` → valid. `python -X utf8 evals/mcp/verify_answers.py` → PASS
  10/10 via the compiled server functions, no model, `pull_engine_ff_only` never called, fixture
  build hash reproducible. No `mcp-server` source change.
- Q07 was reworded during freezing (validator exit codes differ between PowerShell and `/bin/sh`).

### T11 — Micro-test mode (DONE_WITH_LIMITATIONS)

- `--micro --case PS01 --variants evals/behavioural/micro/PS01-variants.json` → 15 cells (control +
  2 variants × 5), `NOT_ASSESSED (zero-spend rule)`, verdict "NOT_ASSESSED: the control was not
  executed", variance note present (`command-output/micro-PS01.json`). The stop rule ("stop: nothing
  to fix" when the control does not fail) and k/n with binomial SD are unit-tested. `validate.yml`
  has no diff (no Tier-3 step in CI).

### T12 — Evidence-rung rule (DONE; ratification pending)

- Files: DRE `skills/ai-evaluation-and-data-flywheel/references/eval-flywheel.md` (new section
  "Evidence rungs for improvement claims" beside "Protected evaluation splits"; Caveman MIT
  attribution, commit 2fd153c); dev `benchmarks/solution-selection/README.md` references it.
- `python -X utf8 scripts/skill_contract_validator.py --baseline tests/skill-engine/quality-baseline.json`
  (DRE) → 59 active, 59 fully compliant, no failures.

### T13 — Report template (DONE)

- `evals/behavioural/REPORT-TEMPLATE.md`; applied in `M10-05-tier3-run-report-2026-09-29.md`
  (limitations section and rung declaration present).

### T14 — Orientation case kind (DONE; execution handed to M10-12)

- Runner kind `orientation` with shape validation, traversal guard and a deterministic path grader;
  template `evals/behavioural/templates/orientation-case.yaml`. Dry run → 1 cell, `NOT_ASSESSED`
  ("ENGINE-TOUR.md does not exist yet; execution handed to M10-12 (UA-11)").

### T15 — Scoring rule (DONE; ratification pending)

- `evals/behavioural/SCORING-RULE.md`: `NOT_ASSESSED` = 0 and kept in the denominator; readiness
  formula for M10-14; applied to T06–T10 (all T3 slots 0).

## Decisions taken under delegated authority (orchestrator under Peter's delegated authority, 29 Sep 2026)

1. Pressure IDs PS03–PS07 used for the phase's PS02–PS06 targets, because PS02 already existed.
2. Withheld tests held in a self-ignoring `benchmarks-private/` folder inside the dev checkout
   rather than editing the dev root `.gitignore`.
3. `initial_commit` defined as a reproducible commit (fixed identity and date, user and system git
   configuration excluded) so it can be recomputed and verified without committing fixtures to a
   separate repository.
4. `experimental.evals` manifest keys not added (see T09).
5. Evidence-rung and scoring rules drafted as recommended; both still need Peter's ratification
   (phase exit criteria).

## Open items for the orchestrator

- Doctrine ratification: evidence-rung rule (T12) and scoring rule (T15).
- Independent reviewer verdict required.
- `benchmarks-private/` is not in any commit by design; back it up locally if the withheld tests
  must survive a clean clone.
- Before any future paid or flat-rate run: verify stream-json field names, the grader no-tools flag,
  and the `--allowedTools` pattern syntax on the day; run `--selftest-isolation --allow-model-calls`
  first (only on Peter's explicit written instruction).
- Hand-offs: M10-12 (UA-11 run), M10-11 (plugin family 2 re-run), M10-14 (scoring rule), M10-03
  ledger (description changes from future fire rates).
