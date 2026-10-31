# Portfolio router wording

Three sentences appear in every engine's `AGENTS.md`. Each names another repository, so each used to carry a
checkout path from one workstation. These files hold the one path-free wording for each sentence.

| File | Replaces (legacy form) | Where it sits in an engine router |
|---|---|---|
| `currentness-gate-location.md` | `Digital Research Engine at `<host path>`.` | Mandatory currentness gate for Kaizen |
| `control-plane-location.md` | `governed centrally by `<host path>\engine-control-plane.md`.` | Control-plane adoption sentence |
| `craft-standard-location.md` | `Load `<host path>\portfolio-craft-standard-2026-09-04.md` when available.` | Portfolio craft contract |

Each file is a single fragment with no trailing newline. The surrounding paragraph stays engine-specific.

## Use

```
python scripts/render_host_files.py --render-router-blocks --engine <engine checkout> --dry-run   # list what would change
python scripts/render_host_files.py --render-router-blocks --engine <engine checkout>             # write AGENTS.md
python scripts/render_host_files.py --check --engines-root <folder> [--engines-root <folder>]    # rules router-host-path, router-former-name
```

The renderer rewrites a sentence only when it still has the legacy form *and* names a host path; it never inserts a sentence an
engine does not already carry, never touches another file, preserves line endings, and is idempotent. `--check` reports any host
path or former engine folder name left in `AGENTS.md` or `CLAUDE.md`.
