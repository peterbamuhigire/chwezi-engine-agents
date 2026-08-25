[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$validator = Join-Path $PSScriptRoot '..\scripts\validate-catalog.ps1'
& $validator -CatalogPath (Join-Path $PSScriptRoot '..\catalog\engines.yaml')
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
Write-Output 'Catalog test passed.'
