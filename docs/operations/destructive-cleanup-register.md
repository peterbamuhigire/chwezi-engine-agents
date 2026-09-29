# Destructive-cleanup register

**Owner:** chwezi-engine-agents · **Created:** 29 September 2026 (M10-04-T12, UA-15) · **Review after:** 29 December 2026

Every recursive removal (`rm -rf`, `shutil.rmtree`, `Remove-Item … -Recurse`) in the scripts of the twelve public engines is listed here with a disposition. A new occurrence that is not in this register is a finding.

The bundled-script rule that new code must follow lives in the canonical `chwezi-dev-engine/skills/sdlc-meta/skill-writing` (quarantine to `.trash-<UTC timestamp>/` inside the work directory, purge only entries older than 7 days, check every removal path is non-empty and inside the work root, exempt only directories the same process created). Rule adapted in paraphrase from Egonex-AI/Understand-Anything (MIT, https://github.com/Egonex-AI/Understand-Anything, commit b05cc3b20990afca537b4fc0a49b4d7fbdc65bb0). No text copied.

## Acceptance grep

The phase file's grep is kept for comparability (Part A). Its `Remove-Item[^\n]*-Recurse` term is defective in POSIX ERE: inside a bracket expression `\n` means "backslash or the letter n", so any `Remove-Item` line with an `n` before `-Recurse` (for example `$destination`) is missed, and Node's `fs.rmSync` is not searched at all. The widened grep (Part B) fixes both and is the one to use from now on.

Part A (phase grep), run from the workspace root that holds the sibling checkouts:

```
for e in chwezi-dev-engine design-system-skills srs-skills website-skills digital-research-engine proposal-skills \
         business-plan-skills social-media-skills linux-skills chwezi-accounting-doctrine windows-admin-engine-skills chwezi-engine-agents; do
  grep -rnE "rm -rf|shutil\.rmtree|Remove-Item[^\n]*-Recurse" "$e" --include=*.py --include=*.sh --include=*.ps1 --include=*.js --include=*.mjs \
    --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=projects --exclude-dir='.trash-*' | grep -v destructive-bash-gate
done
```

Part B (widened grep): the same loop with the pattern
`"rm -rf|shutil\.rmtree|Remove-Item.*-Recurse|-Recurse.*Remove-Item|rmSync|rimraf|fs\.rm\(|rmdir /s"`.

Excluded by design: `node_modules/`, `projects/` (client work), `.git/`, `.trash-*/`, and the destructive-bash-gate hook and its tests (they hold the patterns as data).

## Count

29 September 2026: Part A finds **33 occurrences**; Part B finds **53** (20 more, listed in rows 34–53). The plan measured 27 with the Part A grep earlier the same day; the six extra Part A lines are new since that measurement: five `shutil.rmtree` calls in `chwezi-engine-agents/tests/test_render_host_files.py` (added by M10-02, commit `35340f6`) and one `trap 'rm -rf "$STAGE_DIR"'` in `srs-skills/scripts/build-doc.sh` (added by M10-01, commit `905b9a4`). All six remove directories created by `mkdtemp`/`mktemp -d` in the same process. One linux line (`validate_safe_operation_fixture.py:41`) is the pattern held as data, not a removal.

## Disposition key

| Disposition | Meaning |
|---|---|
| `waived-temp` | Removes a directory the same process created (`mkdtemp`, `mktemp -d`, GUID-suffixed temp path). Exempt under the canonical rule. |
| `waived-regenerable` | Removes generated, tracked or rebuildable output at a fixed path derived from the script's own root. Interim waiver; conversion recommended. |
| `guarded-confirm` | Removes user-supplied or user-owned content after an interactive confirmation. Interim; conversion to quarantine recommended. |
| `linux-handoff` | Runs on Linux servers. No edit without a Linux test (Peter's rule); waiver cites the existing guard, and any change goes to the P10 Linux lab. |
| `data` | The pattern appears as a string literal, not a removal. |
| `converted` | Replaced by quarantine-to-`.trash-<timestamp>/`. (None yet.) |

No script was edited in this phase: dev is being changed by M10-06 and srs by M10-07 at the same time, and linux changes need a Linux test. Conversions are listed as open items below.

## Register

| # | Repository | Location | What it removes | Guard in place | Disposition |
|---:|---|---|---|---|---|
| 1 | chwezi-dev-engine | `skills/languages/python-modern-standards/scripts/desktop_suite_packager.py:827` | Generated PowerShell removes `dist/stage` before a release build | `Test-Path`; path joined from the project root | `waived-regenerable` (convert: O-1) |
| 2 | chwezi-dev-engine | `…/desktop_suite_packager.py:828` | Same, the build work directory | `Test-Path`; path joined from the project root | `waived-regenerable` (convert: O-1) |
| 3 | srs-skills | `02-requirements-engineering/waterfall/01-initialize-srs/init_skill.py:53` | `../project_context/` when the user picks "clean" | Interactive prompt only | `guarded-confirm` (convert: O-2, highest priority: user content) |
| 4 | srs-skills | `scripts/build-doc.sh:64` | `mktemp -d` stage directory on exit | Created by the same process | `waived-temp` |
| 5 | srs-skills | `scripts/seed_example_project.py:33` | Tracked example under `00-meta-initialization/new-project/examples/<slug>` before re-seeding | Fixed path under the repository root; content is in git | `waived-regenerable` (convert: O-3) |
| 6 | srs-skills | `scripts/setup-srs-project.ps1:97` | An existing clone at the target directory | `y/N` confirmation | `guarded-confirm` (convert: O-2) |
| 7 | srs-skills | `scripts/setup-srs-project.sh:99` | An existing clone at the target directory | `y/N` confirmation | `guarded-confirm` (convert: O-2) |
| 8 | website-skills | `scripts/rollback.sh:164` | `mktemp -d "$target/.rollback.XXXXXX"` | Same process; `case` pattern refuses any other path | `waived-temp` |
| 9 | website-skills | `scripts/rollback.sh:205` | `mktemp -d "$target/.rollback-recovery.XXXXXX"` | Same process; `case` pattern refuses any other path | `waived-temp` |
| 10 | website-skills | `scripts/test-banned-phrase-scan.sh:12` | `mktemp -d` test directory on exit | Same process | `waived-temp` |
| 11 | digital-research-engine | `engine/tests/test_example_project_seed.py:19` | `tempfile.mkdtemp` test directory | Same process | `waived-temp` |
| 12 | digital-research-engine | `engine/tests/test_kernel.py:25` | `tempfile.mkdtemp` test directory | Same process | `waived-temp` |
| 13 | digital-research-engine | `scripts/seed_example_project.py:31` | `projects/example-*` before re-seeding | Fixed names from a constant tuple, relative to the working directory | `waived-regenerable` (convert: O-3; also resolve against the repository root, not the working directory) |
| 14 | linux-skills | `scripts/lib/common.sh:693` | Temp paths registered by `safe_tempfile`/`safe_tempdir` (registry file) | `-n` and `-e` checks; paths come only from the registry | `linux-handoff` (waiver) |
| 15 | linux-skills | `scripts/lib/common.sh:698` | Temp paths in `SK_CLEANUP_PATHS` | `-e` check; array holds only registered temp paths | `linux-handoff` (waiver; add `-n` guard in P10 lab: O-4) |
| 16 | linux-skills | `scripts/sk-mysql-backup.sh:103` | `$DUMP_DIR` in the cleanup trap | `-n` check; set at l.165 by the same run | `linux-handoff` (waiver) |
| 17 | linux-skills | `scripts/sk-mysql-backup.sh:229` | `$DUMP_DIR` after `tar` succeeds | Set at l.165 as `$BACKUP_DIR/dump_$TIMESTAMP` by the same run; runs only after `tar` succeeds (`|| die`) | `linux-handoff` (waiver; add `-n` guard in P10 lab: O-4) |
| 18 | linux-skills | `scripts/tests/install-skills-bin.test.sh:11` | `mktemp -d` test root on exit | Same process | `waived-temp` |
| 19 | linux-skills | `scripts/validate_safe_operation_fixture.py:41` | Nothing: the string `"rm -rf"` in a list of unsafe tokens | n/a | `data` |
| 20 | chwezi-engine-agents | `evals/runners/run-host-smoke-tests.ps1:17` | GUID-suffixed temp install target | Same process; `Test-Path` | `waived-temp` |
| 21 | chwezi-engine-agents | `scripts/install.ps1:154` | `<destination>.backup-<GUID>` (the previous install) after a successful swap | Same run created it by `Move-Item`; runs only after the new install is in place | `waived-temp` (quarantine option: O-5) |
| 22 | chwezi-engine-agents | `scripts/install.ps1:162` | `<destination>.staging-<GUID>` on failure | Same process | `waived-temp` |
| 23 | chwezi-engine-agents | `scripts/install.sh:73` | `<destination>.staging.$$` in the exit trap | Same process | `waived-temp` |
| 24 | chwezi-engine-agents | `scripts/install.sh:106` | `<destination>.backup.$$` (the previous install) after a successful swap | `-n` check; same run created it by `mv` | `waived-temp` (quarantine option: O-5) |
| 25 | chwezi-engine-agents | `tests/install/test_fork_discovery.ps1:19` | GUID-suffixed temp target | Same process | `waived-temp` |
| 26 | chwezi-engine-agents | `tests/install/test_install_targets.ps1:19` | GUID-suffixed temp target | Same process | `waived-temp` |
| 27 | chwezi-engine-agents | `tests/security/test_mutation_gates.ps1:16` | GUID-suffixed temp target | Same process | `waived-temp` |
| 28 | chwezi-engine-agents | `tests/security/test_path_boundaries.ps1:16` | GUID-suffixed temp target and "outside" directory | Same process | `waived-temp` |
| 29 | chwezi-engine-agents | `tests/test_render_host_files.py:135` | `tempfile.mkdtemp` workspace | Same process | `waived-temp` |
| 30 | chwezi-engine-agents | `tests/test_render_host_files.py:238` | Engine folder inside the `mkdtemp` workspace | Inside the same-process temp tree | `waived-temp` |
| 31 | chwezi-engine-agents | `tests/test_render_host_files.py:257` | `tempfile.mkdtemp` workspace | Same process | `waived-temp` |
| 32 | chwezi-engine-agents | `tests/test_render_host_files.py:298` | `tempfile.mkdtemp` workspace | Same process | `waived-temp` |
| 33 | chwezi-engine-agents | `tests/test_render_host_files.py:326` | Engine folder inside the `mkdtemp` workspace | Inside the same-process temp tree | `waived-temp` |

### Part B additions (widened grep)

| # | Repository | Location | What it removes | Guard in place | Disposition |
|---:|---|---|---|---|---|
| 34 | chwezi-engine-agents | `scripts/install.ps1:156` (catch) | A partly moved destination on failure, before the backup is restored on the next line | Same run; `Test-Path` | `waived-temp` |
| 35 | chwezi-engine-agents | `tests/security/install-engine-ownership.test.js:43` | Temp install target | Asserts the path is inside the temp root first | `waived-temp` |
| 36 | chwezi-engine-agents | `tests/security/install-engine-ownership.test.js:131` | Test sandbox | Asserts the sandbox is inside `os.tmpdir()` first | `waived-temp` |
| 37 | chwezi-engine-agents | `tests/security/install-package-preservation.ps1:58` | A `README.md` directory the test itself created inside its sandbox | Inside the same-process sandbox | `waived-temp` |
| 38 | chwezi-engine-agents | `tests/security/install-package-preservation.ps1:90` | Test sandbox | Refuses any path outside `TEMP` | `waived-temp` |
| 39 | chwezi-engine-agents | `tests/security/install-shell-preservation.ps1:63` | A `README.md` directory the test itself created | Inside the same-process sandbox | `waived-temp` |
| 40 | chwezi-engine-agents | `tests/security/install-shell-preservation.ps1:92` | Test sandbox | Refuses any path outside `TEMP` | `waived-temp` |
| 41 | design-system-skills | `hooks/test-token-file-gate.js:24` | `os.tmpdir()/chwezi-token-gate-test-<name>-<pid>` before reuse | Fixed temp prefix plus PID | `waived-temp` |
| 42 | srs-skills | `scripts/plan-canvas.js:350` | One file: the server-info record in the state directory | Not recursive | `single-file` |
| 43 | srs-skills | `scripts/plan-canvas.js:363` | Same file on shutdown | Not recursive | `single-file` |
| 44 | srs-skills | `tests/hooks/plan-canvas-sessions-hook.test.js:95` | Test temp directory | Same process | `waived-temp` |
| 45 | srs-skills | `tests/plan-canvas/e2e.test.js:253` | Test temp directory | Same process | `waived-temp` |
| 46 | srs-skills | `tests/plan-canvas/sessions.test.js:213` | Fixture temp directories | Same process | `waived-temp` |
| 47 | srs-skills | `tests/scripts/plan-canvas.test.js:471` | Test temp directory | Same process | `waived-temp` |
| 48 | srs-skills | `tests/scripts/plan-canvas.test.js:472` | The test's "outside" temp directory | Same process | `waived-temp` |
| 49 | website-skills | `hooks/test-drift-check-hook.js:54` | `mkdtempSync` directory | Same process | `waived-temp` |
| 50 | website-skills | `hooks/test-drift-check-hook.js:91` | One file: the test's backup copy after restoring the real script | Not recursive | `single-file` |
| 51 | website-skills | `hooks/test-quality-gate.js:80` | Test temp project | Same process | `waived-temp` |
| 52 | website-skills | `hooks/test-quality-gate.js:147` | One file: a stub | Not recursive | `single-file` |
| 53 | website-skills | `hooks/test-quality-gate.js:161` | Test stub directory | Same process | `waived-temp` |

`single-file` = a non-recursive single-file removal matched only by the widened pattern; out of scope for the quarantine rule.

Totals, Part A (33): `waived-temp` 21, `waived-regenerable` 4, `guarded-confirm` 3, `linux-handoff` 4, `data` 1, `converted` 0. Part B additions (20): `waived-temp` 16, `single-file` 4. All 53 dispositioned.

## Open items (recommended conversions)

- **O-1 (dev, after M10-06 releases the file):** make the generated packager script move `stage`/`work` to `.trash-<UTC timestamp>/` under `dist`, or confirm they are same-run artefacts and add a comment.
- **O-2 (srs, after M10-07 releases the scripts):** replace the confirmed deletions in `init_skill.py`, `setup-srs-project.ps1` and `setup-srs-project.sh` with a move to `.trash-<UTC timestamp>/` beside the target, with an empty-variable guard. These touch user content and should go first.
- **O-3 (srs, DRE):** example re-seeders may quarantine instead of delete, or keep the waiver because the content is tracked in git; decide once.
- **O-4 (linux, P10 lab):** add explicit non-empty checks to `common.sh:698` and `sk-mysql-backup.sh:229`; test on Linux before merging.
- **O-5 (agents installers):** optionally keep the previous-install backup in quarantine for 7 days instead of deleting it. The installers are rendered into all eleven engines (`catalog/shared-assets.yaml`, `engine-install-*`), so any change goes through the template and the drift check.
