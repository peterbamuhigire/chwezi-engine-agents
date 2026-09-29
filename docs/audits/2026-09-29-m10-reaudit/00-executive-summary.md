# 00 — Executive summary

> **Correction (29 Sep 2026, after the M10-14 independent review, finding F1/F3).** The Engine Eval Readiness used here (47.7) scored collision cleanliness 1.0 although the coordination package is not in the union collision scan, and excluded three executed known-defect oracles from p@1. Corrected: collision-clean `NOT_ASSESSED` = 0, p@1 30/42 = 0.7143, T2 = 40 x 0.1786 = 7.14, **Readiness 37.1**. Measured-constrained: hygiene = (52 + 37.1 + 66) / 3 = 51.70, overall 16.20 + 11.875 + 7.50 + 5.20 + 6.00 + 5.170 = **51.9**; **published 51.9**. The T1 of 8/8 uses a stand-in validator list (no `validators` entry for the package in `catalog/engines.yaml`). Source: `docs/operations/m10-kaizen-evidence/M10-14/eval-readiness.json`.

**Scores.** Raw 52.5; measured-constrained 52.3; published 52.3 (the 65 cap does not bind).
Engine Eval Readiness 47.7 / 100 (measured). No dimension, group or output type is scored 70 or
above.

## Verdict

`chwezi-engine-agents` is now a working, tested control plane for the portfolio rather than a
registry with shape-only checks. Every validator run for this audit passed. What keeps it in the
low fifties is the gap between structural proof and applied proof: routing quality is known only
through a lexical proxy, the behavioural tier is entirely unexecuted, and the package's own release
and governance trail is incomplete.

## Headline findings

1. **Routing evidence is lexical only, and weak where it matters most.** Route oracles reach the
   expected primary skill 30 of 39 times (76.9 %) with three known defects removed from the
   denominator (30 of 42, 71.4 %, if they are counted). Nine gated misses remain, one at rank 435
   (oracle 031, live anti-slop). The twelve per-engine acceptance prompts reach the right primary
   lexically 2 times in 12 (16.7 %). Tier 3 has 0 grading files; all 299 planned runs are
   `NOT_ASSESSED` under the zero-spend rule. T2_neg and T2_cov are 0 for this package because its
   own skill has no fixtures.
2. **Release chain never exercised and still misdescribed.** No git tag exists after 130 commits;
   versions read 1.1.0 in plugin manifests while `mcp-server/package.json` and the MCP server
   identity read 1.0.0. `docs/security/supply-chain-policy.md` still says the release workflow runs
   adapter, installer and security checks and a secret scan; `.github/workflows/release.yml` runs
   only the catalogue schema, contract evals and the MCP build/test. This was baseline weakness 5
   and is unchanged.
3. **Legacy naming the drift checker cannot see.** `.codex-plugin/plugin.json` is still named
   `skills-engine-agents`; the release archive and artefact are `skills-engine-agents.tar.gz`; the
   MCP server calls itself `skills-engine-agents-mcp` 1.0.0. `render_host_files.py --check` reports
   0 findings because none of these surfaces is in its closed list.
4. **Contract text contradicts the checked state.** `docs/operations/claude-bridge-contract.md`
   line 56 says the coordination bridge "carries no Claude-only section"; `CLAUDE.md` has one, and
   `catalog/shared-assets.yaml` registers it under `coordination.claude_only_block`. The checker
   follows the register, so the contract document is the stale party.
5. **Governance trail incomplete.** `docs/operations/m10-kaizen-execution-2026-09-29.md` records
   M10-00 and M10-02 only, although commits and evidence folders run to M10-13; the third-party
   dispositions D1–D5 await Peter's exact-text ratification; the execution contract
   (`05-execution-contract.md`) is recorded as lost. `catalog/engines.yaml` `released_commit`
   values were refreshed today but are already 4–14 commits behind every engine, with no check.

Secondary: CI runs 12 of the 20 pytest files (the book-extraction, lifecycle, rule-marker,
prompt-injection, retrieval-metric, behavioural-harness and Kaizen-card tests are local only) and
none of the hook JavaScript tests; the portfolio metadata load is 291,636 characters against the
package's own 60,000 runtime budget, with 27 duplicate skill names, and no target is set.

## What is strong

- `scripts/render_host_files.py --check`: 12 repositories, 0 findings, 0 not assessed; 16 shared
  assets registered with byte, block and registered-variant modes.
- Union collision gate: 1,169 skills, 21 cross-engine pairs ≥ 0.75, all declared in
  `evals/routing/ownership.yaml`, 0 undeclared; a routing change ledger records rejected as well as
  accepted changes (RC-006 rejected).
- A ratchet (`scripts/validate-routing-baseline.py`) that only raises floors.
- A Tier-3 harness with a hard zero-spend gate (`--allow-model-calls`) and 32/32 grader and trace
  self-checks passing without a model call.
- MCP server: six read-only or approval-gated tools, realpath boundary checks, catalogue-declared
  validators only, constant-time confirmation-token comparison; 16/16 vitest tests pass.
- Baseline defect 4 (validators joined with `|`) is fixed: validators are arrays and run one by one.

## Path to the bar

P0 closes the naming, release-policy and contract-text defects and adds routing fixtures for the
package's own skill (target 56). P1 fixes the nine oracle misses and executes a bounded Tier-3 set
once spend is authorised (target 61). P2 cuts a signed release, puts every test in CI and sets a
portfolio metadata target (target 65, still under the published cap until craft-standard
acceptance evidence exists). See `10-roadmap-to-world-class.md`.
