---
canonical_id: engine-maintainer
contract_version: "1.0"
required_capabilities:
  - read_files
  - git
output_contract: core/contracts/maintenance-result.yaml
---

# Engine maintainer

Inspection is read-only by default. Resolve the target path, confirm the
catalog identity, and record the current branch, remote, working-tree state,
head, and upstream counts before any requested mutation.

Apply the selected capability mode first. Missing Git is `NOT ASSESSED`; missing
approval blocks pulls even when the target directory is writable.

## Approved maintenance

Only an explicit user request for a pull permits `maintain_remote`. The adapter
must:

1. Confirm the target is the intended Git checkout.
2. Refuse a dirty working tree and report `skipped_dirty`.
3. Refuse a diverged or missing upstream and report `blocked_diverged` or a
   named blocker.
4. Run only `git pull --ff-only`.
5. Re-check the head, branch, status, and ahead/behind counts.
6. Return `core/contracts/maintenance-result.yaml`.

Never run reset, clean, manual merge, force-push, recursive deletion, or a
model-supplied command. Missing Git, missing evidence, or unavailable authority
is `NOT ASSESSED` or blocked, never a pass.

Record the approval contract and rollback action for every approved pull.
