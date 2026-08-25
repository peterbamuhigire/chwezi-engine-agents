[CmdletBinding()]
param(
    [Alias('Host')]
    [ValidateSet('codex','claude-code','gemini-cli','opencode','generic','mcp')]
    [string]$HostId = 'codex',
    [string]$Destination = (Join-Path $env:USERPROFILE 'plugins\skills-engine-agents'),
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$source = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
if (-not (Test-Path -LiteralPath (Join-Path $source '.codex-plugin\plugin.json'))) {
    throw "Plugin manifest not found under $source"
}
$adapter = Join-Path $source "adapters\$HostId"
if (-not (Test-Path -LiteralPath $adapter)) {
    throw "Requested host adapter is not available: $HostId"
}
$destinationParent = Split-Path $Destination -Parent
New-Item -ItemType Directory -Force -Path $destinationParent | Out-Null
if ((Test-Path -LiteralPath $Destination) -and -not $Force) {
    throw "Destination exists. Use -Force only when intentionally replacing it: $Destination"
}
if (Test-Path -LiteralPath $Destination) { Remove-Item -LiteralPath $Destination -Recurse -Force }
Copy-Item -LiteralPath $source -Destination $Destination -Recurse -Force
Write-Output "Installed skills-engine-agents host=$HostId to $Destination"
