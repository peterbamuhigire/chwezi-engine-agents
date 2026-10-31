# Final report: portfolio kaizen pass 2 (31 October 2026)

Chwezi Core Systems coordination cycle, prompt 12 of 12. Scope: this package only; the eleven engines were read, never edited.

## Result

Nine backlog items were kept and none was reverted; one critical finding (the vulnerable MCP lockfile) is escalated because its fix needs
a command outside the one permitted. The cycle's main finding is that the portfolio's own checks assumed one Windows workspace with
catalogue folder names, so on this workstation most of them could not run and the drift they exist to catch went unseen. It added a shared
engine locator and then one check per recurring drift class, each with a control that fails when the check is broken: public-repository
hygiene, the shared hook files (canonical copy named, installed copies compared), `released_commit` pins (with a refresh script that refuses
unsafe trees), catalogue validators, router wording. The catalogue pins themselves were not refreshed, by instruction.

The checks found real exposures in other engines (listed below and in `06`). They did not fix them; fixing belongs to the documentation wave.
Nothing was pushed, tagged, released or sent to a model. The 95 target is not reached and is not claimed.

**Branches.** Started on `kaizen/2026-10` at `edc0a70` (clean tree); work is on `kaizen/2026-10-pass2`, 17 commits after the starting HEAD, this
one included (`git log edc0a70..kaizen/2026-10-pass2`). `kaizen/2026-10` is checked out again at the end. The earlier branch was not modified.

## Scores

Same eleven dimensions and equal weights as the 29 October baseline; reviewer judgements against named evidence (inference), not
measurements. Published figure is `min(raw, 65)`.

| Dimension | 29 Oct baseline | Pass-2 baseline | Final | Evidence for the movement and what is still short |
|---|---:|---:|---:|---|
| Doctrine and philosophy | 65 | 62 | 66 | The router names no workstation path; one path-free wording for three managed sentences; the canonical hook copy and its update procedure are written; the supply-chain policy no longer claims checks the workflows lack. Still short: the bridge-contract dispositions D1 to D5 are unratified. |
| Taxonomy and structure | 60 | 56 | 61 | Former folder names are catalogue aliases; validators refreshed for six engines and checked against engine manifests; suite counts drift 2 to 0; pin lag now visible. Still short: 11 of 11 pins lag until the last step; 21 engine-side drift findings. |
| Skill depth and rigour | 55 | 56 | 60 | Six new checks with 101 tests and 27 single-line mutations (two survivors, each fixed with a new test); the MCP tool no longer calls an unstartable validator a failure. Still short: CI is unproven until a push. |
| Worked examples and applied proof | 40 | 40 | 42 | Live runs of every new check across the twelve repositories are recorded; two validated handoffs (one ends blocked on a draft register entry). Still short: no executed behavioural grading. |
| Standards currency | 40 | 40 | 44 | MCP specification `2026-07-28`, npm versions and the Codex manifest layout read from primary sources; the rest reported by a delegated read. Still short: SDK pin stale and affected (escalated), Codex manifest is the fallback layout, nothing acted on in the hosts' formats. |
| Output readiness and coverage | 40 | 40 | 44 | Every portfolio script now resolves all 12 engines on this host's layout; the graph script runs. Still short: union metadata 290,189 characters against a 60,000 budget (engine-side). |
| Accessibility and inclusivity | 45 | 45 | 45 | Not worked on. |
| Production, handoff and release | 35 | 34 | 40 | MCP tests 18 of 18 on any branch; CI runs every test file and the hook tests; release calls validate; a one-command pin refresh. Still short: no remote CI run, `release/manifest.json` and the MCP package say 1.0.0 against 1.1.0, no provenance manifest or signing. |
| Redundancy and hygiene | 45 | 40 | 48 | Package-side path findings 7 to 0; suite marketplace drift 2 to 0; portfolio hygiene check exists. Still short: 19 live hygiene findings in five engines, 21 engine-side drift findings, 27 duplicate skill names. |
| Discovery and routing | 45 | 37 | 37 | Stand-in readiness unchanged (p@1 31 of 42, no new fixtures); the strict figure rose from 19.4 to 25.4 because the coordinator's declared validators now pass 3 of 5. |
| Safety and integrity | 35 | 36 | 42 | Portfolio-wide scan for settings, env and key files and credential shapes (none found); hook copies verified identical; unstartable validators are `NOT ASSESSED`. Still short: F-01 critical lockfile finding open; two tracked settings files in public repositories (engine-side, history untouched). |

