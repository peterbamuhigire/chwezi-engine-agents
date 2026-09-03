[CmdletBinding()]
param(
    [string]$WorkspaceRoot = 'C:\wamp64\www',
    [string]$CoordinatorRoot = 'C:\wamp64\www\chwezi-engine-agents'
)

$ErrorActionPreference = 'Stop'
$standard = Join-Path $CoordinatorRoot 'docs\operations\portfolio-craft-standard-2026-09-04.md'
$engines = @(
    'srs-skills', 'business-plan-skills', 'website-skills', 'social-media-skills',
    'linux-skills', 'proposal-skills', 'skills-web-dev',
    'chwezi-accounting-doctrine', 'design-system-skills', 'digital-research-engine',
    'windows-admin-engine-skills'
)

if (-not (Test-Path -LiteralPath $standard)) {
    throw "Portfolio craft standard is missing: $standard"
}

$failures = @()
foreach ($engine in $engines) {
    $root = Join-Path $WorkspaceRoot $engine
    if (-not (Test-Path -LiteralPath $root)) {
        $failures += "${engine}: engine checkout not found"
        continue
    }

    $router = Join-Path $root 'AGENTS.md'
    if (-not (Test-Path -LiteralPath $router)) {
        $failures += "${engine}: AGENTS.md not found"
        continue
    }

    $text = Get-Content -LiteralPath $router -Raw
    foreach ($marker in @('PORTFOLIO CRAFT CONTRACT', 'Observe -> Baseline -> Select -> Experiment -> Check -> Standardise -> Teach -> Re-measure', 'NOT ASSESSED')) {
        if ($text -notmatch [regex]::Escape($marker)) {
            $failures += "${engine}: missing marker '$marker'"
        }
    }

    $readme = Join-Path $root 'README.md'
    if (-not (Test-Path -LiteralPath $readme)) {
        $failures += "${engine}: README.md not found"
    } else {
        $firstH2 = Get-Content -LiteralPath $readme | Where-Object { $_ -match '^## ' } | Select-Object -First 1
        if ($firstH2 -ne '## Capability map') {
            $failures += "${engine}: first README H2 must be '## Capability map' (found '$firstH2')"
        }
    }
}

if ($failures.Count -gt 0) {
    $failures | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Output "PASS: portfolio craft contract is propagated to $($engines.Count) engines."
