# Claude Code adapter

This adapter uses project-local `CLAUDE.md`, agent wrappers, and a routing
skill. Copy it into a project when you want the package to apply only there;
copy the same files to the host's user-level locations only after reviewing the
scope and permissions.

```powershell
.\scripts\install.ps1 -Host claude-code -Destination .claude\skills-engine-agents
```

Confirm loading by asking Claude Code to identify the current Git root and
return the selected catalog entry without editing files. Run validation through
the portable scripts. Pulls and writes require approval; no provider or model
configuration belongs in this adapter.

DeepSeek-compatible endpoints are a provider fixture only. Test host/tool
behavior and label model or endpoint quality separately. No-shell hosts return
`NOT ASSESSED` for validation and maintenance. Forks without a catalog entry
may be inspected but receive no invented validator.
