# Documentation wave follow-ups (31 October 2026)

Owner: coordination maintainer. These are findings from the documentation wave that its scope did not allow it to fix: scripts,
catalogue data, the marketplace file, the MCP lockfile, skill bodies and other repositories were not edited. Each item names the
file, what is wrong, and how it was seen. Measurements were taken in scratch copies of this package against the eleven engines at
the `main` commits pinned in `catalog/engines.yaml`.

## Skill content

No change needed. `skills/rules-distill/SKILL.md` names no host path and no former engine name (searched for workstation paths, the
`skills-engine-agents` identity and `digital-research-skills`).

## Script and CI defects found by running the documented commands

| Item | File | Evidence | Suggested fix |
|---|---|---|---|
| `update.sh` fails on a fresh clone | `scripts/update.sh` line 11 runs `install.sh` directly; `git ls-files -s` gives mode 100644 | `sh scripts/update.sh --destination <folder>` exits 126, `Permission denied`; `sh scripts/install.sh --host codex --destination <folder>` over the managed copy exits 0 | Call `sh "<dir>/install.sh"` from `update.sh`, or commit the executable bit; the README names the workaround |
| `uninstall.sh --force` leaves empty folders | `scripts/uninstall.sh` | Exit 0, 0 files left and 17 empty folders left in the destination | Remove empty managed folders, or state the behaviour in its output |
| CI skips three installer tests | `.github/workflows/validate.yml`, `adapter-smoke-tests.yml` | No workflow names `tests/security/install-engine-ownership.test.js` (passes locally, 1 test), `tests/security/install-package-preservation.ps1` or `tests/security/install-shell-preservation.ps1` | Add the Node test to the ubuntu job and the two scripts to the Windows job |
| Two tests skip on any layout that does not hold folders named `chwezi-dev-engine` and `chwezi-design-engine` beside the package | `tests/test_run_behavioural_eval.py` lines 20, 252, 260; `tests/test_validate_rule_markers.py` line 13 | Three skips in 265 collected tests; none with a workspace folder that holds them | Resolve the sibling through `scripts/lib/engine_roots.py` (the cross-engine item M12 in `06-next-cycle.md`) |

## Catalogue, marketplace and policy data (not changed)

| Item | File | Note |
|---|---|---|
| Research repository name | `catalog/engines.yaml` lines 100 to 102 (`repository: digital-research-skills`, `path: digital-research-engine`) | The GitHub repository is `chwezi-research-engine` (GitHub API, 2026-10-31); `digital-research-skills` redirects and is the catalogue id. The `repository` field is the only place that still holds the old name as a repository |
| Research URLs | `.claude-plugin/marketplace.json` lines 182 to 189; `.github/workflows/validate.yml` lines 125 and 166 | They use `peterbamuhigire/digital-research-skills`, which redirects. The workflows also check it out into a folder named `digital-research-engine` |
| Hygiene ceiling | `catalog/hygiene-policy.yaml`, `chwezi-engine-agents.record_path_ceiling` | This wave removed five Windows user paths from `docs/runtime-skill-budget.md`; the dated-record count is now 963 against a ceiling of 968. Lower the ceiling to 963 (the policy says ceilings only fall) |
| MCP example paths | `mcp-server/.mcp.json.example` | Placeholders are `C:/path/to/skills-engine-agents/...`: Windows style, and the legacy identity (decision 3 in `06-next-cycle.md`) |
| Generated tour out of date | `docs/engine-tours/chwezi-engine-agents.md` and `.json` | `generate_engine_tour.py --check` passes with a warning: the tour was generated from `aef2dc5`. The MCP `engine_tour` tool reports it as stale. Regenerate in a cycle that is allowed to commit generated files |
| CHANGELOG wording | `CHANGELOG.md`, 2026-09-24 entry | Says the catalogue `repository` was "corrected to its GitHub name `digital-research-skills`". It was true that day and is now wrong; a dated entry, left as written |

## Cross-engine documentation mismatches (read from each engine's `main`, not edited)

| Engine and file | Mismatch |
|---|---|
| social-media-skills `README.md` lines 325 and 403 | Presents `digital-research-skills` as the research engine's current name and `chwezi-research-engine` as a former folder name. The GitHub repository is `chwezi-research-engine`; `digital-research-skills` is a redirecting alias and the catalogue id |
| social-media-skills `rules/common/core.md` (commit `3075062`, 31 October) | The edit made this file differ from its registered variant: the drift check now reports 17 `shared-asset-unregistered-variant` findings, 16 when pass 2 closed. Either register the new hash with owner and reason after review, or align the wording with the other copies |
| business-plan-skills `README.md` line 289 | Says "`digital-research-skills`, formerly checked out as `chwezi-research-engine`"; the order is reversed (the repository is `chwezi-research-engine`) |
| Engine READMEs generally | The research engine's catalogue path is `digital-research-engine`, its id `digital-research-skills` and its repository `chwezi-research-engine`. Documents that need all three should say which is which, as the [portfolio table](../../../README.md#portfolio) does |

## Checked and correct

- The 18 cross-engine routes in the README lifecycle map exist in the sibling checkouts (read-only check).
- The twelve marketplace plugin names in the README equal `.claude-plugin/marketplace.json`; the 77 contract cases, 1 skill and 11 schemas equal `find` counts.
- The managed router sentences: `render_host_files.py --render-router-blocks --engine <this package> --dry-run` reports `{"changed": []}`. This package carries none of the three sentences in their legacy form, and its design trigger block was not hand-edited.
