# M10-02 — README contract repair evidence

Date: 29 Sep 2026. Scope: a bounded stop-the-line repair supporting M10-02-T14 (`portfolio-drift` CI job). The
28 Sep "docs: refresh engine README" commits shortened every public engine README and the coordination README,
removing markers and links that portfolio validators and engine tests require. This repair keeps the refreshed
content and adds back only what a contract requires. `srs-skills/README.md` is excluded (owned by the M10-07
executor); what it needs is recorded below.

## Status

| Item | Status |
|---|---|
| Accounting prompt-contract markers (`validate-prompt-capability.ps1`) | DONE |
| Portfolio craft README heading, 10 engines (`validate-portfolio-craft.ps1`) | DONE (srs outstanding, out of scope) |
| Runtime-orchestration link: accounting, proposal, business-plan tests | DONE |
| Proposal `encoding_link_gate.py` canonical sibling routes | DONE (found during this repair; not in the brief) |
| Engine-agents coordination-card links (`validate-kaizen-cards.py`) | DONE |
| Social-media link checker excludes `node_modules` | DONE |
| Linux `fcntl` tests skipped on Windows with a reason | DONE |

## What the refresh removed and what was restored

Method: `git show <refresh-commit>^:README.md` compared with the current file for each repository, then each
validator's or test's actual requirement read from source.

| Repository | Refresh commit | Contract broken | Restored (minimum) |
|---|---|---|---|
| chwezi-accounting-doctrine | `f186f63` | `validate-prompt-capability.ps1` reads `README.md` as accounting's router and needs `DOMAIN PROMPT GENERATION CONTRACT`, the contract path, `Ready-to-paste prompt`, `Failure action`. `tests/test_runtime_orchestration_guidance.py` needs `runtime-agnostic-orchestration-2026-09-07.md`. Craft heading. | The pre-refresh `## DOMAIN PROMPT GENERATION CONTRACT` section, verbatim, placed before References; one References bullet linking the orchestration contract; `## Skills` renamed `## Capabilities`. |
| proposal-skills | `d12ab93` | Test needs the orchestration link. `scripts/encoding_link_gate.py` needs the canonical `business-plan-skills` and `social-media-skills` GitHub URLs in README (pre-refresh cross-engine table carried them). Craft heading. | Two References bullets: orchestration contract; the two sister-engine URLs with their pre-refresh route descriptions. Heading renamed. |
| business-plan-skills | `27c2c9b` | Test needs the orchestration link. Craft heading. | One References bullet; heading renamed. |
| chwezi-engine-agents | `71fd6b4` | `validate-kaizen-cards.py` needs README links to the three coordination cards. | The pre-refresh "Coordination cards" list (three links), placed under the Capabilities table. |
| chwezi-dev-engine, design-system-skills, digital-research-engine, website-skills, social-media-skills, linux-skills, windows-admin-engine-skills | `204e321`, `52b85e5`, `4898c6b`, `47f9e34`, `23ccda3`, `74a73c3`, `132cbe9` | `validate-portfolio-craft.ps1` needs `## Capability map` or `## Capabilities` within the first four H2 headings; the refresh used `## Skills`. | `## Skills` renamed `## Capabilities` (the section is the capability table; `## Capabilities` matches the refreshed engine-agents README). No other change. |

Decision under delegated authority (orchestrator, 29 Sep 2026): the heading was renamed rather than the validator
relaxed, because the brief asks for README contracts to be restored, not weakened. No test or script in the
portfolio asserts a `## Skills` heading in an engine README (searched `*.py, *.ps1, *.js, *.sh, *.yml, *.yaml`).

## Checker and test tweaks

- `social-media-skills/tests/test_engine_quality.py`: the repository Markdown link test now skips any path under
  `node_modules` (vendored third-party content; the failing file was
  `projects/maduuka-2026-09/node_modules/idb-keyval/README.md`, which is git-ignored). `node_modules` untouched.
- `linux-skills/tests/test_admin_activity.py`: module-level `pytestmark = pytest.mark.skipif(sys.platform ==
  "win32", reason=...)`, because `scripts/linux_admin_activity.py` imports `fcntl` (POSIX only). No test deleted;
  all 12 cases still run on Linux CI.

## Verification (run 29 Sep 2026, Windows host)

| Command | Before | After |
|---|---|---|
| `scripts/validate-prompt-capability.ps1` | FAIL (accounting marker) | PASS, 11 engines, identical local contracts |
| `scripts/validate-portfolio-craft.ps1` | FAIL, 11 engines | FAIL, srs-skills only (out of scope, see below) |
| `python -X utf8 scripts/validate-kaizen-cards.py` | FAIL (3 README links) | PASS |
| `proposal-skills: python -X utf8 scripts/encoding_link_gate.py` | FAIL (2 findings) | PASS (0 findings) |
| `pytest tests` accounting | 1 failed, 6 passed | 7 passed |
| `pytest tests` proposal | 1 failed, 51 passed | 52 passed |
| `pytest tests` business-plan | 1 failed, 61 passed | 62 passed |
| `pytest tests` social-media | 1 failed, 29 passed | 30 passed |
| `pytest tests` linux | 12 failed, 22 passed | 22 passed, 12 skipped (Windows; reason recorded) |
| `pytest tests` chwezi-engine-agents | 1 failed, 58 passed | 65 passed |
| `pytest tests` dev / design / DRE / website / windows-admin | 187 / 99 / 129 / 80 / 24 passed | unchanged, all pass |
| Declared engine validators (`catalog/engines.yaml`), 10 engines excl. srs | all exit 0 except proposal link gate | all exit 0 except dev `skill_catalog_guardrails.py` (see open items) |
| `python -X utf8 scripts/render_host_files.py --check --workspace-root ..` | 0 findings | 2 findings, both in dev `skills/sdlc-meta/skill-writing/` (see open items) |

The linux `fcntl` tests are NOT_ASSESSED on this host; they are assessed only on a POSIX runner.

## Open items

1. **srs-skills/README.md (M10-07 owns it).** To pass `validate-portfolio-craft.ps1`, rename `## Skills` (line 25)
   to `## Capabilities` (or `## Capability map`); it must stay within the first four H2 headings. No srs test or
   prompt-capability check reads the srs README (its router is `AGENTS.md`), so nothing else is needed for these
   contracts.
2. **Dev `skills/sdlc-meta/skill-writing/` (another executor's in-progress edits, not touched here).**
   `render_host_files.py --check` reports `shared-asset-unregistered-variant` for `SKILL.md` and
   `scripts/quick_validate.py`, and `skill_catalog_guardrails.py` reports a broken reference to
   `scripts/render_host_files.py` from that `SKILL.md`. Both clear once that executor registers the new hashes in
   `catalog/shared-assets.yaml` and fixes the reference.