**Raw sum 529, raw mean 529 / 11 = 48.09; published `min(48.09, 65) = 48.09`.** Pass-2 baseline 44.18 (486 / 11). The 29 October scorecard
printed 46.82, but its rows sum to 505 (45.91), so the corrected comparison is 45.91 to 48.09. There was no 29 October final (the cycle stopped
after its second commit). Target 95 is a target, not a forecast. F-01 overrides the aggregate.

## Kept changes

| ID | Commit | Change |
|---|---|---|
| K1 | `eb8dae1`, `9329a82` | Engine locator, catalogue aliases, `--engines-root`; graph script fixed |
| K2 | `5d7dbc8`, `2259900` | Portfolio public-repository hygiene check and policy |
| K3 | `0d539fa` | Canonical hook copy named; repository and installed copies compared; fourth file registered |
| K4 | `2af312e` | `released_commit` refresh script and pin-lag rule |
| K5 | `608f466` | Catalogue validators refreshed; validator drift rules |
| K6 | `d4450f7` | Path-free router wording, router rules, `--render-router-blocks` |
| K7 | `0267684` | MCP discovery test branch-independent; unstartable validator is `NOT ASSESSED` |
| K8 | `6763854` | CI runs every test file and hook tests; release calls validate; policy corrected |
| K9 | `f099c75` | Suite marketplace counts |
| Teach | `903243e` | Router and changelog |
| Evidence | `39ee3a1`, `c887dfa`, and the closing commit | Baseline, backlog, and files 03 to 06 |

Reverted: none. Escalated: F-01.

## Critical defect

**F-01, vulnerable MCP lockfile (carried from 29 October).** 13 packages (6 moderate, 6 high, 1 critical; the critical one is transitive and
sits behind the HTTP transport the stdio server does not import; `zod`, also flagged, is used by the SDK at run time and its exposure was not
assessed). The SDK pin 1.30.0 is behind 1.32.2, which the registry shows was published 2026-10-23. Not fixed: it needs
`npm install` of two minor versions, and only `npm ci --ignore-scripts` was permitted. Exact command and acceptance in `06`.

## Portfolio table

Scores are taken from each engine's own `05-final-report.md` (raw, rounded as the engine printed them); capped is `min(raw, 65)`. Linux is the
only engine the cap binds. "29 Oct" is the first cycle on 29 October (its stricter initial cap of 45 was a presentation override and is not shown).
Business Plan's 29 October baseline is its reassessed 42.5 (it first printed 60.0).

