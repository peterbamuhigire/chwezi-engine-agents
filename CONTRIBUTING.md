# Contributing

Keep this plugin portable and conservative.

Before submitting a change:

1. Read the affected engine's `AGENTS.md` or `README.md` router.
2. Keep repository paths relative or discoverable from Git metadata.
3. Do not add a validation command unless it is documented by the target engine.
4. Treat unavailable checks as `NOT ASSESSED`, never as passing.
5. Run the plugin validator, catalog validation, PowerShell parser checks, and `git diff --check`.
6. Inspect the complete diff and confirm no machine-specific secrets or paths were added.

Agent prompts should define scope, evidence requirements, safety boundaries, degraded behavior, and a predictable handoff format.
