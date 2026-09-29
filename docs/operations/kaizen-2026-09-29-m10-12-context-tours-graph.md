# Kaizen record — M10-12 context contract, engine tours and skill graph (29 Sep 2026)

**Phase:** M10-12 (my-10-kaizen). **Executor evidence:**
[`m10-kaizen-evidence/M10-12/M10-12-context-tours-graph-evidence.md`](m10-kaizen-evidence/M10-12/M10-12-context-tours-graph-evidence.md).
**Decisions:** taken by the orchestrator under Peter's delegated authority, 29 Sep 2026, using the
phase file's recommended options. The record is dated 29 Sep 2026 rather than the planned
`2026-10-DD` because the phase ran on that day.

## What changed

| Task | Result |
|---|---|
| T01 IM-11 contract | `project-context-contract.md`, `schemas/project-context.schema.json` (closed object), `templates/project-context/PROJECT.md`; `validate-contracts.py` reads Markdown front matter |
| T02 IM-11 doctor | `scripts/project_context_doctor.py` (read-only; nine finding codes, one seeded fixture each) |
| T03 IM-11 pilots | Medic8 and BIRDC pilots kept outside every repository; doctor PASS, 0 errors, 0 duplicated-content |
| T04 IM-11 read rule | One identical line in the eleven engine `AGENTS.md` files and this package's `AGENTS.md`; orchestrator step 7 pre-fills the craft brief |
| T05 UA-12 fan-in | `scripts/skill_fanin.py`; dev pointer in `skill-engine-audit/references/audit-dimensions.md` |
| T06 UA-09 tours | `scripts/generate_engine_tour.py`; 12 tours (24 files) under `docs/engine-tours/` |
| T07 UA-10 MCP | Read-only `engine_tour` tool (`mcp-server/src/engine-tour.ts`) with tests |
| T08 GR-01 spike | **KEEP**: `scripts/skill_graph.py`, `docs/skill-graph/skill-graph.json` |
| T09 GR-03 | Read-only `query_skill_graph` tool (`mcp-server/src/skill-graph.ts`) with tests |
| T10 AO-20 | "## Lifecycle map" in `README.md` after "## Capabilities" |
| T11 CV-05 | `scripts/skill_usage_scan.py`; CSV and summary kept outside every repository |
| UA-11 | Case `evals/cases/077-orientation-dev-tour.yaml` built; execution `NOT_ASSESSED` (zero-spend rule) |

## Commands and results (local, 29 Sep 2026)

| Command | Result |
|---|---|
| `python -X utf8 -m pytest tests -q -p no:cacheprovider` | 162 passed |
| `project_context_doctor.py --project tests/fixtures/project-context/valid/PROJECT.md --workspace-root tests/fixtures/project-context/workspace` | exit 0 (stale mentions only, from checkout times) |
| Doctor on the Medic8 and BIRDC pilots, `--workspace-root C:\wamp64\www` | PASS; errors 0; duplicated-content 0; mentions 2 and 4 (declared absences; BIRDC brand brief is a mention) |
| `generate_engine_tour.py --all` twice, then SHA-256 of `docs/engine-tours/*` | 24/24 identical |
| `generate_engine_tour.py --all --check` | PASS: 12 tours, 0 dangling paths, 0 missing gate commands |
| `generate_engine_tour.py --check-links README.md` | PASS: 40 links and routes |
| `mcp-server`: `npm ci; npm run build; npm test` | build clean; 16 tests passed (6 files) |
| `Measure-Command { skill_fanin.py --engine chwezi-dev-engine --json }` | 3.35 s; 167 rows |
| `skill_graph.py` twice | graph and report byte-identical |
| `skill_usage_scan.py --since 2026-08-01 --until 2026-09-30` (Claude plus Codex) | written outside the repositories; 5/5 spot-check match |
| `render_host_files.py --check --workspace-root C:\wamp64\www` | 12 repositories; 0 findings |
| Catalogue validators of all eleven engines (26 commands) | all exit 0 |
| `skill_catalog_guardrails.py` (dev) | 167 active; 0 errors |
| `validate-catalog.ps1`, `validate-portfolio-craft.ps1`, `validate-prompt-capability.ps1`, `validate-no-book-extractions.py`, `validate-kaizen-cards.py`, `validate-routing-baseline.py`, `run-contract-evals.py` (77/77), collision scan (0 undeclared) | all pass |

