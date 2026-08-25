# Phase 12 — Release Documentation and Operations Plan

> **For agentic workers:** Use executing-plans or subagent-driven-development. Do not publish until every release check has evidence.

**Goal:** Publish a package that developers can install, verify, update, troubleshoot, and report against without knowing the internal architecture.

**Depends on:** Phases 1–11.

**Produces:** Adapter guides, release workflows, provenance metadata, changelog, and incident runbook.

## Files

- Create: docs/adapters/codex.md.
- Create: docs/adapters/claude-code.md.
- Create: docs/adapters/gemini-cli.md.
- Create: docs/adapters/opencode.md.
- Create: docs/adapters/generic.md.
- Create: docs/adapters/mcp.md.
- Create: docs/operations/upgrade-policy.md.
- Create: docs/operations/incident-runbook.md.
- Create: docs/operations/compatibility-report-template.md.
- Create: CHANGELOG.md.
- Create: .github/workflows/release.yml.
- Create: .github/workflows/adapter-smoke-tests.yml.
- Create: release/manifest.json.
- Create: release/checksums.txt.
- Create: release/NOTICE.txt.
- Modify: README.md, CONTRIBUTING.md, docs/distribution.md, and .github/workflows/validate.yml.

## Required guide sections

Every adapter guide must state:
- prerequisites and operating systems
- install, update, and uninstall commands
- how to confirm loading
- read-only discovery command
- validation command
- safe pull request flow
- model-provider configuration boundary
- fork behavior
- NOT ASSESSED cases
- missing dependency and permission troubleshooting
- compatibility report link

## Release metadata

release/manifest.json must record:
- source commit
- release version
- core schema versions
- adapter versions
- assessed hosts and model labels
- engine integration commit references
- build timestamp
- artifact filenames
- checksum file reference

## Tasks

- [ ] Rewrite README to distinguish host adapters from model providers.
- [ ] Add one installation guide for each adapter and one generic guide.
- [ ] Add release workflow that runs plugin, catalog, schema, adapter, install, security, and evaluation checks.
- [ ] Build the MCP package from its lockfile.
- [ ] Create release archive containing core, adapters, scripts, schemas, and docs.
- [ ] Generate SHA-256 checksums.
- [ ] Exclude API keys, local paths, private engine contents, and credential-bearing reports.
- [ ] Add protected-main release instructions and rollback procedure.
- [ ] Add issue template fields for host, model, adapter version, core version, OS, capability profile, reproduction case, and evidence.
- [ ] Add a changelog entry for the first multi-host release.
- [ ] Run a documentation consistency review against the compatibility matrix and adapter manifests.

## Tests and evidence

Run:
- python C:\Users\BIRDC\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .
- powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate-catalog.ps1 -CatalogPath "$PWD\catalog\engines.yaml"
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\validate_catalog.ps1
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\security\test_path_boundaries.ps1
- python evals\runners\run-contract-evals.py --cases evals\cases --out evals\reports\release.json
- git diff --check

Expected evidence: all available checks pass and every unavailable check is explicitly NOT ASSESSED.

## Failure handling

- Any plugin, schema, security, or forbidden-action failure blocks release.
- A missing host dependency removes that host from assessed support; it does not invalidate unrelated adapters.
- A release archive with untracked or secret-bearing files is discarded and rebuilt.

## Exit criteria

- Documentation agrees with actual install targets and manifests.
- Release artifacts are reproducible from a protected main commit.
- A developer can select an adapter without changing canonical instructions.

## Commit checkpoint

Stage the files listed above and commit:
release: add multi-host packaging and operating documentation
