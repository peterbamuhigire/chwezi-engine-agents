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
    $sourceItem = Get-Item -LiteralPath $from -Force
    if ($sourceItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Refusing linked install source: $RelativePath" }
    foreach ($item in (Get-ChildItem -LiteralPath $from -Recurse -Force -ErrorAction SilentlyContinue)) {
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Refusing linked install source: $RelativePath/$($item.FullName)" }
    }
    $to = Join-Path $Stage $RelativePath
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $to) | Out-Null
    Copy-Item -LiteralPath $from -Destination $to -Recurse -Force
}

function Get-RelativeFiles {
    param([string]$Root)
    if (-not (Test-Path -LiteralPath $Root)) { return @() }
    $prefix = $Root.TrimEnd('\', '/')
    return @(Get-ChildItem -LiteralPath $Root -Recurse -File -Force | ForEach-Object {
        $_.FullName.Substring($prefix.Length).TrimStart('\', '/').Replace('\', '/')
    })
}

function Get-SourceRelativeFiles {
    param([string[]]$Paths)
    $result = @()
    foreach ($relative in $Paths) {
        $item = Join-Path $source $relative
        $entries = if ((Get-Item -LiteralPath $item -Force).PSIsContainer) {
            Get-ChildItem -LiteralPath $item -Recurse -File -Force
        } else { @(Get-Item -LiteralPath $item -Force) }
        foreach ($entry in $entries) {
            $result += $entry.FullName.Substring($source.TrimEnd('\','/').Length).TrimStart('\','/').Replace('\','/')
        }
    }
    return @($result | Sort-Object -Unique)
}

function Test-SafeRelativePath {
    param([string]$RelativePath)
    if ([string]::IsNullOrWhiteSpace($RelativePath) -or [IO.Path]::IsPathRooted($RelativePath)) { return $false }
    $normalised = $RelativePath.Replace('\', '/')
    return ($normalised -notmatch '(^|/)\.\.?(/|$)' -and $normalised -notmatch '^[A-Za-z]:')
}

$paths = @('.codex-plugin','agents','catalog','core','schemas','scripts','skills',"adapters\$HostId",'README.md','CONTRIBUTING.md','docs\distribution.md')
if ($HostId -eq 'mcp') { $paths += @('mcp-server\package.json','mcp-server\package-lock.json','mcp-server\tsconfig.json','mcp-server\README.md','mcp-server\.mcp.json.example','mcp-server\src') }

if (Test-Path -LiteralPath $destination) {
    $destinationItem = Get-Item -LiteralPath $destination -Force
    if (-not $destinationItem.PSIsContainer) { throw "Destination is not a directory: $destination" }
    if ($destinationItem.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Refusing linked install destination: $destination" }
    foreach ($item in (Get-ChildItem -LiteralPath $destination -Recurse -Force -ErrorAction SilentlyContinue)) {
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "Refusing linked path in destination: $($item.FullName)" }
    }
    $existingManifest = Join-Path $destination '.skills-engine-agents-install.json'
    $existingFiles = @(Get-ChildItem -LiteralPath $destination -Force)
    if ($existingFiles.Count -gt 0 -and -not (Test-Path -LiteralPath $existingManifest) -and -not $Force) { throw "Destination is non-empty and unmanaged. Use -Force only after reviewing it: $destination" }
    $oldManaged = @()
    $oldHashes = @{}
    if (Test-Path -LiteralPath $existingManifest) {
        try { $oldManifest = Get-Content -Raw -LiteralPath $existingManifest | ConvertFrom-Json -ErrorAction Stop }
        catch { throw "Refusing unreadable install ownership manifest: $existingManifest" }
        $oldManaged = @($oldManifest.installed_files | Where-Object { $_ -ne '.skills-engine-agents-install.json' })
        foreach ($file in $oldManaged) {
            if (-not (Test-SafeRelativePath -RelativePath ([string]$file))) { throw "Refusing unsafe path in install manifest: $file" }
        }
        if ($oldManifest.installed_hashes) {
            foreach ($property in $oldManifest.installed_hashes.PSObject.Properties) { $oldHashes[$property.Name] = [string]$property.Value }
        }
        foreach ($file in $oldManaged) {
            if (-not (Test-Path -LiteralPath (Join-Path $destination $file) -PathType Leaf)) { continue }
            if (-not $oldHashes.ContainsKey([string]$file)) {
                if (-not $Force) { throw "Cannot verify ownership hash for managed file '$file'; use -Force only after reviewing the destination." }
                continue
            }
            $actualHash = (Get-FileHash -LiteralPath (Join-Path $destination $file) -Algorithm SHA256).Hash.ToLowerInvariant()
            if ($actualHash -ne $oldHashes[[string]$file].ToLowerInvariant() -and -not $Force) {
                throw "Refusing to overwrite locally modified managed file '$file'. Review the edit or use -Force deliberately."
            }
        }
    }
    foreach ($file in (Get-SourceRelativeFiles -Paths $paths)) {
        $targetFile = Join-Path $destination $file
        $relativeParts = $file.Split('/')
        $parentPath = $destination
        for ($partIndex = 0; $partIndex -lt ($relativeParts.Length - 1); $partIndex++) {
            $parentPath = Join-Path $parentPath $relativeParts[$partIndex]
            if ((Test-Path -LiteralPath $parentPath) -and -not (Test-Path -LiteralPath $parentPath -PathType Container)) {
                throw "Refusing file/directory collision at '$parentPath'. Move the existing file before installing."
            }
        }
        if ((Test-Path -LiteralPath $targetFile -PathType Container)) {
            throw "Refusing file/directory collision at '$targetFile'. Move the existing directory before installing."
        }
        if ((Test-Path -LiteralPath $targetFile -PathType Leaf) -and $oldManaged -notcontains $file -and -not $Force) {
            throw "Refusing to overwrite unowned destination file '$file'. Review the collision or use -Force deliberately."
        }
    }
}

$stage = "$destination.staging-$([Guid]::NewGuid().ToString('N'))"
if ($WhatIfPreference) { Write-Output "What if: install host adapter $HostId to $destination"; return }
New-Item -ItemType Directory -Force -Path $stage | Out-Null
try {
    foreach ($path in $paths) { Copy-ManagedPath -RelativePath $path -Stage $stage }
    $managedFiles = @(Get-RelativeFiles -Root $stage)
    if (Test-Path -LiteralPath $destination) {
        foreach ($file in (Get-RelativeFiles -Root $destination)) {
            if ($file -eq '.skills-engine-agents-install.json' -or $oldManaged -contains $file) { continue }
            $sourceFile = Join-Path $destination $file
            $targetFile = Join-Path $stage $file
            if (-not (Test-Path -LiteralPath $targetFile)) {
                New-Item -ItemType Directory -Force -Path (Split-Path -Parent $targetFile) | Out-Null
                Copy-Item -LiteralPath $sourceFile -Destination $targetFile -Force
            }
        }
    }
    $adapterText = Get-Content -Raw (Join-Path $adapter 'adapter.yaml')
    $adapterVersion = if ($adapterText -match '(?m)^version:\s*(\S+)') { $matches[1] } else { 'unknown' }
    $installedHashes = [ordered]@{}
    foreach ($file in $managedFiles) { $installedHashes[$file] = (Get-FileHash -LiteralPath (Join-Path $stage $file) -Algorithm SHA256).Hash.ToLowerInvariant() }
    $manifest = [ordered]@{ source_repository = Get-SourceValue -Arguments @('remote','get-url','origin'); source_commit = Get-SourceValue -Arguments @('rev-parse','HEAD'); adapter_id = $HostId; adapter_version = $adapterVersion; core_version = '1.0.0'; destination = $destination; installed_files = @($managedFiles + '.skills-engine-agents-install.json' | Sort-Object -Unique); installed_hashes = $installedHashes; installed_at = [DateTimeOffset]::UtcNow.ToString('o'); installer_version = '1.0.0' }
    $manifest | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath (Join-Path $stage '.skills-engine-agents-install.json') -Encoding utf8
    if (-not (Test-Path -LiteralPath (Join-Path $stage "adapters\$HostId\adapter.yaml"))) { throw 'Staged adapter manifest is missing.' }
    if (-not (Test-Path -LiteralPath (Join-Path $stage 'core\instructions\engine-orchestrator.md'))) { throw 'Staged canonical core is missing.' }
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
