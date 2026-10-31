# Scope and evidence: portfolio kaizen pass 2 (31 October 2026)

Chwezi Core Systems coordination cycle, prompt 12 of 12, run last. This is a continuation of the 29 October cycle
and uses the eleven engine pass-2 cycles as input. Nothing here was pushed, tagged, released or sent to a model.

## Repository state at the start

| Item | Value |
|---|---|
| Repository | `chwezi-engine-agents` (router: `AGENTS.md`) |
| Starting branch | `kaizen/2026-10` (two commits ahead of `origin/main`, no upstream) |
| Starting HEAD | `edc0a70` ("reject foreign drive paths in C2 fixture bounds") |
| `git status --porcelain` at start | 0 lines (clean tree, no foreign files) |
| Working branch | `kaizen/2026-10-pass2`, created from that HEAD |
| Branch to restore at the end | `kaizen/2026-10` |

## What the 29 October cycle did and did not finish

`docs/kaizen/2026-10-engine-kaizen/` holds only `00`, `01`, `02` and an `evidence/` folder; there is no `03` to `06`.

| 29 October item | State found now |
|---|---|
| Frozen baseline (raw 46.82, eleven dimensions) | Done and kept as the prior baseline. |
| C2 fixture-path boundary (P0) | Done in `edc0a70`; the previously failing negative test passes (stand-in run, see `04-validation-record.md`). |
| C1 vulnerable MCP dependency lock (P0) | Not done. `npm audit` still reports the same 13 packages (6 moderate, 6 high, 1 critical). Escalated here, see `02`. |
| C3 Codex identity, C4 CI and release claims, C5 shared-asset hashes, C6 pins, C7 portable router, C8 routing and handoff proof, C9 closure | Not done; the cycle stopped after C2. The portions still open are re-measured below and carried into `02`. |
| Final report and next-cycle record | Never written. |

The earlier plan said "no release tag after 130 commits". That is no longer true: tag `v1.1.0` (8c1df8b, 2026-09-29) exists.
It is local knowledge only; whether it is on the remote was not checked.

## Where every engine is

All eleven engines are clean (0 porcelain lines) on local `main` with their pass-2 branch fast-forward-merged and nothing
pushed. HEADs are in [`evidence/engine-heads-baseline.txt`](evidence/engine-heads-baseline.txt). The private `political` engine is not
installed on this host and is recorded `NOT_ASSESSED`; it was not searched for. Each engine's 29 October and pass-2 final
reports were read (`05-final-report.md` and `06-next-cycle.md`); the portfolio table is in `05-final-report.md`.

Engines live under two parents on this host (`~/skill-engines/` and `~/.claude/skills/`) and four carry pre-rename directory
names (dev engine in `skills-web-dev`, design in `design-system-skills`, SDLC in `srs-skills`, research in
`chwezi-research-engine`), while this package assumes one workspace folder with catalogue names. A scratch workspace of
symlinks and a git-archive copy of each HEAD were used to run the portfolio scripts; neither is committed. `skill_graph.py`
cannot run against a symlinked or two-parent layout at all (it resolves each engine root, then calls `relative_to` on the
unresolved workspace root and raises `ValueError`); `skill_fanin.py` ran on the symlinked layout. This is finding F-04 below.

## Inputs from the orchestrator, each checked before use

