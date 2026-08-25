---
canonical_id: capability-negotiator
contract_version: "1.0"
required_capabilities: [read_files]
output_contract: schemas/capability-profile.schema.json
---

# Capability negotiator

Read a capability profile produced by the detection scripts and select the
narrowest mode in `core/capabilities/degraded-modes.md`.

Never infer a capability from the selected model name. Never treat write access
as approval. If detection failed, preserve `not_assessed` and explain which
operation cannot be evaluated.

Required decisions:

- route only with `read_files`;
- validate only with `read_files` and `shell`;
- inspect Git only with `read_files` and `git`;
- pull only with `read_files`, `git`, and `user_approval`;
- use sequential execution when `subagents` is absent;
- use portable scripts when `mcp` is absent;
- use Markdown field names when `structured_output` is absent.
