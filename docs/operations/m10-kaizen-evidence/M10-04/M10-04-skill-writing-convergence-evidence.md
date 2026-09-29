# M10-04 evidence: skill-writing convergence, pressure testing and byte warnings

**Phase:** M10-04 (my-10-kaizen). **Date:** 29 September 2026. **Executor scope:** T01–T07 and the canonical-rule half of T12. T08–T10 are in `M10-04-safety-gate-and-register-evidence.md`. T11, the T12 register, and T13–T15 are in `M10-04-agents-governance-evidence.md`.
**Authority:** Peter delegated approval ("Implement the Plan!"). Where the phase says "Peter decides/ratifies", the plan's recommended option was taken: *decided by orchestrator under Peter's delegated authority, 29 Sep 2026*. Doctrine-class changes (canonical standard, stubs, quarantine rule) still need Peter's ratification before the public push gate.
**Hard rules kept:** zero spend (no model runs), no git state changes (all edits unstaged), no README.md edits, no new active skill (dev stays at 167).

## Summary

| Task | Status | One line |
|---|---|---|
| T01 | DONE | Decision record written; the pre-change preservation map hashes every file of all seven copies |
| T02 | DONE | Harvest table below: 11 rules merged into the canonical, 13 carried as stub delta, 6 discarded, each with a reason |
| T03 | DONE | Six pointer stubs, 59–60 body lines; script mirrors are byte-identical; register rewritten; drift check reports 0 findings on every skill-writing row; all Tier-1 validators, routing smoke tests and engine test suites pass |
| T04 | DONE | `references/discipline-skill-pressure-testing.md` added, with attribution, and linked from References, §6 and the Upgrade Checklist |
| T05 | DONE_WITH_LIMITATIONS | Validator extended; PS01 is seeded in a new sibling file, not in `fixtures.json` (concurrency deviation). Both PS01 outcomes are `NOT_ASSESSED` (zero-spend rule; no runner before M10-05) |
| T06 | DONE | `references/form-matches-failure.md` added with attribution; Upgrade Checklist item added |
| T07 | DONE_WITH_LIMITATIONS | Byte warning live in dev (13 expected files plus one M10-06 file) and design (6 files). srs (6 files) is a patch for the orchestrator, because M10-07 owns the srs scripts |
| T12 (canonical rule) | DONE | Quarantine-not-delete rule in `references/bundled-script-safety.md`, linked from the canonical `SKILL.md` |

## T01: canonical decision and preservation map