| Input | Verdict | Evidence |
|---|---|---|
| Catalogue validator lists are stale | **Confirmed** for windows (unit tests and source-register gate missing), website (six of eight manifest commands missing), accounting and design (new checks are in no manifest or catalogue; design's CI runs 14 commands the catalogue lacks). Also proposal (`git diff --check`) and research (register gate) differ. | `evidence/baseline-18-validators-vs-manifests.txt`, engine CI files, engine `06` records |
| `released_commit` lags every engine | **Confirmed**: 11 of 11, 28 to 51 commits behind each, 451 in all; every pin is still an ancestor of HEAD. | `evidence/baseline-12-measures.txt` |
| Router blocks carry Windows paths or pre-rename names | **Partly confirmed.** Windows paths remain in accounting (`AGENTS.md` lines 56, 145), social (lines 47, 60, 443) and this package (line 14). Research, business-plan, SDLC, Linux and website no longer carry them at HEAD. No pre-rename engine name occurs in any engine's `AGENTS.md`, `CLAUDE.md`, `README.md`, manifest or plugin files; they survive only in the design and accounting `integration/` migration records. | `git grep` over the eleven checkouts, 2026-10-31 |
| Hook copy: which is canonical | **Established**: this package (`catalog/shared-assets.yaml`, row `hooks-destructive-bash-gate`, owner `chwezi-engine-agents`). All 11 engine copies, 7 Claude plugin-cache copies, one synced `writing` plugin copy and one trashed copy have the same SHA-256 (prefix `0b1465ca`). The register check already covers the 11 repository copies and passes; nothing covers installed copies and no document names the canonical file. | `04-validation-record.md` |
| Three engines track `.claude/settings.local.json` | **Two of three**: dev engine and Linux still track it. The SDLC engine untracked it in its pass 2. | `git ls-files` in each checkout |
| Date-triggered failures | **Confirmed**, see the calendar in `05-final-report.md`. | engine `06` records |
| Engine Eval Readiness 37.1 and twelve acceptance prompts | Recomputed in `01`: p@1 31/42 including three known defects, acceptance primary 2 of 12 (unchanged), acceptance engine-level 5 of 12 (was 6). | `evidence/baseline-oracles-summary.json` |

## Observation: twenty requests and two handoffs

Twenty realistic requests (15 single-engine, 5 two-engine; every engine at least once) were written with the expected owner
fixed before any routing was run, then ranked by the lexical proxy over the union of 1,092 skills
([requests](evidence/routing-20-requests.json), [results](evidence/routing-20-lexical-results.txt)).

- Single-engine: primary skill at rank 1 in 6 of 15; owning engine at rank 1 in 10 of 15. Worst ranks: the PRD request ranks its
  owner 691st (the proxy places the accounting engine's school pack first), the social calendar 53rd, the font request 17th,
  the website request 14th.
- Two-engine: both expected engines in the top five for 2 of 5.
- This is a lexical proxy, not live routing. The expectations were written by the cycle author, who also read the skill list, so
  they are a practitioner judgement and not an independent oracle. No model call was made.

Two handoffs were followed by reading the files each leg names and were recorded as
[research to accounting](evidence/handoff-1-research-to-accounting.yaml) and
[SDLC to development](evidence/handoff-2-sdlc-to-dev.yaml). Both validate against `schemas/handoff.schema.json` using a
stand-in validator (`jsonschema` is not installed; the stand-in covers `type`, `const`, `required`, `properties`,
`additionalProperties`, `items` and `minLength` and rejects the repository's invalid fixture). Every file a record names was
confirmed to exist at the engine's HEAD. Handoff 1 ends blocked: the accounting register entry `UG-VAT-REG-THRESHOLD` is `draft`.
One claim from an engine report (a dev-engine alias prefix mismatch) was checked and not accepted as a blocker: the alias file
declares `external_target_prefixes`, so those targets are name-resolved.

## Confirmed defects and findings at baseline

| ID | Severity | Finding | Evidence |
|---|---|---|---|
| F-01 | Critical (carried) | MCP lockfile: 13 vulnerable packages, one critical (`proxy-addr`, transitive). The SDK pin 1.30.0 is behind `latest` 1.32.2 and six advisories affect 1.30.0. The server imports only the stdio transport, so HTTP-path advisories are probably unreachable (inference); `zod` is used by the SDK at runtime and its exposure was not assessed. | `evidence/baseline-17-npm-audit-summary.json` |
| F-02 | Major | `mcp-server/tests/discovery.test.ts` asserts the branch is `main`, so `npm test` fails (15 of 16) on any other branch. | `evidence/baseline-15-npm-test-summary.txt` |
| F-03 | Major | Drift check: 21 findings (8 on 29 October): 16 unregistered shared-asset variants, four byte drifts (three in website's vendored copy of the design detector, one design `install.sh`), one stale plugin exclusion. Suite marketplace counts are stale for business-plan (134, plugin lists 137) and design (101, lists 102). | `evidence/baseline-0-render-check.log`, `baseline-9-marketplace.log` |
| F-04 | Major | The portfolio scripts assume one workspace folder with catalogue names; this host has two parents and four renamed folders. `skill_graph.py` crashes on a symlinked layout (`ValueError` from `relative_to`). | log in `04` |
| F-05 | Major | Public-repository hygiene: dev and Linux track `.claude/settings.local.json`; about 1,630 machine-path lines in tracked text across the twelve repositories (mostly dated records; 877 of them in this repository); real user-profile paths in design and accounting `integration/` records. No check scans for any of this portfolio-wide. | `evidence/baseline-12-measures.txt` |
| F-06 | Major | CI runs 12 of 19 Python test files and none of the hook JavaScript tests (61 and 7 assertions, both pass locally). `unittest discover` silently collects zero tests from five plain-function test files. | `validate.yml`, `evidence/baseline-3-unittest-summary.txt` |
| F-07 | Major | `docs/security/supply-chain-policy.md` says the release workflow runs adapter, installer, security and secret-scan checks; `release.yml` runs the catalogue schema check, contract evals and the MCP build and tests only. `release/manifest.json` says 1.0.0, plugin manifests 1.1.0, the MCP package 1.0.0. | `release.yml`, `release/manifest.json` |
| F-08 | Minor | `AGENTS.md:14` and `scripts/skill_usage_scan.py:261` carry `C:\wamp64\www`; `scripts/validate-portfolio-craft.ps1` defaults to it. | `git grep` |
| F-09 | Minor | Lexical routing drifted: acceptance engine-level hits fell from 6 to 5 of 12 after engine descriptions changed in pass 2. | `evidence/baseline-oracles-summary.json` |

Portfolio measures at baseline (details in `01-baseline-scorecard.md`): union metadata 290,189 characters against a 60,000
budget; 27 skill names duplicated across engines (all cross-engine, none within one engine); union collisions 15 pairs at
0.75 or above with none undeclared; dangling cross-engine skill references 0 (14 stale intra-engine "moved from" paths in
social and website); `released_commit` lag 11 of 11.

## Environment limits

No `pytest`, `jsonschema`, `pwsh`, WSL or paid model call. Five plain-function test files and two pytest-only files were run through
a labelled stand-in runner (not pytest; not committed); real pytest results are `NOT_ASSESSED`. `npm ci --ignore-scripts` was run
inside `mcp-server/` only (lockfile present, `node_modules/` gitignored); nothing else was installed. Host hooks blocked one
recursive deletion in the scratch folder during the cycle; it was not retried or worked around.