| Engine | 29 Oct before | 29 Oct after | Pass-2 baseline | Pass-2 final (raw) | Pass-2 final (capped) | Open P0 items | Open handoff mismatches (ids below) |
|---|---:|---:|---:|---:|---:|---|---|
| Accounting Doctrine | 51.5 | 57.3 | 56.4 | 58.2 | 58.2 | None labelled. Statutory values (Uganda LST, WHT, VAT threshold, PAYE, EFRIS) remain `draft` and block final output; seven drafts overdue; decision D5 | M1, M6, M7, M8 |
| Digital Research | 52.1 | 58.2 | 56.3 | 59.5 | 59.5 | None labelled. Archive snapshots for live-source verification (release-evidence blocker); provenance lines D-13; the unbound `political` target | M2, M9, M10, M11 |
| Dev engine | 46.5 | 59.5 | 55.0 | 62.5 | 62.5 | None labelled. Tracked local settings file (D-13, history) | M6, M12 |
| Design engine | 54.0 | 59.0 | 56.9 | 60.3 | 60.3 | None labelled. Critical H-1 (download paths and acquisition-site names) repaired in the tree, still in public history | M3, M4, M6, M7, M13 |
| SDLC documentation | 50.28 | 53.98 | 52.18 | 55.68 | 55.68 | None labelled. Critical D-01 (tracked settings file) repaired in the tree, still in public history; six owner decisions | M4, M14 |
| Linux | 50.5 | 74.0 | 70.1 | 75.6 | **65.0** | None labelled; P1 first. Decision: installed copies on this workstation are stale | M4, M6, M16 |
| Windows administration | 49.3 | 57.9 | 56.7 | 59.5 | 59.5 | None labelled; P1 first (service-state window and authority are text only; no Windows run). Source rows lapse 2026-11-10 | M4, M7 |
| Proposal | 53.0 | 58.5 | 54.5 | 61.4 | 61.4 | None labelled; P1 first (no real solicitation; PPDA e-GP, thresholds, AfDB, UNDP, PRAG unverified) | M4, M12, M15 |
| Business plan | 42.5 | 49.0 | 44.0 | 50.0 | 50.0 | **P0: rebuild the projection workbook (needs `xlsxwriter`); P0: make the recalculation report part of the release gate** | M4, M5, M8, M10, M15 |
| Website | 55.5 | 60.0 | 55.7 | 62.9 | 62.9 | **P0: re-sync the vendored detector (3 byte drifts confirmed here); P0: Lighthouse CI dependency tree; P0: lab LCP of a font-using site** | M3, M4 |
| Social media | 58.5 | 58.5 | 58.2 | 60.0 | 60.0 | None labelled. Five quarantined source records still fail the freshness gate (a release blocker) | M1, M4, M6 |
| This package | 45.91 | none | 44.18 | 48.09 | 48.09 | F-01 (escalated) | none |

Mean of the eleven engines: pass-2 baseline 56.0, final 60.5 raw and 59.5 capped. Every engine rose from its pass-2 baseline. Several
baselines sit below their 29 October final because the fresh pass measured things the first did not (each engine says so); neither
column is a trend line on its own.

## Handoff mismatches still open

Confirmed this cycle by running a check or reading both sides (V), or reported by an engine and not re-checked here (R). Files and fixes are in `06`.

| ID | Mismatch | State |
|---|---|---|
| M1 | Windows checkout paths in the managed router sentences of accounting (2) and social (3) | V |
| M2 | Research's standard and currentness gate still name a workstation path (`...standard...md` line 76, `...currentness-gate.md` line 52) | V |
| M3 | Website's vendored design detector differs from the design engine in three files | V |
| M4 | 16 shared-asset variants unregistered and one design `install.sh` drift across business-plan, dev, SDLC, proposal, linux, windows, website, research, social, design | V |
| M5 | Business-plan manifest exclusion `country-context/*` matches nothing | V |
| M6 | Public-repository hygiene: tracked settings (dev, Linux), 17 live path lines (Linux 10, social 3, accounting 3, design 1) | V |
| M7 | Accounting and design manifests do not register the checks their pass 2 added (the catalogue now does) | V |
| M8 | Business plan restates Uganda rates as plain facts while the accounting register entries are `draft` | R |
| M9 | Research's register validator cannot read other engines' register schemas | R |
| M10 | Research's canonical scanner cannot scan another engine by path; its degraded-mode pattern misses `not-assessed` | R |
| M11 | Oracle `055` expects the dev engine's `validation-contract`; research holds a near-duplicate; the `political` fixture target is unbound | R |
| M12 | Sibling lookups by hard-coded names in dev and proposal tests (the locator here can replace them) | R |
| M13 | Hard-ban font list parity across routers was never compared (secondary list was) | R |
| M14 | Three SDLC owned negatives are `NOT_ASSESSED` locally and belong in the union | R |
| M15 | Proposal narrative pricing versus business-plan financial model; SDLC figure-render handoff unproven | R |
| M16 | Linux and dev: "package branch, not upstream stable" wording for Nginx; Windows, Cisco and BIND register rows sit in the dev register | R |

