# Claude Code repository memory

@AGENTS.md

## Claude-only notes

- Read the workflow definitions in `agents/` and every engine `SKILL.md` directly; they are not
  registered with Claude Code's native `Skill` tool.
- An engine's `CLAUDE.md` is a bridge that imports its `AGENTS.md`, so either file gives the
  same router.
