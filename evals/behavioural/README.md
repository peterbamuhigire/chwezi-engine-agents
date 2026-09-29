# Tier-3 behavioural evaluation (opt-in, local, never in CI)

`scripts/run_behavioural_eval.py` is the single Tier-3 runner for the portfolio (M10-05). It runs
existing cases only; it adds no general schema or corpus (P05).

| Suite | Source | Arms | Default n |
|---|---|---|---|
| `solution-selection` | chwezi-dev-engine `benchmarks/solution-selection/fixtures.json` + `materialised/Fxx/` | baseline, engine, short_prompt | 3 |
| `acceptance` | `evals/cases/*-accept-*.yaml` (M10-03-T10) | engine | 3 |
| `pressure` | dev `fixtures.json` `pressure_scenarios` + `pressure-scenarios.json` | baseline, engine | 3 |
| `mcp` | `evals/mcp/coordinator-qa.yaml` | mcp_only | 1 |
| `orientation` | `templates/orientation-case.yaml` (UA-11; run handed to M10-12) | engine | 1 |

Plugin evals (`evals/plugin/`) run through `--plugin-eval`, which hard-codes `--no-publish`.

**Zero-spend gate.** Anything that starts a model is refused unless `--allow-model-calls` is passed.
Under the zero-spend rule (Peter, 29 Sep 2026) it is never passed, and every model-executed cell is
recorded `NOT_ASSESSED (zero-spend rule)`.

Free commands (no model call):

```powershell
python -X utf8 scripts/run_behavioural_eval.py --suite solution-selection --dry-run
python -X utf8 scripts/run_behavioural_eval.py --selftest-isolation
python -X utf8 scripts/run_behavioural_eval.py --selftest
python -X utf8 scripts/run_behavioural_eval.py --micro --case PS01 --variants evals/behavioural/micro/PS01-variants.json
python -X utf8 -m pytest -q tests/test_run_behavioural_eval.py
```

- `results/` is gitignored (raw stream-json traces may hold local paths); commit summaries, hashes
  and `solution_evidence` JSON only.
- `samples/` holds SYNTHETIC traces and grader outputs for self-tests; they are not model output.
- Reports use `REPORT-TEMPLATE.md`; scores follow `SCORING-RULE.md` (`NOT_ASSESSED` = 0, kept in the
  denominator).
- Before any executed run, verify on the day: the stream-json field names (`system/init` plugins,
  skills, model; the result event's cost field), the grader's no-tools flag syntax, and the
  `--allowedTools` pattern syntax. An unknown shape makes a cell `NOT_ASSESSED`.
