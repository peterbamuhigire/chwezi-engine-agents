---
name: engine-validator
description: Codex wrapper for the canonical engine-validator instruction.
canonical_id: engine-validator
contract_version: "1.0"
required_capabilities: [read_files, shell]
output_contract: core/contracts/validation-result.yaml
---

Load `core/instructions/engine-validator.md` and follow it as the source of
truth. Codex supplies the shell boundary; this wrapper does not duplicate
validator or verdict policy.
