# M10-12 executor evidence — context contract, engine tours and skill graph

**Executor:** M10-12 executor (Claude Code), 29 Sep 2026. **Scope:** all tasks of M10-12 plus the
UA-11 case build. **Git:** no state-changing Git; every edit is left unstaged for the orchestrator.
**Decisions:** where the phase says "Peter ratifies", the recommended option was taken and is
recorded as *decided by orchestrator under Peter's delegated authority, 29 Sep 2026*.
**Operations record:** [`../../kaizen-2026-09-29-m10-12-context-tours-graph.md`](../../kaizen-2026-09-29-m10-12-context-tours-graph.md).

## T01 IM-11 contract — DONE

- Files: `docs/operations/project-context-contract.md` (112 lines), `schemas/project-context.schema.json`,
  `templates/project-context/PROJECT.md`, `scripts/validate-contracts.py` (Markdown instances are
  validated on their front matter).
- Commands: `validate-contracts.py --schema schemas/project-context.schema.json --instance templates/project-context/PROJECT.md` → PASS;
  same against `tests/fixtures/project-context/schema-invalid/PROJECT.md` → FAIL (`favourite_colour_scheme` unexpected), exit 2.
- The contract names the boundary with `shared_context.py` (task packets) and the craft brief, and
  keeps SRS `_context/` authoritative. Attribution: pbakaus/impeccable (Apache-2.0, commit `114ea1d`).
- Decision under delegation: contract wording and schema as proposed in the phase notes; one extra
  finding code `project/schema-invalid` for non-`required` schema failures (unknown field, wrong type).

## T02 IM-11 doctor — DONE

- Files: `scripts/project_context_doctor.py`, `tests/test_project_context_doctor.py`,
  `tests/fixtures/project-context/` (valid, nine seeded cases, synthetic workspace).
- Commands: `pytest tests/test_project_context_doctor.py` → 8 passed (each code from exactly one
  fixture; valid fixture exit 0 with no findings; tree hashes unchanged after runs; declared absence is
  a `mention`; absent repository folder is exit 3). Phase command 2 → exit 0.
- Severity: `error` only for schema failure and pointers outside the workspace; findings carry the
  AR-09 fields; severity mapping to AR-09 (`HIGH`/`MEDIUM`/`INFO`) is written into the contract.

## T03 IM-11 pilots — DONE

- Pilot files are outside every repository: `C:\Users\Peter\Documents\my-10-kaizen-private\M10-12\pilots\{medic8,birdc}\PROJECT.md`
  (SHA-256 `dd376a40…b7f83` and `e0eb3842…9b6d6`; doctor JSON `e7108b99…9c01` and `64677ee9…8b9c`).
- Doctor (`--workspace-root C:\wamp64\www`): Medic8 PASS, errors 0, duplicated-content 0, mentions 2
  (no project brief, no design brief: both declared absent). BIRDC PASS, errors 0,
  duplicated-content 0, mentions 4; the missing brand brief is a `mention` with `declared_absent: true`.
- Client repositories (`Medic8`, `birdc_erp`, `medic8-website`, `birdc-website`) and SRS `projects/`
  are unchanged; no `PROJECT.md` was placed anywhere in them.

## T04 IM-11 read rule — DONE

- Line (identical everywhere): "Project context: if the working project root holds a `PROJECT.md` with
  `project_schema: 1`, read it before planning. It points to this engine's own context sources and
  never replaces them."
- Files: `AGENTS.md` in srs-skills, business-plan-skills, website-skills, social-media-skills,
  linux-skills, proposal-skills, chwezi-dev-engine, chwezi-accounting-doctrine, design-system-skills,
  digital-research-engine, windows-admin-engine-skills and chwezi-engine-agents (+2 lines each);
  `core/instructions/engine-orchestrator.md` step 7.
- Deviation: the phase names `chwezi-engine-agents/CLAUDE.md`; that file is a checked thin bridge
  (`render_host_files.py` compares it with the registered block), so the line went into
  `chwezi-engine-agents/AGENTS.md`, which the bridge imports.
- Checks: `grep -c "project_schema: 1"` → 1 in each of the twelve `AGENTS.md`; the SRS rule "The source
  of truth for project context is `projects/<ProjectName>/_context/`" is unchanged (now line 149, shifted by the two inserted lines);
  all 26 catalogue validator commands exit 0; `render_host_files.py --check` → 0 findings.
- Registry change required: `catalog/shared-assets.yaml` coordination `plugin_exclusions` gains
  `tests/fixtures/*-workspace/*` (synthetic fixture skills), otherwise the check reported four
  `plugin-unlisted-skill` findings.