## Engine Eval Readiness (recheck)

The 29 September corrected figure of 37.1 and the 29 October upper bound of 37.38 both used the stand-in for Tier 1. Recomputed: stand-in
37.4 (unchanged: p@1 31 of 42, no new fixtures, Tier 3 zero); strict 25.4 (T1 3 of 5). Twelve acceptance prompts: primary 2 of 12 (unchanged),
engine-level 5 of 12 (was 6 on 29 October; two ranks moved after engine descriptions changed). Twenty fresh requests: primary at rank 1 in 6 of
15 single-engine requests, both engines in the top five for 2 of 5 two-engine requests. All lexical; none is live routing.

## Portfolio calendar of date-triggered failures

Sources are the engines' own records unless marked (V). "Now" means the check fails today.

| Date | Engine and effect |
|---|---|
| Now | Social: freshness gate exits 1 on five quarantined records (`UG-DPPR-2021`, `UG-COPYRIGHT-2026`, `KE-DP-GENERAL-2021`, `RW-DPP-2021`, `ITU-INTERNET-USAGE`). Business plan: CI evidence step exits 1 on four stale rows. Accounting: seven draft entries overdue (LST since 2026-10-27); reported by its Python tool, not its gate. This package: the drift check exits 1 (V); the portfolio craft standard (review 2026-10-04) and domain prompt contract (2026-10-16) are overdue for review (V) |
| 2026-11-03 | Dev: Next.js security notice to be re-read; its register record stays `NOT_ASSESSED` until then |
| 2026-11-05 to 11-07 | Windows re-audit (before any fleet change); Linux re-audit |
| 2026-11-10 | Windows: 35 source rows reach 90 days; PowerShell 7.4 and 7.5 support ends (the dev register carries the same dates); Windows 11 23H2 Enterprise servicing ends |
| 2026-11-11 | **Windows: `check_source_register.py` starts to exit 1** unless rows are re-verified |
| 2026-11-12 | PostgreSQL 14 final release (dev register; Linux provisioning example) |
| 2026-11-27 | Research re-audit (earlier than 11-30 on purpose) |
| 2026-11-29 | SDLC: first source review dates pass; its register check then fails in CI. Research: four OpenAI platform records reach their review date |
| 2026-11-30 | **Proposal: `validate_skills.py` fails by design** until its volatile register is renewed. **Research: the register gate fails** `validate_engine.py` and CI (four OpenAI platform records; two more on 2026-12-01). Business plan: Bank of Uganda policy-rate row due. Dev: OpenAI Evals and `v1/prompts` shutdown. Website, social, SDLC monthly re-audits |
| 2026-12-28 | Dev: model comparison due |
| 2026-12-29 | Accounting re-audit and Uganda and IFRS rechecks; design targeted recheck; 103 records in this package dated 2026-12-29 (shared-asset rows, ownership pairs, security registers, hygiene policy) fall due for review (V) |
| 2027-01-27, 2027-01-31 | Design full re-audit; website full audit |

## Residual risk

- The new rules make pre-existing defects visible, so the drift check and the portfolio hygiene check exit 1 until the engine-side work and the pin refresh land. That is the intended signal, not a regression.
- The pin-lag rule fails locally after any engine commit (default allowance 0); in a shallow CI clone it is skipped. Set `--pin-lag-max` if a standing allowance is wanted.
- The hygiene check recognises the patterns in its docstring only. It found no credential-shaped string, which is not proof that none exists, and a user name is caught only on the paths and the one private name in its policy.
- CI edits, the full pytest run, the PowerShell suites and every host install are unproven here.
- Routing evidence is lexical; the expectations for the twenty requests were written by the cycle author.
- The suite marketplace counts and the pins will move again when the Linux and documentation waves land.

See `06-next-cycle.md` for the exact commands, the decisions needed and the one small experiment.
