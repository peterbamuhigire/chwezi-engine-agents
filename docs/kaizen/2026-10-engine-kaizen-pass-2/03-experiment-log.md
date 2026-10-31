# Experiment log: portfolio kaizen pass 2 (31 October 2026)

One change at a time. After each kept change the touched suites were re-run; the full replay of every registered command is in
`04-validation-record.md`. "Mutation" below means a temporary single-line break of the new code, run against the new tests, then
restored byte for byte from a saved copy; a control that survives a mutation is not a control.

| ID | Commit | Hypothesis | Change | Result | Decision |
|---|---|---|---|---|---|
| K1 | `eb8dae1`, `9329a82` | Every portfolio check can run on any layout if engines are found by a shared locator and a missing engine is `NOT_ASSESSED` | `scripts/lib/engine_roots.py`; catalogue `aliases` for the four renamed engines; `--engines-root` and `CHWEZI_ENGINES_ROOT` for the drift check; `skill_graph.py` reports paths relative to each engine root | 13 locator tests, 5 layout tests for the drift check and one linked-layout test for the graph script. All 12 engines resolve on this host's two-parent layout. Drift output on that layout equals the hand-built symlink workspace byte for byte (37 findings both ways in the final run). `skill_graph.py` raised `ValueError` on a linked layout before and exits 0 after (1,105 nodes, 12,035 edges, equal to the git-archive baseline run) | Kept |
| K2 | `5d7dbc8`, `2259900` | A policy-driven scan of tracked files finds the two tracked settings files and every live host path, without drowning in dated records | `scripts/check_public_hygiene.py`, `catalog/hygiene-policy.yaml`: six rules, record ceilings that only fall, redacted output | 26 tests. Seven mutations (settings rule off, key-body check off, placeholders ignored, ceiling off, allow ignores reason, records excuse secrets, entropy gate off) were each caught; the entropy mutation survived until a test was added, then was caught. Live run: 26 findings in 7 repositories, none in credential shape. The first draft flagged 12 documentation lines (a quoted key header, code references, a sample key) as secrets; four refinements removed them with no loss of seeded detection | Kept |
| K3 | `0d539fa` | Naming the canonical copy and comparing installed copies closes the "which copy is canonical" question | `scripts/check_hook_copies.py`, `docs/operations/hook-canonical-copy.md`, register row for the fourth hook file | 13 tests; five mutations caught (installed copies skipped, CRLF not normalised, trash not skipped, missing engine passes, difference passes). Live: 11 repositories and 8 installed copies, 76 files, 0 differences | Kept |
| K4 | `2af312e` | A pin refresh that refuses unsafe trees, plus a lag rule in the drift check, makes the end-of-waves refresh one command | `scripts/refresh_released_commits.py`, `scripts/lib/released_commits.py`, rule `released-commit-*` with `--pin-lag-max` | 21 tests on real throw-away repositories; six mutations caught. Live check: 11 of 11 lag (28 to 51 commits). The catalogue pins were **not** committed: the write mode was run once by mistake (see below) and reverted | Kept (tool); pins deliberately unchanged |
| K5 | `608f466` | Catalogue validators match what the engines run if the drift check compares them | Validators added for six engines; rules `validator-script-missing` and `validator-undeclared` | 8 tests; four mutations caught. The rule found exactly the ten manifest commands the catalogue lacked (website six, windows three, proposal one) and no missing script; zero after the refresh | Kept |
| K6 | `d4450f7` | One path-free wording plus a rule and a renderer lets the doc wave fix the routers mechanically | `templates/agents-blocks/`, rules `router-host-path` and `router-former-name`, `--render-router-blocks` | 14 tests; five mutations caught (one survived as an equivalent mutant until a mixed-sentence test was added). Rule flags exactly accounting (lines 56, 145) and social (47, 60, 443). On scratch copies of both routers the renderer rewrote the legacy sentences, was idempotent on re-run and left no path finding | Kept |
| K7 | `0267684` | The discovery test should follow the checkout's branch and the MCP tool should never call an unstartable validator a failure | Test compares with `git branch --show-current`; exit 126 and 127 map to `NOT ASSESSED` | 15 of 16 before (on this branch), 18 of 18 after; the two new tests fail against the old `engine-validation.ts` (`[PASS, FAIL]` returned). Build clean | Kept |
| K8 | `6763854` | CI should run every Python test and the hook tests, and the release should call the full validate workflow | `validate.yml` and `release.yml` edited; policy text corrected | Workflow YAML parses; every referenced file exists; each added command replayed locally (exit codes in `evidence/k8-ci-local-replay.txt`). Real CI not run | Kept |
| K9 | `f099c75` | The two stale suite counts are the only marketplace drift | Two leading counts edited | `generate-plugin-manifest.js --check-marketplace`: 21 ok, 2 drift before; 23 ok, 0 drift after | Kept |
| F-01 | none | A lock refresh clears the critical dependency finding | Not attempted | The fix is `npm install` of two minor versions, outside the one permitted command (`npm ci --ignore-scripts`). `npm audit fix --dry-run` failed inside npm (`Cannot read properties of null`), so the residual after a refresh is `NOT_ASSESSED` | Escalated |

## Negative results and corrections

- **Accidental write.** While testing `refresh_released_commits.py`, a stray `--write --any-branch` was run against the live
  catalogue. It updated all 11 pins correctly (an unplanned live proof that the writer touches only the pin values) but the
  orchestrator plans to refresh pins last. `git diff` confirmed only those 11 lines changed; `git restore catalog/engines.yaml`
  discarded them (rollback: run the script again). Nothing was committed from that run.
- **Test-data collision.** The first pin tests failed because two throw-away repositories produced the same commit hash (same
  tree, message, author and second). The fixture now varies each repository's content. The code was not at fault.
- **Host hook block.** The destructive-command gate (loaded from the accounting engine's plugin on this host) blocked one
  `rm -rf` of a scratch folder that did not yet exist. It was not retried; a fresh folder name was used. Which plugin copy
  fires is any of the 11 repository or 8 installed copies, all identical (K3).
- **Two claims not accepted as reported.** The SDLC report's dev-engine alias-prefix mismatch is not a defect (the file declares
  `external_target_prefixes`). The 29 October scorecard's printed mean (46.82) does not match its rows (505 over eleven is 45.91).
- **Not tried.** Registering the 16 unregistered shared-asset variants (each needs a content review and will change again when the
  Linux and documentation waves land); renaming the Codex plugin identity (documented deliberate choice); any model-judged routing.
- **Pytest.** The new tests are `unittest` classes so they run here. Seven older files are pytest-style: five plain-function
  files that `unittest discover` silently skips (zero tests collected) and two that import pytest. They were run through a
  labelled stand-in runner (58 passed, 3 skipped, 0 failed); real pytest remains `NOT_ASSESSED`.
