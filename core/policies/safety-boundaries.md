# Safety boundaries

These rules apply to every adapter and transport.

## Defaults

- Read files, inspect Git metadata, read routers, and review documented
  commands without mutation.
- Require explicit approval for pulls, writes, overwrite, update, uninstall,
  submissions, publication, external messages, and dependency installation.
- Treat missing capability, dependency, source, platform, or authority as
  `NOT ASSESSED`.

## Allowed Git mutation

The only maintenance pull is `git pull --ff-only`, after a clean-tree and
upstream check. A dirty tree, divergence, missing upstream, or non-main target
blocks the operation.

## Denylist

Adapters must reject model-supplied arbitrary commands and never invoke reset,
clean, force-push, manual merge, broad recursive deletion, path traversal,
unapproved external publication, or a validator not declared by the catalog or
engine manifest.

## Evidence

Every write records the requested operation, approval, target, before and after
heads where applicable, result, and rollback action. Structured and Markdown
handoffs use the same contract field names.
