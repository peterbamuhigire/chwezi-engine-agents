[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$validator = Join-Path $root 'scripts\validate-contracts.py'
$schema = Join-Path $root 'schemas\adapter-manifest.schema.json'
foreach ($hostId in @('claude-code','gemini-cli','opencode')) {
    $dir = Join-Path $root "adapters\$hostId"
    $manifest = Join-Path $dir 'adapter.yaml'
    & python -X utf8 $validator --schema $schema --instance $manifest
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    if ((Get-ChildItem -LiteralPath $dir -Recurse -File).Count -lt 2) { throw "Adapter has no readable entrypoints: $hostId" }
}
$generic = Join-Path $root 'adapters\generic'
foreach ($name in @('engine-orchestrator.prompt.md','engine-maintainer.prompt.md','engine-validator.prompt.md')) {
    if (-not (Test-Path -LiteralPath (Join-Path $generic $name))) { throw "Missing generic fallback: $name" }
}
Write-Output 'Other host adapter smoke test passed.'
