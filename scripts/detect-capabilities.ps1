[CmdletBinding()]
param(
    [ValidateSet('Json')][string]$Format = 'Json',
    [string]$HostName = 'generic',
    [string]$Path = (Get-Location).Path
)

$ErrorActionPreference = 'Stop'
$detector = Join-Path $PSScriptRoot 'detect-capabilities.py'
if (-not (Test-Path -LiteralPath $detector)) { throw "Capability detector not found: $detector" }
& python -X utf8 $detector --format $Format.ToLowerInvariant() --host $HostName --path $Path
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
