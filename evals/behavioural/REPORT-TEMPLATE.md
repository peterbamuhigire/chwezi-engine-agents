# Tier-3 run report: <suite> — <YYYY-MM-DD>

Template for every behavioural run report (M10-05-T13). Honest-reporting structure adapted from
DietrichGebert/ponytail benchmark write-ups (MIT, https://github.com/DietrichGebert/ponytail,
commit e3ba2aa); paraphrased, no text copied. Keep every section; write "none" rather than
deleting one.

## Run record

| Field | Value |
|---|---|
| Suite and cases | |
| Arms | |
| Runs per arm (n) | |
| Executor model ID (from `system/init`) | |
| Grader model ID | |
| Claude Code version (`claude --version`) | |
| UTC timestamp (start, end) | |
| Isolation self-test hash | |
| Engine commit(s) under test | |
| Runner command line | |
| Evidence file and validator result (`tools/solution_evidence.py validate`) | |

## Claim

What the run shows, in one or two sentences, with its evidence rung.

## Critique

The strongest reasons the claim could be wrong (contamination, grader drift, fixture leakage,
lexical-to-live gap, one model, small n, stochastic invocation).

## Method change

What changed since the previous run of this suite and why. "None" for a first run.

## Corrected number

The figure after any correction, beside the superseded figure. Never overwrite a published number.

## Results

| Case | Arm | Runs PASS / executed | NOT_ASSESSED runs (reason) | Notes |
|---|---|---|---|---|

Readiness contribution (scoring rule, `SCORING-RULE.md`): T3 pass rate = PASS runs / all planned
runs, with `NOT_ASSESSED` counted as 0 and kept in the denominator.

## Limitations

One model; n; lexical-to-live gaps; Codex arm `NOT_ASSESSED`; any fixture not materialised;
anything a checker cannot decide.

## Superseded runs

Earlier runs are kept and labelled here with the reason they were superseded (never deleted).

## Evidence rung

State one rung (`deterministic_remeasure`, `controlled_holdout`, `counterfactual_replay`,
`before_after`) per figure, per the evidence-rung rule in
digital-research-engine `skills/ai-evaluation-and-data-flywheel/references/eval-flywheel.md`.
Never add or average figures from different rungs. List confounders.

## Cost

Measured cost per cell and in total, or `null` where the CLI did not report it. Unknown cost is
never written as 0.

## NOT_ASSESSED list

Every planned cell or case that did not execute, each with its reason (zero-spend rule, quota,
authentication, CLI flag unavailable, fixture not materialised, input absent).
