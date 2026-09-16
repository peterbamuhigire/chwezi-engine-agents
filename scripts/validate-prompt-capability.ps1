[CmdletBinding()]
param(
    [string]$WorkspaceRoot = 'C:\wamp64\www',
    [string]$CoordinatorRoot = 'C:\wamp64\www\chwezi-engine-agents'
)

$ErrorActionPreference = 'Stop'
$contract = Join-Path $CoordinatorRoot 'docs\operations\domain-prompt-compilation-contract-2026-09-16.md'
if (-not (Test-Path -LiteralPath $contract)) {
    throw "Domain prompt compilation contract is missing: $contract"
}

$engines = @(
    @{ Id = 'srs-skills'; Router = 'AGENTS.md' },
    @{ Id = 'business-plan-skills'; Router = 'AGENTS.md' },
    @{ Id = 'website-skills'; Router = 'AGENTS.md' },
    @{ Id = 'social-media-skills'; Router = 'AGENTS.md' },
    @{ Id = 'linux-skills'; Router = 'AGENTS.md' },
    @{ Id = 'proposal-skills'; Router = 'AGENTS.md' },
    @{ Id = 'skills-web-dev'; Router = 'AGENTS.md' },
    @{ Id = 'chwezi-accounting-doctrine'; Router = 'README.md' },
    @{ Id = 'design-system-skills'; Router = 'AGENTS.md' },
    @{ Id = 'digital-research-engine'; Router = 'AGENTS.md' },
    @{ Id = 'windows-admin-engine-skills'; Router = 'AGENTS.md' }
)

$failures = @()
$contractHashes = @()
foreach ($engine in $engines) {
    $root = Join-Path $WorkspaceRoot $engine.Id
    $router = Join-Path $root $engine.Router
    if (-not (Test-Path -LiteralPath $router)) {
        $failures += "$($engine.Id): router not found ($($engine.Router))"
        continue
    }

    $localContract = Join-Path $root 'docs\ai-prompting\domain-prompt-compilation-contract.md'
    if (-not (Test-Path -LiteralPath $localContract)) {
        $failures += "$($engine.Id): local prompt contract not found"
    } else {
        $contractHashes += (Get-FileHash -Algorithm SHA256 -LiteralPath $localContract).Hash
    }

    $text = Get-Content -LiteralPath $router -Raw
    foreach ($marker in @(
        'DOMAIN PROMPT GENERATION CONTRACT',
        'docs/ai-prompting/domain-prompt-compilation-contract.md',
        'Ready-to-paste prompt',
        'Failure action'
    )) {
        if ($text -notmatch [regex]::Escape($marker)) {
            $failures += "$($engine.Id): missing marker '$marker'"
        }
    }
}

if (($contractHashes | Sort-Object -Unique).Count -gt 1) {
    $failures += 'engine-local prompt contracts are not byte-identical; resynchronise before release'
}

if ($failures.Count -gt 0) {
    $failures | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Output "PASS: domain prompt capability is routed in $($engines.Count) engines with identical local contracts."
