[CmdletBinding()]
param([string]$CatalogPath = '')

$ErrorActionPreference = 'Stop'
if ([string]::IsNullOrWhiteSpace($CatalogPath)) {
    $CatalogPath = Join-Path $PSScriptRoot '..\catalog\engines.yaml'
}
$catalogResolved = (Resolve-Path -LiteralPath $CatalogPath).Path
$contractValidator = Join-Path (Split-Path $PSScriptRoot -Parent) 'scripts\validate-contracts.py'
if (-not (Test-Path -LiteralPath $contractValidator)) {
    Write-Error "Contract validator not found: $contractValidator"
    exit 3
}
& python -X utf8 $contractValidator --schema (Join-Path (Split-Path $PSScriptRoot -Parent) 'schemas\engine-catalog.schema.json') --instance $catalogResolved
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
$expected = @('srs-skills','business-plan-skills','website-skills','social-media-skills','linux-skills','proposal-skills','chwezi-dev-engine','chwezi-accounting-doctrine','design-system-skills','digital-research-skills','windows-admin-engine-skills')
$items = @()
$current = $null
$inValidators = $false
foreach ($line in Get-Content -LiteralPath $CatalogPath) {
    if ($line -match '^\s*-\s+id:\s*(.+?)\s*$') {
        if ($null -ne $current) { $items += [pscustomobject]$current }
        $current = [ordered]@{ id = $matches[1].Trim(); repository = ''; path = ''; router = ''; validators = ''; validatorList = @() }
        $inValidators = $false
        continue
    }
    # Validators may be a YAML list (one command per item); each item runs and is judged separately.
    if ($null -ne $current -and $inValidators -and $line -match '^\s+-\s+"?(.*?)"?\s*$') {
        $current.validatorList += $matches[1].Trim()
        $current.validators = ($current.validatorList -join ' ; ')
        continue
    }
    $inValidators = $false
    if ($null -ne $current -and $line -match '^\s+(repository|path|router|validators):\s*"?(.*?)"?\s*$') {
        $current[$matches[1]] = $matches[2].Trim()
        if ($matches[1] -eq 'validators') {
            if ([string]::IsNullOrWhiteSpace($current.validators)) { $inValidators = $true } else { $current.validatorList = @($current.validators) }
        }
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
    # A pipe would feed one validator into the next and mask the first exit code (M10-01-T07).
    foreach ($command in @($item.validatorList)) {
        if ($command -match '\|') { $errors += "$($item.id) validator contains a pipe; declare each command as a separate list item: $command" }
    }
}
if ($errors.Count -gt 0) {
    $errors | ForEach-Object { Write-Error $_ }
    exit 1
}
Write-Output "Catalog valid: $($items.Count) unique engines."
