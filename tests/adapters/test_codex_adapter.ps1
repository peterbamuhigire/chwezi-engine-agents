[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$manifest = Join-Path $root 'adapters\codex\adapter.yaml'
& python -X utf8 (Join-Path $root 'scripts\validate-contracts.py') --schema (Join-Path $root 'schemas\adapter-manifest.schema.json') --instance $manifest
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
foreach ($name in @('engine-orchestrator','engine-maintainer','engine-validator')) {
    $path = Join-Path $root "agents\$name.md"
    if (-not (Test-Path -LiteralPath $path)) { throw "Missing Codex entrypoint: $path" }
    $body = Get-Content -Raw $path
    foreach ($field in @('canonical_id:','contract_version:','required_capabilities:','output_contract:')) {
        if ($body -notmatch [regex]::Escape($field)) { throw "$name missing frontmatter field $field" }
    }
}
if ((Get-Content -Raw $manifest) -notmatch 'host: codex') { throw 'Codex host missing from manifest.' }
Write-Output 'Codex adapter smoke test passed.'
