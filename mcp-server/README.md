# MCP server

This optional stdio server exposes six typed operations:

- `discover_engine(path)`
- `inspect_engine(path)`
- `validate_engine(path, scope)`
- `pull_engine_ff_only(path, confirmation_token)`
- `engine_tour(path)`: read-only; returns the committed `docs/engine-tours/<id>.json` for the
  engine that contains `path`, with `stale: true` when the engine HEAD (read from `.git` as data)
  differs from the tour's `generated_from_commit`. It never runs a process and never writes.
- `query_skill_graph(operation, skill, target?)`: read-only `neighbours`, `path` or `explain`
  over the committed report-only `docs/skill-graph/skill-graph.json`; never a routing input.

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

Set `SKILLS_ENGINE_CATALOG` when running from outside the repository
(and `SKILLS_ENGINE_TOURS_DIR` or `SKILLS_ENGINE_SKILL_GRAPH` for the read-only tour and graph files). The
server uses its working directory as the approved root by default.
