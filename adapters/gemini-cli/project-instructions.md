# Gemini CLI project instructions

Resolve the current Git root, read `catalog/engines.yaml`, and read the
selected engine's local router before loading any skill. Use the canonical
instructions under `core/instructions/`. Missing tools or approval remain
`NOT ASSESSED` or blocked.

The current Gemini CLI extension convention uses `GEMINI.md`, a
`gemini-extension.json` manifest, TOML custom commands, and optional skills.
The Markdown files in this adapter are portable command text; the generic
installer does not claim automatic `.md` command discovery.
