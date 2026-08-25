# Generic engine orchestrator prompt

Read `catalog/engines.yaml`, resolve the current Git root, and read the matched
engine's `AGENTS.md` or `README.md` router. Select the smallest relevant skills
set. Add accounting doctrine for finance, design system for visual output, and
digital research for current or source-sensitive claims. Return `scope`,
`engines`, `inputs`, `sequence`, `evidence`, `blockers`, and `next_action`.

PowerShell read-only discovery:

```powershell
.\scripts\discover-engine.ps1 -Path (Get-Location).Path
```

POSIX read-only discovery:

```sh
git rev-parse --show-toplevel
```
