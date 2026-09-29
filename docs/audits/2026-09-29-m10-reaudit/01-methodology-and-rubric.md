# 01 — Methodology and rubric

## Auditor independence

The auditor did not execute any my-10-kaizen phase and made no change to the package outside this
folder. No git state was changed (read-only `git log`, `git status`, `git rev-list` only). No paid
API, `claude -p` or model-executed evaluation was run. The M10-14 executor was writing under
`docs/operations/` during the audit; that folder was read but not touched.

## Method

Followed `chwezi-dev-engine/skills/sdlc-meta/skill-engine-audit/SKILL.md` with
`references/scoring-rubric.md` (including "Engine Eval Readiness (measured)"),
`references/eval-readiness-worked-example.md`, `references/audit-dimensions.md` and
`references/report-structure.md`.

1. **Harness first.** Ran the nine package validators named in the brief, then three further free
   checks (route oracles, Tier-3 self-test, fan-in). Commands, exit codes and output lines are in
   `11-measured-evidence.md`.
2. **Scope.** Read `AGENTS.md`, `CLAUDE.md`, `README.md`, `catalog/engines.yaml`,
   `catalog/shared-assets.yaml`, the bridge contract, the craft standard and craft Kaizen record,
   the ownership register, the routing baseline and change ledger, the M10 execution log, the
   third-party dispositions, the project-context contract, this package's engine tour, MCP sources,
   both CI workflows and the release manifest.
3. **Sampling.** The package holds only three `SKILL.md` files (plus seven synthetic fixture skills
   under `tests/fixtures/`, excluded). The twelve-unit sample therefore covers every instruction-bearing
   unit: 3 `SKILL.md` (`skills/rules-distill`, the Claude Code and OpenCode adapter skills), the
   4 canonical instructions in `core/instructions/`, the 3 Codex wrappers in `agents/`,
   `adapters/claude-code/CLAUDE.md` and `adapters/generic/engine-validator.prompt.md` (13 units).
4. **Output types.** Adapted to a coordination package: engine catalogue and routing; host-file
   generation and drift control; cross-engine routing evaluation; Tier-3 harness; MCP server; plugin
   marketplace; governance records; project context contract and engine tours; skill graph and
   fan-in tooling.
5. **Comparison.** With `my-10-kaizen/02-engine-baselines/baseline-chwezi-engine-agents.md`
   (29 Sep, unscored, five named weaknesses) and the portfolio craft Kaizen of 4 Sep (portfolio-wide
   structural baseline 64.8, different scope). Movement is recorded against the baseline's named
   weaknesses, not its numbers, because it published none for this package.

**Documented limitation.** The standard parallel audit fleet was not used. The auditor worked
through each concern in turn (standards, existing units, taxonomy, output types, hardening), so the
scores are not independent draws from separate agents. No fresh external research was done;
standards currency is judged from the engine's own currentness records.

## Rubric

Bar: top 0.1 % of portfolio control planes for agent skill catalogues (single-source generation,
behavioural evaluation with pinned models, signed releases, enforced ownership). Bands: 90–100
rivals the best; 75–89 excellent; 60–74 solid but visibly short; 40–59 major gaps; under 40
skeletal. Default 45–65; any 70+ needs an extraordinary-justification paragraph (none was needed).

Labels: **measured** (cites a command and result), **judged**, **NOT_ASSESSED** (0 in any formula).

## Weighting

| Bucket | Weight | Dimension(s) |
|---|---:|---|
| Output-type readiness and coverage | 30 % | dimension 6 |
| Skill depth and worked examples | 25 % | mean of dimensions 3 and 4 |
| Standards currency | 15 % | dimension 5 |
| Taxonomy and structure | 10 % | dimension 2 |
| Doctrine and philosophy | 10 % | dimension 1 |
| Hygiene | 10 % | mean of dimensions 9, 10, 11 |

Accessibility (7) and production/handoff (8) are scored for comparability but carry no weight.

## Engine Eval Readiness

`Readiness = 30 × T1 + 40 × mean(T2_p1, T2_neg, T2_cov, T2_clean) + 30 × T3`, with
`NOT_ASSESSED` = 0 kept in the denominator. For this package T1 is the eight package validators
used by the M10-14 executor (the package has no `validators` entry of its own in
`catalog/engines.yaml`, so this denominator is executor-selected, not declared), and T2_p1 is the
portfolio route-oracle primary@1, because the package's own skill has no routing fixtures.
