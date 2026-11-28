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

Narrow final regression suite exits 0 with 9 tests. Remote CI, provider-backed routing, native host integration and PowerShell Core-specific tests are NOT_ASSESSED.


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