- Decision record: `chwezi-engine-agents/docs/operations/decisions/skill-writing-canonical.md`. It cites:
  - srs `AGENTS.md` l.81 (the plan's l.76; the line has since moved);
  - srs `docs/skill-authoring-standard.md` l.40;
  - srs `CONTRIBUTING.md` l.44;
  - design `governance/skill-authoring-standard.md` l.4.

  All were verified on disk on 29 Sep.
- Preservation map (pre-change): `preservation/skill-writing-preservation-map.md` and `.json`. For every file of the seven copies (SKILL.md, references, scripts, LICENSE) it records the byte count, line count, raw SHA-256, CRLF-normalised SHA-256, whether the file equals the dev file, and each engine's HEAD at capture:

  | Engine | HEAD at capture |
  |---|---|
  | dev | `33574d94a5` |
  | DRE | `2aa54bcdfd` |
  | social | `52399fc556` |
  | website | `26677c5f2d` |
  | business-plan | `7b21210b22` |
  | linux | `42b3c1b7e7` |
  | proposal | `ead7a38ae2` |

  Capture script: scratch `m1004_premap.py`, whose logic is recorded in the JSON header.
- Post-change hashes: `preservation/skill-writing-post-change-hashes.md`.
- Hash drift since the plan was measured: the dev `quick_validate.py` was `5c3995403c…` at M10-02, not the plan's `673057d63a` (it changed in M10-01). Every copy was re-hashed from disk.

## T02: harvest table

Every rule found only in a non-canonical copy, with its decision:

| # | Rule (source copies) | Decision | Where it went / reason |
|---|---|---|---|
| 1 | Inputs table records source and behaviour when absent (BP, linux, proposal, website, social) | Merged | Canonical "Contract section rules" + canonical Inputs table gained an `If absent` column |
| 2 | Degraded mode returns the narrowest qualified result; unrun checks `NOT ASSESSED`, never a pass (all six) | Merged | Canonical "Contract section rules" |
| 3 | Decision tables name the failure or risk avoided, not the action again (BP, linux) | Merged | Canonical "Contract section rules" |
| 4 | Pair every anti-pattern with a `Fix:` correction (BP, linux, proposal, website) | Merged | Canonical "Contract section rules" |
| 5 | Extracted references carry a back-link to the parent skill (linux, proposal) | Merged | Canonical "Contract section rules"; the new references carry the back-link |
| 6 | Delegate authoring only in non-overlapping cohorts; shared routers, validators, CI and baselines stay with one owner (BP) | Merged | Canonical "Contract section rules" |
| 7 | Routing threshold: expected skill in the router's top three; stop on collision (BP, linux, proposal, website) | Merged | Canonical §6, worded as "the host engine's routing threshold" |
| 8 | Recover by fixing the named contract; never weaken the gate or baseline (BP, linux, proposal) | Merged | Canonical §6 |
| 9 | British English; imperative mood; add only what the model would not infer (linux, social) | Merged | Canonical Repository Rules |
| 10 | Illustrative file names in `skill-authoring-best-practices.md` written as plain names, not broken links (social, website, proposal) | Merged | Canonical reference now uses the social wording (removes 10 dead links) |
| 11 | mPDF example link made conditional in `generation-template.md` (website); book-extraction owner rule of 2026-09-23 (proposal `source-distillation-and-copyright.md`) | Merged | Canonical references (owner rule reworded engine-neutrally) |
| 12 | 13 contract sections enforced by `skill_contract_validator.py`; no runner-specific tool names in body (DRE) | Stub delta | DRE stub |
| 13 | Replay-gated revision for research skills (DRE `b09c468`, `d9c44f5`; lives in `ai-evaluation-and-data-flywheel/references/replay-gated-skill-revision.md`) | Stub delta | DRE stub (linked); named in the canonical "Canonical Source and Engine Stubs" |
| 14 | `skill-composition-standards` is the normalisation neighbour (DRE) | Stub delta | DRE stub Do Not Use When and References |
| 15 | Market and currency; never publish, spend or change a live account while authoring (social) | Stub delta | Social stub |
| 16 | `anti-ai-slop` during writing, `ai-slop-audit` at release (social, BP, proposal) | Stub delta | Social, BP and proposal stubs (these skills live in those engines, not dev) |
| 17 | Website authoring standard; acknowledgement placement; `update-claude-documentation` for router-only changes (website) | Stub delta | Website stub |
| 18 | Refuse skills created to improve catalogue metrics (website, BP, proposal) | Stub delta | Website stub; the canonical already bars duplicate skills |
| 19 | Dual-compatible template and dual-surface migration rules; inventory `skills/` and `country-context/` (BP) | Stub delta | BP stub; the two references stay in BP (engine-specific; the BP validator requires the template) |
| 20 | Financial figures verified or assigned to professional review (BP) | Stub delta | BP stub |
| 21 | `## Distro support` first H2; `common.sh` primitives; manual commands as baseline; never mutate a server while writing (linux) | Stub delta | Linux stub |
| 22 | Author metadata keys; local standard and template (linux) | Stub delta | Linux stub frontmatter and delta |
| 23 | Frontmatter limited to `name`, `description`, `metadata`; acknowledgement under the title (proposal) | Stub delta | Proposal stub |
| 24 | Run `scripts/source_ingestion_guardrail.py` when a copyrighted source informs work (proposal) | Stub delta | Proposal stub |
| 25 | "Do not add compatibility, version, or license fields to frontmatter" (social) | Discarded | Conflicts with the canonical approved-keys rule (`license` is allowed; linux requires it) |
| 26 | "Copy the canonical body into each engine, translated to the local domain, one local source" (proposal anti-pattern) | Discarded | Superseded by this phase's canonical-plus-stub decision |
| 27 | "Preserved Domain …" legacy sections (website) | Discarded | Generic filler left by an earlier migration; nothing that the canonical does not already cover |
| 28 | `references/legacy-guidance.md` (website; 514 lines of the old generic skill-creator guide) | Discarded | Superseded by the canonical `skill-authoring-best-practices.md` and `workflows.md`; hash kept in the preservation map |
| 29 | Old DRE script variants (`contract_gate.py` warning severity, `fix_mojibake.py`, `upgrade_dual_compat.py` template text, `quick_validate.py` 1,024-character limit) | Discarded | Older forks of the dev scripts; the dev versions are newer and stricter. DRE now mirrors the dev `quick_validate.py` and `upgrade_dual_compat.py` |
| 30 | Social body-section list and `init_skill.py`/`package_skill.py` workflow | Discarded (covered) | The canonical covers sections; both scripts remain as byte mirrors in every stub folder |

## T03: pointer stubs, mirrors and the drift register

**Stub shape.** Every stub has the same `name`, and a description naming "the canonical chwezi-dev-engine skill-writing standard" (237–316 characters). The body has:
- the canonical source (GitHub URL and local path);
- the Tier-1 contract sections each engine requires, with the portable minimum as Quality Standards (7 bullets covering the 8 phase items);
- the engine-local delta;
- the degraded mode.

Blank lines around headings are omitted so the body fits in ≤ 60 lines. Stubs are rendered by `preservation/render_skill_writing_stubs.py` (a copy of the executor's generator) so they can be regenerated.

| Engine | Body lines | Removed (canonical copies) | Kept / mirrored |
|---|---:|---|---|
| DRE | 60 | 5 references; `scripts/contract_gate.py`, `fix_mojibake.py`, `split_oversized_skills.py` (unreferenced in DRE) | `quick_validate.py`, `upgrade_dual_compat.py` (byte mirrors); `init_skill.py`, `package_skill.py`, LICENSE |
| social | 60 | 3 references | `references/skill-authoring-best-practices.md` (byte mirror; a dated Kaizen record links it); 3 scripts; LICENSE |
| website | 59 | 6 references incl. `legacy-guidance.md` | 3 scripts; LICENSE |
| business-plan | 59 | 4 references | the two BP-only references; 3 scripts; LICENSE |
| linux | 59 | 5 references | 3 scripts; LICENSE |
| proposal | 60 | 5 references | 3 scripts; LICENSE |

Empty `references/` folders left in DRE, website, linux and proposal were removed with `rmdir`, under the AO-21 empty-directory approval:
- `proposal-skills/skills/meta/skill-writing/references`
- `digital-research-engine/skills/skill-writing/references`
- `website-skills/skills/meta/skill-writing/references`
- `linux-skills/meta/skill-writing/references`

**Depth-independent scripts.** `quick_validate.py` and `upgrade_dual_compat.py` replaced `REPO_ROOT = parents[4]` with `_find_repo_root()`. It walks up to the first `.git` entry or `AGENTS.md` and falls back to the old depth. In dev it resolves to the same root as before. One byte-identical file therefore works at `meta/skill-writing` (linux) and `skills/skill-writing` (DRE). Each engine's mirrored quick validator returns "Skill is valid." on its own stub.

**Register** (`catalog/shared-assets.yaml`, M10-02's check extended, not duplicated). The pre-edit copy is in the scratchpad.
- `skill-writing-skill`: six stub variants (hash, owner, reason). The canonical is listed as canonical but deliberately not hashed.
- `skill-writing-quick-validate`: changed from registered-variant to **byte**.
- New **byte** rows: `skill-writing-init-skill`, `skill-writing-package-skill`, `skill-writing-upgrade-dual-compat` (DRE), `skill-writing-license`, `skill-writing-authoring-practices` (social).

**Results:**
- `python -X utf8 scripts/render_host_files.py --check`: 0 findings on every skill-writing row.
- Seeded check: appending one line to the linux mirror gave `shared-asset-byte-drift` with exit 1. The file was then restored byte-identical (`command-output/drift-check-seeded-mirror-drift.txt`).
- The final full run shows one finding that is **not** M10-04's: `rules-common-core` for `srs-skills/rules/common/core.md`, which another executor modified while this phase ran (see Open items).

**Validators before and after** (`command-output/six-engines-before.txt`, `six-engines-after.txt`). All exit 0 after the change:

| Engine | Tier-1 validator | Routing smoke | Engine tests (`pytest tests`) |
|---|---|---|---|
| DRE | `skill_contract_validator.py --baseline …` 59/59 compliant, `{}` | 29/29 | 129 passed, 2 skipped |
| website | `validate-skill-contracts.py --baseline quality/skill-contract-baseline.json`: zero debt | 36/36 | 80 passed |
| business-plan | `validate_skill_engine.py --baseline docs/quality/…` 137/137; `compileall` rc 0 | 61/61 | 62 passed |
| social | `validate_skill_engine.py --baseline quality-baseline.json` 191/191 | 56/56 | 30 passed |
| proposal | `git diff --check` rc 0; `validate_skills.py` 0 findings; source-ingestion guardrail 0 | 25/25 | 52 passed |
| linux | `validate_skills.py --baseline quality-baseline.json` 48/48 (**helper-only on Windows**; Linux-native tests `NOT_ASSESSED`) | 30/30 | 22 passed, 12 skipped |

`generate-plugin-manifest.js --engine . --check` reports every plugin.json as current (linux has no `skills/` root, so it is not applicable there).

**Decision taken under delegation.**
- **Business-plan stub:** the first draft failed the BP capability rule, because "authority" does not match `authori[sz]`. The wording was changed to "permission … authorisation" in all six stubs.
- **Mirror strategy:** mirror the scripts an engine calls, and remove unreferenced script variants only in DRE. The three removed DRE scripts were stale forks, and their hashes are in the preservation map.

## T04 and T06: new canonical references

- Files:
  - `skills/sdlc-meta/skill-writing/references/discipline-skill-pressure-testing.md`
  - `references/form-matches-failure.md`
  - `references/bundled-script-safety.md` (T12)
- Each carries the verbatim attribution line required by the phase: obra/superpowers, MIT, commit `8ca22dba9a94f28898bbce59f2537ff4d87c747d`, "No text copied". The bundled-script file carries the Understand-Anything attribution instead.
- **Pressure-testing reference.** It covers:
  - the scope rule (reference skills are not pressure-tested; discipline skills are, only after a RED baseline);
  - RED/GREEN/REFACTOR;
  - scenario design (at least 3 combined pressures, a forced A/B/C choice, real paths);
  - the micro-test protocol (control, at least 5 repetitions, manual reading, variance as a signal, stop when the control does not fail, zero-spend `NOT_ASSESSED`);
  - the Excuse/Reality template;
  - the interpreter rule;
  - the restriction of capitalised imperatives to engineering discipline gates.
- **Form-matches-failure reference.** It covers the four-row table, "no nuance clauses", "exemption clauses do not scope", and the prohibition-versus-recipe claim recorded as a vendor lead to verify.
- **SKILL.md changes.**
  - References list: +2 entries.
  - §6: a pointer to the pressure method.
  - Upgrade Checklist: +2 items, "form matches failure type" and a RED baseline for discipline skills.
  - Repository Rules: the interpreter rule.
- **Size.** 378 lines (≤ 500) and 20,479 bytes, just under the new 20,480-byte warning; T02 and T12 detail was moved to references to stay under it.
- **Checks.**
  - `quick_validate.py skills/sdlc-meta/skill-writing`: "Skill is valid." (rc 0).
  - `contract_gate.py --all`: 161 scanned, 0 errors, 0 warnings.
  - dev `pytest -q`: 187 passed, 3 skipped.
  - dev `routing_smoke_test.py`: 187/187 top-3, 0 failures.

  Output is in `command-output/dev-checks.txt`.
- **Dependency.** M10-03-T13 (description-narration warning in `quick_validate.py`) had **not** landed when this phase ran. When it lands, re-copy the canonical `quick_validate.py` to the six mirrors, or the drift check fails. That failure is intended.

## T05: pressure-scenario case type

- `tools/validate_benchmark_fixtures.py` gains an optional pressure-scenario check. The F01–F16 rule is unchanged, and `tests/test_benchmark_fixtures.py` still passes.
  - **Fields checked:** the ID pattern `PS\d{2}`, unique across files; `target_skill` as `<engine>/<skill>`; at least 3 distinct pressures from the fixed set; `forced_choice` with exactly A/B/C and a compliant letter; outcomes as `NOT_ASSESSED` or `{choice, rationalisations_verbatim[], run_ref}`; `materialisation_status`; and an optional non-empty `short_prompt`.
  - **Warning only:** an outcome of `NOT_ASSESSED` without a `not_assessed_reason`.
  - **Output:** `pressure_scenario_count` and `pressure_scenario_sources`.
- **Deviation (concurrency, recorded):** the phase puts the array in `fixtures.json`. M10-06 was editing that file and had already added PS02 there. PS01 therefore sits in a **new sibling file** `benchmarks/solution-selection/pressure-scenarios.json` (the same array shape), and the validator reads both. There is no new schema file. The orchestrator may later move PS01 into `fixtures.json` without changing the validator.
- **PS01 (verification gate).** Target: `world-class-engineering` `references/verification-loop.md` and `rules/common/verification.md`. Pressures: time, authority, social and pragmatic. It uses real paths (`tools/validate_benchmark_fixtures.py`, `python -m pytest -q`), with B as the compliant choice. `baseline_outcome` and `with_skill_outcome` are `NOT_ASSESSED`, with the reason "no isolated runner before M10-05; zero-spend rule". The case is handed to M10-05 (AO-18).
- **Results:**
  - `python -X utf8 tools/validate_benchmark_fixtures.py`: PASS, rc 0, `pressure_scenario_count: 2` (PS02 from M10-06, PS01 from this phase). One warning: PS02 has no `not_assessed_reason`, a hand-off to M10-06/M10-05.
  - A seeded 2-pressure scenario in a scratch copy fails with "PS09 needs at least three distinct combined pressures", rc 1.
- The benchmark `README.md` still describes only `fixtures.json`; it was not edited (README rule). See Open items.

## T07: report-only byte warning

The default threshold is 20,480 bytes and can be changed with `--max-skill-bytes`. The warning never enters failure counts or baselines.

| Engine | File | Result |
|---|---|---|
| dev | `scripts/skill_catalog_guardrails.py` (edited) | 14 `[WARNING] skill-bytes`: the 13 expected files, including `saas/subscription-billing` at 28,881 bytes, plus `sdlc-meta/world-class-engineering` (21,649 bytes, grown by M10-06 today). Default-mode exit 0, errors 0 |
| design | `scripts/validate_engine.py` (edited) | 6 `WARN skill-bytes` lines; rc 0 with and without `--baseline tests/quality-baseline.json` (the baseline name is `quality-baseline.json`, not the plan's `skill-quality-baseline.json`); design `pytest tests` 99 passed |
| srs | `scripts/validate_skill_engine.py` (**not edited**) | Patch in `patches-for-orchestrator/srs-validate_skill_engine-byte-warning.patch` (`git apply --check` passes). The patched copy run against the live srs tree gives 6 WARN lines, `failure counts: {}` and rc 0 with `--baseline tests/skill-quality-baseline.json` |

Output: `command-output/dev-checks.txt` and `command-output/byte-warnings-design-srs.txt`.

## T12: canonical bundled-script rule

The rule sits in `references/bundled-script-safety.md` and is linked from the canonical `SKILL.md`. It says:
- move intermediate files to `.trash-<UTC timestamp>/` and purge only after 7 days;
- guard every removal path as non-empty and inside the work root;
- exempt `mkdtemp` and test-fixture temporary directories, with a comment beside the call;
- treat a server-side cleanup as a waiver until it is tested on that platform.

Attribution: Understand-Anything, MIT, commit `b05cc3b…`. The register and the grep are in the governance evidence.

## Files changed (this scope)

The authoritative list is in the executor's final report to the orchestrator.

## Open items

1. **srs byte warning:** apply `patches-for-orchestrator/srs-validate_skill_engine-byte-warning.patch` after M10-07 releases the srs scripts.
2. **PS01 placement:** move PS01 into `fixtures.json` `pressure_scenarios` after M10-06 commits, or keep the sibling file; the validator accepts both. Add `not_assessed_reason` to PS02 (M10-06).
3. **Benchmark README line** (README owner): "`pressure-scenarios.json` holds discipline-skill pressure scenarios (`PS01`…); `tools/validate_benchmark_fixtures.py` validates them together with any `pressure_scenarios` array in `fixtures.json`."
4. **M10-03-T13:** when the narration warning lands in the canonical `quick_validate.py`, re-copy it to the six mirrors (the drift check fails until then, as designed).
5. **Drift-check finding outside M10-04:** `srs-skills/rules/common/core.md` was modified by another executor during this run. Re-register its hash in `rules-common-core` when that change is committed.
6. **Client-project copies:** nineteen uncontrolled `skill-writing` copies (`preservation/client-project-skill-writing-copies.txt`, depth ≤ 7; the plan counted 16) are left for Peter's decision.
7. **Ratification:** Peter to ratify the canonical standard changes, the stubs and the quarantine rule (doctrine class) before the public push.
8. **Independent review:** an independent reviewer verdict (ACCEPT / ACCEPT_WITH_DOCUMENTED_LIMITATIONS / REJECT) is still to be recorded here.
