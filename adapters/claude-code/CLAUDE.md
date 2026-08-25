# Skills Engine Agents for Claude Code

At the start of a task, resolve the current Git root and read the matching
entry in `catalog/engines.yaml`. Then read that engine's `AGENTS.md` or
`README.md` router before loading any domain `SKILL.md`.

Load the canonical instructions from the installed package's `core/instructions`
directory. Use the `engine-orchestrator`, `engine-maintainer`, and
`engine-validator` wrappers for the three workflows. If the host lacks shell,
Git, web, structured output, or approval, follow the capability profile and
return `NOT ASSESSED` or a blocked result as required.

Pulls, writes, submissions, external messages, and publication require an
explicit user approval in this session. Provider/model settings belong to
Claude Code or its configured endpoint, not this adapter.
