[CmdletBinding(SupportsShouldProcess = $true, ConfirmImpact = 'High')]
param(
    [Alias('Host')]
    [ValidateSet('codex','claude-code','gemini-cli','opencode','generic','mcp')]
    [string]$HostId = 'codex',
    [string]$Destination = (Join-Path $env:USERPROFILE 'plugins\skills-engine-agents'),
    [switch]$Force
)

$ErrorActionPreference = 'Stop'
$source = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$destination = [IO.Path]::GetFullPath($Destination)
$adapter = Join-Path $source "adapters\$HostId"
if (-not (Test-Path -LiteralPath (Join-Path $source '.codex-plugin\plugin.json'))) { throw "Plugin manifest not found under $source" }
if (-not (Test-Path -LiteralPath (Join-Path $adapter 'adapter.yaml'))) { throw "Requested host adapter is not available: $HostId" }

function Get-SourceValue {
    param([string[]]$Arguments)
    $value = (& git -C $source @Arguments 2>$null) -join ''
    if ($LASTEXITCODE -ne 0) { return '' }
    return $value.Trim()
}

function Copy-ManagedPath {
    param([string]$RelativePath, [string]$Stage)
    $from = Join-Path $source $RelativePath
    if (-not (Test-Path -LiteralPath $from)) { throw "Required install path is missing: $RelativePath" }
    $to = Join-Path $Stage $RelativePath
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $to) | Out-Null
    Copy-Item -LiteralPath $from -Destination $to -Recurse -Force
}

function Get-RelativeFiles {
    param([string]$Root)
    if (-not (Test-Path -LiteralPath $Root)) { return @() }
    $prefix = $Root.TrimEnd('\', '/')
    return @(Get-ChildItem -LiteralPath $Root -Recurse -File | ForEach-Object {
        $_.FullName.Substring($prefix.Length).TrimStart('\', '/').Replace('\', '/')
    })
}

if (Test-Path -LiteralPath $destination) {
    if (-not (Get-Item -LiteralPath $destination).PSIsContainer) { throw "Destination is not a directory: $destination" }
    $existingManifest = Join-Path $destination '.skills-engine-agents-install.json'
    $existingFiles = @(Get-ChildItem -LiteralPath $destination -Force)
    if ($existingFiles.Count -gt 0 -and -not (Test-Path -LiteralPath $existingManifest) -and -not $Force) { throw "Destination is non-empty and unmanaged. Use -Force only after reviewing it: $destination" }
    if ($Force -and -not (Test-Path -LiteralPath $existingManifest)) {
        foreach ($protected in @('.git','AGENTS.md','CLAUDE.md','GEMINI.md')) {
            if (Test-Path -LiteralPath (Join-Path $destination $protected)) { throw "Refusing to overwrite protected file: $protected" }
        }
    }
}

$stage = "$destination.staging-$([Guid]::NewGuid().ToString('N'))"
New-Item -ItemType Directory -Force -Path $stage | Out-Null
try {
    $paths = @('.codex-plugin','agents','catalog','core','schemas','scripts','skills',"adapters\$HostId",'README.md','CONTRIBUTING.md','docs\distribution.md')
    if ($HostId -eq 'mcp') { $paths += @('mcp-server\package.json','mcp-server\package-lock.json','mcp-server\tsconfig.json','mcp-server\README.md','mcp-server\.mcp.json.example','mcp-server\src') }
    foreach ($path in $paths) { Copy-ManagedPath -RelativePath $path -Stage $stage }
    $managedFiles = @(Get-RelativeFiles -Root $stage)
    if (Test-Path -LiteralPath (Join-Path $destination '.skills-engine-agents-install.json')) {
        $oldManifest = Get-Content -Raw (Join-Path $destination '.skills-engine-agents-install.json') | ConvertFrom-Json
        $oldManaged = @($oldManifest.installed_files)
        foreach ($file in (Get-RelativeFiles -Root $destination)) {
            if ($file -eq '.skills-engine-agents-install.json' -or $oldManaged -contains $file) { continue }
            $sourceFile = Join-Path $destination $file
            $targetFile = Join-Path $stage $file
            if (-not (Test-Path -LiteralPath $targetFile)) {
                New-Item -ItemType Directory -Force -Path (Split-Path -Parent $targetFile) | Out-Null
                Copy-Item -LiteralPath $sourceFile -Destination $targetFile -Force
            }
        }
        $managedFiles = @($managedFiles + $oldManaged | Sort-Object -Unique)
    }
    $adapterText = Get-Content -Raw (Join-Path $adapter 'adapter.yaml')
    $adapterVersion = if ($adapterText -match '(?m)^version:\s*(\S+)') { $matches[1] } else { 'unknown' }
    $manifest = [ordered]@{ source_repository = Get-SourceValue -Arguments @('remote','get-url','origin'); source_commit = Get-SourceValue -Arguments @('rev-parse','HEAD'); adapter_id = $HostId; adapter_version = $adapterVersion; core_version = '1.0.0'; destination = $destination; installed_files = @($managedFiles + '.skills-engine-agents-install.json' | Sort-Object -Unique); installed_at = [DateTimeOffset]::UtcNow.ToString('o'); installer_version = '1.0.0' }
    $manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $stage '.skills-engine-agents-install.json') -Encoding utf8
    if (-not (Test-Path -LiteralPath (Join-Path $stage "adapters\$HostId\adapter.yaml"))) { throw 'Staged adapter manifest is missing.' }
    if (-not (Test-Path -LiteralPath (Join-Path $stage 'core\instructions\engine-orchestrator.md'))) { throw 'Staged canonical core is missing.' }
    if ($WhatIfPreference) { Write-Output "What if: install host adapter $HostId to $destination"; return }
    $backup = "$destination.backup-$([Guid]::NewGuid().ToString('N'))"
    if (Test-Path -LiteralPath $destination) { Move-Item -LiteralPath $destination -Destination $backup }
    try {
        Move-Item -LiteralPath $stage -Destination $destination
        if (Test-Path -LiteralPath $backup) { Remove-Item -LiteralPath $backup -Recurse -Force }
    } catch {
        if (Test-Path -LiteralPath $destination) { Remove-Item -LiteralPath $destination -Recurse -Force }
        if (Test-Path -LiteralPath $backup) { Move-Item -LiteralPath $backup -Destination $destination }
        throw
    }
    Write-Output "Installed skills-engine-agents host=$HostId to $destination"
} catch {
    if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
    throw
}
