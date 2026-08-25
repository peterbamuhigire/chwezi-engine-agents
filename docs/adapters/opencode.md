# OpenCode adapter

## Prerequisites and operating systems

Use a cloned release on Windows PowerShell 5.1 or 7+; POSIX users should use the matching shell scripts. Python 3.11+ is required for contract validation. MCP additionally requires Node.js 20+ and npm.

## Install, update, and uninstall

Install:
.\scripts\install.ps1 -Host opencode -Destination .agents\skills-engine-agents
Update:
.\scripts\update.ps1 -Destination .agents\skills-engine-agents
Uninstall:
.\scripts\uninstall.ps1 -Destination .agents\skills-engine-agents -Force

The installer writes .skills-engine-agents-install.json and refuses an unmanaged non-empty destination unless -Force is explicit. Review downloaded scripts before execution.

## Confirm loading and read-only discovery

Ask the host to identify the current Git root, catalog entry, and local router without editing. Direct discovery command:
.\scripts\discover-engine.ps1

## Validation

python scripts\validate-contracts.py --schema schemas\engine-catalog.schema.json --instance catalog\engines.yaml

## Safe pull flow

Inspect status, branch, upstream counts, and router first. Request an explicit user approval for a pull. The maintainer permits only git pull --ff-only; dirty trees, divergence, missing upstreams, and non-main targets are skipped or blocked. OpenCode permission prompt.

## Model-provider boundary

OpenCode owns provider/model selection; its permission settings are the approval boundary. Model quality, context limits, tool access, and current provider availability are not certified by this package.

## Fork behaviour

A fork with a local AGENTS.md or README.md can be inspected. If it is not catalogued, the package does not invent validator commands or mutate it automatically.

## NOT ASSESSED cases and troubleshooting

Missing shell, Git, web access, structured output, dependencies, host discovery, provider keys, or approval authority returns NOT ASSESSED. Install the named dependency or switch to the generic prompt path. A failed check remains FAIL until its evidence is reviewed.

See the compatibility contract, host matrix, and incident runbook under docs/.
