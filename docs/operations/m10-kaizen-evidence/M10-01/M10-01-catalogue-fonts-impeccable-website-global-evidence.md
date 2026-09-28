# M10-01 evidence — T07, T08, T13, T14, T15, T16, T17

Executor scope: catalogue validators and contract-eval fixtures (engine-agents), font-sweep
verification and trigger block `v2` (all engines), Impeccable source record (research, design,
dev), truthful website slop documentation and design routes (website), global `CLAUDE.md`.
Date: 29 Sep 2026. All edits are unstaged; nothing was committed or pushed. Zero spend: no model
runs, no paid services.

## M10-01-T07 — catalogue validator lists (AO-01): DONE

Files changed (chwezi-engine-agents):
- `catalog/engines.yaml`: all nine piped `validators` strings converted to YAML lists; accounting's
  single command became a one-item list.
- `scripts/validate-catalog.ps1`: parses list-form validators and rejects any validator containing
  a pipe (a pipe masks the first command's exit code).
- `mcp-server/tests/validation.test.ts` (new): `[exit 3, exit 0]` yields checks `FAIL, PASS` and
  `overall: FAIL`; `[exit 0, exit 0]` yields `PASS`; every live catalogue entry is a list with no pipe.

No TypeScript source change was needed: `runDeclared` already iterates `commands(entry.validators)`.

Release-gate alignment (names verified on disk at execution):
- dev: added `python -X utf8 scripts/skill_catalog_guardrails.py`;
- proposal: `git diff --check` replaced by `python -X utf8 scripts/validate_skills.py --baseline quality-baseline.json` and `python -X utf8 scripts/routing_smoke_test.py`;
- website: added `python scripts/routing-smoke-test.py`.

Commands and results:
- `Select-String catalog/engines.yaml ' | '` equivalent (`grep -c ' | '`): **0**.
- `powershell -File scripts/validate-catalog.ps1`: exit 0, "Catalog valid: 11 unique engines".
- Negative control: a copy of the catalogue with `"python a.py | python b.py"` as a list item: exit 1, "validator contains a pipe".
- `python -X utf8 scripts/validate-contracts.py --schema schemas/engine-catalog.schema.json --instance catalog/engines.yaml`: PASS.
- `npm --prefix mcp-server ci; npm --prefix mcp-server test`: 4 files, 8 tests passed (including the three new ones); `npm run build`: clean.
- All CI PowerShell suites from `validate.yml` (catalog, adapters, install, security, host smoke): exit 0.
- Every declared validator of all 11 engines run separately: transcript `M10-01-T07-catalogue-validators-run.txt`.

Finding surfaced by un-piping (the risk the phase predicted): website
`python scripts/validate-skill-registry.py` **exited 1** on the live tree (README count surfaces
removed by the 2026-09-28 README refresh). The pipe had hidden it. Fixed under T16 (below); the
validator now exits 0. Every other declared validator exits 0.

## M10-01-T08 — contract-eval fixtures (AO-02): DONE

Files (chwezi-engine-agents):
- `evals/fixtures/<case-id>/task.md` and `expected.yaml` for 21 cases (001–018, 020–022). The
  fixture carries the task and the expected observation in the existing case vocabulary
  (`required_observations`, `forbidden_actions`, `expected_verdict`), plus the engine list that
  used to sit in `fixture_path`. No new schema (P05).
- Case 019 (prompt injection) points to the existing `tests/fixtures/prompt-injection`.
- Case 020 (path traversal) got its own fixture folder: the old path `evals/fixtures/unknown-path`
  was a placeholder, and the traversal target is described in `task.md`.
- `evals/cases/*.yaml`: every `fixture_path` is now one directory. Case 022's comma-joined value is
  gone, and so are the comma-joined values in 002, 003, 004, 006 and 021 (same defect).
- `evals/runners/run-contract-evals.py`: `fixture_path` must be a single existing directory inside
  the repository; a materialised fixture must hold `task.md` and `expected.yaml`, whose `case_id`,
  `expected_verdict` and `forbidden_actions` must agree with the case. Minimum suite size raised
  from 20 to 22. `--cases`/`--out` now default to `evals/cases` and `evals/reports/latest.json`.
  `generated_at` carries the local offset.
- `tests/test_run_contract_evals.py` (new): live suite passes; missing path, comma-joined path and
  a fixture borrowed from another case each fail.
- `evals/README.md`: documents the fixture layout.
- `evals/reports/latest.json`, `evals/reports/release-gate.json`: regenerated with the free
  deterministic runner, `generated_at` 2026-09-29T02:24+03:00, 22 cases, 22 passed.

Commands and results:
- `python -X utf8 evals/runners/run-contract-evals.py`: `{"failed": 0, "passed": 22, "total": 22}`, exit 0.
- Temporary cases dir with a missing fixture path and a comma-joined path: exit 1; both cases FAIL with the expected evidence.
- `python -X utf8 -m pytest tests -q`: 17 passed, 1 failed. The failure is
  `test_kaizen_coordination_cards.py` ("README does not link agentic-h2-readiness-card.md"),
  pre-existing and unrelated to these edits (the card was committed in `80e8498`). Open item for
  the agents owner.

Behavioural execution of the fixtures: `NOT_ASSESSED` (zero-spend rule; M10-05).

## M10-01-T13 — font-sweep verification and trigger block v2: DONE

Verification of the committed sweep (design `b7e1003`):
1. `node hooks/test-banned-font-gate.js`: 18/18 passed. Additional probe through the hook
   (scratchpad script): Fraunces → block (2); IBM Plex Sans Arabic → block (2, prefix rule);
   IBM Plex Mono → block (2); Public Sans, Source Serif 4, JetBrains Mono → allow (0).
2. `hardBan` names in `ai-slop-banned-fonts.md` §1 equal the JSON's (19 names including the IBM Plex
   cuts; prefix rule `IBM Plex` present): **EQUAL**.
