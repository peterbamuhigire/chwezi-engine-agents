# OpenCode adapter

OpenCode discovers project `AGENTS.md` rules and project skills. Copy the
adapter into the project-local `.agents` or configured skill location, then
confirm with a read-only request that the catalog and router are loaded.

```powershell
.\scripts\install.ps1 -Host opencode -Destination .agents\skills-engine-agents
```

Use OpenCode permission prompts for pulls, writes, and external actions. The
provider/model remains host configuration. If the current host version does
not load the target path, use the generic prompt bundle and label the host
adapter `NOT ASSESSED`.
