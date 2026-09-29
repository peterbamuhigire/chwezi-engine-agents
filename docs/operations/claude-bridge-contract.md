# Claude bridge contract (portfolio)

Status: adopted in M10-02-T01 (29 Sep 2026). Applies to every public Chwezi repository: the eleven
catalogued domain engines and this coordination package. The private political-essay engine is out of
scope and is never checked.

## Why

`AGENTS.md` is the single, runner-neutral router and doctrine file for each repository. Claude Code reads
`CLAUDE.md`; Codex and other hosts read `AGENTS.md`. When both files carry doctrine they drift, because a
session in one runner updates only the file it reads. The bridge removes that surface: `CLAUDE.md` imports
`AGENTS.md` and carries nothing else except, optionally, a short note on how Claude Code itself behaves.

## The contract

`CLAUDE.md`, after CRLF is normalised to LF, must be exactly:

```text
# Claude Code repository memory

@AGENTS.md
```

(three lines, ending with one newline), optionally followed by one section:

```text

## Claude-only notes

<body>
```

Rules:

1. Line 1 is the heading `# Claude Code repository memory`; line 2 is blank; line 3 is `@AGENTS.md`.
   No other `@` import is permitted.
2. At most one further section, headed exactly `## Claude-only notes`, with no sub-headings.
3. The section is at most 25 lines, heading included.
4. The section holds **runner mechanics only**: how Claude Code loads or reaches something (for example,
   "skills are read directly, not through the native `Skill` tool", "skip the Codex-only sections of
   `AGENTS.md`"). It never holds doctrine: no routing rules, quality rules, bans, approval rules, the
   book-extraction rule, or the design trigger block. Doctrine lives in `AGENTS.md`, which the import
   loads for Claude anyway.
5. No UTF-8 byte-order mark.
6. `AGENTS.md` must exist beside `CLAUDE.md`.

The book-extraction ban is doctrine. It lives in `AGENTS.md`, not in the bridge. (Before M10-02 the dev
engine allowed a duplicated `## Never store book extractions` section in its bridge; that allowance is
withdrawn and the dev test follows this contract.)

## Single source for the Claude-only section

The body of the optional section is held in the engine's `.skills-engine/engine-manifest.yaml` as a literal
block under `claude_only_block:`. `scripts/render_host_files.py --render --engine <path>` writes `CLAUDE.md`
from the fixed bridge plus that block; `--check` fails when `CLAUDE.md` differs from what would be rendered.
The coordination package has no engine manifest; its bridge carries no Claude-only section.

## How it is checked

- `python -X utf8 scripts/render_host_files.py --check --workspace-root ..` (rule `bridge`), for every public
  repository, from this package.
- The dev engine's `tests/test_engine_control_plane.py` (`bridge_failures()`) applies the same contract
  inside that repository.

## Converting a fat `CLAUDE.md`

Before replacing a fat `CLAUDE.md`, write a sentence-level preservation map
(`docs/operations/m10-kaizen-evidence/M10-02/preservation/<engine>.md`): pre and post SHA-256 of both
files, and a table classifying each `CLAUDE.md` sentence as *duplicate* (already in `AGENTS.md`),
*doctrine-moved* (copied into `AGENTS.md`), *Claude-mechanics* (kept in the Claude-only section) or
*obsolete* (with a reason and owner sign-off). No sentence may be recorded as lost.

## Attribution

Canary-invariant and version-consistency checks adapted from DietrichGebert/ponytail (MIT,
https://github.com/DietrichGebert/ponytail, commit e3ba2aa); Windows hook failure modes adapted from
obra/superpowers release notes (MIT, https://github.com/obra/superpowers, commit 8ca22db).
