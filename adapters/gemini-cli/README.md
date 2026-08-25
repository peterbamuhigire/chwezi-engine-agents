# Gemini CLI adapter

Use the project instruction text as `GEMINI.md` and the command texts as the
source for host custom commands. For a verified Gemini CLI extension, place the
instruction file in the extension's documented context file and translate
each command into the host's TOML custom-command format.

```powershell
.\scripts\install.ps1 -Host gemini-cli -Destination .gemini\skills-engine-agents
```

Confirm loading with a read-only catalog and router inspection. Use the
portable scripts for validation. Approval is required for pulls, writes,
submissions, and external messages. Model selection remains Gemini CLI's
configuration boundary. Missing shell or Git is `NOT ASSESSED`; uncatalogued
forks receive inspection only.