## Pilot hashes (files kept outside every repository)

| File | SHA-256 |
|---|---|
| `my-10-kaizen-private/M10-12/pilots/medic8/PROJECT.md` | `dd376a40aca5859fec8a831bad76f17347baf6dae8fd03a16da55e8fe55b7f83` |
| `my-10-kaizen-private/M10-12/pilots/birdc/PROJECT.md` | `e0eb3842f1b44db17689bb365e86e18492f2514776cebc9e086e499eb5a9b6d6` |

No `PROJECT.md` was placed in any client repository; that waits for Peter's instruction.

## Spike verdict (GR-01): KEEP

Three defect classes that no named guardrail reports (dev `skill_catalog_guardrails.py`, design
`validate_route_existence.py` and `validate_cross_engine_routes.py`, SRS `validate-skills`,
`validate-runtime-skill-budget.py`, the M10-03 collision gate and ownership register, and
`render_host_files.py --check`):

1. **Dangling prose skill paths:** 155 lines (45 distinct references), 151 of them in
   business-plan-skills, which cites `skills/10-financial-projections/...` where the tree is
   `skills/pipeline/10-financial-projections/...`; the dev engine cites
   `skills/sdlc-meta/reliability-engineering` (now `skills/devops-cloud/`). The link checkers read
   Markdown links and `references/` paths only; these are backticked prose paths.
2. **Retired alias slugs named as live skills:** 237 lines in 130 files (36 slugs), mostly in the
   dev engine, for example `` `saas-deployment-models` `` and `` `dual-auth-rbac` ``. The alias
   integrity check reads the registry, not prose.
3. **Renamed engine folders:** five lines point at `C:\wamp64\www\digital-research-skills\...` or
   `skills-web-dev/...`; no guardrail reads these paths.

The graph stays report-only: never a routing input, loader or CI gate (P04). No NetworkX or other
dependency was added. The fixes belong to the owning engines under drift control (hand-off to
M10-02 and each engine's owner); the per-line list is in
`m10-kaizen-evidence/M10-12/skill-graph-report.json`.

## Usage evidence (counts only; CV-05)

Window 2026-08-01 to 2026-09-30; 450 Claude transcript files and 32 Codex session files (Codex
shape recognised and parsed). 1,177 inventoried skills; 168 EXTRACTED reads and 2,971 INFERRED
reads; 958 SKILL.md reads could not be mapped to the P01 inventory (variables in loops, skills
consolidated since P01, copies outside the engines); 32 private-engine paths dropped unread.
**587 skills were never read in the window** (dev 73 of 168, SRS 97 of 160, social media 109 of
191, business plan 73 of 137, accounting 70 of 108, proposal 60 of 115, linux 34 of 48, design 24
of 102, research 24 of 61, windows 14 of 21, website 9 of 63). Top-decile threshold 7 reads (135
skills at or above); bottom decile 0.

Interpretation rule: zero reads in the window is dead-load *evidence* for consolidation review,
never a retirement decision. The data covers one machine and one user's sessions and cannot see
sessions on other hosts. The CSV (SHA-256 `d9969af47c8091e496391eaee2b0ea9126f62412d68187b66644067a112b2b3f`)
stays local.

## NOT_ASSESSED

- UA-11 execution (needs a model; zero-spend rule). The M10-05 runner resolves the case document
  inside the engine checkout, so its dry run reports the tour as absent; see the evidence file.
- CI for the portfolio-wide tour, fan-in and graph runs: CI cannot see sibling repositories; it
  runs the fixture-workspace variants only.
- `rg` is not installed on this host; the CV-05 spot-check used the equivalent `grep -o` count.

## Rollback

Each part is additive. Revert the router line per engine; delete the new scripts, tours, graph and
MCP source files; remove the two tool entries in `mcp-server/src/index.ts` to restore the
four-tool server.
