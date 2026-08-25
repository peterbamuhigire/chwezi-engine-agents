# Codex adapter

The Codex adapter preserves the three existing entrypoints and points each
wrapper to one canonical instruction under `core/instructions/`.

## Install and confirm

From a cloned release:

```powershell
.\scripts\install.ps1 -Host codex -Destination "$env:USERPROFILE\plugins\skills-engine-agents"
python C:\Users\Peter\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .
```

Run `scripts/discover-engine.ps1` for read-only discovery. Use the validator
agent only with documented engine commands. Ask the user before pulling,
overwriting, updating, uninstalling, or publishing anything.

The model/provider is selected by Codex and is not configured by this adapter.
Uncatalogued forks can be inspected, but no validator is invented for them.
