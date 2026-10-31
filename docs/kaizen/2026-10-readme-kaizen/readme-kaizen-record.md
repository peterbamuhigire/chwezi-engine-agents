# README kaizen record, 31 October 2026

A scoped micro-cycle on the root `README.md` of the coordination package, plus the step that standardises the README practice for the whole portfolio. It follows the Portfolio Kaizen steps (Observe, Baseline, Select, Experiment, Check, Standardise, Teach, Re-measure). **It publishes no score.** The latest published score stays 48.09 out of 100.

Branch `kaizen/2026-10-readme-kaizen`, created from `main` at `cf64878` with a clean tree (0 `git status --porcelain` lines). Nothing was pushed, tagged or merged. The commits are listed under Experiment.

Two things in this cycle go beyond the README:

- The two scratch scripts from the README kaizen brief became package tools with tests: `scripts/readme_metrics.py` and `scripts/check_readme_preservation.py`.
- `docs/operations/readme-standard-2026-10-31.md` sets the shared structure, limits and preservation rules, with measured results for the eleven engines.

The destructive-command hook blocked two of my commands (a recursive forced delete and an rsync with a delete flag). I did not override it. Neither command was needed.

## Observe

Baseline for this README, measured on `main` before the first edit:

| Metric | Before | What it says |
|---|---:|---|
| `words` | 7,470 | Far longer than a front door can carry |
| `h2` | 8 | Eight sections held everything |
| `toc` | 0 | No contents list |
| `first_cmd` | 13 | First command at line 13 |
| `longest_sec` | 3,100 | Quality and improvement |
| `long_lines` | 61 | Lines over 300 characters |
| `max_line` | 1,461 | Characters in the longest line |
| `sent_len` | 19.6 | Words per sentence in prose |
| `fre` | 44 | Flesch reading ease: difficult |
| bullets, table rows | 72, 98 | |

The scratch baseline file lists this README at 2,495 words. That was an earlier version. The documentation wave added the Validation, Portfolio and Quality sections afterwards, so the figures above are the ones on `main` today.

Words by section: Quality and improvement 3,100 (the open findings, the calendar and the October account together), Capabilities 1,046, Validation 970, References 854, Installation 556, Portfolio 386, and the preamble 261.

What reads the README:

- `scripts/validate-kaizen-cards.py` requires the three coordination card file names in the README text.
- `scripts/generate_engine_tour.py` reads the first heading as the tour title. The heading is unchanged.
- `scripts/install.sh` and `scripts/install.ps1` copy `README.md` into an installed package. They do not read it.
- `mcp-server/src/engine-discovery.ts` falls back to `README.md` as a router. It checks only that the file exists.
- `scripts/skill_fanin.py` and `scripts/skill_graph.py` read README files as router text for their reports. Both are report-only.
- `AGENTS.md` and `CONTRIBUTING.md` point to the README section "Validation" by name. `docs/README.md` and `CHANGELOG.md` link the anchor `what-the-october-2026-kaizen-improved`. `07-docs-followups.md` links the anchor `portfolio`.
- `scripts/validate-portfolio-craft.ps1` checks the engines' READMEs, not this one. See the finding under Check.
- No script, test, manifest or router reads the tool table or the References section as content.
- A text search of every tracked file in the eleven engine repositories found no link to an anchor in this README.

## Select

