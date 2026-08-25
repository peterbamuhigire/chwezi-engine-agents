[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$hosts = @('codex','claude-code','gemini-cli','opencode','generic','mcp')
$results = @()
foreach ($hostId in $hosts) {
    $target = Join-Path ([IO.Path]::GetTempPath()) "skills-engine-host-smoke-$hostId-$([Guid]::NewGuid().ToString('N'))"
    try {
        & (Join-Path $root 'scripts\install.ps1') -Host $hostId -Destination $target
        $status = if ($LASTEXITCODE -eq 0 -and (Test-Path -LiteralPath (Join-Path $target '.skills-engine-agents-install.json'))) { 'PASS' } else { 'FAIL' }
        $results += [ordered]@{ host = $hostId; status = $status; evidence = 'Managed manifest and host target created.' }
    } catch {
        $results += [ordered]@{ host = $hostId; status = 'FAIL'; evidence = $_.Exception.Message }
    } finally {
        if (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Recurse -Force }
    }
}
$results | ConvertTo-Json -Depth 4
if (@($results | Where-Object status -ne 'PASS').Count -gt 0) { exit 1 }