- Pre-existing uncommitted edits: design-system-skills showed `AGENTS.md` as modified before this
  edit (line endings only; `git diff --numstat` now shows +2/−0). Canary: adding the line to M10-02's
  canary invariants is a hand-off (M10-02), not done here.

## T05 UA-12 fan-in — DONE_WITH_LIMITATIONS

- Files: `scripts/skill_fanin.py`, `tests/test_skill_fanin.py`, fixture `tests/fixtures/engine-workspace/`;
  dev pointer line in `chwezi-dev-engine/skills/sdlc-meta/skill-engine-audit/references/audit-dimensions.md`
  (with the `NOT_ASSESSED` fallback).
- Results: dev 167 rows in 3.35 s (`Measure-Command`); dev count stays 167; fixture reports exactly the
  seeded `delta-orphan` as zero-inbound. Portfolio (`--all`): zero-inbound dev 14, SRS 36, accounting 61,
  social 33, design 13, windows 10, business plan 8, proposal 2, website 2, research 1, linux 0.
- Limitation: the M10-03 fixture adapters named in the phase (`portfolio_route_eval.py`) do not exist;
  fixture files are read directly with a generic key walk and the report says so. Reachability is
  copied from P01 (every row is `raw_candidate_reachability_unassessed`), not recomputed.

## T06 UA-09 tours — DONE

- Files: `scripts/generate_engine_tour.py`, `tests/test_generate_engine_tour.py`, `docs/engine-tours/*.json|md` (24 files).
- Results: 12/12 tours (9 or 10 steps each), two runs byte-identical (24/24 SHA-256), `--check` PASS with
  0 dangling paths and every manifest and catalogue gate command present. Dev display name is
  "Chwezi Dev Engine" (M10-01 fix present).
- Open item: tours record each engine's HEAD. Committing the T04 router lines moves eleven HEADs, so
  regenerate the tours after the engine commits and before the engine-agents commit
  (`python -X utf8 scripts/generate_engine_tour.py --workspace-root C:\wamp64\www --all`). The
  engine-agents tour is always one commit behind its own HEAD; `--check` reports that as a `stale`
  warning only.

## T07 UA-10 MCP `engine_tour` — DONE

- Files: `mcp-server/src/engine-tour.ts`, `mcp-server/src/index.ts`, `mcp-server/tests/engine-tour.test.ts`, `mcp-server/README.md`.
- Reads HEAD from `.git` as data (no Git or Python process); refuses a path outside the root with
  `path_boundary`; test asserts no write. `npm ci; npm run build; npm test` → 16 tests passed.

## T08 GR-01 spike — DONE (verdict KEEP)

- Files: `scripts/skill_graph.py`, `tests/test_skill_graph.py`, fixture `tests/fixtures/graph-workspace/`,
  `docs/skill-graph/skill-graph.json` (250 KB, compact one-edge-per-line), report
  `skill-graph-report.json` (this folder; every candidate with `path:line`).
- Graph: 1,183 nodes, 12,198 edges (links_to 1,238; routes_to 1,159; alias_of 37; mentions 9,214;
  defers_to 529; similar_trigger 21). Two runs byte-identical. Fixture detects the seeded retired
  alias and the seeded cross-engine collision; shrink guard refuses a > 20 % edge loss.
- Candidate defects and why each named guardrail missed them:

| Class | Count | Example `path:line` | Guardrails checked | Why missed |
|---|---|---|---|---|
| Dangling prose skill path | 155 lines, 45 references | `business-plan-skills/skills/meta-finance/meta-agent-bankability-and-investor-readiness/SKILL.md:146` (`skills/10-financial-projections/...`, real path `skills/pipeline/10-financial-projections/...`); `chwezi-dev-engine/skills/frontend-ux/pos-sales-operations-engineering/SKILL.md:179` | dev `skill_catalog_guardrails.py` (broken references); design route validators; business-plan `validate_skill_engine.py` (137/137 compliant) | They check Markdown links or `references/`/`templates/`/`scripts/` paths, not backticked `skills/...` prose paths |
| Retired alias named as a live skill | 237 lines, 130 files, 36 slugs | `chwezi-dev-engine/skills/saas/multi-tenant-saas-architecture/references/saas-deployment-models-decision-tree.md:3` (`saas-deployment-models`) | dev alias integrity; runtime budget (duplicate names); M10-03 collision gate | Alias checks read the registry and `ALIAS.md` files, not prose mentions |
| Renamed engine folder in a path | 5 lines | `business-plan-skills/skills/language/writing-quality/references/english-collocations-and-lexical-precision-2026-09-02.md:3` (`C:\wamp64\www\digital-research-skills\...`); `srs-skills/09-governance-compliance/31-kaizen-engine-and-product-improvement/references/book-driven-kaizen-wave-3-2026-09-02.md:5` (`skills-web-dev/...`) | `render_host_files.py --check`; all link checkers | No check reads prose paths for engine folder names |

