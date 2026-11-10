# Model classes and token economy (10 November 2026)

Status: adopted. Applies to every engine and project repository that carries `AGENTS.md` or `CLAUDE.md`, in Claude Code and Codex.

## Why

Usage evidence over 30 days showed that most cost was context carried between turns (cache reads and writes were roughly 88 to 90% of
API-equivalent value), not output. A fixed start-up load of 55,000 to 70,000 tokens (skill listings, connector tool names, global and
project instructions) was paid on every session. Long plans that were resumed by reading very large status files made this worse.

## Model classes (version-free)

Repositories name a class, never a model version. A model upgrade is then an edit in one owner-held routing file, not in every repository.

| Class | Role | Typical use |
|---|---|---|
| M Mundane | fastest, cheapest | mechanical work with a clear right answer: link checks, formatting, extraction |
| N Normal | default | executes an approved plan; routine implementation and drafting |
| X Expert | strongest standard class | planning, judging, hard debugging, final review |
| S Special occasion | premium class above X | rare; only through a written gate that includes approved billing |

A new model is classified by relative price and vendor positioning. With no S class available, X is the ceiling. Escalate one class
only on a trigger: two failed acceptance checks, an undecidable choice, or unreviewed money, tenant, security or legal work.

Subagent definitions pin a model through `model:` front matter and return summaries, not transcripts.

## Token rules (both runners)

- Start-up files: at most about 8,000 tokens; `AGENTS.md` at most 32 KiB; `CLAUDE.md` at most 32 KB. Move detail to reference files and read on demand.
- One task per session; clear or start a new thread between tasks; compact near 80%.
- Plan to a file, then execute in a fresh session. Resume a long plan from a small `RESUME.md` (at most 8,000 bytes); keep history in `archive/` and per-phase files, opened only when the active phase needs one.
- Read the router section, then one `SKILL.md`; search instead of loading; consult only the engine that matches the task.
- Cap tool output, disable unused MCP tools, keep a stable prefix, do not edit instruction files mid-session.
- Effort medium by default; high needs a recorded reason; the maximum needs approval.
- Parallel agents only with a written budget; batch or non-interactive runs only with an approved API budget.

## Enforcement

- `scripts/check_token_budget.py REPO_DIR ...` implements rules T-01 to T-07 (sizes, class block present and version-free, subagent pins, plan-file size).
- The class block is delimited by `MODEL-ROUTING-BLOCK` markers and is replaced as a unit.
- Monthly Kaizen first step: check the vendor's current model and pricing announcements and record `currency check YYYY-MM-DD: no change|changed`.
- Codex: the engine `.codex` policies set `model_reasoning_effort` to medium; the user-level config sets a post-turn compaction threshold, a tool-output token limit and a concurrency cap.

## Plan resume

Command: "resume plan-name". The runner reads only `docs/plans/<plan>/RESUME.md`, does one phase, updates `RESUME.md`, and tells the owner to start a fresh session.

## New device or fresh clone (do this before relying on any engine)

A rule that lives only in one machine's personal instruction file is not enforced on another. On every device that runs an engine:

1. Pull all engine repositories and confirm each carries the class block (marker `MODEL-ROUTING-BLOCK`) in `AGENTS.md` or `CLAUDE.md`.
2. Put the owner's class-to-model mapping and the token rules in that device's personal (global) instruction file, copied from the owner's routing file (`model-routing.json`). Repositories name classes only; the mapping is never copied into a repository.
3. Install the `resume-plan` command so "resume plan x" reads only the small `RESUME.md`.
4. Run `python scripts/check_token_budget.py <repo> [<repo> ...] --strict --deep` from this repository. Any FAIL (start-up file over its cap, missing block, unpinned subagent, oversize resume file, retired model ID) is fixed before work starts. A check that cannot be run is reported as NOT_ASSESSED.
5. Apply the organisation-level settings that live outside the repositories: engine consultation by task domain (one engine, a second only when the task spans two domains), and disable unused connectors and plugin skill listings.
6. Record the date and result in the monthly Kaizen note.

An agent that finds step 2 or step 4 missing on a device says so at the start of the session and does not continue silently.
