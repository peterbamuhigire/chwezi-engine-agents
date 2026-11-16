# Publication of approved engine improvements, 16 November 2026

The owner authorised committing and pushing all pending engine changes to main,
superseding the earlier hold. Source changes, portability repairs and model-policy
updates were reviewed and committed; local settings and source-book material were
excluded. The full twelve-repository hygiene scan reports zero findings.

The incoming auto-agents 2.0.1 macOS/BSD restart fix was preserved alongside the
2.1.1 owner-intent and receipt-read changes. Only unpublished local commits were
rebased. README/manifest conflicts and both changelog entries were reconciled.
No force push or published-history rewrite was used.

Combined community runtime validation: 80 tests in 361.555
seconds; 79 passed and 1 skipped (a live-Mac test on Windows).
The stubbed macOS fallback test passed; the earlier real-Mac evidence remains
dated to its original revision. Manifests validate 23 files in each community
copy, and config, PLAN.md and ENGINE.md hashes are unchanged. Earlier coordinator
validation passed 378 tests and 24 subtests; those sources did not change during
publication integration. The staged-content and no-book-extraction scans pass.

After the domain commits, the guarded updater refreshed all eleven release pins.
The full host-drift check now exits zero, with no tolerance or guard weakened.
The final pin-refresh and host-rendering regression run passed 78 tests in 62.32 seconds.
The preceding hold statements in dated records describe their earlier checkpoints.
This publication does not start a factory run, install a schedule or deploy an app.
Other dated backlog items in the README remain separate work.
