[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$target = Join-Path ([IO.Path]::GetTempPath()) "skills-engine-security-mutation-$([Guid]::NewGuid().ToString('N'))"
try {
    & (Join-Path $root 'scripts\install.ps1') -Host generic -Destination $target -WhatIf | Out-Null
    if (Test-Path -LiteralPath $target) { throw 'WhatIf install created a destination.' }
    $mcpSafety = Get-Content -Raw (Join-Path $root 'mcp-server\src\safety.ts')
    if ($mcpSafety -notmatch 'requireConfirmationToken' -or $mcpSafety -notmatch 'timingSafeEqual') { throw 'MCP approval gate is missing.' }
    $maintainer = Get-Content -Raw (Join-Path $root 'core\instructions\engine-maintainer.md')
    foreach ($term in @('git pull --ff-only','dirty','diverged','approval')) { if ($maintainer -notmatch $term) { throw "Mutation rule missing: $term" } }
    Write-Output 'Mutation gate tests passed.'
} finally {
    if (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Recurse -Force }
}
