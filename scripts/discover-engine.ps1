[CmdletBinding()]
param(
    [string]$Path = (Get-Location).Path,
    [string]$CatalogPath = (Join-Path $PSScriptRoot '..\catalog\engines.yaml')
)

$ErrorActionPreference = 'Stop'

function Read-EngineCatalog {
    param([Parameter(Mandatory)][string]$FilePath)

    $items = @()
    $current = $null
    foreach ($line in Get-Content -LiteralPath $FilePath) {
        if ($line -match '^\s*-\s+id:\s*(.+?)\s*$') {
            if ($null -ne $current) { $items += [pscustomobject]$current }
            $current = [ordered]@{ id = $matches[1].Trim(); repository = ''; path = ''; router = ''; validators = '' }
            continue
        }
        if ($null -ne $current -and $line -match '^\s+(repository|path|router|validators):\s*"?(.*?)"?\s*$') {
            $current[$matches[1]] = $matches[2].Trim()
        }
    }
    if ($null -ne $current) { $items += [pscustomobject]$current }
    return $items
}

$gitRoot = (& git -C $Path rev-parse --show-toplevel 2>$null)
if ($LASTEXITCODE -ne 0 -or [string]::IsNullOrWhiteSpace(($gitRoot -join ''))) {
    Write-Error "Path is not inside a Git repository: $Path"
    exit 2
}
$gitRoot = (Resolve-Path -LiteralPath ($gitRoot -join '')).Path
$remote = ((& git -C $gitRoot remote get-url origin 2>$null) -join '').Trim()
$repoName = [IO.Path]::GetFileNameWithoutExtension(($remote.TrimEnd('/') -split '/')[-1])
$folderName = Split-Path $gitRoot -Leaf
$catalog = @(Read-EngineCatalog -FilePath (Resolve-Path -LiteralPath $CatalogPath).Path)
$engine = $catalog | Where-Object { $_.repository -eq $repoName -or $_.path -eq $folderName } | Select-Object -First 1
$routerRelative = if ($engine) { $engine.router } elseif (Test-Path -LiteralPath (Join-Path $gitRoot 'AGENTS.md')) { 'AGENTS.md' } elseif (Test-Path -LiteralPath (Join-Path $gitRoot 'README.md')) { 'README.md' } else { $null }
$routerPath = if ($routerRelative) { Join-Path $gitRoot $routerRelative } else { '' }
$result = [ordered]@{
    matched = ($null -ne $engine)
    engineId = if ($engine) { $engine.id } else { $null }
    repository = $repoName
    folder = $folderName
    repoRoot = $gitRoot
    remote = $remote
    branch = ((& git -C $gitRoot branch --show-current 2>$null) -join '').Trim()
    router = $routerRelative
    routerExists = if ($routerRelative) { Test-Path -LiteralPath $routerPath } else { $false }
}
$result | ConvertTo-Json -Depth 4
if (-not $engine) { exit 3 }
