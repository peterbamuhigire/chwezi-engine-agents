# M10-08 evidence — SRS elicitation, as-built recovery and test design

Executor scope: all M10-08 tasks in `C:\wamp64\www\srs-skills`, plus the one AC-05 pointer line in
`C:\wamp64\www\chwezi-dev-engine\skills\sdlc-meta\advanced-testing-strategy\SKILL.md`, plus the two
M10-07 hand-offs (`EI` prefix; titled-FR stimulus-response pattern). Date: 29 September 2026. Zero
spend: local tools only. No commits, pushes, resets or branch changes. Client workspaces under
`srs-skills/projects/` were read only (GarageFlow, KampusPad for impact measurement);
`projects/_demo-hybrid-regulated` was re-seeded by the §7 command `seed_demo_project.py` (gitignored).
A temporary probe workspace `projects/_m1008probe` was created with `engine new-project` to check the
seed and removed afterwards (it was created by this executor).

srs HEAD at start: `6218681`; during execution another executor committed `9b8a27f` (M10-04 T07).
srs working tree was clean at start. chwezi-dev-engine held other executors' uncommitted files
(M10-04 skill-writing work); only `advanced-testing-strategy/SKILL.md` was touched here.

## Summary

| Task | Status |
|---|---|
| T01 SP-01 (SRS part) | DONE |
| T02 SP-15 | DONE |
| T03 GR-10 | DONE |
| T04 GR-11 | DEFERRED — NOT_ASSESSED (no annotated codebase) |
| T05 UA-06 | DONE (client use NOT_ASSESSED) |
| T06 UA-07 | DONE |
| T07 UA-08 | DONE |
| T08 AO-19 | DONE |
| T09 AC-05 | DONE_WITH_LIMITATIONS (29119-4 clause number NOT_ASSESSED) |
| T10 UX-10 | DONE |
| T11 CV-04 | NO CHANGE (decision rule not met) |
| Hand-off: `EI` prefix | DONE |
| Hand-off: `**FR-nnn Title.**` pattern | DONE |

## T01 — New Project Protocol no longer depends on an external plugin

- `AGENTS.md` (the protocol moved there under M10-02 PT-01; `CLAUDE.md` is the `@AGENTS.md` bridge and was
  not touched): step 1 is now the engine-native gate (decision-frontier elicitation, intent write-back, stop
  until the owner confirms; ceremony classification) and states that `superpowers:brainstorming` is optional
  where installed. The duplicate "5." is fixed; steps run 1–11 without duplicates. "ask during brainstorming
  session only" became "ask during the shared-understanding step only".
- `rules/common/core.md`: heading "Brainstorming is mandatory…" became "Establish shared understanding before
  starting a new project"; text rewritten to match. Not a generated or hash-checked copy (grep of srs and
  chwezi-engine-agents scripts found no drift control on it), so it was edited directly.
- `SETUP_GUIDE.md`: Step 4 heading, the "Kick-off Prompt" subsection, the prompt wording and the line-152
  statement now name the decision-frontier method; plugin optional.
- Residue beyond the three named files: `scripts/setup-srs-project.sh` and `.ps1` echoed "Run the brainstorming
  skill"; two echo lines each changed to "Run the shared-understanding step" / "Paste the kick-off prompt".
- Check: `grep -rn "superpowers:brainstorming" CLAUDE.md AGENTS.md rules/ SETUP_GUIDE.md` → 3 lines, all
  "may be used as an optional aid … it is not required". No mandatory mention remains.
- `python -m engine validate-skills` → SKILLS OK; `python scripts/validate_engine.py` → exit 0.
- Doctrine class: requires Peter's ratification before merge (phase §9).

## T02 — Ceremony classification, section-scoped approval, Review Focus

- New `02-requirements-engineering/fundamentals/before/02-elicitation-toolkit/references/ceremony-and-section-approval.md`
  (bounded / architectural / spike; ratchet-upwards rule; one numbered IEEE section at a time; approval log row).
- Linked from the toolkit's References and from Workflow step 1 (net +2 lines: 429 → 431, cap 500), and from
  `references/decision-frontier-elicitation.md` (shared-understanding gate continues into drafting).
