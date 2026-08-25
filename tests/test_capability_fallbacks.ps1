[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path $PSScriptRoot -Parent
$validator = Join-Path $root 'scripts\validate-contracts.py'
$schema = Join-Path $root 'schemas\capability-profile.schema.json'
foreach ($fixture in Get-ChildItem (Join-Path $root 'tests\fixtures\capability-profiles') -Filter '*.yaml') {
    & python -X utf8 $validator --schema $schema --instance $fixture.FullName
    if ($LASTEXITCODE -ne 0) { throw "Capability fixture failed: $($fixture.Name)" }
}
$modes = Get-Content -Raw (Join-Path $root 'core\capabilities\degraded-modes.md')
foreach ($term in @('NOT ASSESSED','Missing approval blocks','sequential','portable scripts','Markdown')) {
    if ($modes -notmatch [regex]::Escape($term)) { throw "Fallback rule missing: $term" }
}
$profile = (& python -X utf8 (Join-Path $root 'scripts\detect-capabilities.py') --format json --host generic --path $root | ConvertFrom-Json)
if ($profile.capabilities.user_approval -ne $false) { throw 'Detector granted approval without host evidence.' }
if ($profile.capabilities.git -ne $true) { throw 'Expected Git to be detected in this checkout.' }
Write-Output 'Capability fallback tests passed.'
