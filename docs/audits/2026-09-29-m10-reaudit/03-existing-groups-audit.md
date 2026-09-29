# 03 — Existing groups audit

All scores judged unless marked measured.

## Per-group scores

| Group | Score | Justification |
|---|---:|---|
| `core/instructions` + contracts | 60 | Clear orchestrator procedure and ownership table; validator verdict semantics (`PASS`/`FAIL`/`NOT ASSESSED`/`PARTIAL`) and session-diagnosis procedure with citation rule. No worked handoff example in `core/`; capability negotiator is 25 lines of rules with no example profile walk-through. |
| `agents/` wrappers | 50 | Correctly thin (12 lines, pointer to canonical text). Codex-only; no test that the wrapper and canonical `contract_version` stay aligned. |
| `adapters/` (6 hosts) | 50 | Covered by PowerShell adapter tests and host smoke tests; hand-written; the generic validator prompt still cites only the catalogue schema check as its example, not the portfolio checks the canonical validator requires. |
| `skills/` (`rules-distill`) | 52 | Useful three-layer filter and verdict table; deterministic scan scripts exist. No fixture, no worked example output, zero inbound references (measured: `skill_fanin.py`, `inbound_skills` 0). |
| `catalog/` | 58 | Validator arrays (baseline defect 4 fixed); schema-validated (measured: exit 0). `released_commit` 4–14 commits behind every engine with no check; package not self-listed. |
| `scripts/` validators and generators | 63 | Measured: all run checks exit 0; 162 tests pass. Render check covers bridges, invariants, versions, BOMs, model IDs, hooks and 16 shared assets. Blind spots named in 05. |
| `evals/` (cases, routing, behavioural) | 55 | 77 cases now with fixtures; route oracles execute (measured 30/39); ownership register and change ledger are good practice. Lexical only; Tier 3 unexecuted; acceptance prompts 2/12. |
| `mcp-server/` | 55 | Measured: 16/16 tests. Sound path and approval gates. Stale identity (1.0.0, old name); `scope` parameter validated but unused; commands run through a shell string. |
| `hooks/` | 58 | Destructive-command gate, fails closed, now byte-registered across engines. JS tests not in CI. |
| `docs/operations` governance | 48 | Rich records, but running log stops at M10-02; ratifications open; plan-package loss recorded; bridge-contract line 56 contradicts `CLAUDE.md`. |
| `docs/security` | 56 | Threat models, permission model, SBOM, 72-entry third-party register. Supply-chain policy overstates the release workflow; no secret scan exists. |

## Per-unit scores (sample: every instruction-bearing unit)

| Unit | Score | Refs? | Worked example? | Cites doctrine? | Note |
|---|---:|---|---|---|---|
| `skills/rules-distill/SKILL.md` (96 lines) | 52 | scripts only | output template, no filled example | yes (dev `rules/README.md`) | Accurate after correction; no fixtures |
| `adapters/claude-code/skills/skills-engine-agents/SKILL.md` (12) | 45 | no | no | points to `core/` | Deliberate stub; description generic ("Route, inspect, validate…") |
| `adapters/opencode/skills/skills-engine-agents/SKILL.md` (11) | 45 | no | no | points to `core/` | As above |
| `core/instructions/engine-orchestrator.md` (90) | 62 | contracts | no filled handoff | yes (craft standard, project context) | Best unit; lacks a filled multi-engine handoff |
| `core/instructions/engine-validator.md` (86) | 60 | contracts | no | yes | Clear verdicts; session diagnosis attributed (MIT, commit pinned) |
| `core/instructions/engine-maintainer.md` (52) | 56 | contracts | no | yes | Strict `--ff-only` rules; no rollback example |
| `core/instructions/capability-negotiator.md` (25) | 50 | degraded modes | no | yes | Terse rule list |
| `agents/engine-orchestrator.md` | 48 | — | — | — | Wrapper |
| `agents/engine-maintainer.md` | 48 | — | — | — | Wrapper |
| `agents/engine-validator.md` | 48 | — | — | — | Wrapper |
| `adapters/claude-code/CLAUDE.md` | 50 | — | — | yes | Repeats the book-extraction rule, as the bridge contract forbids for root bridges (adapter file, so not in scope of the check) |
| `adapters/generic/engine-validator.prompt.md` | 47 | — | commands | partial | Omits the portfolio checks the canonical validator requires |
| `CLAUDE.md` (root bridge) | 55 | — | — | — | Conforms to the bridge contract (measured: render check 0 findings); the contract document itself says it should have no Claude-only section |

Median unit score 50. No unit reaches 70.