- `07-requirements-validation/SKILL.md`: new Step 7 "Review Focus" with the six-column table template
  (No., Implied condition, Why it matters, Acceptance criterion, Disposition, Owner) and the cap-of-five stop
  rule; later steps renumbered 8–9; output format gains "9. Review Focus"; checklist item added; References
  link. Detail in new `references/review-focus.md` (three worked rows).
- Golden-path example: new `templates/project-examples/uganda-public-sector/_context/elicitation-log.md` with the
  ceremony classification, three per-section approval rows (approved / approved with conditions / returned) and
  a Review Focus table of 3 rows, each with an acceptance criterion, disposition and owner. README line added.
  Checked by scaffolding a probe (`engine new-project _m1008probe --example uganda-public-sector`): the file is
  copied; it raises no marker or identifier findings (the probe's other findings are the expected empty-seed
  phase-gate findings).
- Attribution line (Superpowers, MIT, commit 8ca22db…) in both references.
- `validate_skill_engine.py --baseline` → 159 active, `failure_counts: {}`.
- `validate_decision_frontier.py templates/decision-frontier.yml` → `decisions=1 findings=0 frontier=DEC-001`, exit 0.

## T03 — As-built recovery

- New `03-design-documentation/01-high-level-design/references/as-built-recovery.md`: the five-step procedure,
  the quoted guard from `04-requirements-analysis` (Fixed policy row, line 167), `[AS-BUILT]` / `[VERIFY: reason]`
  tagging, commit pin (`generated_from_commit`, `source_repository`, `referenced_paths`), M10-07 diagram IR for
  recovered figures, the PHP member-call grep cross-check, and a checklist. Tooling points to the dev engine's
  GR-05 reference `skills/sdlc-meta/ai-assisted-development/references/graph-first-codebase-comprehension.md`
  (committed in dev `65e3315`). No install command and no product recommendation (Graphify named in the
  attribution only).
- Linked from HLD, LLD and Database Design References.
- HLD `description` gained "or an as-built design must be recovered from existing code" (326 characters, within
  the 350 limit) so the positive routes.
- Kernel: `engine/parsers/markers.py` `_KNOWN_TAGS` gains `AS-BUILT` and `VERIFY`. Finding: the phase file said
  these tags "parse today"; they did not — the parser drops tags not in `_KNOWN_TAGS`. They are NOT added to
  `_BLOCKING_TAGS`. Whether unresolved `[VERIFY]` should block client delivery is left for Peter to ratify.
- Test `engine/tests/test_as_built_markers.py` over fixture `engine/tests/fixtures/as_built/`: `all_markers()`
  returns exactly `{AS-BUILT: 3, VERIFY: 2}` with the expected reasons; markers quoted in inline code are ignored;
  the blocking-marker gate reports 0 findings.
