# Kaizen 2026-09-29 — my-10-kaizen (M10-00 to M10-14)

Record of the my-10-kaizen operation: the actionable, still-unadopted mechanisms of ten public skill repositories, absorbed as patterns into the Chwezi engines without installing the packs and without repeating earlier Kaizen work. Plan package: `C:\Users\Peter\Documents\my-10-kaizen\` (local only). Running log: `m10-kaizen-execution-2026-09-29.md`. Evidence: `m10-kaizen-evidence/M10-00/` … `M10-14/`. This record is append-only; corrections are dated addenda.

## 1. Scope and dates

- **Dates.** Planned and executed on 29 September 2026 (the font ruling was committed at 28 Sep 23:10 UTC; the last phase push at 29 Sep 04:06 UTC; M10-14 close-out the same day).
- **Phases.** M10-00 mobilisation; M10-01 stop-the-line defects; M10-02 host-file single source and drift control; M10-03 Tier-2 routing evaluation and collision gate; M10-04 skill-authoring convergence and vetting; M10-05 Tier-3 behavioural harness; M10-06 dev methodology and comprehension; M10-07 SRS verifiable diagrams; M10-08 SRS elicitation, as-built recovery and test design; M10-09 design slop detector and doctrine refresh; M10-10 design data, retrieval and critique vocabulary; M10-11 website truthful gates, minimalism and intake; M10-12 portfolio context contract, engine tours and skill graph; M10-13 cross-engine extensions; M10-14 measured re-audit and close-out.
- **Repositories (12).** chwezi-engine-agents, chwezi-dev-engine, design-system-skills, srs-skills, website-skills, digital-research-engine, proposal-skills, business-plan-skills, social-media-skills, linux-skills, chwezi-accounting-doctrine, windows-admin-engine-skills. The private political-essay-skills engine was out of scope and never read.
- **Source repositories (patterns only, paraphrased with attribution).** obra/superpowers (MIT, `8ca22db`); DietrichGebert/ponytail (`e3ba2aa`); nextlevelbuilder/ui-ux-pro-max-skill (MIT, `09170ee`); Graphify-Labs/graphify (Apache-2.0, `d6eaa8a`); JuliusBrussee/caveman (licence NOASSERTION); addyosmani/agent-skills (MIT, `2686b62`); Egonex-AI/Understand-Anything (`b05cc3b`); ComposioHQ/awesome-claude-skills (no root licence); tt-a1i/archify (`0e4949f`, `v3.0.1`); pbakaus/impeccable (Apache-2.0, `114ea1d`). Licences and pins of record are those in `01-repo-reports/` of the plan package, `third-party-tool-dispositions-2026-09-29.md` and each phase's attribution lines.
- **Standing rules.** Zero spend (every model-executed cell `NOT_ASSESSED`); no new active dev skill (167 held); British English; no book extractions; no copied third-party text; push to public `main` after three accepted phases unless a recorded deviation applies.

## 2. Baseline

- M10-00 snapshot: `m10-kaizen-evidence/M10-00/baseline-snapshot.json` (SHA-256 `7b61d10f…6f4f00`); close snapshot and diff: `M10-14/close-snapshot.json`, `M10-14/close-snapshot-diff.md`.
- Roadmap §5 baselines (29 Sep 2026): dev CI red for 12 consecutive runs; 18 of 691 SRS `.docx` files with raw Mermaid; 23 undeclared cross-engine pairs ≥ 0.75; 1 engine (partial) with owned negatives; design p@1 85 %; no Tier-3 harness; 4 of 12 thin `CLAUDE.md` bridges; 0 executable slop rules; banned-font copies drifted in 3+ versions; 7 silently drifting `skill-writing` copies.
- Scores before: the dev 2026-09-06 scorecard withheld an overall score (taxonomy 52, standards currency 50, local 65 cap); the website overall was `NOT ASSESSED` with a cap of 65; routing was one third of a 10 % hygiene bucket and was never measured.

## 3. Decisions

| Decision | Record | Authority |
|---|---|---|
| D1 Superpowers: absorb, keep optional, upgrade 4.3.1 → 6.4.2, telemetry off (SP-02) | `third-party-tool-dispositions-2026-09-29.md`; log M10-00 T06 | Peter (SP-02 approved) |
| D2 Understand Anything: reject estate-wide; bounded pilot deferred (UA-01) | dispositions | orchestrator under delegation |
| D3 Archify: reject estate-wide; rebuild the pattern in SRS (AR-18) | dispositions | orchestrator under delegation |
| D4 Graphify: rejected for this host; P06 stands (GR-13) | dispositions; P06 addendum in `skills-kaizen-execution-2026-09-26.md` | orchestrator under delegation |
| D5 UI UX Pro Max: no install, no data reuse; provenance undetermined, attributed as a precaution (UX-15) | dispositions; `design-system-skills/docs/continuous-improvement/design-catalog-provenance-2026-09-29.md` | Peter's stated position |
| D-M10-01: stop-the-line repairs may be pushed ahead of the three-phase gate | log M10-00 T12 | Peter |
| Font ruling: Fraunces and all IBM Plex hard-banned (HOUSE), replacements by role | log M10-00 T09 | Peter (design authority) |
| Watchlist ruling: ten faces with ≥ 2 independent AI-tool sources moved to the secondary ban (Newsreader, Cormorant, Crimson Pro, Plus Jakarta Sans, Instrument Sans, DM Sans, Outfit, Playfair Display, Lora, Space Mono); trigger block v3 | M10-09 evidence; design `7a2ab6b` | orchestrator under delegation (M10-09) |
| AC-03: vetting register and intake rule for third-party skills | M10-02 / M10-04 evidence; `docs/security/third-party-skill-register.json` | orchestrator under delegation |
| PT-04: versions at 1.1.0; tags only with release authority | `docs/distribution.md`; M10-02 T08 | tags await Peter |
| AO-14: Engine Eval Readiness sub-score, `NOT_ASSESSED` = 0, routing capped at 50 without harness output | dev `skill-engine-audit/references/scoring-rubric.md` (M10-14) | **Peter's ratification required** |
| Zero-spend rule | roadmap §3 | Peter |

## 4. Per-engine findings and changes (commits per phase)

Commit subjects name the phase; the full list is `git log <M10-00 HEAD>..HEAD` per repository. Push events are in §10.

| Phase | Commits |
|---|---|
| M10-00 | agents `4c187d1` (log, evidence tree, dispositions, change-class matrix); design `a77ad8f` (UX-15 provenance) |
| M10-01 | dev `6941e08`, `b3161da` (CI repair, hygiene); srs `15422d7`, `905b9a4` (Mermaid rendered before Pandoc, `.docx` guard, 18 documents regenerated); website `75bc5c9` (truthful slop-gate docs, brand-alignment route); design `f69c5d4`; DRE `d4a613d` (Impeccable record at `114ea1d`); trigger block v2 in bp `2b41c08`, linux `9de82cf`, proposal `ba94f15`, social `724970f`; agents `c0caf8d`, `9510270` (validator lists, eval fixtures) |
| M10-02 | thin bridges and preservation maps: design `655d983`, srs `f8ce9fa`, website `442290f`, `26677c5`, DRE `2aa54bc`, bp `7b21210`, social `52399fc`, linux `42b3c1b`, proposal `ead7a38`, finance `a209c26`, windows `b1100c5`, dev `33574d9`; agents `35340f6`, `3ca32b6` (`render_host_files.py`, `shared-assets.yaml`, marketplace check, 1.1.0) |
| M10-03 | agents `5a9153f` (union collision gate, ownership register, 42 route oracles, 12 acceptance cases, ratchet, `findings[]`); owned negatives and floors: dev `ca226ae`, design `3b7c980`, srs `702a5ab`, website `488efc8`, DRE `d2fdf57`; mirrors bp `8919b72`, linux `e8d10a7`, proposal `1f18b87`, social `9b11fbf` |
| M10-04 | dev `317b475` (canonical `skill-writing`, pressure testing, safety gate items 9–11); pointer stubs: website `0fecec9`, DRE `95f69ea`, bp `5f5e17d`, social `5d955fc`, linux `c70b73b`, proposal `86996f4`; design `34a5ab2`, srs `9b8a27f` (byte warning); agents `fe10a45` |
| M10-05 | agents `5ef3019` (Tier-3 runner, isolation self-test, scoring rule); dev `0a799d8` (F01–F16 materialised with adversarial checkers); DRE `f76c818` (evidence-rung rule) |
| M10-06 | dev `65e3315` (methodology and comprehension absorption; 36 orphan payloads merged); agents `3a7ece3` |
| M10-07 | srs `6218681` (typed diagram IR, trace checks, baseline delta, figure manifest); design `68f373b`, `34a5ab2`; agents `0f62e27` |
| M10-08 | srs `360854a` (elicitation gate, as-built recovery, staleness, pairwise design); dev `1e87460`; agents `c74d73a` |
| M10-09 | design `3fe84a6` (chwezi-slop detector, 49 rules, hooks); DRE `20564b8` (K5 AS1–AS7 re-audit); website `3c9fdca`; dev `4121093`; agents `bb6dec1` |
| M10-10 | design `dab2b6e` (doctrine lint, BM25 with abstention, cited records, visitor modes); agents `48af46b` (retrieval metrics); dev `e0466ba` |
| M10-11 | website `7ad522b` (slop-scan over the vendored detector, minimalism, intake, Lighthouse route); agents `6c65f6c`, `8063bd5` |
| M10-12 | agents `ea7ecbb`, `e7c36a8` (PROJECT.md contract and doctor, engine tours, fan-in, report-only skill graph); router pointer in all eleven engines (`dec6bd9`, `2315408`, `0da72de`, `88d2af4`, `eaa53c1`, `fbde091`, `29d6aa3`, `f9b9067`, `30ac859`, `d2d013c`, `243221f`); graph-defect fixes dev `c29972d`, srs `5f58f11`, website `ec72bca`, DRE `2b9c87d`, proposal `07722b6`, bp `8949387`, social `09eebe7` |
| M10-13 | proposal `3e4330d`, `5de27f8`; finance `af2af30`; DRE `340b200`; bp `d84a599`; srs `fa85fba` (renderer follow-up); agents `2500c89`, `8a438c9` |
| Outside the phase tags | watchlist ruling and trigger block v3 in all twelve (`7a2ab6b`, `5b3e72a`, `20ca40c`, …); README "Capabilities" heading repairs; dev alias fixes `9fd98a9`, `67ae982`; design Gantt guidance `25ce1e6` |
| M10-14 | dev rubric extension and worked example; agents evidence, this record, log close; six audit folders — commits pending the orchestrator |

Headline changes by engine: dev CI green again and the rubric now measures routing (pending Peter's ratification of the AO-14 change); SRS builds render Mermaid to figures and refuse raw Mermaid; the design engine owns an executable 49-rule slop detector; website gates report only what they check; every `CLAUDE.md` is a checked bridge and shared files are drift-checked; cross-engine routing has an ownership register and a ratchet; a Tier-3 harness exists and has proven it can fail without a model.

## 5. Validator and harness evidence (final run, 29 Sep 2026)

| Command (location) | Result |
|---|---|
| `python -X utf8 scripts/kaizen_portfolio_snapshot.py …` ×2 (agents) | identical digests; 1,174 raw public `SKILL.md`; all 12 repositories clean |
| each `catalog/engines.yaml` validator in its engine root (`readiness/run_tier1.py`) | 27 declared: 26 pass, 1 `NOT_ASSESSED` (linux `bash scripts/tests/check-distro-matrix.sh` on Windows) |
| `validate-runtime-skill-budget.py --collisions --ownership evals/routing/ownership.yaml --format json` | PASS, exit 0; 1,169 skills; 21 cross-engine pairs ≥ 0.75, 0 undeclared; 24 within-engine pairs (reported) |
| `evals/runners/run-contract-evals.py --route-oracles --workspace-root .. --min-oracle-primary 74` | exit 0; contract cases 77/77; oracle primary@1 30/39 (76.9 %), engine@1 84.6 %, must_co_activate@5 3/4; acceptance lexical primary@1 2/12 |
| `validate-routing-baseline.py` | PASS (5 engines + portfolio) |
| routing smoke tests with floors and `--lint-fixtures` (dev 88, design 92, srs 83, website 92, research 84) | all exit 0; lint 0 findings |
| `render_host_files.py --check --workspace-root .. --json` | 12 repositories, 0 findings, 0 not assessed |
| `generate-plugin-manifest.js --check-marketplace --workspace-root ..` | 23 ok, 0 drift |
| `validate-no-book-extractions.py`; `validate-kaizen-cards.py`; `validate-catalog.ps1` | PASS (roots 12, findings 0); PASS; 11 unique engines |
| agents `pytest tests` | 162 passed |
| dev guardrails / contract gate / compliance / pytest | 0 errors / 0 errors / 136 of 165 / 207 passed, 3 skipped |
| design `node --test tools/slop-detector/test/`; `--validate-registry`; `--doctrine-consistency` | 116 pass, 1 skipped; PASS 49 rules; 0 conflicts |
| srs `check_docx_diagrams.py --scan projects --exclude _kaizen,render-runs`; malformed `build-doc.sh` | 0 of 691 with Mermaid, 2 missing figures (exit 1); malformed build exit 1, no `.docx` |
| dev `benchmarks/solution-selection/materialised/run_selftests.py` | PASS 16/16, `model_calls: 0` |
| `find C:/wamp64/www -name grading.json` | 0 |

Transcripts: `M10-14/agents-verification.txt`, `dev-verification.txt`, `readiness/*`, `slop-*.txt`, `srs-*`.

## 6. Before/after

| # | Measure | Baseline | Target | After (29 Sep 2026) | Status |
|---|---|---|---|---|---|
| 1 | Dev CI on `main` | red, 12 runs (13 at execution) | green incl. hook tests | green on the last three pushes; hook tests in the log | MET on the checkpoint-3 HEAD `67ae982`; re-confirm on the final pushed HEAD |
| 2 | SRS `.docx` with raw Mermaid | 18 / 691 | 0, blocked by the build | 0 / 691; malformed build refused | MET |
| 3 | Undeclared cross-engine pairs ≥ 0.75 | 23 | 0 | 0 | MET |
| 4 | Engines with owned negatives, all passing | 1 (partial) | 5 focus engines | 5 engines at minimum; 1 cross-engine mirror fails | NOT_MET |
| 5 | Design p@1 | 85 % | ≥ 90 %, ratchet | 94.1 %, floor 92 | MET |
| 6 | Tier 3 | none | harness, 16 fixtures, self-tests; ≥ 28 case records | 46 case records with run evidence (233 runs; with the 11 plugin-eval cases, 66 runs, 299 planned in all; micro-test separate), **0 executed**; 16/16 self-tests | MET (zero-spend target) |
| 7 | Thin `CLAUDE.md` bridges | 4 / 12 | 12 / 12 | 12 / 12 | MET |
| 8 | Executable slop rules | 0 | ≥ 30 mapped to AS1–AS7 | 49 | MET |
| 9 | Banned-font copies | drifted | 1 canonical + checked mirror | 1 + 1 byte mirror, 0 drift | MET |
| 10 | Silent `skill-writing` drift | 7 | 0 | 0 | MET |
| s1 | Dev `engine_compliance.py` | 138 / 167 (plan) | — | 136 / 165 | recorded |
| s2 | Dev p@1 | 96 % | — | 90.6 % (after fixture-lint rewrites; floor 88) | recorded |
| s3 | SRS routing | 54 / 54 | — | 55 / 55 top-3; p@1 47 / 55 | recorded |
| s4 | Claude-loaded router bytes | per engine | — | rose in 11 of 12 (bridge imports `AGENTS.md`) | recorded |
| s5 | Portfolio metadata characters | 291,636 (M10-02) | — (60,000 self-declared) | 292,390; 27 duplicate names | recorded |
| s6 | Marketplace consistency | 13 drift lines | 11 / 11 | 23 ok, 0 drift | recorded |

Source: `M10-14/success-measures.jsonl`.

## 7. Scores

Method: dev `skill-engine-audit` with the AO-14 extension (M10-14-T01), weighting output readiness 30, skill depth and worked examples 25, standards currency 15, taxonomy 10, doctrine 10, hygiene 10 (mean of redundancy, discovery/routing and safety). Each re-audit was run by one independent agent that executed no M10 phase; folders `docs/audits/2026-09-29-m10-reaudit/` in each repository. **Raw** uses the auditor's judged routing score; **measured-constrained** replaces it with Readiness; **published** is `min(measured-constrained, 65)` because no engine yet has the craft standard's acceptance evidence. No dimension, group or output type in any of the six audits reached 70.

| Repository | Raw | Measured-constrained | Published | Readiness (T1 / T2 / T3 points) | Prior published figure |
|---|---|---|---|---|---|
| design-system-skills | 57.1 | 57.1 | **57.1** | 59.4 (30.00 / 29.41 / 0) | 51 (June strict baseline) |
| website-skills | 55.3 | 55.2 | **55.2** | 59.6 (30.00 / 29.62 / 0) | NOT ASSESSED, cap 65 |
| srs-skills | 54.6 | 54.6 | **54.6** | 58.5 (30.00 / 28.54 / 0) | 65 published (88.8 raw self-review, 8 Sep) |
| chwezi-dev-engine | 52.7 | 52.5 | **52.5** | 59.7 (30.00 / 29.72 / 0) | withheld (6 Sep) |
| chwezi-engine-agents | 52.5 | 51.9 | **51.9** | 37.1 (30.00 / 7.14 / 0), corrected after review; T1 uses a stand-in validator list | none |
| digital-research-engine | 51.6 | 51.6 | **51.6** | 57.5 (30.00 / 27.51 / 0) | none comparable |

Readiness only (no full re-audit in M10-14; figures after the review correction): proposal 47.3; business-plan, social, windows and finance 40.0; linux 30.0 (`eval-readiness.json`).

Reading the scores:
- Every auditor recomputed Readiness from the stored inputs and agreed. Two caveats were raised: research T1 = 1.0 holds only with sibling repositories present (in a single-repository checkout, as on CI, it is 2/3 and Readiness 47.5); the agents Readiness was first published as 47.7; the independent reviewer (REJECT, finding F1) found its collision-clean slot scored 1.0 although the package is outside the union scan, and that its p@1 excluded three executed known-defect oracles. Both were corrected: collision-clean `NOT_ASSESSED` = 0, p@1 30/42, Readiness 37.1, published 51.9. The agents T1 (8/8) uses a stand-in validator list chosen by the executor, because `catalog/engines.yaml` declares none for the package.
- Routing weighs about 3.3 points of an engine score, so measured Readiness moves the overall by at most 0.2 points here; it is reported beside the overall, not folded away.
- The 97/100 target cannot be claimed: T3 is unexecuted (0 of 30 points) and routing coverage is near zero in every engine.
- The main score-limiting findings, common to most engines: worked examples are short scenarios rather than applied outputs (dev 39 of 167 skills mention one; research 56 of 59 under 60 words; srs 4 of 159 with inputs and expected output); duplicated or generic contract sections pass the section-presence gates; standards currency gaps (dev: Android target SDK 35 against Play's API 36 rule, Next.js 15/16 removals; srs: IEEE 830-1998 still mapped in the clause registry; research: superseded TOP guidelines; design: no EN 301 549 or European Accessibility Act); dangling references to retired or non-existent skills that no validator catches.
- Scores need Peter's ratification before publication (M10-14 exit criteria).

## 8. NOT_ASSESSED items and evidence limits

- **Every model-executed cell** (zero-spend rule): 299 planned Tier-3 runs across solution selection (144), acceptance (36), pressure (42), plugin evals (66) and MCP QA (10), plus the 15-cell micro-test and the live isolation smoke. Executed: 0. The T3 slot is 0 for every engine and no engine can exceed 70 Readiness.
- Superpowers 6.4.2 clean-session acceptance prompt (needs a model session; Peter).
- PT-11 subagent doctrine reach test; UA-14 Understand Anything sandbox pilot.
- Linux-native validators on this Windows host (linux `check-distro-matrix.sh`; the SRS render step on Linux).
- Browser-tier slop acceptance in CI (no locked Playwright on the runner; exercised locally in M10-09).
- Remote CI for the M10-14 commits (not yet pushed).
- Tier 2 is a lexical proxy throughout; live skill firing is unmeasured (agent-skills issue #620).
- p@1 is not reported by the business-plan, social, linux and windows harnesses, and finance has no routing harness; their p@1 slot is 0.
- The six measured re-audits were each run by one independent agent working through the fleet's concerns in turn, not by a six-agent fleet per engine; standards currency was judged from the engines' own currentness records unless the audit says otherwise.
- The running log holds reviewer sections for M10-00 and M10-02 only; the other phases' acceptance is evidenced by their evidence folders and the three push checkpoints.

## 9. Rollback points (last pre-M10 commit per repository)

| Repository | Pre-M10 commit (M10-00 snapshot HEAD) |
|---|---|
| chwezi-engine-agents | `eaa2152` |
| chwezi-dev-engine | `7adc9fc` (font sweep; D-M10-01 dev repair followed at `6941e08`) |
| design-system-skills | `b7e1003` |
| srs-skills | `efa18e6` |
| website-skills | `1660bc1` |
| digital-research-engine | `5c4313c` |
| proposal-skills | `e72dc66` |
| business-plan-skills | `ceeb240` |
| social-media-skills | `bcf43e3` |
| linux-skills | `9443e50` |
| chwezi-accounting-doctrine | `8c1d683` |
| windows-admin-engine-skills | `132cbe9` |

Revert by phase commit (never by rewriting history). The AO-14 rubric change rolls back by reverting the single M10-14 dev commit.

## 10. Push record

Push events reconstructed from the remote CI runs each push triggered (`gh run list`, UTC). Every local `HEAD` equalled `origin/main` at the M10-14 freeze.

| Event | When (UTC) | Content | Heads (agents / dev / design / srs / website / DRE / proposal / bp / social / linux / finance / windows) |
|---|---|---|---|
| Font ruling | 28 Sep 23:10 | owner-approved, outside the counter | `—` / `7adc9fc` / `b7e1003` / `efa18e6` / `1660bc1` / `5c4313c` / `e72dc66` / `ceeb240` / `bcf43e3` / `9443e50` / `8c1d683` / — |
| D-M10-01 early push | 28 Sep 23:31; 29 Sep 00:11 | M10-01 stop-the-line repairs | `9510270` / `b3161da` / `f69c5d4` / `905b9a4` / `75bc5c9` / `d4a613d` / `ba94f15` / `2b41c08` / `724970f` / `9de82cf` / — / — |
| Checkpoint 1 | 29 Sep 00:33 | M10-00 to M10-02 | `35340f6` / `33574d9` / `655d983` / `f8ce9fa` / `26677c5` / `2aa54bc` / `ead7a38` / `7b21210` / `52399fc` / `42b3c1b` / `a209c26` / `b1100c5` |
| Checkpoint 2 | 29 Sep 02:11 | M10-03 to M10-05, plus later-phase work already committed (M10-06 to M10-10, part of M10-13) | `5ef3019` / `0a799d8` / `3fe84a6` / `702a5ab` / `3c9fdca` / `f76c818` / `3e4330d` / `d84a599` / `9b11fbf` / `e8d10a7` / `af2af30` / `4d82599` |
| Checkpoint 3 | 29 Sep 04:06 | remaining M10-06 to M10-13 work | `8a438c9` / `67ae982` / `25ce1e6` / `fa85fba` / `ec72bca` / `2b9c87d` / `5de27f8` / `8949387` / `09eebe7` / `87c6421` / `82279fa` / `55c53cc` |
| Final (M10-14) | pending | M10-14 close-out: dev rubric, agents records, six audit folders | orchestrator to record after `git fetch`: actual pre-push `origin/main` (for agents it has already moved past checkpoint 3 to `cea785e`/`86a7776`, commits outside M10-14; for the other eleven it was the checkpoint-3 head at the freeze); pushed HEAD; CI conclusion. No silent rebase |

Remote CI at checkpoint 3: success for agents `validate`, dev `skill-catalog-guardrails`, design, website and finance; **failure** for srs, DRE, proposal, business-plan, social, linux (`Skill quality`; its Bash suites pass) and windows. All seven failures predate M10 (see §11 items 1–2); the six link failures come from sibling-relative or absolute `C:/wamp64/www/…` links that resolve only on this host. The dev and agents gates named in M10-14-T11 are `success`.

Proposed release tags (PT-04; only with Peter's authority; every manifest is at 1.1.0): after the final push, in each of the twelve repositories, `git tag -a v1.1.0 -m "my-10-kaizen close-out (29 Sep 2026)" <pushed HEAD>` then `git push origin v1.1.0`. Recommendation: tag only the five repositories whose CI is green at the pushed HEAD (agents, dev, design, website, finance) and hold the other seven until their CI is repaired, so that no release tag marks a red build.

## 11. Next opportunities

Each item is a candidate for the next Kaizen, not a completed change. "Earliest" is the first date on which re-audit or action is sensible.

| # | Candidate | Evidence | Owner engine | Earliest |
|---|---|---|---|---|
| 1 | **Stop-the-line: remote CI red in six engines from links that only resolve on this host.** Skills link to sibling engines by relative path (`../../../<engine>/…`) or by absolute `C:/wamp64/www/…` path; CI checks out one repository, so srs (1: absolute paths in `hospitality-operating-model-srs/SKILL.md` lines 156–157), DRE (2: `ai-slop-audit`, `anti-ai-slop` → dev reference), proposal (4), business-plan (4), social (5) and linux (1) fail, while every validator passes locally. All predate M10. Decide one portfolio rule (sibling checkouts in CI, or validators that treat sibling-engine links as external when the sibling is absent; ban absolute paths) and apply it | M10-14 evidence "Remote CI"; `gh run view --log-failed`; srs and research re-audits | chwezi-engine-agents (rule) with the six engines | next Kaizen, first slice |
| 2 | **Stop-the-line: windows-engine-ci red** since at least 16 Sep: `missing module function: Get-WseAdminActivityReport` on the runner, although the function file and manifest entry exist and local validators pass | M10-14 evidence "Remote CI" | windows-admin-engine-skills | next Kaizen, first slice |
| 3 | §5 row 4 NOT_MET: route oracle 055 (research release-evidence mirror) ranks the dev owner `validation-contract` 4th behind `deployment-release-engineering`; lands with the `fix_alias` follow-up for validation-contract | `success-measures.jsonl` row 4; `route-oracles-summary.json` | digital-research-engine + chwezi-dev-engine | next Kaizen |
| 4 | `fix_alias` follow-ups in the ownership register (validation-contract, ai-slop-audit, anti-ai-slop, excel-spreadsheets, blog-idea-generator); known-defect oracles 030, 032, 044 turn green then; the 029 tie resolves | M10-03 evidence; `evals/routing/ownership.yaml` | chwezi-engine-agents with dev, DRE, srs, bp, social | next Kaizen |
| 5 | Tier 3 executed = 0: 299 planned runs are `NOT_ASSESSED (zero-spend rule)`; every T3 Readiness slot is 0 and no engine can exceed 70 Readiness or claim 97. Needs Peter's explicit spend approval before any run | M10-05 run report; `eval-readiness.json` | chwezi-engine-agents + chwezi-dev-engine | when Peter approves spend |
| 6 | Routing coverage is near zero everywhere (skills with ≥ 3 positives and ≥ 2 owned negatives: dev 11/167, website 1/62, others 0); raise P0 engines towards 100 % per the Addy threshold table | `readiness/coverage.json` | dev, design, srs, website, DRE | next Kaizen |
| 7 | p@1 is not reported by the business-plan, social, linux and windows routing harnesses, and finance has no routing harness: their p@1, owned-negative and coverage slots score 0. Add p@1 output and owned negatives (the six non-focus engines) | `eval-readiness.json`; `readiness/*-smoke.txt` | bp, social, linux, windows, finance, proposal | next Kaizen |
| 8 | Claude-loaded router bytes rose in 11 of 12 repositories after the bridge conversion (srs 33.5k → 51.2k; website 21.2k → 42.0k). Measure whether any of it is context waste before any budget (P04 rule) | `close-snapshot-diff.md` | chwezi-engine-agents | next Kaizen (CV-01 data now exists) |
| 9 | Portfolio metadata 292,390 characters against the self-declared 60,000; 27 duplicate skill names; 24 within-engine description pairs ≥ 0.75 (reported, not gated) | `runtime-budget-portfolio.json`; `readiness/collision-scan.json` | all engines | next Kaizen |
| 10 | Behavioural acceptance prompts: lexical primary@1 2/12; behavioural run `NOT_ASSESSED` | `route-oracles-summary.json` | chwezi-engine-agents | with item 5 |
| 11 | PT-11 subagent doctrine reach test `NOT_ASSESSED` (needs a live Task-spawned run) | `traceability-closure.md` | chwezi-dev-engine | with item 5 |
| 12 | UA-14 Understand Anything sandbox pilot `NOT_ASSESSED` (needs spend approval and a UA-01 reversal trigger) | DRE `340b200` | digital-research-engine | D2 review date |
| 13 | IM-15 `DEFERRED`: it waited for the detector, which now exists (design `3fe84a6`); hand it back to dev | `traceability-closure.md` | chwezi-dev-engine | next Kaizen |
| 14 | GR-11 `DEFERRED`: `@req` code-to-requirement trace needs a codebase whose team keeps annotations; Peter to name one | M10-08 evidence | srs-skills | when a codebase is named |
| 15 | CV-04 dropped at execution (16.3 % of SRS router bytes against the 25 % rule); re-evaluate only on a new CV-01 measurement | M10-08 evidence | srs-skills | next CV-01 snapshot |
| 16 | AO-12 design Tier-1 refinements: `M10-03/patches-for-orchestrator/design-validate_engine-t12.patch` is still unapplied (`git apply --check` passes on `25ce1e6`) | M10-03 evidence; M10-14 check | design-system-skills | next Kaizen, first slice |
| 17 | GarageFlow user manual: `screenshots/manager-home.png` missing, so `check_docx_diagrams.py` flags 2 missing figures; a client deliverable, Peter must supply the screenshot | `srs-docx-scan.json` | srs-skills (client project) | when Peter supplies it |
| 18 | Client re-issue of the 10 regenerated SRS documents (M10-01 T11) awaits Peter | M10-01 evidence | srs-skills (client delivery) | Peter's decision |
| 19 | JetBrains Mono and Fira Code (the only approved monospace faces) meet the two-source ban threshold; still approved | M10-09 evidence; design memory | design-system-skills | 2026-12-29 recheck (Peter) |
| 20 | design-system-skills still holds 9 mentions of retired alias slugs | `M10-12/M10-12-graph-defect-remediation.md` (retired_alias_mentions: design 9) | design-system-skills | next Kaizen |
| 21 | `skill_graph.py` false positives need tuning before the graph report can gate anything | `M10-12/M10-12-graph-defect-remediation.md` (scanner false positives, e.g. valid `references/<slug>.md` paths) | chwezi-engine-agents | next Kaizen |
| 22 | 587 of 1,177 skills were not read in August–September usage (consolidation review evidence, not a retirement list) | `kaizen-2026-09-29-m10-12-context-tours-graph.md` (usage scan, 1,177 inventoried skills) | all engines | next consolidation value gate |
| 23 | No slop rule maps to AS6 | `slop-rules.txt` | design-system-skills | next Kaizen |
| 24 | Release tags `v1.1.0` not yet created (PT-04) | `docs/distribution.md`; §10 | orchestrator with Peter | after the final push, green CI first |
| 25 | Peter's ratifications outstanding: AO-14 rubric change; the published scores; D1–D5; the M10-03 register dispositions and the mysql/postgresql allow-list; the watchlist-to-secondary-ban ruling; AR-12/AR-13 diffs | this record §3; phase evidence | Peter | before the next Kaizen starts |
| 26 | Superpowers 6.4.2 clean-session acceptance prompt ("Let's make a react todo list") in a new Claude Code session | log M10-00 T06 | Peter's machine | any session |
| 27 | Standing re-audit dates: K5 AS1–AS7 re-audit (due 3 Oct) **met** on 29 Sep with detector evidence (DRE `20564b8`); K7 portfolio craft review (due 2026-10-04) **open**; Pocock workflow re-audit (due before 2026-10-11) **open** (`chwezi-dev-engine/docs/plans/NEXT_FEATURES.md`) | M10-09 evidence; `portfolio-craft-standard-2026-09-04.md` | chwezi-engine-agents; chwezi-dev-engine | 2026-10-04; 2026-10-11 |
| 28 | Full re-audits of the six engines not re-audited here (proposal, business-plan, social, linux, finance, windows) with the AO-14 rubric | `eval-readiness.json` | each engine | each engine's own cycle |
| 29 | Remaining registered variants (source-ingestion guardrail, `rules/common/core.md`, installer fork) for a consolidation value gate; duplicated meta-skills other than `skill-writing` (`skill-safety-audit` ×6, `anti-ai-slop`, `ai-slop-audit`) | `catalog/shared-assets.yaml`; backlog §1.1 | chwezi-engine-agents | next Kaizen |
| 30 | Running log gap: M10-01 and M10-03 to M10-13 have no reviewer-verdict section in `m10-kaizen-execution-2026-09-29.md`; add dated verdict entries (append-only) | this record §8 | chwezi-engine-agents | before the next Kaizen |
| 31 | Open P06/P09/P10 items of the Skills Kaizen that M10 did not absorb | `skills-kaizen-execution-2026-09-26.md` | chwezi-engine-agents | next Kaizen |
| 32 | **Doctrine breach in dev:** `professional-word-output` registers Inter as a brand font and recommends Arial for watermarks, both hard-banned | dev re-audit `2026-09-29-m10-reaudit/` finding 5 | chwezi-dev-engine | next Kaizen, first slice |
| 33 | Dev standards currency: Android skill targets SDK 35 (Play requires API 36 since 31 Aug 2026) and claims a crash without `enableEdgeToEdge()`; Next.js skill uses APIs removed in 15 and `middleware.ts` deprecated in 16; PostgreSQL stops at 16 (18.6 current); two `ai-platforms.md` source rows past review date | dev re-audit `06-standards-benchmark.md` (cited) | chwezi-dev-engine | next Kaizen |
| 34 | Duplicated or generic contract sections pass the section-presence gates (dev: 59 of 167 skills duplicate Inputs/Outputs/Decision rules; 19 of 26 AI skills share one generic block; research: 19 skills repeat H2 sections; srs: 34 identical worked-example paragraphs). Add a duplicate/boilerplate check | dev, research, srs re-audits | chwezi-dev-engine (`contract_gate.py`) and mirrors | next Kaizen |
| 35 | Dangling references no validator catches: srs `04-database-design` makes a non-existent `mysql-best-practices` mandatory, `03-api-specification` cites `api-error-handling`/`api-pagination`; research ~100 mentions of 52 retired skills; dev `postgresql-engineering` ↔ `postgresql-operations/ALIAS.md` circular pointer | srs, research, dev re-audits | srs, DRE, dev; portfolio check in agents | next Kaizen |
| 36 | Standards records: srs clause registry maps Phase 02 checks to superseded IEEE 830-1998; research `academic-reporting-standards` describes the superseded TOP structure; design register has 5 rows and omits EN 301 549 and the European Accessibility Act | srs, research, design re-audits | srs, DRE, design | next Kaizen |
| 37 | Coordination package: `docs/security/supply-chain-policy.md` describes release checks that `release.yml` does not run; old name `skills-engine-agents` in `.codex-plugin/plugin.json`, the release archive and the MCP server (version 1.0.0); `claude-bridge-contract.md` line 56 contradicts the coordination `CLAUDE.md`; no `validators` entry for the package in `catalog/engines.yaml`; CI runs 12 of 20 pytest files | agents re-audit | chwezi-engine-agents | next Kaizen |
| 38 | Catalogue validator lists under-declare what engine CI enforces (design 2 of 7, website 3 of about 7), so T1 measures less than CI; diagrams have no owning design skill or routing fixture | design, website re-audits | chwezi-engine-agents with design, website | next Kaizen |
| 39 | A personal phone number appears in 120 dev `SKILL.md` acknowledgement lines; confirm with Peter whether it should be public | dev re-audit | chwezi-dev-engine (Peter decides) | Peter's decision |
| 40 | Two fallback banned-font lists sit outside the drift register and are out of date: `srs-skills/scripts/render_diagrams.py` and `chwezi-engine-agents/scripts/project_context_doctor.py`. They are used when the canonical design JSON is absent, as in single-repository CI. Register them or generate them from the canonical list | `M10-14-independent-review.md` F7 | chwezi-engine-agents with srs-skills | next Kaizen |
| 41 | Declare a `validators` list for the coordination package in `catalog/engines.yaml` (its Readiness T1 is currently a stand-in), give its skill routing fixtures and add the package to the union collision scan | review F1, F2 | chwezi-engine-agents | next Kaizen |

## 12. Traceability closure and review

Independent review: `m10-kaizen-evidence/M10-14/M10-14-independent-review.md`. First verdict REJECT (finding F1, a non-zero slot without input); corrections applied the same day (F1 to F6 and F8 to F10 fixed or stated; F7 carried as item 40). The traceability count script is stored at `m10-kaizen-evidence/M10-14/readiness/verify_traceability.py` (RESULT: PASS).

`m10-kaizen-evidence/M10-14/traceability-closure.md`: 161 backlog IDs, each once. DONE 111; DONE_WITH_LIMITATIONS 42; DONE in M10-14 (commit pending) 3; NOT_ASSESSED 2 (PT-11, UA-14); DEFERRED 2 (IM-15, GR-11); DROPPED-AT-EXECUTION 1 (CV-04, decision rule not met); PARTIAL 0. The sixteen §3 dropped items stayed dropped, and no phase proposed an install that D1–D5 rejected.