3. Portfolio scan of the 13 engine repos (tracked and untracked text files): 95 mentions,
   ban-context 95, **recommendation-context 0**. Report: `M10-01-T13-font-mention-scan.md`. Three
   mentions are ban-context only by the dated-history rule (the July 2026 file inventory lists the
   since-removed Fraunces font folder). Classifier as specified in the phase notes, plus two
   refinements recorded here: month-named folders (`engine-upgrade-july-2026`) count as dated
   history, and "bad"/"reject" count as ban wording (a new SRS test iterates rejected faces).
4. Trigger block `v2`:
   - Decision (T13 option): **(a) canonical `v2` adopts the linux runner-neutral wording** ("the
     active runner's global engine-routing table or `AGENTS.md`"). Decided by orchestrator under
     Peter's delegated authority, 29 Sep 2026 (the plan's recommended option).
   - Canonical `design-system-skills/integration/trigger-block.md` marked `v2`.
   - 14 copies replaced: srs, business-plan, website, social-media, linux, research (`AGENTS.md` and
     `CLAUDE.md` each); proposal and dev (`AGENTS.md`). Dev's "Migration status" paragraph moved
     after the closing marker as a labelled local note, so the block is byte-identical.
   - `integration/integration-plan.md`: embedded block updated to `v2`, version history added,
     consumer table corrected (dev and research paths, linux row, which files hold a copy).

Commands and results:
- `grep -l 'design-system-skills:trigger v1' C:/wamp64/www/*/CLAUDE.md */AGENTS.md`: **0 files**; `v2`: 14 files.
- Block hash (SHA-256 of the text between markers, LF-normalised): canonical `cced18e555f7…`; all 14 copies **SAME**. No documented variants remain.
- `python -X utf8 scripts/validate_engine.py --baseline tests/quality-baseline.json` (design): 101/101 compliant; `routing_smoke_test.py`: p@3 100%.

Engines without a block (accounting, windows-admin, engine-agents): unchanged; M10-02-T06 decides.

## M10-01-T14 — Impeccable source record refresh (IM-05): DONE

Upstream check, 29 Sep 2026 (free GitHub API through `gh api`, plus WebFetch of the slop page):
- `pbakaus/impeccable` `main` HEAD = `114ea1d3838fca73b253af45f873b9c4f5f213c8` (2026-09-28T17:12:18Z); licence `Apache-2.0`.
- `crates/foundation/src/registry.rs` at that commit: **61 unique rule ids**.
- impeccable.style/slop: "61 detector rules and 6 patterns for design review".
- Repository `CLAUDE.md`: v4 replaced the register with four modes; per-domain references
  (including `motion-design.md`, `responsive-design.md`, `ux-writing.md`) removed; `skill/reference/`
  listing confirms their absence.

Files:
- research: `docs/continuous-improvement/impeccable-slop-source-record-2026-09-29.md` (new; review
  date 2026-12-29); `impeccable-slop-source-record-2026-09-03.md` gains a "Superseded" banner
  linking forward (both-way cross-link).
- design: `design-audit/SKILL.md`, `ai-output-design/references/ai-slop-prevention/entrypoint.md`,
  `motion-design/SKILL.md` (`superseded-upstream`).
- dev: `tailwind-css/references/responsive-design/entrypoint.md`,
  `ux-content-strategy/references/ux-writing/entrypoint.md` (both `superseded-upstream`).

Commands and results:
- Re-grep "Bakaus" across all 13 engines: 5 lines, all 5 contain `Apache-2.0` and `114ea1d`.
- Research `skill_contract_validator.py --baseline tests/skill-engine/quality-baseline.json`: 59 fully compliant, exit 0; `validate_engine.py`: exit 0.
- Dev `skill_catalog_guardrails.py`: 0 findings, exit 0. Design validator: 101/101.

Open item: dev `docs/source-registers/skills-engine-currentness-2026-09.json` still classes
`impeccable-slop-catalog` as `context-bound` from the 3 Sep page; M10-09 can point it at the new record.

## M10-01-T15 — truthful website slop documentation: DONE

