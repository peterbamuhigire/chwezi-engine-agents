# Canonical copy of the shared hook files

Status: operating rule, 31 October 2026. Owner: coordination maintainer. Review: 2026-12-29.

## Which copy is canonical

The copy in **this package's `hooks/` folder** is canonical for four files:

| File | Purpose |
|---|---|
| `hooks/destructive-bash-gate.js` | Blocks destructive shell and Git commands in a `PreToolUse` hook until a person has approved them. |
| `hooks/plugin-hook-config.js` | Reads the plugin's `hooks_enabled` setting for the gate. |
| `hooks/test-destructive-bash-gate.js` | The gate's own test (61 assertions on 31 October 2026). |
| `hooks/test-plugin-hook-config.js` | The configuration reader's test (7 assertions). |

`catalog/shared-assets.yaml` records the same fact: rows `hooks-destructive-bash-gate`, `hooks-plugin-hook-config`,
`hooks-test-destructive-bash-gate` and `hooks-test-plugin-hook-config` name this package as canonical and owner, and list the eleven
engine copies. No engine's copy is edited first; an engine, a plugin installed from it, or a plugin bundled by a host never becomes
the source for another copy.

## Why more than one copy exists and which one runs

Each engine ships its own `hooks/hooks.json`, which starts the gate from `${CLAUDE_PLUGIN_ROOT}/hooks/destructive-bash-gate.js`. When
several engines are installed as plugins, the host runs the gate from whichever installed plugin it reaches first; an agent that
sees a block can therefore name any engine's plugin as the source. All copies are meant to be identical, so the one that fires does not
matter, provided none has fallen behind. Plugins installed from a marketplace are copied into the host's plugin cache and stay at
the version installed until the plugin is updated, so an installed copy can lag its repository.

## Checks

| Check | Command (run from this package) | Fails when |
|---|---|---|
| Repository copies, byte for byte, plus unregistered copies found on disk | `python scripts/render_host_files.py --check --engines-root <folder>` | any registered copy differs or a copy exists that the register does not list |
| Repository copies and installed plugin copies, the four files | `python scripts/check_hook_copies.py --engines-root <folder>` | any copy differs or is missing, including a stale installed copy (exit 1); an engine is not found (exit 3) |
| The gate's behaviour | `node hooks/test-destructive-bash-gate.js` and `node hooks/test-plugin-hook-config.js` | any assertion fails |

`--engines-root` is repeatable and may also be given through `CHWEZI_ENGINES_ROOT`. The check finds engines by catalogue path, repository,
id or a registered former folder name. By default `check_hook_copies.py` also reads the host plugin directory (`~/.claude/plugins`);
`--plugins-dir` overrides it. Folders named `.trash` are ignored.

## Changing the hook

1. Edit the file here. Run both hook tests and `python -X utf8 -m unittest tests.test_check_hook_copies`.
2. Copy the changed files byte for byte into each engine's `hooks/` folder, then run that engine's hook tests and its own router checks. Each
   engine commits its own copy; this package never writes to an engine.
3. Run `check_hook_copies.py` again. Repository copies must be identical before the engines are released.
4. Reinstall or update each plugin that bundles the hook, then run `check_hook_copies.py` once more so the installed copies are compared.
5. Update the register `review_date` if the change is deliberate and the date has passed.

An override of the gate itself (`CHWEZI_GATEGUARD=off`) is not a way to change a copy; it needs the person's separate approval for the
command that was blocked, and a repeat attempt does not count as approval.
