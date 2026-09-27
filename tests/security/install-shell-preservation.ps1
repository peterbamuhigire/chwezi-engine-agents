$ErrorActionPreference = 'Stop'
$sandbox = Join-Path $env:TEMP ("skills-engine-agents-shell-preservation-" + [Guid]::NewGuid().ToString('N'))
$source = Join-Path $sandbox 'source'
$target = Join-Path $sandbox 'target'
$bash = 'C:\Program Files\Git\bin\bash.exe'
$cygpath = 'C:\Program Files\Git\usr\bin\cygpath.exe'

function Write-FixtureFile([string]$RelativePath, [string]$Content) {
    $path = Join-Path $source $RelativePath
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $path) | Out-Null
    Set-Content -LiteralPath $path -Value $Content -NoNewline
}

function Invoke-FixtureInstaller([switch]$Force) {
    $args = @($installerPosix, '--host', 'codex', '--destination', $targetPosix)
    if ($Force) { $args += '--force' }
    $stdoutPath = Join-Path $sandbox 'installer.stdout'
    $stderrPath = Join-Path $sandbox 'installer.stderr'
    $process = Start-Process -FilePath $bash -ArgumentList ($args -join ' ') -Wait -PassThru -NoNewWindow -RedirectStandardOutput $stdoutPath -RedirectStandardError $stderrPath
    $output = @()
    if (Test-Path -LiteralPath $stdoutPath) { $output += Get-Content -LiteralPath $stdoutPath }
    if (Test-Path -LiteralPath $stderrPath) { $output += Get-Content -LiteralPath $stderrPath }
    return @{ ExitCode = $process.ExitCode; Output = ($output -join "`n") }
}

function Assert-Equal([string]$Actual, [string]$Expected, [string]$Message) {
    if ($Actual -cne $Expected) { throw "$Message (actual='$Actual')" }
}

try {
    if (-not (Test-Path -LiteralPath $bash) -or -not (Test-Path -LiteralPath $cygpath)) {
        throw 'Git Bash and cygpath are required to exercise the shell installer on this host.'
    }
    foreach ($directory in @('.codex-plugin','agents','catalog','core','schemas','scripts','skills','adapters\codex','docs')) {
        New-Item -ItemType Directory -Force -Path (Join-Path $source $directory) | Out-Null
    }
    Write-FixtureFile '.codex-plugin\plugin.json' '{"name":"fixture"}'
    Write-FixtureFile 'adapters\codex\adapter.yaml' "id: codex`nversion: 1.0.0`n"
    Write-FixtureFile 'core\instructions\engine-orchestrator.md' 'fixture router'
    Write-FixtureFile 'docs\distribution.md' 'fixture distribution'
    Write-FixtureFile 'README.md' 'source version 1'
    Write-FixtureFile 'CONTRIBUTING.md' 'fixture contribution guide'
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot '..\..\scripts\install.sh') -Destination (Join-Path $source 'scripts\install.sh')
    Copy-Item -LiteralPath (Join-Path $PSScriptRoot '..\..\scripts\resolve-install-target.py') -Destination (Join-Path $source 'scripts\resolve-install-target.py')

    $installerPosix = (& $cygpath -u (Join-Path $source 'scripts\install.sh')).Trim()
    $targetPosix = (& $cygpath -u $target).Trim()
    New-Item -ItemType Directory -Force -Path $target | Out-Null
    Set-Content -LiteralPath (Join-Path $target 'user-notes.txt') -Value 'keep user notes' -NoNewline
    Set-Content -LiteralPath (Join-Path $target '.env') -Value 'keep hidden file' -NoNewline
    $result = Invoke-FixtureInstaller
    if ($result.ExitCode -eq 0 -or $result.Output -notmatch 'non-empty and unmanaged') { throw "shell installer did not refuse an unmanaged non-empty destination: $($result.Output)" }

    $result = Invoke-FixtureInstaller -Force
    if ($result.ExitCode -ne 0) { throw "forced shell install failed: $($result.Output)" }
    Assert-Equal (Get-Content -Raw (Join-Path $target 'user-notes.txt')) 'keep user notes' 'forced shell install lost user notes'
    Assert-Equal (Get-Content -Raw (Join-Path $target '.env')) 'keep hidden file' 'forced shell install lost hidden user data'

    Remove-Item -LiteralPath (Join-Path $target 'README.md') -Force
    New-Item -ItemType Directory -Path (Join-Path $target 'README.md') | Out-Null
    $result = Invoke-FixtureInstaller -Force
    if ($result.ExitCode -eq 0 -or $result.Output -notmatch 'file/directory or special-file collision') { throw 'shell installer did not refuse a file/directory collision, even with --force' }
    Remove-Item -LiteralPath (Join-Path $target 'README.md') -Recurse -Force
    $result = Invoke-FixtureInstaller -Force
    if ($result.ExitCode -ne 0) { throw "forced shell reinstall after the collision fixture failed: $($result.Output)" }

    $newFile = Join-Path $target 'agents\new-source-file.md'
    Set-Content -LiteralPath $newFile -Value 'user-owned collision' -NoNewline
    Write-FixtureFile 'agents\new-source-file.md' 'new package file'
    $result = Invoke-FixtureInstaller
    if ($result.ExitCode -eq 0 -or $result.Output -notmatch 'unowned file') { throw 'shell update did not refuse an unowned path collision' }
    Assert-Equal (Get-Content -Raw $newFile) 'user-owned collision' 'refused shell update changed the user file'

    Set-Content -LiteralPath (Join-Path $target 'README.md') -Value 'user local edit' -NoNewline
    Write-FixtureFile 'README.md' 'source version 2'
    $result = Invoke-FixtureInstaller
    if ($result.ExitCode -eq 0 -or $result.Output -notmatch 'locally modified') { throw "shell update did not refuse a locally modified managed file: $($result.Output)" }
    Assert-Equal (Get-Content -Raw (Join-Path $target 'README.md')) 'user local edit' 'refused shell update changed the local edit'

    $result = Invoke-FixtureInstaller -Force
    if ($result.ExitCode -ne 0) { throw "forced shell update failed: $($result.Output)" }
    Assert-Equal (Get-Content -Raw (Join-Path $target 'README.md')) 'source version 2' 'forced shell update did not apply source version 2'
    Assert-Equal (Get-Content -Raw $newFile) 'new package file' 'forced shell update did not install the colliding source file'
    Assert-Equal (Get-Content -Raw (Join-Path $target '.env')) 'keep hidden file' 'shell update lost hidden user data'
    Write-Output 'POSIX shell installer ownership: PASS (unmanaged refusal, hidden/unmanaged preservation, file/directory and unowned collisions, modified-file refusal)'
} finally {
    $resolvedTemp = [IO.Path]::GetFullPath($env:TEMP).TrimEnd('\') + '\'
    $resolvedSandbox = [IO.Path]::GetFullPath($sandbox)
    if (-not $resolvedSandbox.StartsWith($resolvedTemp, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Refusing cleanup outside TEMP: $resolvedSandbox"
    }
    if (Test-Path -LiteralPath $resolvedSandbox) { Remove-Item -LiteralPath $resolvedSandbox -Recurse -Force }
}