Files (website-skills): `skills/quality-gates/visual-qa/references/slop-rules.md` (coverage table of
what the script actually checks; families 2, 4, 5, 7, 8, 9, 10, 11, 12 marked "documented; not
automated; manual review required; script result NOT_ASSESSED"; `--palette-check` removed; real
output `reports/design-quality/slop-scan.md`; escalation split into automatic block, reviewer block
and warning; font check routed to the design engine's `banned-font-gate.js`),
`scripts/visual-qa.sh` (line 63 names the real report),
`design-quality-score/references/banned-patterns.md` (header: "The script hard-codes its patterns;
this file is the documentary catalogue"; "How the slop-scan uses this" corrected),
`design-quality-score/SKILL.md` (reference description),
`visual-qa/references/hierarchy-overflow-checks.md` (slop-scan does not count opt-outs),
`brand-voice/references/banned-phrases.md` (enforces a subset), `certification/exam.md` A25
(distractors are now real script checks).

Families 8 and 9 were also marked not automated: the script implements neither, so leaving them
unmarked would keep a false claim. `scripts/slop-scan.sh` is unchanged; its header comment still
says it reads `banned-patterns.md` and declares an exit code 3 it never emits. Handed to M10-11
(IM-03) because this task must not change the script.

Commands and results:
- `grep -rn 'palette-check\|slop-scan.json' skills scripts certification`: **0**.
- `bash scripts/slop-scan.sh fixtures/website-basic` (reports to scratchpad): exit 0 before and after; script diff empty.
- `python -X utf8 scripts/validate-skill-contracts.py --baseline quality/skill-contract-baseline.json`: "zero debt", exit 0.
- `python -m pytest -q`: 80 passed (includes `tests/gates/cases.json` pass/fail pairs).

## M10-01-T16 — dangling design routes: DONE

Files (website-skills): `AGENTS.md`, `CLAUDE.md`, `docs/relocation-map.md`, `skills/manifest.yml`,
`scripts/validate-skill-registry.py`, `certification/exam.md` (D3 now points at the banned-phrases
catalogue), `glossary.md`, `prompts/new-project-kickstart.md`, 15 skill reference files, and
`tests/test_kaizen_wave1_contracts.py`; new `tests/test_design_routes.py`.

- `design-system-skills:brand-alignment` → `design-system-skills:brand-visual-identity` (whose
  `references/brand-consistency-gate.md` and `trust-architecture-checklist.md` exist).
- `sectors/legal` → `design-system-skills:legal-sector-ui-ux`.
- Remaining `brand-alignment` lines outside history files are legacy-name redirect keys only:
  the relocation-map row and the manifest/validator `relocations` key (legacy name → new
  destination), and the relocated-skills notes in `AGENTS.md`/`CLAUDE.md`, now marked "historical
  name; folded into `brand-visual-identity`". History files untouched: `docs/engine-upgrade-july-2026/`,
  `MEMORY.md`, `tools/migrate_skills.py`.
- Validator: new sibling-existence check. Every `design-system-skills:<name>` route in live files
  (HTML-comment markers, history files and `tests/` excluded) must match
  `../design-system-skills/skills/**/<name>/SKILL.md`; a missing sibling reports `NOT_ASSESSED`.
- Count surfaces (masked failure from T07): the validator and `test_kaizen_wave1_contracts.py` now
  also read the 2026-09-28 README forms ("Its 62 active skills" and the `| \`category\` | N |`
  table), still compared with the filesystem. Decision taken under Peter's delegated authority,
  29 Sep 2026: accept the refreshed README format rather than re-add the old tree to a public README;
  the anti-drift control is kept, not weakened.

Commands and results:
- `python scripts/validate-skill-registry.py`: "design routes: PASS (8 routed design skills exist)", "registry valid: 62 skills", exit 0 (was exit 1 before).
- Fixture with `design-system-skills:no-such-skill`: `FAIL` naming the route; missing sibling: `NOT_ASSESSED`.
- `python scripts/routing-smoke-test.py`: 36/36; `python -m pytest -q`: 80 passed.

## M10-01-T17 — global CLAUDE.md: DONE

- Backup taken first: `global-CLAUDE.md.pre-T17-2026-09-29.bak` in this folder.
- Removed "(Embeds `proposal-skills` as a submodule.)" from the website-skills routing row; the
  Notes line now reads "Each engine is independent (no git-submodule embedding between engines, no
  mirroring)."
- Verified: website-skills has no `.gitmodules`, no submodule and no `proposal-skills` folder.
- `Select-String $env:USERPROFILE\.claude\CLAUDE.md -Pattern 'embeds'` equivalent: **0**.

Caution for the orchestrator: the backup copies Peter's private global instructions, including the
description of the private `political-essay-skills` engine, into a public repository's evidence
folder. Do not commit it to the public repo without Peter's say-so; keep it local or move it out.

## Decisions taken under delegation (29 Sep 2026)

- T13: trigger block option (a), runner-neutral wording, as canonical `v2`.
- T16: website count surfaces follow the refreshed README format (validator and test extended).
- T08: all six comma-joined `fixture_path` values fixed, not only case 022's.
