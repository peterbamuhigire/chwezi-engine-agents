[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$target = Join-Path ([IO.Path]::GetTempPath()) "skills-engine-agents-fork-$([Guid]::NewGuid().ToString('N'))"
try {
    New-Item -ItemType Directory -Force -Path $target | Out-Null
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'fixtures\forked-engine\AGENTS.md') -Destination (Join-Path $target 'AGENTS.md')
    & git -C $target init -q
    & git -C $target remote add origin https://github.com/example/forked-engine.git
    & (Join-Path $root 'scripts\discover-engine.ps1') -Path $target | Out-File (Join-Path $target 'discovery.json')
    $exitCode = $LASTEXITCODE
    $result = Get-Content -Raw (Join-Path $target 'discovery.json') | ConvertFrom-Json
    if ($exitCode -ne 3) { throw "Expected uncatalogued exit code 3, got $exitCode" }
    if ($result.matched -ne $false -or $result.routerExists -ne $true) { throw 'Fork discovery did not preserve local router evidence.' }
    Write-Output 'Fork discovery tests passed.'
} finally {
    if (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Recurse -Force }
}
