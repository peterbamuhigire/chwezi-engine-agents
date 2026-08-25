[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$validator = Join-Path $PSScriptRoot '..\scripts\validate-catalog.ps1'
& $validator
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'Catalog test passed.'