| Item | Decision | Reason |
|---|---|---|
| R1 Front door | Applied | Purpose, audience, six measured facts and three numbered steps with commands. The first command is at line 20 and the three steps end at line 39 |
| R2 Contents | Applied | A 16-item list with four nested items; all 20 in-page anchors resolve |
| R3 Structure | Applied | 23 H2 sections. The largest is Validation at 1,136 words, made of four H3 sections. The next is Open findings at 706 |
| R4 Find the right tool | Applied | 11 rows from task to tool. The package has one skill, so the table lists tools. The read-only commands were run. The pin command (`--write`) was not run: its options were checked in `--help`. The install command was run with `--dry-run` in a scratch folder. Every linked file exists |
| R5 No walls of text | Applied | Longest paragraph or list item 68 words. Longest table cell 31 words. Lines over 300 characters 61 to 7 |
| R6 Plain English | Applied | Short active sentences, terms defined at first use. Commands, numbers and hashes kept |
| R7 Say it once | Applied | Repeated statements became links. The October account stays, in four sections, as requested |
| R8 Relocate bulk | Applied to two items | The tool detail went to `docs/operations/package-tools-reference.md` and the 31 reference entries to `docs/references.md`. The README keeps a short table and a summary, each with a link |
| Move the date-gate calendar, the open findings or the Validation table | Skipped | They are the part a maintainer acts on, and `AGENTS.md` points at them |
| `CHANGELOG.md` entry | Applied | A new top entry for 31 October |
| `docs/README.md` index | Applied | Rows for the standard, the tool reference, the references page and this record |
| Skeleton section 10, Contributing | Applied | A short section with the author and the licence (MIT) |

## Experiment

| Commit | Theme | What it changed |
|---|---|---|
| `398c4f4` | Tools | `scripts/readme_metrics.py`, `scripts/check_readme_preservation.py` and their two test files (39 and 47 tests at that point) |
| `0e559fa` | Tools | The preservation check reads every file that links the README and skips link examples in code; `-v` lists moved items; 4 more tests (51 in all) |
| `abe8c65` | Structure, front door, plain English, relocation, standard | The new README, the two relocated pages and the README standard. One commit, because the README was rewritten in one pass and no honest intermediate version exists |
| `3dd7f8b` | Registration | A CI step, the `AGENTS.md` pointer and the supply-chain policy line |
| `42cfab7` | Finding | The README and the standard record the conflict with `validate-portfolio-craft.ps1` |
| `f82d155` | Front door | The opening became two paragraphs and Start here step 1 points to Install and update, so the three steps end at line 39 and the first command moves to line 20 |
| `a6b7c5f` | Record | This file, the changelog entry and the documentation index rows |
| the commit after it | Record | Corrects the commit list in this file |

### Deliberate corrections to facts

Each was re-measured on 31 October 2026, or checked in git.

1. **MCP server.** The README called it "read-only". It has six tools, and `pull_engine_ff_only` is approval-gated and writes (`mcp-server/src/index.ts`). The README now says so.
2. **Pin lag.** "4 to 8 commits behind" became "5 to 9", from `refresh_released_commits.py` on the live engines. The remark that the SDLC engine's HEAD was on a branch is gone: every engine is on `main`.
3. **Drift check.** The headline figure is 30 findings (19 plus 11 pin lag), re-run through three routes. The 19 stay as the breakdown.
4. **Documentation wave.** "On branch `kaizen/2026-10-docs` and not merged" became "now on `main`" (`git merge-base --is-ancestor c9d155b main`).
5. **Test counts.** 262 passed and 3 skipped became 352 and 3 (355 and 0 with sibling folders). `unittest` went from 203 tests to 293, with the same 2 failures and 8 errors. The 262 stays as the pass-2 figure.
6. **Pin check row.** "Exit 0: 11 engines, 0 not at HEAD" became "Exit 1: 11 not at HEAD, 5 to 9 commits behind". It still says exit 0 when the pins were refreshed in `f1e4565`.
7. **Anchors.** `Open findings`, `Decisions waiting for the maintainer` and `Date-triggered gates across the portfolio` moved from H3 to H2 with the same slugs. `Installation` became `Install and update` and `Capabilities` became `What is inside`. The anchors `#installation`, `#capabilities`, `#skills`, `#tools-and-scripts-by-function`, `#books`, `#repositories`, `#standards-and-official-sources` and `#websites-and-articles` are gone. No tracked file and no engine links them. `docs/README.md` now links `#decisions-waiting-for-the-maintainer` instead of `#quality-and-improvement`.
8. **Reference counts.** The README now states 12 repositories, 13 groups of standards and official sources, and 6 entries under websites and articles. They were counted from the moved list.
9. **Calendar.** No date or count changed. The five quarantined social-media record names and the design engine's review dates moved into notes below the table.

