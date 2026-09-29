# 05 — Per-output-type readiness

Scores are judged, anchored on the measured results in `11-measured-evidence.md`.

## Scores

### 1. Host-file generation and drift control — 64

Evidence: `render_host_files.py --check --workspace-root ..` exit 0, "checked 12 repositories;
findings 0; not assessed 0"; 16 shared assets registered; tests in CI (portfolio job with sibling
checkouts).
Gaps: (a) closed list does not cover `.codex-plugin/plugin.json` (still `skills-engine-agents`),
the MCP server identity (`skills-engine-agents-mcp` 1.0.0) or release archive names; (b)
`claude-bridge-contract.md` line 56 contradicts the checked `CLAUDE.md`; (c) adapter wrappers are not
rendered from `core/`.
Lift: extend the version and name invariants to those three surfaces; render adapter prompts.

### 2. Plugin marketplace — 58

Evidence: `generate-plugin-manifest.js --check-marketplace` exit 0, "23 ok, 0 drift, 0 not
assessed"; relevance signals present; tests in CI.
Gaps: every domain plugin is sourced from `ref: main`, so an install is not reproducible; versions
1.1.0 with no tag in any repository checked here; the Codex manifest keeps the old name.
Lift: pin `ref` to release tags once tags exist; add the Codex manifest to the check.

### 3. Engine catalogue and routing (catalogue, orchestrator) — 58

Evidence: `validate-catalog.ps1` exit 0, 11 unique engines; validator arrays; orchestrator with
single-owner handoff table and craft brief.
Gaps: `released_commit` 4–14 commits behind every engine with no freshness check; package not
self-catalogued; no filled example handoff; engine@1 84.6 % means one oracle in six still goes to
the wrong engine (lexical).
Lift: a freshness check with a stated tolerance; a worked handoff under `core/examples/`.

### 4. Cross-engine routing evaluation (collision gate, ownership, oracles, ratchet) — 55

Evidence: union scan 1,169 skills, 21 pairs ≥ 0.75 all declared, 0 undeclared; route oracles
primary@1 30/39, engine@1 33/39, must-co-activate@5 3/4; ratchet passes; change ledger RC-001 to
RC-014.
Gaps: nine gated misses (031 rank 435, 050 rank 7, 045 rank 6, 051 rank 5, 036 rank 4, 055 rank 4,
042 rank 3, 037 rank 2, 053 rank 2) plus three known defects at 0/3; acceptance prompts 2/12; all
figures lexical; nine register entries mostly `canonical_owner` with follow-up deferred to a
"later wave".
Lift: fix the misses by description or fixture work under the ledger; converge the duplicated
meta-skills that the register names.

### 5. MCP server — 55

Evidence: `npm test` 16/16; six tools; realpath boundary; allowlisted validators; constant-time
token check.
Gaps: stale name and version; `scope` argument accepted but ignored; validators executed via
`powershell -Command` or `/bin/sh -c` with the catalogue string (safe only while the catalogue is
trusted); cannot validate the coordination package itself.
Lift: tokenised argv execution; implement or drop `scope`; self-catalogue.

### 6. Project context contract and engine tours — 52

Evidence: contract, schema, template, read-only doctor with tests; 12 generated tours; MCP
`engine_tour` flags staleness.
Gaps: no real project has adopted `PROJECT.md` in evidence; this package's own tour was generated at
`48af46b`, six commits behind HEAD; orientation Tier-3 case unexecuted.
Lift: one pilot project with doctor output; regenerate tours in CI.

### 7. Governance records (Kaizen records, third-party register, dispositions) — 50

Evidence: 72-entry third-party register; dispositions D1–D5 with rationale, conditions and
reversal triggers; kaizen cards validator exit 0; change-class matrix.
Gaps: running log covers M10-00 and M10-02 only; D1–D5 and the M10-00 deviations await
ratification; execution contract lost; supply-chain policy misdescribes the release workflow.
Lift: complete the running log for M10-03 to M10-14; record ratifications; correct the policy.

### 8. Skill graph and fan-in tooling — 48

Evidence: `skill_fanin.py` exit 0; skill graph report-only; tests pass.
Gaps: fan-in output says "M10-03 adapters not delivered" and "reachability … not recomputed"; the
graph is explicitly never a routing input, so its value is diagnostic only and unproven on a
decision.
Lift: deliver the fixture adapters; recompute reachability; cite one consolidation decision taken
from fan-in data.

### 9. Tier-3 behavioural harness — 42

Evidence: `run_behavioural_eval.py --selftest` status PASS, 32/32 checks, `model_calls` 0; zero-spend
gate enforced in code; report template and scoring rule.
Gaps: 0 grading files; `evals/behavioural/results/` absent; 299 planned runs `NOT_ASSESSED`; the
harness has never been run against a live CLI, so its stream-json assumptions are unverified (its
own README says to verify them on the day).
Lift: a bounded, authorised pilot (for example the 12 acceptance cases, n = 3, pinned model).

## Ranked table

| Rank | Output type | Score |
|---:|---|---:|
| 1 | Host-file generation and drift control | 64 |
| 2 | Plugin marketplace | 58 |
| 2 | Engine catalogue and routing | 58 |
| 4 | Cross-engine routing evaluation | 55 |
| 4 | MCP server | 55 |
| 6 | Project context contract and engine tours | 52 |
| 7 | Governance records | 50 |
| 8 | Skill graph and fan-in tooling | 48 |
| 9 | Tier-3 behavioural harness | 42 |
| | **Mean (output-type readiness)** | **53.6 → 54** |
