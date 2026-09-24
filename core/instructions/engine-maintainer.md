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

## Content-integrity inspection (read-only, every maintenance pass)

Never store book extractions in any engine. Book knowledge enters only as
paraphrased, task-oriented skill content (procedures, decision rules,
checklists, rubrics, original examples) with a short `Sources` line. Run
`python -X utf8 scripts/validate-no-book-extractions.py` and report each
finding as a blocker for the owning engine. The check is path-based: it fails
on `book-extractions/`, `extracted-books/`, `book-study/`, `book-studies/` or
`book-summaries/` folders and on book-digest file names such as
`*-book-extraction.md`; a generic `*-extraction.md` passes inside a skill's
`references/`, `templates/` or `examples/` folder (for example a
food-processing `juice-extraction.md`) and elsewhere needs a reasoned entry in
`catalog/content-integrity-allowlist.txt`. Git-ignored local working data is
out of scope. Do not delete flagged files yourself; removal is a separate,
approved change in the owning engine.
