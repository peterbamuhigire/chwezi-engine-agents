# Generic engine validator prompt

Read the selected engine router and run only validators declared in the
catalog or engine manifest. Check dependencies and working directory first.
Return `PASS`, `FAIL`, or `NOT ASSESSED` with command, exit code, evidence, and
duration. Missing shell or dependencies cannot be a pass.

PowerShell:

```powershell
.\scripts\validate-catalog.ps1 -CatalogPath .\catalog\engines.yaml
```

POSIX:

```sh
python scripts/validate-contracts.py --schema schemas/engine-catalog.schema.json --instance catalog/engines.yaml
```
