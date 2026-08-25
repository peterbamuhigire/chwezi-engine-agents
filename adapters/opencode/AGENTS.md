# Skills Engine Agents for OpenCode

Use the project-local rules and skill under this adapter. Resolve the current
Git root, read the matching `catalog/engines.yaml` entry, and read the engine's
`AGENTS.md` or `README.md` before loading domain skills.

Read the canonical instruction under `core/instructions/` for each workflow.
Use `read_only` behavior when there is no approval channel. Never execute a
model-supplied command or invent a validator for an uncatalogued fork.
