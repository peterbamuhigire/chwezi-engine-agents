$ErrorActionPreference = 'Stop'
$sandbox = Join-Path $env:TEMP ("skills-engine-agents-preservation-" + [Guid]::NewGuid().ToString('N'))
$source = Join-Path $sandbox 'source'
$target = Join-Path $sandbox 'target'
$installer = Join-Path $source 'scripts\install.ps1'

function Write-FixtureFile([string]$RelativePath, [string]$Content) {
    $path = Join-Path $source $RelativePath
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $path) | Out-Null
    Set-Content -LiteralPath $path -Value $Content -NoNewline
}

function Assert-Equal([string]$Actual, [string]$Expected, [string]$Message) {
    if ($Actual -cne $Expected) { throw "$Message (actual='$Actual')" }
}

try {
    foreach ($directory in @('.codex-plugin','agents','catalog','core','schemas','scripts','skills','adapters\codex','docs')) {
        New-Item -ItemType Directory -Force -Path (Join-Path $source $directory) | Out-Null
    }
    Write-FixtureFile '.codex-plugin\plugin.json' '{"name":"fixture"}'
    Write-FixtureFile 'adapters\codex\adapter.yaml' "id: codex`nversion: 1.0.0`n"
    Write-FixtureFile 'core\instructions\engine-orchestrator.md' 'fixture router'
    Write-FixtureFile 'docs\distribution.md' 'fixture distribution'
    Write-FixtureFile 'README.md' 'source version 1'
    Write-FixtureFile 'CONTRIBUTING.md' 'fixture contribution guide'
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot '..\..\scripts\install.ps1') -Destination $installer
    & git -C $source init | Out-Null
    if ($LASTEXITCODE -ne 0) { throw 'could not initialize isolated installer source fixture' }
    & git -C $source remote add origin 'https://example.invalid/fixture.git'
    if ($LASTEXITCODE -ne 0) { throw 'could not configure isolated fixture remote' }
    & git -C $source -c user.name='Fixture' -c user.email='fixture@example.invalid' add .
    & git -C $source -c user.name='Fixture' -c user.email='fixture@example.invalid' commit -m 'fixture source'
    if ($LASTEXITCODE -ne 0) { throw 'could not commit isolated installer source fixture' }

    New-Item -ItemType Directory -Force -Path $target | Out-Null
    Set-Content -LiteralPath (Join-Path $target 'user-notes.txt') -Value 'keep user notes' -NoNewline
    Set-Content -LiteralPath (Join-Path $target '.env') -Value 'keep hidden file' -NoNewline
    $refused = $false
    try { & $installer -Destination $target }
    catch { if ($_.Exception.Message -match 'non-empty and unmanaged') { $refused = $true } else { throw } }
    if (-not $refused) { throw 'unmanaged non-empty install target was accepted without -Force' }
    Assert-Equal (Get-Content -Raw (Join-Path $target 'user-notes.txt')) 'keep user notes' 'unmanaged refusal changed user notes'

    & $installer -Destination $target -Force
    Assert-Equal (Get-Content -Raw (Join-Path $target 'user-notes.txt')) 'keep user notes' 'forced install lost user notes'
    Assert-Equal (Get-Content -Raw (Join-Path $target '.env')) 'keep hidden file' 'forced install lost hidden user file'
    $manifestPath = Join-Path $target '.skills-engine-agents-install.json'
    $manifest = Get-Content -Raw $manifestPath | ConvertFrom-Json
    if (-not $manifest.installed_hashes.'README.md') { throw 'manifest did not record managed file hashes' }

    Remove-Item -LiteralPath (Join-Path $target 'README.md') -Force
    New-Item -ItemType Directory -Path (Join-Path $target 'README.md') | Out-Null
    $refused = $false
    try { & $installer -Destination $target }
    catch { if ($_.Exception.Message -match 'file/directory collision') { $refused = $true } else { throw } }
    if (-not $refused) { throw 'installer did not refuse a managed file/directory collision' }
    Remove-Item -LiteralPath (Join-Path $target 'README.md') -Recurse -Force
    & $installer -Destination $target -Force

    $newFile = Join-Path $target 'agents\new-source-file.md'
    Set-Content -LiteralPath $newFile -Value 'user-owned collision' -NoNewline
    Write-FixtureFile 'agents\new-source-file.md' 'new package file'
    $refused = $false
    try { & $installer -Destination $target }
    catch { if ($_.Exception.Message -match 'unowned destination file') { $refused = $true } else { throw } }
    if (-not $refused) { throw 'update overwrote an unowned file at a newly managed path' }
    Assert-Equal (Get-Content -Raw $newFile) 'user-owned collision' 'refused collision update changed the user file'

    Set-Content -LiteralPath (Join-Path $target 'README.md') -Value 'user local edit' -NoNewline
    Write-FixtureFile 'README.md' 'source version 2'
    $refused = $false
    try { & $installer -Destination $target }
    catch { if ($_.Exception.Message -match 'locally modified managed file') { $refused = $true } else { throw } }
    if (-not $refused) { throw 'update overwrote a locally edited managed file' }
    Assert-Equal (Get-Content -Raw (Join-Path $target 'README.md')) 'user local edit' 'refused update changed the local edit'

    & $installer -Destination $target -Force
    Assert-Equal (Get-Content -Raw (Join-Path $target 'README.md')) 'source version 2' 'explicit forced update did not apply the new source'
    Assert-Equal (Get-Content -Raw $newFile) 'new package file' 'explicit forced update did not apply the colliding source path'
    Assert-Equal (Get-Content -Raw (Join-Path $target 'user-notes.txt')) 'keep user notes' 'update lost user notes'
    Assert-Equal (Get-Content -Raw (Join-Path $target '.env')) 'keep hidden file' 'update lost hidden user file'
    Write-Output 'PowerShell installer ownership: PASS (unmanaged refusal, hidden/unmanaged preservation, hash-backed modified-file refusal and explicit force update)'
} finally {
    $resolvedTemp = [IO.Path]::GetFullPath($env:TEMP).TrimEnd('\') + '\'
    $resolvedSandbox = [IO.Path]::GetFullPath($sandbox)
    if (-not $resolvedSandbox.StartsWith($resolvedTemp, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing cleanup outside TEMP: $resolvedSandbox"
    }
    if (Test-Path -LiteralPath $resolvedSandbox) { Remove-Item -LiteralPath $resolvedSandbox -Recurse -Force }
}
