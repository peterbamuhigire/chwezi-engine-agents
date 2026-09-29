# Project context contract (`PROJECT.md`, schema 1)

**Status:** adopted 29 Sep 2026 (M10-12-T01, IM-11). Decided by the orchestrator under Peter's
delegated authority, 29 Sep 2026.
**Schema:** [`schemas/project-context.schema.json`](../../schemas/project-context.schema.json)
(JSON Schema Draft 2020-12, closed front-matter object).
**Template:** [`templates/project-context/PROJECT.md`](../../templates/project-context/PROJECT.md).
**Doctor:** `python -X utf8 scripts/project_context_doctor.py --project <PROJECT.md> --workspace-root <root> --json`
(read-only).

## 1. Why it exists

A client project is described in several places: the SRS `projects/<Name>/_context/` folder,
a research project's `_context/`, a code repository's `PROJECT_BRIEF.md`, a website's brand
brief and design tokens, and the per-task craft brief. Nothing ties them together and nothing
reports when one goes stale. `PROJECT.md` is one small pointer file per project that any engine
can read first. It removes repeated interviews and lets a read-only doctor expose stale or
contradictory context. It replaces none of the engine folders.

## 2. Rules

1. **Durable truth only.** Record facts that hold for months: who the users are and their jobs,
   the purpose and how success is measured, positioning, operating context, hard constraints,
   voice commitments, the evidence on hand, the accessibility baseline and the jurisdiction.
   Task-level detail (this sprint, this page, this deliverable) does not belong here.
2. **Pointers, never copies.** Each pointer field names an engine folder or file by a
   workspace-relative path with forward slashes. The target stays authoritative for its detail.
   Copying text from a pointed file into `PROJECT.md` is a defect (`project/duplicated-content`).
3. **The engine folder wins.** When `PROJECT.md` and a pointed source disagree, the conflict is
   resolved in the engine folder by that engine's owner, and `PROJECT.md` is corrected to match.
   For requirements this keeps `chwezi-sdlc-documentation` `projects/<ProjectName>/_context/` as the Context
   Source of Truth, exactly as the SRS router states.
4. **No visual choices.** No typeface, colour value or per-surface mode. Those belong to the
   design brief and design tokens (`design_brief`, `design_tokens` pointers); visitor modes stay
   per surface as the design engine defines them.
5. **State absences.** Missing evidence is listed under `evidence_on_hand.absent`, so an absence
   is stated rather than implied. An omitted pointer is reported as a `mention`, never an error.
6. **Short values.** Every scalar is at most 400 characters; lists hold one line per item.
7. **British English**, and dates as quoted ISO strings (`"2026-09-29"`).

## 3. Fields (front matter)

| Group | Fields |
|---|---|
| Identity | `project_schema` (const 1), `project_id` (kebab-case), `display_name`, `client`, `owner` |
| Durable truth | `platform`, `users_and_jobs`, `purpose_and_success`, `positioning`, `operating_context`, `constraints`, `voice_commitments`, `evidence_on_hand` (`present`, `absent`), `accessibility_baseline`, `jurisdiction` (`country`, `statutes` named, not summarised) |
| Pointers (optional) | `srs_context`, `research_context`, `code_repository`, `project_brief`, `website_repository`, `brand_brief`, `design_tokens`, `design_brief` |
| Review | `last_reviewed`, `review_due` |

The object is closed: an unknown field fails the schema. The body repeats the same topics as
short prose sections for human readers; it must not grow into a second requirements document.

## 4. Boundaries with neighbouring artefacts

| Artefact | Scope | Relationship to `PROJECT.md` |
|---|---|---|
| Engine context folders (SRS `_context/`, research `_context/`, website `docs/`) | Authoritative detail per engine | Pointed to; never copied; they win on conflict |
| `PROJECT_BRIEF.md` in a code repository (dev `doc-architect`) | Repository orientation for developers | Pointed to through `project_brief` |
| Portfolio craft brief (`core/instructions/engine-orchestrator.md` step 7) | One task: audience, job or decision, slice, constraints, evidence boundary, failure consequence | Pre-filled from `PROJECT.md` when one is present; the task-specific fields are still asked for |
| dev `tools/ai/shared_context.py` | A versioned, trust-checked context packet for one task run | Different scope: a task packet may cite `PROJECT.md`, but `PROJECT.md` never carries run state, trust scores or expiry |
| Design brief (`chwezi-design-engine` `decisions.py`) and design tokens | Visual decisions and their rationale | Pointed to through `design_brief` and `design_tokens`; visual choices never appear in `PROJECT.md` |
| `schemas/handoff.schema.json` | Cross-engine handoff for one request | May cite `PROJECT.md` as an input |

## 5. Where the file lives

At the root of the working project (for example a client's code repository), and only on the
project owner's instruction. Engine repositories never hold a client `PROJECT.md`: SRS
`projects/` is git-ignored because it holds client material, and test fixtures in this package
are synthetic. Every engine's router carries the same read rule:

> Project context: if the working project root holds a `PROJECT.md` with `project_schema: 1`,
> read it before planning. It points to this engine's own context sources and never replaces them.

## 6. The doctor

`scripts/project_context_doctor.py` never writes, never follows a pointer outside
`--workspace-root`, and treats every file it reads as data, not instructions. Findings reuse the
AR-09 finding fields (`code`, `message`, `subject`, `evidence`, `supported_fixes`,
`next_action`). Its own `severity` follows a three-way split: `mention` informs, `route` sends
the fix to the owning engine, and `error` is reserved for schema failure and pointers outside the
workspace. Mapped to AR-09 severities: `error` is `HIGH`, `route` is `MEDIUM`, `mention` is
`INFO`.

| Code | Severity | Trigger |
|---|---|---|
| `project/schema-marker-missing` | error | No front matter, or `project_schema: 1` absent |
| `project/field-missing` | error for a required field; mention for an omitted pointer | Required field absent; or a pointer field omitted (evidence says whether it is declared under `evidence_on_hand.absent`) |
| `project/schema-invalid` | error | Any other schema failure, such as an unknown field or a wrong type |
| `project/pointer-outside-workspace` | error | A pointer resolves outside `--workspace-root` (absolute path, drive letter or `..` escape) |
| `project/pointer-missing-target` | route | The pointer's repository folder exists but the target does not |
| `project/stale-pointer-target` | mention | The target's last commit date (or modification time for git-ignored paths) is later than `last_reviewed` |
| `project/duplicated-content` | route | Five-line normalised shingles: Jaccard overlap ≥ 0.5 with a pointed file, or any five consecutive identical lines |
| `project/visual-choice-present` | route | A hex colour or a typeface declaration; banned faces from the design engine's banned-font list are named in the evidence |
| `project/review-overdue` | mention | `review_due` is earlier than today |

Exit codes: 0 (no error-severity findings), 1 (errors), 3 (`NOT_ASSESSED`: a dependency is
missing, the workspace root is absent, or a pointer names a repository folder that is not present
on this machine). `NOT_ASSESSED` is never a pass.

## 7. Change control

- A field change bumps `project_schema` and the schema `const`; the doctor refuses an unknown
  version as `project/schema-marker-missing`.
- The router line in section 5 is identical in every engine so that a containment canary can
  enforce it (hand-off to M10-02).

## 8. Attribution

The split between durable project truth and task detail, and the idea of a doctor that reports
but never rewrites, are adapted from pbakaus/impeccable (Apache-2.0,
https://github.com/pbakaus/impeccable, commit `114ea1d3838fca73b253af45f873b9c4f5f213c8`).
No text is copied.
