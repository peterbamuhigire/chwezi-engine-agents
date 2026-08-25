# MCP server

This optional stdio server exposes four typed operations:

- `discover_engine(path)`
- `inspect_engine(path)`
- `validate_engine(path, scope)`
- `pull_engine_ff_only(path, confirmation_token)`

No tool accepts a command or executable string from the model. Validation is
limited to commands declared by `catalog/engines.yaml`; pull is restricted to a
clean `main` branch, a readable upstream, `git pull --ff-only`, and a host token
held in `SKILLS_ENGINE_CONFIRMATION_TOKEN`.

## Build and test

```powershell
npm ci
npm test
npm run build
```

Set `SKILLS_ENGINE_CATALOG` when running from outside the repository. The
server uses its working directory as the approved root by default.
