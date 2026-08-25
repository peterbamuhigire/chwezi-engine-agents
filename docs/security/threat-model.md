# Threat model

The package crosses a model-controlled instruction boundary into local files,
Git repositories, validators, and optional host transports. The security goal
is to make read-only inspection useful while keeping mutations explicit and
bounded.

| Threat | Boundary | Control | Evidence |
| --- | --- | --- | --- |
| Prompt injection in a router or fork | Engine files to agent | Routers are read as data; validators come from catalog or manifest only. | `tests/security/test_command_allowlist.ps1` |
| Malicious catalog entry | Catalog to validator | JSON Schema, relative paths, and declared-command dispatch. | `scripts/validate-contracts.py` |
| Path traversal or junction escape | Host path to filesystem | Real-path containment and manifest path checks. | `tests/security/test_path_boundaries.ps1`, MCP safety tests |
| Dirty or diverged pull | Git checkout to remote | Clean-tree check, upstream counts, main-branch rule, `--ff-only`. | `tests/security/test_mutation_gates.ps1` |
| Model-supplied shell command | Tool input to process | Typed tool inputs exclude commands; allowlist compares exact catalog strings. | `tests/security/test_command_allowlist.ps1` |
| Dependency or release compromise | Package build to consumer | Lockfile, CI checks, checksums, provenance manifest, no secrets in archive. | `docs/security/supply-chain-policy.md` |
| Credential leakage | Host environment to package | Credentials stay in host stores or environment variables; reports redact values. | release workflow and review |

Residual risk remains for a compromised host, a malicious declared validator,
or a user who approves an unsafe operation. The package records that approval;
it cannot decide whether the human's business intent is sound.
