[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
param(
    [Parameter(Mandatory)][string]$Destination,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$manifestPath = Join-Path ([IO.Path]::GetFullPath($Destination)) '.skills-engine-agents-install.json'
if (-not (Test-Path -LiteralPath $manifestPath)) { throw "Managed install manifest not found: $manifestPath" }
$manifest = Get-Content -Raw $manifestPath | ConvertFrom-Json
$installer = Join-Path $PSScriptRoot 'install.ps1'
& $installer -Host $manifest.adapter_id -Destination $Destination -Force:$Force -WhatIf:$WhatIfPreference
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
