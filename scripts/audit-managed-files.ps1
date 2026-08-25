[CmdletBinding()]
param([Parameter(Mandatory)][string]$Destination)

$ErrorActionPreference = 'Stop'
$destination = [IO.Path]::GetFullPath($Destination)
$manifestPath = Join-Path $destination '.skills-engine-agents-install.json'
if (-not (Test-Path -LiteralPath $manifestPath)) { Write-Error "Manifest missing: $manifestPath"; exit 2 }
$manifest = Get-Content -Raw $manifestPath | ConvertFrom-Json
$errors = @()
foreach ($relative in @($manifest.installed_files)) {
    $target = [IO.Path]::GetFullPath((Join-Path $destination $relative))
    if (-not $target.StartsWith($destination.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) { $errors += "Path escapes destination: $relative"; continue }
    if ($relative -ne '.skills-engine-agents-install.json' -and -not (Test-Path -LiteralPath $target)) { $errors += "Managed file missing: $relative" }
}
$result = [ordered]@{ destination = $destination; checked = @($manifest.installed_files).Count; status = if ($errors.Count -eq 0) { 'PASS' } else { 'FAIL' }; errors = $errors }
$result | ConvertTo-Json -Depth 4
if ($errors.Count -gt 0) { exit 1 }
