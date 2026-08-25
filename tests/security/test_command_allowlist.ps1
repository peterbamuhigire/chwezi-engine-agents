[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$source = Get-Content -Raw (Join-Path $root 'mcp-server\src\index.ts')
$safety = Get-Content -Raw (Join-Path $root 'mcp-server\src\safety.ts')
if ($source -match 'arguments\.command' -or $source -match 'shell\s*:\s*true') { throw 'MCP tool accepts arbitrary command text.' }
if ($safety -notmatch 'assertDeclaredValidator' -or $safety -notmatch 'validator_not_allowlisted') { throw 'Validator allowlist is missing.' }
if ($safety -match 'exec\s*\(') { throw 'Unsafe arbitrary exec call found in safety module.' }
Write-Output 'Command allowlist tests passed.'
