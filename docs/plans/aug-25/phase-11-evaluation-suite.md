# Phase 11 — Cross-Host and Cross-Model Evaluation Plan

> **For agentic workers:** Use executing-plans or subagent-driven-development. Define expected behavior before running provider-backed evaluations.

**Goal:** Prove adapters preserve routing, safety, validation verdicts, and fork behavior across hosts while reporting model differences honestly.

**Depends on:** Phases 1–10.

**Produces:** Contract cases, deterministic runner, host smoke runner, optional provider matrix, and regression reports.

## Files

- Create: evals/README.md.
- Create: evals/contracts/routing.yaml.
- Create: evals/contracts/maintenance.yaml.
- Create: evals/contracts/validation.yaml.
- Create: evals/contracts/fork-discovery.yaml.
- Create: evals/cases/001-route-srs.yaml.
- Create: evals/cases/002-add-finance-cross-cutting.yaml.
- Create: evals/cases/003-skip-dirty-pull.yaml.
- Create: evals/cases/004-block-divergence.yaml.
- Create: evals/cases/005-report-unavailable-validator.yaml.
- Create: evals/cases/006-discover-fork.yaml.
- Create: evals/cases/007-reject-injected-validator.yaml.
- Create: evals/runners/run-contract-evals.py.
- Create: evals/runners/run-host-smoke-tests.ps1.
- Create: evals/reports/template.md.
- Create: .github/workflows/validate.yml.
- Modify: README.md and CONTRIBUTING.md.

## Evaluation case format

Each case contains:
- id
- task
- fixture_path
- required_observations
- forbidden_actions
- expected_verdict
- evidence_fields

## Required case set

Create at least 20 cases:
- 10 routing cases covering every engine and cross-cutting additions.
- 4 maintenance cases covering clean, dirty, diverged, and missing-upstream repositories.
- 4 validation cases covering pass, fail, unavailable dependency, and malformed command.
- 2 security cases covering prompt injection and path traversal.

Required cross-cutting cases:
- business plan plus accounting doctrine
- website plus design system
- current standards check plus digital research
- proposal plus source verification

## Tasks

- [ ] Write case files before implementing the runner.
- [ ] Implement deterministic shape and forbidden-action assertions.
- [ ] Add fixture repositories for clean, dirty, diverged, forked, unknown, and malformed-router states.
- [ ] Add host smoke tests that install every adapter into a temporary directory.
- [ ] Add optional provider-backed runs for Codex/GPT, Claude/DeepSeek-compatible, and other configured host combinations.
- [ ] Treat provider outage, missing key, unavailable host, and quota errors as NOT ASSESSED, not package failures.
- [ ] Record host, model label, adapter version, core version, case ID, status, duration, and evidence.
- [ ] Set release thresholds: 100% contract shape pass, 100% forbidden-action pass, 100% safety-gate pass, and no unqualified PASS for missing evidence.
- [ ] Add a regression report template comparing core and adapter versions.
- [ ] Run the suite after every canonical instruction change.

## Tests and evidence

Run:
- python evals\runners\run-contract-evals.py --cases evals\cases --out evals\reports\latest.json
- powershell -NoProfile -ExecutionPolicy Bypass -File evals\runners\run-host-smoke-tests.ps1

Expected evidence: deterministic cases pass; provider-backed cases are separately labelled PASS, FAIL, or NOT ASSESSED with reason and evidence.

## Failure handling

- A forbidden-action failure blocks release even if answer quality is high.
- A routing mismatch blocks the affected adapter.
- A provider failure is isolated from deterministic contract tests.
- A model-generated answer that lacks required evidence cannot receive PASS.

## Exit criteria

- Adapter changes cannot ship without proving preservation of routing and safety contracts.
- Model differences are measured with host, model, and version labels.

## Commit checkpoint

Stage the files listed above and commit:
test: add cross-host agent evaluation suite
