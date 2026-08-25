[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$target = Join-Path ([IO.Path]::GetTempPath()) "skills-engine-agents-install-$([Guid]::NewGuid().ToString('N'))"
try {
    & (Join-Path $root 'scripts\install.ps1') -Host generic -Destination $target
    $manifestPath = Join-Path $target '.skills-engine-agents-install.json'
    if (-not (Test-Path -LiteralPath $manifestPath)) { throw 'Install manifest missing.' }
    New-Item -ItemType File -Path (Join-Path $target 'user-notes.txt') | Out-Null
    & (Join-Path $root 'scripts\update.ps1') -Destination $target
    if (-not (Test-Path -LiteralPath (Join-Path $target 'user-notes.txt'))) { throw 'Update removed a user-created file.' }
    & (Join-Path $root 'scripts\uninstall.ps1') -Destination $target -Force
    if (Test-Path -LiteralPath (Join-Path $target 'core\instructions\engine-orchestrator.md')) { throw 'Uninstall left a managed core file.' }
    if (-not (Test-Path -LiteralPath (Join-Path $target 'user-notes.txt'))) { throw 'Uninstall removed a user-created file.' }
    Write-Output 'Install target tests passed.'
} finally {
    if (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Recurse -Force }
}
