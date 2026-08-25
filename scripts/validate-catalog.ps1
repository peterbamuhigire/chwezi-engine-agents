[CmdletBinding()]
param([string]$CatalogPath = (Join-Path $PSScriptRoot '..\catalog\engines.yaml'))

$ErrorActionPreference = 'Stop'
$expected = @('srs-skills','business-plan-skills','website-skills','social-media-skills','linux-skills','proposal-skills','skills-web-dev','chwezi-accounting-doctrine','design-system-skills','digital-research-skills')
$items = @()
$current = $null
foreach ($line in Get-Content -LiteralPath $CatalogPath) {
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

$errors = @()
if ($items.Count -ne $expected.Count) { $errors += "Expected $($expected.Count) engines, found $($items.Count)." }
$ids = @($items | ForEach-Object { $_.id })
if (@($ids | Sort-Object -Unique).Count -ne $ids.Count) { $errors += 'Duplicate engine IDs found.' }
foreach ($id in $expected) { if ($ids -notcontains $id) { $errors += "Missing engine ID: $id" } }
foreach ($item in $items) {
    foreach ($field in @('repository','path','router','validators')) {
        if ([string]::IsNullOrWhiteSpace($item.$field)) { $errors += "$($item.id) has an empty $field field." }
    }
}
if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}
Write-Output "Catalog valid: $($items.Count) unique engines."
