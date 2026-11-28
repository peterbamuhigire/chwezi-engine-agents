# Validation record

Baseline at ab1039c and final candidate at 2fb96e1. Windows host.

| Check | Baseline exit | Final exit | Observation |
| --- | --- | --- | --- |
| `python -X utf8 scripts/check_token_budget.py . --strict` | 0 | 0 | Both token-budget gates report zero findings. |
| `python -X utf8 -m pytest -p no:cacheprovider tests -q` | NOT_ASSESSED | NOT_ASSESSED | 480-second baseline timeout. Report unavailable results as NOT_ASSESSED. |
| `python -X utf8 -m unittest discover -s tests -p test_*.py` | NOT_ASSESSED | NOT_ASSESSED | 480-second baseline timeout. |
| `python -X utf8 scripts/render_host_files.py --check` | NOT_ASSESSED | 1 | 480-second baseline timeout. |
| `python -X utf8 scripts/check_public_hygiene.py` | NOT_ASSESSED | 1 | 480-second baseline timeout. |
| `python -X utf8 scripts/check_public_hygiene.py --repo .` | 1 | 1 | Local tracked-content warnings predate the case-runner edit. |
| `python -X utf8 scripts/check_hook_copies.py` | 1 | 1 | Installed cache control has existing differences. |
| `python -X utf8 scripts/refresh_released_commits.py` | 1 | 1 | Published pin lag remains open. No pin refresh was applied. |
| `python -X utf8 scripts/validate-contracts.py --schema schemas/engine-catalog.schema.json --instance catalog/engines.yaml` | 0 | 0 |  |
| `python -X utf8 scripts/validate-no-book-extractions.py --workspace-root <engine-root>` | 0 | 0 |  |
| `python -X utf8 scripts/validate-kaizen-cards.py` | 0 | 0 |  |
| `python -X utf8 scripts/validate-routing-baseline.py` | 0 | 0 |  |
| `python -X utf8 scripts/validate-runtime-skill-budget.py --root skills` | 0 | 0 |  |
| `python -X utf8 scripts/validate-runtime-skill-budget.py --collisions --ownership evals/routing/ownership.yaml --workspace-root <engine-root>` | 0 | 0 |  |
| `python -X utf8 scripts/validate-skill-lifecycle.py --root skills` | 0 | 0 |  |
| `python -X utf8 scripts/validate-rule-markers.py ../chwezi-design-engine/doctrine/references/ai-slop-banned-fonts.md` | 0 | 0 |  |
| `python -X utf8 evals/runners/run-contract-evals.py --cases evals/cases --route-oracles --workspace-root <engine-root> --out <scratch-report>` | 0 | 0 | 77/77 before and after. Entire deterministic route-oracle result object matched. |
| `node hooks/test-destructive-bash-gate.js` | 1 | 1 | 56/61 baseline and 59/61 final. Ordinary simulated push cases are falsely blocked. Outcome varies between runs. |
| `node hooks/test-plugin-hook-config.js` | 0 | 0 |  |
| `node scripts/generate-plugin-manifest.js --check-marketplace --workspace-root <engine-root>` | 1 | 1 | Suite engineering description reports 168 skills while the dev manifest lists 169. |
| `node --test tests/security/install-engine-ownership.test.js` | 0 | 0 |  |
| `bash -n scripts/install.sh` | 1 | 1 | Default Bash invokes WSL with no functional distro. Git Bash retry below. |
| `bash -n scripts/update.sh` | 1 | 1 | Default Bash invokes WSL with no functional distro. Git Bash retry below. |
| `bash -n scripts/uninstall.sh` | 1 | 1 | Default Bash invokes WSL with no functional distro. Git Bash retry below. |
| `claude plugin validate .` | 0 | 0 |  |
| `python -X utf8 scripts/readme_metrics.py --check README.md` | 0 | 0 | Six absolute checks passed before and after. Comparative score tracked separately. |
| `python -X utf8 scripts/check_readme_preservation.py . 146714c HEAD` | 0 | 0 | See exact committed comparison below. |
| `python -X utf8 scripts/check_readme_contract.py --engines-root <engine-root>` | 0 | 0 |  |
| `python -X utf8 scripts/validate-contracts.py --schema schemas/adapter-manifest.schema.json --instance adapters/claude-code/adapter.yaml` | 0 | 0 |  |
| `python -X utf8 scripts/validate-contracts.py --schema schemas/adapter-manifest.schema.json --instance adapters/codex/adapter.yaml` | 0 | 0 |  |
| `python -X utf8 scripts/validate-contracts.py --schema schemas/adapter-manifest.schema.json --instance adapters/gemini-cli/adapter.yaml` | 0 | 0 |  |
| `python -X utf8 scripts/validate-contracts.py --schema schemas/adapter-manifest.schema.json --instance adapters/generic/adapter.yaml` | 0 | 0 |  |
| `python -X utf8 scripts/validate-contracts.py --schema schemas/adapter-manifest.schema.json --instance adapters/mcp/adapter.yaml` | 0 | 0 |  |
| `python -X utf8 scripts/validate-contracts.py --schema schemas/adapter-manifest.schema.json --instance adapters/opencode/adapter.yaml` | 0 | 0 |  |
| `Git Bash: bash -n scripts/install.sh` | 0 | 0 | Syntax only. |
| `Git Bash: bash -n scripts/update.sh` | 0 | 0 | Syntax only. |
| `Git Bash: bash -n scripts/uninstall.sh` | 0 | 0 | Syntax only. |
| `npm ci` | 0 | NOT_ASSESSED | Clean scratch lockfile install. |
| `npm run build` | 0 | NOT_ASSESSED | Clean scratch build. |
| `npm test` | 0 | NOT_ASSESSED | 16 pass, 2 skip in live tree. Scratch attempt could not resolve relative repository test inputs. |
| `npm audit --json` | 1 | NOT_ASSESSED | 13 advisory findings, including 1 critical. F-01 remains open. |
| `run-contract-evals.py --route-oracles (one valid case and one malformed)` | 1 | 1 | Same exit 1. Candidate writes JSON and ranks the valid oracle. Baseline aborts before JSON. |
| `python -X utf8 scripts/check_readme_preservation.py . ab1039c 2fb96e1` | NOT_ASSESSED | 0 | 87 links, 60 commands retained and no broken anchors. |
| `powershell.exe -NoProfile -File tests/validate_catalog.ps1` | NOT_ASSESSED | 0 | Windows PowerShell 5.1. |
| `powershell.exe -NoProfile -File tests/adapters/test_claude_code_adapter.ps1` | NOT_ASSESSED | 0 | Windows PowerShell 5.1. |
| `powershell.exe -NoProfile -File tests/adapters/test_codex_adapter.ps1` | NOT_ASSESSED | 0 | Windows PowerShell 5.1. |
| `powershell.exe -NoProfile -File tests/adapters/test_other_host_adapters.ps1` | NOT_ASSESSED | 0 | Windows PowerShell 5.1. |
| `powershell.exe -NoProfile -File tests/test_capability_fallbacks.ps1` | NOT_ASSESSED | 0 | Windows PowerShell 5.1. |
| `powershell.exe -NoProfile -File scripts/validate-portfolio-craft.ps1` | NOT_ASSESSED | 1 | Windows PowerShell 5.1. |
| `powershell.exe -NoProfile -File scripts/validate-prompt-capability.ps1` | NOT_ASSESSED | 0 | Windows PowerShell 5.1. |
| `powershell.exe -NoProfile -File evals/runners/run-host-smoke-tests.ps1` | NOT_ASSESSED | 0 | Six install-manifest fixture targets. |
| `powershell.exe -NoProfile -File tests/install/test_fork_discovery.ps1` | NOT_ASSESSED | 0 | Windows PowerShell 5.1. |
| `powershell.exe -NoProfile -File tests/install/test_install_targets.ps1` | NOT_ASSESSED | 0 | Disposable install/update/uninstall fixture. |
| `powershell.exe -NoProfile -File tests/security/install-package-preservation.ps1` | NOT_ASSESSED | 0 | PowerShell installer preservation fixture. |
| `powershell.exe -NoProfile -File tests/security/install-shell-preservation.ps1` | NOT_ASSESSED | 0 | Git Bash installer preservation fixture. |
| `powershell.exe -NoProfile -File tests/security/test_command_allowlist.ps1` | NOT_ASSESSED | 0 | Windows PowerShell 5.1. |
| `powershell.exe -NoProfile -File tests/security/test_mutation_gates.ps1` | NOT_ASSESSED | 0 | Windows PowerShell 5.1. |
| `powershell.exe -NoProfile -File tests/security/test_path_boundaries.ps1` | NOT_ASSESSED | 0 | Windows PowerShell 5.1. |

