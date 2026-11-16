# Live owner-input checks, 16 November 2026

An owner could revise a plan after the driver started while the next worker
still used the previous intent. The runtime now checks the tracked owner plan
and optional contract against their startup baseline at operation boundaries
and before accepting a checkpoint. Drift blocks subsequent work and retains
the operation evidence for reconciliation. Unrelated checkout changes do not
block the run. A prepared operation is not launched under changed intent; an
active operation is observed without replay. These are discrete checks, not
continuous revocation. CANCEL remains the immediate-stop control.

A bounded Windows PermissionError read retry also prevents a brief receipt
access denial from immediately aborting observation. It never retries the job.
Persistent denial, missing files and malformed JSON remain failures. Tests
inject denial rather than claiming to identify the original Windows lock holder.

Release 2.1.1 validation is recorded in
[runtime evidence](../../auto-agents/EVIDENCE.md). The coordinator is the
community canonical source. Managed propagation preserves each target's config,
plan, ENGINE.md and runtime state. Private engine content is not part of this
community release. Independent read-only review found no confirmed material
defect; live contention across other environments remains NOT_ASSESSED.

The full runtime suite passed 78 tests in 486.008 seconds. The coordinator suite
passed 378 tests and 24 subtests in 334.36 seconds. The managed update to the two
named community engine copies completed, with no files removed; a repeated
preview reported zero changes. All three community manifests validate 23 files
each and match. Protected project files and Git HEADs remained unchanged.

The owner requested local changes only. No engine commit, push, deployment or
scheduled task was performed. The separate
[portfolio drift record](2026-11-16-portfolio-drift.md) retains release-pin work
until clean commits are authorised; no guards are bypassed.