- The orchestrator's `digital-research-skills` at step 4 is not a defect (it is the catalogue id and is
  explained in place); no in-flight M10 phase fixes the three classes above (grep of the phase files).
- Decision under delegation: KEEP, report-only; no dependency added; fixes handed to each engine owner
  and to M10-02 drift control.

## T09 GR-03 MCP `query_skill_graph` — DONE

- Files: `mcp-server/src/skill-graph.ts`, `mcp-server/src/index.ts`, `mcp-server/tests/skill-graph.test.ts`.
- Neighbours, path and explain for two known skills; unknown operation and skill refused; no write
  (asserted). Included in the 16 passing MCP tests.

## T10 AO-20 lifecycle map — DONE

- File: `README.md` ("## Lifecycle map" after "## Capabilities"; three capability rows added for T12).
- Every stage names at least one route; `generate_engine_tour.py --check-links README.md` → PASS (40);
  `validate-portfolio-craft.ps1` → PASS. Attribution: addyosmani/agent-skills (MIT, commit `2686b62`).

## T11 CV-05 usage scan — DONE

- Files: `scripts/skill_usage_scan.py`, `tests/test_skill_usage_scan.py`, fixture `tests/fixtures/usage-scan/` (synthetic).
- Output (local only): `C:\Users\Peter\Documents\my-10-kaizen-private\CV-05\skill-usage.csv` and
  `skill-usage-summary.json`. Counts are in the operations record; no transcript text in any output
  (test asserts it); an output path inside `C:\wamp64\www` is refused (exit 1, tested).
- Spot-check (all-time run, Read calls): strategy-personal-brand 20/20, playbook-agency-operations 11/11,
  playbook-paid-social-advertising 11/11, biz-dev-proposal 10/10, source-evaluation 1/1 → 5/5.
  `rg` is not installed, so the manual count used `grep -r -o -E` over the transcripts.
- Codex: the `exec` custom-tool shape was recognised; 32 files parsed.

## T12 phase close — DONE_WITH_LIMITATIONS

- Files: `docs/operations/kaizen-2026-09-29-m10-12-context-tours-graph.md`, `CHANGELOG.md`,
  `README.md` capability rows, `.github/workflows/validate.yml` (doctor, fan-in, tour, graph and usage
  tests; template schema check; tour generation and `--check` on the fixture workspace; MCP tests
  already run in the existing step).
- Limitation: CI green is `NOT_ASSESSED` until the orchestrator pushes; the local equivalents pass
  (162 Python tests, 16 MCP tests).

## UA-11 orientation case — DONE_WITH_LIMITATIONS (execution NOT_ASSESSED)

- Files: `evals/cases/077-orientation-dev-tour.yaml`, `evals/fixtures/077-orientation-dev-tour/{task.md,expected.yaml}`.
  Number 077 was the next free number after checking `evals/cases` (M10-05 added no numbered case).
- Six questions; every expected path is present in `docs/engine-tours/chwezi-dev-engine.md` (checked).
  `run-contract-evals.py` → 77/77 PASS. No `run_mode` key, so M10-03's acceptance count (12) is unchanged.
- Execution needs a model: `NOT_ASSESSED (zero-spend rule)`.
- For M10-05: `run_behavioural_eval.py --suite orientation --case-file evals/cases/077-orientation-dev-tour.yaml --dry-run`
  validates the case but resolves `document` inside the engine checkout, so it reports the tour as absent.
  The runner needs to resolve the document from chwezi-engine-agents (owner: M10-05).

## Open items for the orchestrator

1. Regenerate tours after committing the eleven engine `AGENTS.md` changes (see T06).
2. `catalog/shared-assets.yaml` also carries another executor's hunks (M10-11 vendored-detector rows; mine is
   only the `plugin_exclusions` entry); stage by hunk.
3. Defect fixes found by the spike belong to business-plan-skills, chwezi-dev-engine, srs-skills and the
   four language references; hand-off to M10-02 and the engine owners.
4. M10-02: add the router line to the canary invariants.
