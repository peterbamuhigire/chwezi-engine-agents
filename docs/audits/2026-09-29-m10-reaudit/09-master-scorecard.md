# 09 — Master scorecard

> **Correction (29 Sep 2026, after the M10-14 independent review, finding F1/F3).** The Engine Eval Readiness used here (47.7) scored collision cleanliness 1.0 although the coordination package is not in the union collision scan, and excluded three executed known-defect oracles from p@1. Corrected: collision-clean `NOT_ASSESSED` = 0, p@1 30/42 = 0.7143, T2 = 40 x 0.1786 = 7.14, **Readiness 37.1**. Measured-constrained: hygiene = (52 + 37.1 + 66) / 3 = 51.70, overall 16.20 + 11.875 + 7.50 + 5.20 + 6.00 + 5.170 = **51.9**; **published 51.9**. The T1 of 8/8 uses a stand-in validator list (no `validators` entry for the package in `catalog/engines.yaml`). Source: `docs/operations/m10-kaizen-evidence/M10-14/eval-readiness.json`.

## Dimensions (the eleven in `audit-dimensions.md`)

| # | Dimension | Label | Score | Evidence |
|---:|---|---|---:|---|
| 1 | Doctrine and philosophy | judged | 60 | Orchestrator single-owner handoff table, capability negotiator, `NOT ASSESSED` semantics, craft standard, zero-spend and approval rules. Deficits: no British English output rule for the router (exempted in `shared-assets.yaml`); bridge contract line 56 contradicts practice; doctrine rulings D1–D5 unratified. |
| 2 | Taxonomy and structure | judged | 52 | See 02: single-skill group, flat `scripts/`, mixed `docs/operations/`, package not self-catalogued, adapters hand-kept. |
| 3 | Skill depth and rigour | judged | 50 | Canonical instructions are procedural and precise but short (25–90 lines); adapter skills are 11–12-line stubs; no worked handoff, maintenance or validation example in `core/`. |
| 4 | Worked examples and applied proof | judged (from measured inputs) | 45 | Applied proof is structural: 162 tests, 77 contract cases, 32 harness self-checks, synthetic traces. Tier-3 `grading.json` files: 0 (NOT_ASSESSED, adds nothing). No filled example of the package's main product, a multi-engine handoff. |
| 5 | Standards currency | judged | 50 | Judged from the engine's own currentness records (no fresh external research). Pinned MCP SDK 1.30.0 and vitest 4.1.11; dispositions dated 29 Sep; third-party register review dates set. No currency check on the Claude Code plugin/marketplace schema or Codex plugin format beyond local tests. |
| 6 | Output-type readiness and coverage | judged | 54 | Mean of nine output types, 53.6 (see 05). |
| 7 | Accessibility and inclusivity | NOT_ASSESSED | — | Not applicable to a coordination package's own outputs beyond British English; carries no weight. |
| 8 | Production, handoff and release | judged | 48 | No git tag ever; `release/checksums.txt` placeholder; release workflow omits adapter, installer and security tests and has no secret scan, contrary to `supply-chain-policy.md`; marketplace sources `ref: main`. Carries no weight. |
| 9 | Redundancy and hygiene | judged | 52 | Legacy `skills-engine-agents` naming in three shipped surfaces; MCP 1.0.0 vs 1.1.0; `released_commit` drift; tour six commits stale; portfolio 27 duplicate names and 291,636 metadata characters vs a 60,000 budget, no target. |
| 10 | Discovery and routing | **measured** | **47.7** | Engine Eval Readiness (11-measured-evidence). Judged value for the raw number: 55. |
| 11 | Safety and integrity | judged | 66 | Destructive-command hook (fails closed, byte-registered), MCP realpath boundaries, declared-validator allowlist, token gate, zero-spend gate, no-book-extraction check (measured: 12 roots, 0 findings), prompt-injection fixtures. Deficits: shell-string execution of catalogue commands, overstated release controls, unpinned marketplace refs, eight test files and hook tests outside CI. |

## Groups

| Group | Score |
|---|---:|
| `scripts/` validators and generators | 63 |
| `core/instructions` + contracts | 60 |
| `catalog/` | 58 |
| `hooks/` | 58 |
| `docs/security` | 56 |
| `evals/` | 55 |
| `mcp-server/` | 55 |
| `skills/` (`rules-distill`) | 52 |
| `agents/` wrappers | 50 |
| `adapters/` | 50 |
| `docs/operations` governance | 48 |

## Output types

| Output type | Score |
|---|---:|
| Host-file generation and drift control | 64 |
| Plugin marketplace | 58 |
| Engine catalogue and routing | 58 |
| Cross-engine routing evaluation | 55 |
| MCP server | 55 |
| Project context contract and engine tours | 52 |
| Governance records | 50 |
| Skill graph and fan-in tooling | 48 |
| Tier-3 behavioural harness | 42 |

## Overall

Weighting: output 30 %, depth and examples 25 %, standards 15 %, taxonomy 10 %, doctrine 10 %,
hygiene 10 % (hygiene = mean of redundancy, discovery/routing, safety).

Skill depth and worked examples bucket = (50 + 45) ÷ 2 = 47.5.

**Raw** (routing judged 55): hygiene = (52 + 55 + 66) ÷ 3 = 57.67.
0.30 × 54 + 0.25 × 47.5 + 0.15 × 50 + 0.10 × 52 + 0.10 × 60 + 0.10 × 57.67
= 16.20 + 11.875 + 7.50 + 5.20 + 6.00 + 5.767 = **52.5**

**Measured-constrained** (routing = Readiness 47.7): hygiene = (52 + 47.7 + 66) ÷ 3 = 55.23.
16.20 + 11.875 + 7.50 + 5.20 + 6.00 + 5.523 = **52.3**

**Published**: portfolio craft-standard acceptance evidence is absent, so `min(52.3, 65)` = **52.3**.

No score in this audit is 70 or above; no extraordinary justification is required.

## Movement against the baseline (29 Sep, unscored)

| Baseline weakness | Status at `8a438c9` |
|---|---|
| 1. Evals shape-only; fixtures missing; reports stale | Largely closed at the structural level: 77 cases with fixtures, route oracles executed, reports dated 29 Sep. Behavioural tier still unexecuted. |
| 2. No cross-engine collision detection | Closed as a gate (0 undeclared of 21 pairs); duplicates themselves still present (27 names). |
| 3. Registry and manifest drift | Marketplace counts now checked (23 ok). `released_commit` refreshed but unchecked; Codex manifest and release archive still use the old name. |
| 4. Validators joined with `|` | Closed: arrays, executed one by one in `engine-validation.ts`. |
| 5. Shared assets copy-pasted; gates outside CI; policy/CI mismatch; no tag | Partly closed: 16 shared assets registered and checked in a CI portfolio job. Release policy mismatch and absence of any tag unchanged; eight pytest files and the hook tests still outside CI. |
| Secondary: `rules-distill` claim about `rules/` | Closed: text now states the package has no `rules/` layer. |

The 4 Sep portfolio craft Kaizen recorded a portfolio-wide structural baseline of 64.8; it scored the
whole portfolio, not this package, and is not directly comparable.
