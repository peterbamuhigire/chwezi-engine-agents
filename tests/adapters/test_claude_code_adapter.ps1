[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$manifest = Join-Path $root 'adapters\claude-code\adapter.yaml'
& python -X utf8 (Join-Path $root 'scripts\validate-contracts.py') --schema (Join-Path $root 'schemas\adapter-manifest.schema.json') --instance $manifest
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
foreach ($path in @('CLAUDE.md','agents\engine-orchestrator.md','agents\engine-maintainer.md','agents\engine-validator.md','skills\skills-engine-agents\SKILL.md')) {
    $full = Join-Path (Join-Path $root 'adapters\claude-code') $path
    if (-not (Test-Path -LiteralPath $full)) { throw "Missing Claude Code target: $full" }
    if ((Get-Content -Raw $full) -notmatch 'engine-orchestrator|engine-maintainer|engine-validator|NOT ASSESSED|skills-engine-agents') { throw "Target lacks canonical reference: $full" }
}
Write-Output 'Claude Code adapter smoke test passed.'
