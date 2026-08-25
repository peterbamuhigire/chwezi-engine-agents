[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
param(
    [Parameter(Mandatory)][string]$Destination,
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
if (-not $Force) { throw 'Uninstall requires -Force because it removes managed files.' }
$destination = [IO.Path]::GetFullPath($Destination)
$manifestPath = Join-Path $destination '.skills-engine-agents-install.json'
if (-not (Test-Path -LiteralPath $manifestPath)) { throw "Managed install manifest not found: $manifestPath" }
$manifest = Get-Content -Raw $manifestPath | ConvertFrom-Json
if ($WhatIfPreference) { Write-Output "What if: remove managed files from $destination"; return }
foreach ($relative in @($manifest.installed_files)) {
    $target = [IO.Path]::GetFullPath((Join-Path $destination $relative))
    if (-not $target.StartsWith($destination.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase) -and $target -ne $destination) { throw "Manifest path escapes destination: $relative" }
    if (Test-Path -LiteralPath $target -PathType Leaf) { Remove-Item -LiteralPath $target -Force }
}
if (Test-Path -LiteralPath $manifestPath) { Remove-Item -LiteralPath $manifestPath -Force }
Write-Output "Removed managed files from $destination; user-created files were retained."