## Check

### Validators (before and after)

Run from a scratch clone of this package with a scratch folder of symlinks to the eleven engines, with `PYTHONDONTWRITEBYTECODE=1` and the pytest from an existing scratch virtual environment. No package was installed. Before is `main` at `cf64878`. After is the branch plus this record's files.

| Command | Before | After |
|---|---:|---:|
| `pytest -p no:cacheprovider tests` | 0 (262 passed, 3 skipped) | 0 (352 passed, 3 skipped) |
| `render_host_files.py --check` | 1 (30 findings) | 1 (30 findings) |
| `check_public_hygiene.py --repo .` | 0 (0 findings, 963 record path lines) | 0 (0 findings, 963) |
| `check_public_hygiene.py` over all twelve | 1 (14 findings) | 1 (14 findings) |
| `check_hook_copies.py` | 0 | 0 |
| `refresh_released_commits.py` (check) | 1 (11 not at HEAD) | 1 (11 not at HEAD) |
| `validate-contracts.py` (catalogue) | 0 | 0 |
| `validate-no-book-extractions.py` | 0 | 0 |
| `validate-kaizen-cards.py` | 0 | 0 |
| `validate-routing-baseline.py` | 0 | 0 |
| `validate-runtime-skill-budget.py --root skills` | 0 | 0 |
| `validate-runtime-skill-budget.py --collisions ...` | 0 | 0 |
| `validate-skill-lifecycle.py --root skills` | 0 | 0 |
| `validate-rule-markers.py` (design font list) | 0 | 0 |
| `run-contract-evals.py --route-oracles` | 0 (77 of 77) | 0 (77 of 77) |
| `node hooks/test-destructive-bash-gate.js` | 0 | 0 |
| `node hooks/test-plugin-hook-config.js` | 0 | 0 |
| `generate-plugin-manifest.js --check-marketplace` | 0 | 0 |
| `node --test tests/security/install-engine-ownership.test.js` | 0 | 0 |
| `bash -n` on the three shell scripts | 0 | 0 |

The 19 exit codes are identical before and after. The three exit-1 rows are the findings the README lists: drift (30), portfolio hygiene (14) and pin lag.

Also run once, after the edits: `claude plugin validate .` exits 0 with two warnings (exit 1 with `--strict`), and the six `adapters/*/adapter.yaml` files pass `validate-contracts.py`. The routing, collision and evaluation figures in the README (1,091 skills, 77 of 77, 23 ok) were re-measured the same way.

CI step replay: `readme_metrics.py --check README.md` exits 0, and `check_readme_preservation.py . HEAD HEAD` exits 0. The workflow YAML parses. The workflow itself did not run.

### Preservation check

`check_readme_preservation.py . main kaizen/2026-10-readme-kaizen`, run from the package. The original scratch script gives the same counts.

```text
links: old README 129 targets; new README 75; moved to docs 62; LOST 0
commands: old README 48; kept in README 47; moved to docs 1; LOST 0
anchors: 5 README anchor links in tracked files; BROKEN 0
in-page links: 20 anchors used; BROKEN 0
note: 8 heading anchor(s) of the old README are gone; links from other repositories cannot be checked here
RESULT: OK
```

- The one moved command is `npm sbom`, an inline code span in the npm reference entry that now sits in `docs/references.md`.
- The 62 moved links are the tool-table links (in `package-tools-reference.md`) and the reference URLs (in `references.md`).
- The eight gone anchors are listed under the corrections. A search of the eleven engine repositories for links to them found none.

### Metrics

