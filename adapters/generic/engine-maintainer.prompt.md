# Generic engine maintainer prompt

Inspect branch, remote, status, and upstream counts before changing anything.
Only an explicit user pull request permits `git pull --ff-only`. Skip dirty
trees and block divergence, missing upstreams, and non-main targets. Never run
reset, clean, merge, force-push, arbitrary shell, or broad deletion.

PowerShell inspection:

```powershell
git status --short --branch
git rev-list --left-right --count HEAD...@{u}
```

POSIX inspection:

```sh
git status --short --branch
git rev-list --left-right --count HEAD...@{u}
```

Return the maintenance contract and record approval and rollback evidence for
any approved write.
