# Tier-3 run report: solution selection, acceptance, pressure, plugin evals, MCP QA — 2026-09-29

Written to `evals/behavioural/REPORT-TEMPLATE.md` (M10-05-T13). One report covers T06, T07, T08,
T09, T10 and T11 because none of them executed a model: the zero-spend rule (Peter, 29 Sep 2026)
bars every model-executed cell.

## Run record

| Field | Value |
|---|---|
| Suite and cases | solution-selection F01–F16; acceptance 065–076; pressure PS01–PS07; plugin evals (11 cases, 5 families); MCP QA Q01–Q10; micro-test PS01 |
| Arms | solution-selection: baseline, engine, short_prompt; acceptance: engine; pressure: baseline, engine; plugin: with/without plugin; MCP: MCP-only; micro: control + 2 wording variants |
| Runs per arm (n) | 3 (micro-test 5) |
| Executor model ID | none — no model was run |
| Grader model ID | none — no model was run |
| Claude Code version | 2.1.284 (Claude Code), from `claude --version` (no model call) |
| UTC timestamp | 2026-09-29 (plans and self-tests only) |
| Isolation self-test hash | `83a06771f3fda7be998cfb0c4045db58fb14c63239a79d367bfc73f8231dea2d` (static + detector checks; live smoke `NOT_ASSESSED (zero-spend rule)`) |
| Engine commit(s) under test | recorded per cell in `runs/*-plan.json` (read-only `git rev-parse HEAD`) |
| Runner command line | `python -X utf8 scripts/run_behavioural_eval.py --suite <suite> --dry-run --emit-evidence docs/operations/m10-kaizen-evidence/M10-05/runs` |
| Evidence file and validator result | `runs/<suite>-evidence.json`; `tools/solution_evidence.py validate … --root runs` returns `NOT_ASSESSED` with no schema errors for all five suites |

## Claim

The Tier-3 harness is built and proven able to fail without a model: all 16 fixture checkers pass
their good reference and fail their bad one, the grader validator rejects every malformed sample,
and the isolation detector flags every contaminated sample. No behavioural result exists yet.
Evidence rung for the harness claims: `deterministic_remeasure`. No quality-delta figure is claimed.

## Critique

- A harness that fails bad references can still pass a wrong live answer that the checker does not
  anticipate; withheld tests and review-style oracles (LLM grader) cover part of that gap.
- The isolation detector is proven only on SYNTHETIC `system/init` samples; the real field names
  of Claude Code 2.1.284 stream-json events are unverified until the first live run.
- The short prompts were written by an author who had read the oracles (see Limitations).

## Method change

First run of this harness; none.

## Corrected number

None; no figure has been published.

## Results

| Task | Cases | Planned runs | PASS | NOT_ASSESSED runs (reason) | Readiness contribution (T3, /30) |
|---|---|---|---|---|---|
| T06 solution selection | 16 (all `MATERIALISED`) | 144 | 0 | 144 (zero-spend rule) | 0 |
| T07 acceptance prompts | 12 | 36 | 0 | 36 (zero-spend rule); first-skill hit rate per engine `NOT_ASSESSED` for all 12 engines | 0 |
| T08 pressure scenarios | 7 (PS01–PS07) | 42 | 0 | 42 (zero-spend rule); with-skill pass rate `NOT_ASSESSED` | 0 |
| T09 plugin evals | 11 (5 families, 7 engines) | 66 | 0 | 66 (zero-spend rule); must-fire and must-not-fire rates `NOT_ASSESSED` | 0 |
| T10 MCP QA | 10 | 10 | 0 | 10 (zero-spend rule); answers frozen and re-derived 10/10 without a model | 0 |
| T11 micro-test (PS01) | 1 | 15 | 0 | 15 (zero-spend rule); verdict "NOT_ASSESSED: the control was not executed" | not scored |
| T14 orientation (UA-11) | 1 | 1 | 0 | 1 (input `ENGINE-TOUR.md` absent; execution handed to M10-12) | 0 |

Readiness contribution under `evals/behavioural/SCORING-RULE.md`: T3 pass rate = 0 / 299 planned
runs = 0.00, so the T3 slot contributes 0 of 30 points for every engine. No engine can exceed
70/100 until Tier 3 runs.

Free steps that did run (harness evidence, not T3 passes):

| Step | Result |
|---|---|
| Checker self-tests (`run_selftests.py`) | PASS 16/16: good PASS, bad FAIL for every fixture; every bad reference passes its public tests; F15's starter passes by design (counterexample) |
| Fixture specification (`validate_benchmark_fixtures.py --verify-commits`) | PASS; 16/16 `MATERIALISED`, `initial_commit` recomputed and matched; 7 pressure scenarios |
| Runner self-test (`--selftest`) | PASS, 32/32 checks, `model_calls: 0` (includes the 16 checker self-tests and the 11-case plugin shape check); `command-output/runner-selftest.json` |
| Isolation self-test (`--selftest-isolation`) | static PASS, detector PASS (7 synthetic samples), live `NOT_ASSESSED (zero-spend rule)`, paid runs not permitted |
| Grader validation over recorded samples | 9 synthetic grader outputs: 2 valid accepted, 7 invalid rejected |
| MCP answers (`evals/mcp/verify_answers.py`) | PASS 10/10 against the compiled server functions, no model; `pull_engine_ff_only` never called |
| Plugin-eval cases shape | PASS, 11 cases; every wrapper command carries `--no-publish` |
| Unit tests | `tests/test_run_behavioural_eval.py` 34 passed (no model; a missing binary and a local fake emitting SYNTHETIC stream-json) |

## Limitations

- No model-executed cell ran; every behavioural slot is `NOT_ASSESSED (zero-spend rule)`.
- One model will be used per set when run; n=3 (micro-test n=5) is small, and invocation is stochastic.
- Lexical-to-live gap: T2 lexical proxies do not predict live firing (agent-skills issue #620).
- Codex arm `NOT_ASSESSED` (out of scope; P00 policy applies if added).
- UA-11 orientation execution deferred to M10-12.
- Short prompts were written from each fixture's title and public task, but the author had read
  the oracles, so they are not strictly blind.
- F09 and F15 record manual accessibility and reviewer checks as `NOT_ASSESSED` in `fixture.json`;
  F10's PostgreSQL leg is `NOT_ASSESSED` (no pinned image). F03, F09 and F16 checkers need Node
  and exit `NOT_ASSESSED` without it.
- Withheld tests exist only on this machine (`benchmarks-private/`, self-ignored); a fresh clone
  can verify `hidden_manifest_hash` only where the private folder is restored.

## Superseded runs

None.

## Evidence rung

`deterministic_remeasure` for the checker self-tests, fixture-commit recomputation, grader
validation and MCP answer re-derivation. No `controlled_holdout` figure exists yet; the planned
three-arm run would be one. Figures from different rungs are not combined.

## Cost

0. No paid call was made. Per-cell `cost_usd` is omitted (unknown, not zero) in the evidence files.

## NOT_ASSESSED list

- T02 live isolation smoke (3 arms): zero-spend rule.
- T06: 144 executor cells and their grader calls: zero-spend rule.
- T07: 36 acceptance cells: zero-spend rule.
- T08: 42 pressure cells: zero-spend rule.
- T09: 11 plugin-eval cases × 2 arms × 3 runs: zero-spend rule.
- T10: the recorded MCP-only model run: zero-spend rule.
- T11: 15 micro-test cells: zero-spend rule.
- T14 / UA-11: input absent; handed to M10-12.