- Routing fixtures (clearly commented with a `comment` field): `as-built-recovery-positive` ("Produce as-built
  design documentation for an existing PHP ERP." → `01-high-level-design`, rank 1) and the owned negative
  `as-built-schema-neighbour` (kind `collision`: schema recovery → `04-database-design`, HLD rank 2). The srs
  script does not yet support an `owner` field (M10-03-T08); the comment invites M10-03 to convert it.
  Fixture count 54 → 56; `tests/skill-quality-baseline.json` `routing.fixture_count` updated to 56.
- `routing_smoke_test.py` → 56/56, top-3 precision 1.000.
- Doctrine class: requires Peter's ratification (as-built doctrine and the `[VERIFY]` blocking question).

## T04 — `@req` annotation traceability (GR-11)

DEFERRED — NOT_ASSESSED (no annotated codebase). Peter named `C:\wamp64\www\Garage` (HEAD
`273a2bb2f17c26a13c8c3ac98e625e560745c83a`, 685 PHP files outside `vendor/`). Read-only
`grep -rIl -E "@req\b" --exclude-dir=vendor --exclude-dir=node_modules` returned no files, so the phase's
condition ("a codebase where the team will maintain annotations") is not met. No extractor or `code_trace.py`
was written; the traceability check is unchanged. Decided by orchestrator under Peter's delegated authority,
29 Sep 2026 (plan default: "Default if no annotated codebase is named").

## T05 — System orientation guide

- New `04-development-artifacts/03-dev-environment-setup/references/system-orientation-guide.md` (fixed seven-part
  outline, ordering rule, 5–15 steps, prose steps, evidence-based hotspots, pin and staleness), `templates/system-orientation-guide.md`
  (frontmatter `generated_from_commit`, `source_repository`, `referenced_paths`) and
  `examples/system-orientation-guide-srs-engine.md` (11-step reading path over `engine/`, pinned to `9b8a27f…`;
  hotspots measured with `git log --format= --name-only -- engine` and `wc -l`). Linked from `SKILL.md`
  References and the Integration table. Cross-links the dev engine's `doc-architect/references/code-tour.md`
  (UA-02 topology tour).
- Test `engine/tests/test_system_orientation_example.py`: every `engine/…` path in the reading path and file map
  resolves (0 unresolved, ≥ 12 cited), 5–15 steps, frontmatter pin well-formed, template present with the three keys.
- Client use of the guide: NOT_ASSESSED (expected limitation).

## T06 — Commit-pinned staleness check

- New `engine/checks/generation_staleness.py` (`GenerationStalenessGate`, id `kernel.generation_staleness`),
  registered in `engine/cli.py::_default_registry()`, so `python -m engine validate` runs it. Report-only
  (MEDIUM / INFO; never blocking).
- Behaviour: reads frontmatter only for the pin; SHA must match `^[0-9a-f]{40}$` and be a quoted string (an
  unquoted numeric SHA is parsed by YAML as an integer and is rejected); `source_repository` resolved relative to
  the project root (absolute allowed); referenced paths = `referenced_paths` plus backticked body paths containing
  `/`; paths resolving outside the repository are rejected (`staleness/path-outside-repository`) and never passed
  to Git; one `git --no-replace-objects -C <repo> diff --name-only <sha> HEAD -- <paths>` per document via
  `subprocess.run` argument list, 30-second timeout; `staleness/changed-since-generation` per changed path;
  repository absent or not a work tree → one INFO `NOT_ASSESSED: source repository unavailable`; unknown commit →
  `staleness/unknown-commit`.
- Interpretation recorded: the phase note "rejects paths containing `..` after resolution outside the declared
  root" is applied to referenced paths against the source repository root, because the source repository itself
  normally lives outside the project root (e.g. `../garage-erp`).
- Test `engine/tests/test_check_generation_staleness.py` (19 cases, temporary Git repositories): one changed
  referenced file → exactly that file; no change → none; repository absent → one INFO `NOT_ASSESSED`; malformed
  SHA rejected (6 parametrised values plus in-document and unquoted-numeric cases); unknown commit; containment;
  gate registered and non-blocking.

## T07 — User-manual walkthrough ordering

`08-end-user-documentation/01-user-manual/SKILL.md`: Step 5 gains the ordering rule (foundational screens →
dependent workflows → administration; 5–12 steps per role); checklist item 5 extended; attribution line added.
`grep -n "foundational screens"` → lines 171 and 239. Routing smoke test unchanged in result (56/56).

## T08 — Agent build brief (executed by a sub-agent of this executor)

- New `engine/agent_brief.py`, `scripts/create_agent_build_brief.py`, `templates/agent-build-brief.md`,
  `engine/tests/test_agent_brief.py` (8 tests; module coverage 98 %), golden
  `engine/tests/fixtures/agent_brief/healthcare_admissions.golden.md`; one paragraph in
  `docs/sdd-phase-boundary-contract.md`. The healthcare fixture was not modified; variants are built in `tmp_path`.
- `python scripts/create_agent_build_brief.py --project engine/tests/fixtures/healthcare_admissions --out <scratch>/brief.md`
  → `entries=26 untraced=0 context_gaps=3`, exit 0; matches the golden file. The three gaps are honest (the
  fixture records no build commands, conventions or test commands). A variant with commands and conventions but no
  test commands yields exactly one `CONTEXT-GAP`, which `NoUnresolvedFailMarkersGate` reports as blocking.
- Limitation: Commands, Structure, Conventions and Never are found by section-heading matching; SRS text under
  other headings shows up as gaps.

## T09 — Pairwise combinatorial test design (executed by a sub-agent)

- New `05-testing-documentation/02-test-plan/references/pairwise-combinatorial-test-design.md`; linked from the
  technique step (Step 4) and References of `02-test-plan/SKILL.md`.
- Worked example: 4 parameters (channel 3, connectivity 2, currency 2, role 3), 1 constraint (card cannot be
  offline-queued). Full product 36 (30 allowed); the table has **9 cases**, the minimum possible (3 channels × 3
  roles). `engine/tests/test_pairwise_example.py` parses the model and table from the reference and checks
  ≥ 4 parameters, ≥ 1 constraint, no violating row, every allowed pair covered, 9 < 36 → pass.
- Attribution SHAs via `git ls-remote`: omkamal/pypict-claude-skill `fbda212bca79dfa7611be12527b102c89cc8faeb`,
  microsoft/pict `ab76c2548f551fcb46314e58653a1bd1172f3a72`; SPDX discrepancy (licence file MIT, API NOASSERTION)
  recorded.
- ISO/IEC/IEEE 29119-4 clause number: NOT_ASSESSED (standard not available offline); the reference cites the
  standard without a clause number and tells the reader to confirm against the edition held.
- Dev pointer: one line under `## References` in `chwezi-dev-engine/skills/sdlc-meta/advanced-testing-strategy/SKILL.md`
  linking to the srs reference on GitHub; no content duplicated. The link resolves only after the srs commit is pushed.
- Dev checks: `python scripts/skill_catalog_guardrails.py` → exit 0, 167 active skills, 0 errors (14 pre-existing
  size warnings); `python -X utf8 scripts/routing_smoke_test.py` → p@3 187/187, p@1 179/187, 0 failures.
  Dev CI status for this phase: NOT_ASSESSED (local runs only).

## T10 — Controls search (executed by a sub-agent)

- New `engine/controls_search.py` (standard-library BM25, k1 1.5, b 0.75, in-module synonym map, corpus-wide IDF
  so filters do not move the threshold), CLI group `python -m engine controls search "<q>" [--domain] [--framework]
  [--top] [--json]` in `engine/cli.py` (read-only), tests `engine/tests/test_controls_search.py` (20 tests, 100 %
  module coverage), calibration fixture `engine/tests/fixtures/controls_search_queries.json` (6 positive, 6 nonsense).
- Threshold 5.5: lowest positive top score 7.016 (margin 1.516); highest nonsense 4.447 (margin 1.053).
- `controls search "cardholder encryption" --domain finance --json` → not abstained, `CTRL-FIN-001` first
  (score 7.016, `domains/finance/controls/control-register.yaml`). `controls search "purple elephant tariff" --json`
  → `"abstained": true`, `results: []`, best score 0.0.
- Value-gate condition met: `09-governance-compliance/03-compliance-documentation/SKILL.md` now tells the drafter
  to run the command and cite the ID and registry path, not paraphrase. Corpus is small (39 controls); recorded.
- Limitation: single-word queries score about 3–5 and may abstain; add a second term.

## T11 — CV-04 router slimming: NO CHANGE

Decision rule (phase §5 notes), measured 29 Sep 2026 with `kaizen_portfolio_snapshot.py` (M10-02 CV-01 fields):

1. CV-01 data recorded: yes — M10-02 evidence (srs `router_effective_bytes` 49,732 after PT-01). Re-measured on
   the working tree including this phase's T01 edit: `router_bytes` 44, `router_import_bytes` 50,258,
   `router_effective_bytes` 50,302.
2. srs largest among primary engines: yes — dev 15,238; design 11,489; website 40,929; srs 50,302.
3. V&V SOP plus documentation and writing standards ≥ 25 % of srs effective bytes: **no**. In `AGENTS.md` the
   "Verification & Validation (V&V) Standard Operating Procedure" section is 5,329 bytes and "Documentation &
   Writing Standards" 2,861 bytes: 8,190 bytes = 16.3 % of 50,302 (16.5 % of the M10-02 figure 49,732). Even the
   whole contiguous block from Documentation & Writing Standards through the V&V SOP (adding Prohibited Actions,
   the Anti-AI-Slop gate and the Git commit protocol) is 11,310 bytes = 22.5 %.

Rule 3 fails, so no content was moved. PT-01 had already made `CLAUDE.md` a 44-byte bridge; the sections live in
`AGENTS.md`. No byte target is proposed (P04). Decided by orchestrator under Peter's delegated authority,
29 Sep 2026 (plan default "no change unless the decision rule is met").

## M10-07 hand-offs folded in

- `engine/idscan.py` `KIND_PREFIXES` gains `EI` (external-interface ids). Test `engine/tests/test_idscan.py`
  (recognition incl. module-prefixed `EI-PAY-012`; `SEI-001`, `EI-12`, `xEI-004` not matched). Read-only check on
  GarageFlow: 10 distinct `EI-` ids now recognised, which should remove the dry run's 11 `diagram/unknown-trace-id` false
  positives (the scratch copy no longer exists, so not re-run). Behaviour change: `sync` will now register `EI-` ids in workspaces that use them.
- `engine/checks/stimulus_response.py` `_FR` now also matches `**FR-nnn Title.** …`. Tests in
  `test_check_stimulus_response.py`: titled FR with "shall" passes; without "shall" flagged; `stimulus_response_frs`
  (diagram trace) recognises titled FRs. Impact measured read-only across `projects/`: 304 titled FRs newly
  recognised (GarageFlow 178, KampusPad 126), **0** newly flagged (all use "shall"); GarageFlow FR-108 is now
  recognised, removing the dry run's `diagram/unmapped-sequence` false positive.

## Verification (srs-skills, repository root)

Transcripts: `srs-pytest.txt`, `srs-verify.txt` in this folder.

| Command | Result |
|---|---|
| `pytest --cov=engine --cov-fail-under=90` | exit 0; 426 passed, 2 skipped; coverage 96.81 % |
| `python scripts/validate_engine.py` | exit 0 |
| `python scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | 159 active, `failure_counts: {}` (report-only byte warnings from M10-04) |
| `python -X utf8 scripts/routing_smoke_test.py` | 56/56, top-3 precision 1.000 |
| `python -m engine validate-skills` | SKILLS OK |
| `python scripts/validate_decision_frontier.py templates/decision-frontier.yml` | exit 0, 0 findings |
| `python scripts/validate_sdd_phase_boundaries.py --feature-dir engine/tests/fixtures/sdd_feature` | PASS |
| `python scripts/seed_demo_project.py` | seeded |
| `python -m engine validate projects/_demo-hybrid-regulated` | ENGINE CONTRACT: PASS |
| `… --break-something` | FAIL as designed (exit 1, 3 synthetic HIGH) |
| `python -m engine controls search "cardholder encryption" --domain finance --json` | CTRL-FIN-001 first |
| `python -m engine controls search "purple elephant tariff" --json` | abstained |
| `python scripts/create_agent_build_brief.py --project engine/tests/fixtures/healthcare_admissions --out <scratch>` | entries 26, untraced 0 |
| `grep -rn "superpowers:brainstorming" CLAUDE.md AGENTS.md rules/ SETUP_GUIDE.md` | 3 optional mentions, 0 mandatory |

`pip install -c requirements-ci.txt -e ".[dev]"` was not re-run (environment already installed; tests run
against the working tree).

## Open items for the orchestrator / Peter

1. Ratification (doctrine class): T01, T02, T03; and the question whether unresolved `[VERIFY]` should block
   client delivery (not added to `_BLOCKING_TAGS`).
2. The dev pointer (T09) links to the srs GitHub path; it resolves once the srs commit is pushed.
3. M10-03-T08 may convert `as-built-schema-neighbour` into an `owner`-field negative.
4. The `EI` prefix makes `python -m engine sync` register `EI-` ids in client workspaces on the next run
   (GarageFlow, KampusPad); registry diffs there are expected.
5. Independent reviewer verdicts are pending for the three slices and T11.
