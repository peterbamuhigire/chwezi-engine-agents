# CLAUDE.md - chwezi-engine-agents (Skills Engine Agents)

Coordination and maintenance layer for the eleven catalogued domain skills
engines. The primary router is [`README.md`](README.md); the Claude Code
adapter is [`adapters/claude-code/CLAUDE.md`](adapters/claude-code/CLAUDE.md).

How to use this package under Claude Code:

1. Resolve the engine for the current task from `catalog/engines.yaml`
   (paths are relative to `C:\wamp64\www\` on this machine).
2. Read that engine's own `CLAUDE.md` (falling back to `AGENTS.md` or
   `README.md`) before loading any of its `SKILL.md` files.
3. Use the three workflows in `agents/` — `engine-orchestrator`,
   `engine-maintainer`, `engine-validator` — by reading their definitions
   directly; they are not registered with Claude Code's native `Skill` tool.
   Canonical instructions live in `core/instructions/`.

Safety boundaries (binding):

- Read-only by default. `git pull --ff-only` only after an explicit user
  request in this session; skip dirty or diverged repositories; never reset,
  delete, merge manually, or force-push.
- Unavailable validation commands are reported as `NOT ASSESSED`, never
  treated as a pass.
- Writes, submissions, external messages, and publication require explicit
  user approval in this session.

Note: `README.md` documents Codex-specific installation and a
`~/.codex/...` validator path; those apply to the Codex host only and are
not expected to exist on this machine for Claude Code use.
