# Plugin evaluation cases (`claude plugin eval`, on demand, never in CI)

Fires and stays-quiet pairs for five misroute families drawn from the M10-03 route oracles
(M10-05-T09, AO-11). Layout: `evals/plugin/<catalogue engine id>/<case>/prompt.md` plus
`graders/*.md`, in the case format used by addyosmani/agent-skills `evals/plugin/` (MIT,
https://github.com/addyosmani/agent-skills, commit 2686b62; format adapted, cases original).

| Family | Fires | Stays quiet |
|---|---|---|
| 1 Business case with ROI | srs-skills/business-case-roi-fires | social-media-skills/business-case-roi-stays-quiet, proposal-skills/business-case-roi-stays-quiet |
| 2 Lighthouse / Core Web Vitals | website-skills/lighthouse-cwv-fires, design-system-skills/lighthouse-cwv-co-activates-fires | (co-activation family; expected to fail until M10-11) |
| 3 Invoice typeface | design-system-skills/invoice-typeface-fires | social-media-skills/invoice-typeface-stays-quiet |
| 4 SRS for billing | srs-skills/billing-srs-fires | srs-skills/billing-srs-game-stays-quiet |
| 5 Validation contract | chwezi-dev-engine/validation-contract-fires | digital-research-skills/validation-contract-stays-quiet |

Each engine is evaluated on its own, because loading several plugins in one arm was not verified.
Skill names in `input_match` carry the engine's plugin namespace (`srs:`, `social:`, `proposal:`,
`website:`, `design-system:`, `engineering:`, `research:`).

Run through the wrapper, which hard-codes `--no-publish` and refuses without `--allow-model-calls`:

```powershell
python -X utf8 scripts/run_behavioural_eval.py --plugin-eval --engine srs-skills --model <pinned> --grader-model <pinned> --runs 3
```

Under the zero-spend rule (29 Sep 2026) no plugin eval has been run: every family is
`NOT_ASSESSED (zero-spend rule)`. Shape is checked by `run_behavioural_eval.py --selftest` and
`tests/test_run_behavioural_eval.py`. Thresholds when run: must-not-fire 0 fires; must-fire rates
recorded as a baseline (target at least 0.8 of runs); read the delta, not the exit code.