An extended final pytest retry completed: 384 passed and 24 subtests passed in 999.94 seconds. Both earlier 480-second attempts remain recorded as timeouts. Narrow final regression suite exits 0 with 9 tests. Remote CI, provider-backed routing, native host integration and PowerShell Core-specific tests are NOT_ASSESSED.


﻿# Mixed-case experiment

Use a scratch case directory containing a copy of `evals/cases/023-route-business-case-roi.yaml` and a case named `999-invalid.yaml` containing `[invalid` followed by a newline. Run `python -X utf8 evals/runners/run-contract-evals.py --cases <scratch-cases> --min-cases 2 --route-oracles --workspace-root <engine-root> --out <scratch-report>`.

| Observation | Baseline ab1039c | Experiment 2fb96e1 |
| --- | --- | --- |
| Process exit | 1 | 1 |
| Evidence output | Parser traceback, no JSON | JSON with two shape results, one pass and one fail |
| Location of malformed content | Traceback reports line 1 | Failure row includes line 1 and column 1 |
| Valid fixture | No lexical record | Expected skill ranks first, cross-engine activation remains a miss |
| Full case set | 77 passes | 77 passes, identical lexical result object |

Nystrom (2021) *Crafting Interpreters*, §6.3.1, informs recovery at the next independent case. The local conversion labels itself a summary. The concept was verified in the author's primary text on 28 November 2026. [Author's text](https://craftinginterpreters.com/parsing-expressions.html#panic-mode-error-recovery)

Retain the case-boundary fix. Revert 2fb96e1 to recover the prior runner. Remeasure the validation dimension from 72 to 75, because the mixed-input failure now has a stable oracle and complete evidence. Other dimensions keep their observed scores. The resulting raw score is 70.5. Validation remains FAIL because the broader suite is not established in this run and known independent failures persist.


﻿# Independent review

Reviewed README.md, evals/runners/run-contract-evals.py and tests/test_run_contract_evals.py against ab1039c. The filter uses each case's shape verdict. Failed cases remain in the JSON summary and still make the command exit 1. The synthetic suite-size failure row is appended after all actual cases, so it does not affect path alignment. Existing lexical thresholds, public catalogue authority and shape-report logic are preserved. The test's route-oracle stub isolates the case boundary without depending on sibling checkouts. No blocking defect found.

- `python -X utf8 -m pytest -q -p no:cacheprovider tests/test_run_contract_evals.py` exits 0 with 9 tests.
- `git diff --check ab1039c` exits 0.
- Model-based routing and claims about how an agent acts remain NOT_ASSESSED. The fixture proves the deterministic case boundary.


The final README preservation check at afb448d retained 87 link targets and 60 commands, with zero broken anchors. The workspace extraction check reported 12 roots and zero findings. The Kaizen card structure validator passed.

## Second-wave MCP dependency check

On 28 November 2026 the second wave reproduced F-01 against the lockfile at `2db40b1`. Windows used Node 24.8.0 and npm 11.6.0. The audit covered production and development dependencies.

| Input and check | Exit | Observed result |
|---|---:|---|
| Original lockfile, `npm audit --json` | 1 | 13 findings, including six high and one critical. |
| SDK 1.32.2 and Vitest 4.1.12, direct pins only, `npm audit --json` | 1 | Eight findings remained, including the critical transitive finding. |
| `npm audit fix --package-lock-only --ignore-scripts --no-fund` | 0 | The compatible transitive refresh cleared the remaining findings. |
| Clean full-repository clone, candidate manifest and lockfile, `npm ci --no-fund` | 0 | Installed 197 packages. |
| Same installation, `npm audit --json` | 0 | Empty findings object. The JSON metadata counts 197 dependencies. The install summary counted 198 packages including the root. |
| Same installation, `npm run build` and `npm test` | 0 each | TypeScript built. Six test files passed, with 16 tests passed and two POSIX cases skipped on Windows. |

The independent package review checked all 197 resolved entries for registry origin and SHA-512 integrity fields. The package identity, script commands, supported-Node declaration and runtime/dev dependency roles are unchanged. The Vite test dependency already required Node 20.19 or later within the Node 20 series. The oldest runtime remains untested. The registry lists the SDK release on 23 October and the Vitest release on 15 October 2026, checked on 28 November. [SDK registry record](https://registry.npmjs.org/@modelcontextprotocol/sdk) · [Vitest registry record](https://registry.npmjs.org/vitest)

The installed Debian guest could not mount its disk. A disposable Alpine Linux 3.23.8 x86_64 guest cloned the product commit `f53a1fa` from a Git bundle. With Node 24.22.3 and npm 11.11.0, `npm ci` installed 147 platform-applicable packages. The first separate audit exited 1 on a registry DNS error. The repeat returned zero findings. The TypeScript build passed and all 18 tests across six files passed, including both POSIX shell exit-code cases.

On Windows the Python suite passed 384 tests and 24 subtests. The 77-case evaluation matched the previous run for all case results and every route-oracle field. Extraction checks found zero findings across 12 roots, and Kaizen card validation passed. The local hygiene gate still reports four previously recorded paths in the managed runner.

The finding closes for this lockfile and this audit date. Production reachability, hosted MCP installation and newly reported advisories remain outside this result. Recheck from the directory containing the lockfile after a dependency or advisory change. Revert the manifest and lockfile together if a compatibility regression requires rollback, and reopen F-01 against the restored lockfile. [npm audit documentation](https://docs.npmjs.com/cli/v11/commands/npm-audit/)