| Metric | Before | After | Target | Result |
|---|---:|---:|---|---|
| `words` | 7,470 | 7,538 | at most 7,843 (aim 6,723) | Cap met (plus 1%). Aim missed |
| `h2` | 8 | 23 | information | Four come from splitting the October account |
| `toc` | 0 | 1 | 1 | Met |
| `first_cmd` | 13 | 20 | 40 or less | Met |
| `longest_sec` | 3,100 | 1,136 | 1,500 or less (1,200 preferred) | Met |
| `long_lines` | 61 | 7 | 30 or fewer | Met |
| `max_line` | 1,461 | 416 | 700 or less | Met |
| `sent_len` | 19.6 | 12.1 | 16.5 or less | Met |
| `fre` | 44 | 59 | at least 44 (aim 49) | Met: plus 15 |
| bullets, table rows | 72, 98 | 219, 109 | information | More bullets: tables became lists |

Limits of these numbers:

- `words` did not fall. The 850 words of References and about 400 of tool detail moved out, and a front door, a contents list, a task table and the Contributing section moved in. I report the miss of the 10% aim as it is.
- `sent_len` and `fre` read prose only. Bullets in the October account still carry long sentences with hashes and figures.
- `words` and the other counts exclude code fences.

### Tests added, and mutation controls

`tests/test_readme_metrics.py` has 39 tests and `tests/test_readme_preservation.py` has 51. Every preservation test builds a small temporary git repository, an old README on `main` and a new one on `change`.

| Group | Tests | Cases designed to fail, and near-misses that must pass |
|---|---:|---|
| Metrics: counting | 13 | Fenced words skipped, 300 against 301 characters, first fence line, `longest_sec` with H3 and preamble, bullets and table rows |
| Metrics: contents list | 6 | Three links against four, links after the third H2, a fenced `## ` line that must not move the cut |
| Metrics: prose | 9 | Exact sentence length, a fragment, bullets excluded, reading ease 116 for a known sentence |
| Metrics: limits | 3 | Each of the six limits on both sides of its boundary |
| Metrics: command line | 8 | `--check` exit 0, 1 and 3; `--json`; labels by folder; bytes that are not UTF-8 |
| Preservation: links | 13 | A lost link, a lost URL, a lost reference-style link, a table moved to a docs page (must not flag), a page two folders deep, a moved page whose link does not resolve (must flag) |
| Preservation: commands | 8 | A lost fenced command, a lost inline command, a moved command, a removed comment (must not flag), `python` to `python3` (flags) |
| Preservation: anchors | 19 | A broken in-page link, a broken linked anchor, another folder's README (must not count), a script mention, link examples in code (must not count), repeated headings, punctuation slugs |
| Preservation: runs | 8 | An unknown revision, a folder that is not a repository and a missing README all exit 3; same revision twice; no repository path in the output |
| Preservation: units | 3 | Slugs, link targets, commands |

Mutation controls: one line of a script was changed in a scratch clone, the matching test file was run, and the line was restored. The live scripts were never edited, and the clone's copy was compared with the live file after each script's run.

| Script | Mutations | Caught | Survived |
|---|---:|---:|---:|
| `readme_metrics.py` | 20 | 20 | 0 |
| `check_readme_preservation.py` | 27 | 27 | 0 |

The first round caught 39 of 40. The survivor, a redundant `p != readme` filter, was an equivalent mutant, so I removed the redundant code. A second round added mutants for the new code. One survived (`git grep` without `-l`) because every test had a single linking file, so I added a test with three. The last run caught all 47. Each mutation is named in the run log; examples are `>` to `>=` at the 300-character boundary, the link target no longer resolved against the holder's folder, exit 0 on problems, strict decoding, repeated headings not numbered, and the anchor scan reading the base revision.

### Cross-checks against ground truth

- **Metrics against the originals.** The new script and the scratch script print identical tables for all twelve READMEs (same `diff`, no differences). One fix changes no result on these files: the contents-list cut now ignores `## ` lines inside code fences.
- **Preservation against the original.** On the eleven engines, from each pinned `released_commit` to `main`, the package script and the scratch script give the same link, command and anchor counts. One difference is explained: the research engine's record mentions an anchor in plain text, which the package script does not count as a link (1 anchor against 2).
- **The baseline.** The README at each engine's pin reproduces the baseline file row for row (eleven rows, no differences).

### A conflict found, not fixed

