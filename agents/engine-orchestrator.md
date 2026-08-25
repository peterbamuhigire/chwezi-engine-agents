---
name: engine-orchestrator
description: Codex wrapper for the canonical engine-orchestrator instruction.
canonical_id: engine-orchestrator
contract_version: "1.0"
required_capabilities: [read_files]
output_contract: core/contracts/handoff.yaml
---

Load `core/instructions/engine-orchestrator.md` and follow it as the source of
truth. Codex supplies the file-reading and tool boundary; this wrapper does not
duplicate routing policy.
