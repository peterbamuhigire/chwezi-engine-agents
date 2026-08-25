# Phase 3 — Schemas and Contract Validation Implementation Plan

> **For agentic workers:** Use `superpowers:executing-plans` or `superpowers:subagent-driven-development`. Every schema change must include a valid fixture and an invalid fixture.

**Goal:** Make catalog entries, adapter manifests, handoffs, maintenance results, validation results, and capability profiles machine-checkable across PowerShell, Python, TypeScript, and host adapters.

**Depends on:** Phases 1 and 2.

**Produces:** JSON Schemas, YAML fixtures, and a deterministic validator with stable exit codes.

## Files

- Create: `schemas/engine-catalog.schema.json` — ten-engine catalog shape.
- Create: `schemas/agent-manifest.schema.json` — canonical agent metadata.
- Create: `schemas/handoff.schema.json` — orchestration output.
- Create: `schemas/maintenance-result.schema.json` — maintenance output.
- Create: `schemas/validation-result.schema.json` — check and aggregate verdicts.
- Create: `schemas/adapter-manifest.schema.json` — host adapter metadata.
- Create: `schemas/capability-profile.schema.json` — host capability profile.
- Create: `scripts/validate-contracts.py` — schema validator.
- Create: `tests/fixtures/valid-handoff.yaml`.
- Create: `tests/fixtures/invalid-handoff-missing-scope.yaml`.
- Create: `tests/fixtures/valid-validation-result.yaml`.
- Create: `tests/fixtures/invalid-validation-result.yaml`.
- Modify: `catalog/engines.yaml` — schema version and optional contract fields.
- Modify: `scripts/validate-catalog.ps1` — call the contract validator.
- Modify: `tests/validate_catalog.ps1` — cover schema and catalog behavior.

## Validator interface

```text
python scripts/validate-contracts.py --schema <schema-path> --instance <yaml-or-json-path>
```

Exit codes:

- `0`: instance validates.
- `2`: schema or instance is invalid.
- `3`: file, parser, or dependency is unavailable.

Output must name the instance, schema, failing path, and human-readable reason. It must not print credential values.

## Required schema rules

- Every instance contains `schema_version`.
- Engine IDs are lowercase hyphenated strings and unique within the catalog.
- Adapter manifests contain `id`, `host`, `version`, `core_version`, `entrypoints`, `install_targets`, and `required_capabilities`.
- Check verdicts are exactly `PASS`, `FAIL`, or `NOT ASSESSED`.
- Aggregate verdicts may additionally be `PARTIAL`.
- A `PASS` check requires a command, exit code, and evidence string.
- A `NOT ASSESSED` check requires a reason or unavailable dependency field.
- Unknown top-level fields are rejected until the schema version is changed or the field is declared optional.

## Tasks

- [ ] Write valid and invalid fixtures before implementing the validator.
- [ ] Implement YAML loading with a pinned approved dependency, or record the dependency as unassessed if unavailable.
- [ ] Implement JSON Schema validation with deterministic error ordering.
- [ ] Add catalog-specific uniqueness and path checks after schema validation.
- [ ] Connect the PowerShell catalog validator to the Python validator with a script-root-safe path.
- [ ] Add tests for missing fields, invalid enums, duplicate engine IDs, malformed YAML, and missing files.
- [ ] Document schema version bump rules in `docs/architecture/compatibility-contract.md`.
- [ ] Make adapters consume these schemas instead of defining local field names.

## Tests and evidence

```powershell
python scripts\validate-contracts.py --schema schemas\engine-catalog.schema.json --instance catalog\engines.yaml
python scripts\validate-contracts.py --schema schemas\handoff.schema.json --instance tests\fixtures\valid-handoff.yaml
python scripts\validate-contracts.py --schema schemas\validation-result.schema.json --instance tests\fixtures\valid-validation-result.yaml
python scripts\validate-contracts.py --schema schemas\handoff.schema.json --instance tests\fixtures\invalid-handoff-missing-scope.yaml
.\tests\validate_catalog.ps1
```

Expected evidence: valid fixtures exit `0`, invalid fixtures exit `2`, and the catalog test reports 10 unique engines.

## Failure handling

- Missing parser dependency: report `NOT ASSESSED` in phase evidence and do not claim contract validation passed.
- Schema incompatibility: preserve the old schema version and add a new version; do not reinterpret fields silently.
- Existing catalog data that cannot validate: stop adapter work until the catalog is repaired and reviewed.

## Exit criteria

- Every downstream language can validate the same contract vocabulary.
- Invalid verdicts and missing evidence cannot enter a release artifact.

## Commit checkpoint

```powershell
git add schemas scripts/validate-contracts.py catalog/engines.yaml scripts/validate-catalog.ps1 tests/validate_catalog.ps1 tests/fixtures
git commit -m "feat: add shared agent contract schemas"
```