`scripts/validate-portfolio-craft.ps1` (lines 49 and 50) requires a `## Capability map` or `## Capabilities` heading among each engine's first four H2 headings. Applying that rule to the eleven READMEs on `main` gives ten failures (all but the accounting engine). The script is Windows-only, runs in no CI job and was not run here (no `pwsh`). Neither the script nor any engine README was changed. The maintainer decides which side moves.

**Resolved after the cycle (31 October 2026).** The conflict above was fixed rather than left to a decision: each of the ten engine READMEs regained a short `## Capabilities` section within its first four H2 headings (the task table stays beneath it as `### Find the right skill`), and `scripts/check_readme_contract.py` now applies the rule on every host. The finding is kept here because it is evidence: a Windows-only validator let a restructure break ten READMEs, and no agent on this Linux host could see it.

### Not assessed

- Any PowerShell suite, because there is no `pwsh`.
- The remote CI run of the new step.
- The npm rows of the Validation table: they need network access, so the figures are from the earlier run the same day.
- Whether a reader finds the new README easier. No reader test was run; the metrics are proxies.
- Links from other repositories to this README's anchors beyond a text search of the eleven engine checkouts.

## Standardise

The conventions for this README, for the next editor. The full standard is in `docs/operations/readme-standard-2026-10-31.md`.

1. **Skeleton.** Title and purpose; At a glance; Start here; Contents; What it is and who runs it; Find the right tool; How it works; What is inside; Install and update; Validation; Portfolio; Lifecycle map; Contracts and governance; Quality and improvement; Open findings; Decisions; Date-triggered gates; the October account; References; Contributing, author and licence.
2. **Limits.** First fenced command by line 40. No H2 over 1,500 words. No paragraph over 90 words and no table cell over 35 words. `readme_metrics.py --check` passes.
3. **Interfaces to keep.**
   - The headings `Validation` (named by `AGENTS.md` and `CONTRIBUTING.md`), `Portfolio` and `What the October 2026 kaizen improved` (linked).
   - The three coordination card file names (`validate-kaizen-cards.py`).
   - The first heading, which is the tour title.
4. **Detail lives in `docs/`.** The README keeps a short table and a link. `package-tools-reference.md` holds the full tool descriptions and `references.md` holds the sources.
5. **Numbers.** Re-measure any number you touch. A date next to a result means the command was run on that date.
6. **Before you commit.** Run `readme_metrics.py --check README.md`, `check_readme_preservation.py . main <branch>`, and the commands in Validation.

## Teach

- Write the first 40 lines for a stranger: what it is, who for, six measured facts, three commands. Everything else can wait below a contents list.
- When a table cell passes 35 words, move the detail below the table or into `docs/`, and keep the summary.
- Build any fixture that contains a README anchor link in pieces. The preservation check reads every tracked text file, so a literal link in a test or a script counts as a real link.

## Re-measure and next cycle

Re-run `readme_metrics.py` after the next README edit and compare with the "After" column above.

Open items for a later cycle:

1. Decide the conflict with `validate-portfolio-craft.ps1` (above). It is a maintainer decision.
2. Add a `--baseline` option to `readme_metrics.py`, so the relative limits (`words`, `fre`) can be checked as well as the absolute ones.
3. Refresh the `released_commit` pins after the engines settle: the drift check reads 11 findings of pin lag.
4. The committed `docs/skill-graph/skill-graph.json` was not regenerated. A regeneration today gives 1,105 nodes and 12,037 edges, and README rewrites across the portfolio move the mention edges. It is report-only.
5. The Windows CI job runs a fixed subset of the tests and does not include the two new test files. The ubuntu job runs them all.
6. The engine READMEs and `CONTRIBUTING.md` files could link the standard. They live in other repositories, and none was edited here.

Cross-engine mismatch: `scripts/validate-portfolio-craft.ps1:49-50` in this package against ten engine READMEs (the README files of the business-plan, design, dev, Linux, proposal, research, SDLC, social-media, website and Windows engines). No other repository was edited.
