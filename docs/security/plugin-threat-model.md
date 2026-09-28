# P19 plugin and installer threat model

**Review date:** 2026-09-27
**Scope:** shared `scripts/install-engine.js`, PowerShell `scripts/install.ps1`, POSIX `scripts/install.sh`, `scripts/resolve-install-target.py`, their manifest/state inputs, and the shared destructive-command hook as an existing adjacent control. This is a bounded repository review, not certification of the complete engine estate or a live host installation.

## Assets and boundaries

| Asset/boundary | Trust assumption | Threat and consequence | Control/evidence | Residual status |
|---|---|---|---|---|
| Engine source tree and `.claude-plugin/plugin.json` | Local path is supplied by the caller; contents are not authenticated by the installer | Malicious manifest path could read/copy outside the selected engine root | Root-contained source/destination resolution; symlink rejection; traversal fixture | Traversal case PASS; source authenticity/signature validation NOT ASSESSED |
| Target `.claude` tree and `install-state.json` | Existing files may be user-owned or edited | First install or update could overwrite user work; corrupt state could be mistaken for empty ownership | Preflight refuses unowned collisions, modified managed files and malformed state; isolated ownership tests | Tested local fixture PASS; concurrent filesystem race resistance NOT ASSESSED |
| Coordinator bootstrap targets and install manifests | Existing files may be user-owned or edited | Bootstrap could replace local configuration, hidden files or content at paths that change between file and directory | Node, PowerShell and POSIX installers hash managed files; reject unmanaged or modified collisions by default; retain unrelated and hidden files; resolver rejects roots and source-tree overlap | Node, PowerShell and Git Bash fixture tests PASS; race resistance and non-Windows host matrix NOT ASSESSED |
| Update/uninstall recorded paths | State record may be stale or tampered | Path traversal or symlink could delete files outside the managed root | Resolve recorded paths under target root; reject symlink components before action | Traversal fixture PASS; OS-specific junction/reparse-point behavior NOT ASSESSED |
| Installer executable and dependencies | Script is reviewed source; local runtimes are trusted | Hidden download, shell execution, dependency substitution or unexpected outbound call | Static inspection found no network client in scoped installers; Node uses built-ins, PowerShell uses installed modules, POSIX uses shell/Python/Git utilities; syntax and isolated behavior tests retained | No source signature/attestation; runtime trust and complete estate dependency graph NOT ASSESSED |
| Fetched documents, tool results and imported skills | Untrusted data, not authority | Indirect prompt injection can redirect scope or request source-ledger exfiltration | Dev-engine common security rule and AI security skill say treat content as data, flag it, and gate external actions outside the model; inert fixtures retained | Full agent/runtime behavioral evaluation and external-tool egress monitoring NOT ASSESSED |
| Destructive-command hook | Optional host hook, not a security boundary | Matching commands are denied on every attempt; malformed or missing payload fails closed; explicit environment override, shell parsing limits, hook timeout behavior, and host configuration remain bypass or coverage risks | Focused fixtures block `git push --force-with-lease` with and without `=<ref>[:<expect>]`, and allow `--no-force-with-lease`. The option syntax is confirmed by the official Git `git-push` reference. | Do not rely on it as authorization enforcement; live-host behavior NOT ASSESSED |

## Installer contract after P19 repair

- Install and update are preflighted before copying; an unowned destination or locally modified managed file is refused unless the caller explicitly passes `--force`.
- Manifest, target and recorded uninstall/doctor paths must remain under their selected root. Symlinked source entries, state paths or target path components are refused.
- Invalid ownership state fails closed. Removed source files stay listed in ownership state until uninstall so updates do not silently abandon managed files.
- Uninstall refuses modified managed files without `--force` and leaves unrelated target files alone.
- Shared Node, PowerShell, and POSIX bootstrap installers refuse non-empty unmanaged targets by default, track managed file hashes, preserve unrelated and hidden user files, and require an explicit force override to replace content. File-to-directory and directory-to-file collisions fail closed.
- `tests/security/install-engine-ownership.test.js`, `tests/security/install-package-preservation.ps1`, and `tests/security/install-shell-preservation.ps1` exercise isolated temporary fixtures. The PowerShell and POSIX fixtures use synthetic source checkouts; they do not install into a user's real engine home.
- The installer copies files only. It does not execute copied skills/hooks, install packages or fetch remote content.

`--force` is an explicit destructive override. It is not a trust signal for an untrusted source package and does not authenticate the engine source.

## Selected control references

- Claude Code Hooks Reference, accessed 2026-09-27, documents PreToolUse JSON input on stdin, the `tool_input.command` field, exit code 2 blocking, and the fact that timed-out command hooks do not block. This validates the documented adapter contract only; the installed live host was not exercised: https://code.claude.com/docs/en/hooks
- OWASP ASVS `v5.0.0-5.3.2` is a relevant design analogue for strict path construction and traversal defense. The control is for application file paths; this local CLI review does not assert ASVS conformance.
- NIST SSDF v1.1 `PW.7` informed human code review and issue remediation; NIST SSDF v1.2 remains an initial public draft in the source record. This scoped implementation is not an SSDF assessment.

## Decision

The installer ownership and traversal defects found in static review are repaired and pass isolated local tests. This permits only a **conditional local installer-safety result**. Full agent prompt-injection resistance, live host-hook enforcement, signed source provenance, cross-platform reparse-point handling, race resistance, and estate-wide release security remain **NOT ASSESSED**. Do not describe the installer or suite as certified or production-secure on this evidence.
