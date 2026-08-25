---
name: engine-maintainer
description: Codex wrapper for the canonical engine-maintainer instruction.
canonical_id: engine-maintainer
contract_version: "1.0"
required_capabilities: [read_files, git]
output_contract: core/contracts/maintenance-result.yaml
---

Load `core/instructions/engine-maintainer.md` and follow it as the source of
truth. Codex supplies the Git and approval boundary; this wrapper does not
duplicate maintenance policy.
