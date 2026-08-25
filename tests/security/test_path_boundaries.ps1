[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$target = Join-Path ([IO.Path]::GetTempPath()) "skills-engine-security-path-$([Guid]::NewGuid().ToString('N'))"
$outside = Join-Path ([IO.Path]::GetTempPath()) "skills-engine-security-outside-$([Guid]::NewGuid().ToString('N'))"
try {
    New-Item -ItemType Directory -Force -Path $target,$outside | Out-Null
    @{ installed_files = @('../outside.txt'); adapter_id = 'generic' } | ConvertTo-Json | Set-Content (Join-Path $target '.skills-engine-agents-install.json')
    New-Item -ItemType File -Path (Join-Path $outside 'outside.txt') | Out-Null
    & (Join-Path $root 'scripts\audit-managed-files.ps1') -Destination $target | Out-Null
    if ($LASTEXITCODE -eq 0) { throw 'Path traversal was accepted by the managed-file audit.' }
    Write-Output 'Path boundary tests passed.'
} finally {
    foreach ($path in @($target,$outside)) { if (Test-Path -LiteralPath $path) { Remove-Item -LiteralPath $path -Recurse -Force } }
}
