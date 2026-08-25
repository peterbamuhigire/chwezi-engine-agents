# Universal Multi-Host Skills Engine Agents Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (recommended) or `superpowers:executing-plans` to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend `skills-engine-agents` from a Codex-only plugin into a model-neutral coordination package with host adapters for Codex, Claude Code, Gemini CLI, OpenCode, and a generic command-line/MCP path, while preserving the ten independent skills-engine repositories as the source of truth.

**Architecture:** Keep one canonical instruction and contract layer in this repository. Add thin adapters for each AI host, because hosts load instructions and tools while models only generate or interpret messages. Expose deterministic repository operations through portable scripts and an optional MCP server; keep mutations approval-gated and preserve the current fast-forward-only maintenance boundary.

**Tech Stack:** Markdown with YAML frontmatter, JSON Schema, YAML, PowerShell 7+, Python 3.11+, Node.js 20+ for the optional MCP server, Git, GitHub Actions, MCP, and host-specific adapter manifests documented by each supported client.

## Global Constraints

- All implementation work stays on `main` unless the user explicitly requests a branch.
- The ten engine repositories remain independent; this repository must not copy their domain `SKILL.md` content.
- `AGENTS.md`, engine routers, and engine `SKILL.md` files remain the domain source of truth.
- The canonical layer must not depend on a fixed path such as `C:\\wamp64\\www`.
- Read-only inspection is the default; writes, pulls, and external mutations require explicit user authority.
- Engine pulls use `git pull --ff-only` only after an explicit pull request; dirty or diverged repositories are skipped and reported.
- No adapter may silently upgrade `NOT ASSESSED` to `PASS`.
- No adapter may use provider-specific model names, API parameters, or proprietary prompt syntax in the canonical layer.
- Secrets must remain in environment variables or host credential stores; no API key belongs in the repository.
- Every phase ends with a deterministic verification command and a commit checkpoint in the implementation phase. This planning document itself is committed as one documentation change.
- Current platform assumptions must be rechecked against official documentation during implementation. Starting references are OpenAI plugin documentation at `https://developers.openai.com/`, Anthropic MCP documentation at `https://docs.anthropic.com/en/docs/mcp`, and DeepSeek API documentation at `https://api-docs.deepseek.com/`.

## Desired end state

The repository should support these installation and execution paths:

| Host | Installation target | Execution contract | Model examples |
|---|---|---|---|
| Codex | Codex plugin package and local plugin directory | Codex agents invoke canonical instructions and repository scripts | GPT-family models, configured compatible providers |
| Claude Code | Claude project/user instruction and agent/skill adapter | Claude Code invokes the same contracts through its own discovery rules | Claude models, DeepSeek through a supported compatible endpoint |
| Gemini CLI | Gemini project instructions and command adapter | Gemini receives the same routing rules and calls portable scripts | Gemini models and configured providers |
| OpenCode | OpenCode project instructions and skill adapter | OpenCode uses the same catalog, contracts, and scripts | OpenCode-supported models, including configured DeepSeek providers |
| Generic client | Plain Markdown prompt bundle plus CLI scripts | A human or host loads the prompt and runs the deterministic commands | Any model with file and shell access |
| MCP-capable host | MCP server configuration | The host discovers typed tools and applies user approvals | Any model supported by that host |

The word “universal” refers to the coordination contract and adapters. It does not promise identical model quality, identical tool permissions, or automatic plugin discovery in every AI product.

## Repository map before implementation

The current repository has these responsibilities:

| Existing path | Current responsibility | Planned treatment |
|---|---|---|
| `.codex-plugin/plugin.json` | Codex plugin metadata | Keep as the Codex adapter manifest; add adapter metadata without breaking Codex validation |
| `agents/*.md` | Three Codex agent definitions | Split canonical behavior from Codex-specific wrapper text |
| `catalog/engines.yaml` | Ten-engine registry and validators | Keep as the canonical catalog; add schema and capability metadata |
| `scripts/discover-engine.ps1` | Current Git-root discovery | Keep as the reference implementation and add a cross-platform equivalent |
| `scripts/install.ps1` | Local Codex installation | Convert into an explicit host-aware installer with safe copy and update behavior |
| `scripts/validate-catalog.ps1` | Catalog shape validation | Extend to validate host adapters and catalog schema |
| `tests/validate_catalog.ps1` | Deterministic catalog test | Add fixtures for host discovery, forks, dirty trees, and unsupported engines |
| `README.md` | Human installation and scope documentation | Add the multi-host model, adapter matrix, and capability limits |
| `docs/distribution.md` | Distribution notes | Document host-specific installation and release channels |
| `docs/plans/aug-25/` | User-requested implementation plan location | Store this plan and later phase evidence links |

## Canonical interfaces

All adapters must preserve these interfaces:

```yaml
engine_identity:
  id: string
  repository: string
  path: string
  repo_root: string
  remote: string
  branch: string
  router: string|null
  matched_catalog_entry: boolean

maintenance_result:
  engine_id: string
  before_head: string
  after_head: string
  branch: string
  working_tree: clean|dirty|missing
  pull_result: not_requested|updated|already_current|skipped_dirty|blocked_diverged|failed
  ahead: integer
  behind: integer
  blocker: string|null

validation_result:
  engine_id: string
  checks:
    - command: string
      status: PASS|FAIL|NOT ASSESSED
      exit_code: integer|null
      evidence: string
      duration_ms: integer|null
  overall: PASS|FAIL|PARTIAL|NOT ASSESSED
  next_action: string

handoff:
  scope: string
  engines: list
  inputs: list
  sequence: list
  evidence: list
  blockers: list
  next_action: string
```

The implementation may represent these contracts as JSON, YAML, Python dataclasses, or typed TypeScript objects inside a specific adapter, but field names and verdict values must remain stable.

---

## Phase 1: Establish the compatibility baseline and acceptance contract

**Purpose:** Replace broad “works with all models” language with a testable definition of host support, model support, capabilities, and fallbacks.

**Files:**

- Create: `docs/architecture/compatibility-contract.md`
- Create: `docs/architecture/host-model-capability-matrix.md`
- Create: `docs/architecture/decision-records/ADR-001-hosts-versus-models.md`
- Create: `tests/fixtures/compatibility-matrix.yaml`
- Modify: `README.md`
- Modify: `docs/distribution.md`

**Interfaces:**

- Consumes: Current plugin manifest, three current agents, `catalog/engines.yaml`, and host documentation verified during implementation.
- Produces: A support taxonomy used by every later phase.

### Work items

- [ ] Define `host` as the application that loads instructions, tools, and permissions.
- [ ] Define `model` as the provider/model selected by the host.
- [ ] Define `adapter` as the host-specific packaging and discovery layer.
- [ ] Define `core` as the model-neutral catalog, policies, contracts, and deterministic operations.
- [ ] Define support levels: `native`, `adapter`, `generic`, and `not_assessed`.
- [ ] Define capability flags: `read_files`, `write_files`, `shell`, `git`, `web`, `subagents`, `mcp`, `structured_output`, and `user_approval`.
- [ ] Define fallback behavior when each capability is absent.
- [ ] Record that a model-only API integration is not an installation target unless a host supplies file/tool orchestration.
- [ ] Add a compatibility matrix with one row per target host and columns for installation, discovery, tool execution, approval handling, and model-provider configuration.
- [ ] Add an explicit boundary: no claim of equal reasoning quality or equal tool access across models.
- [ ] Add the official documentation links as verification starting points, with a note that the implementation must recheck them before adapter release.

### Acceptance checks

Run:

```powershell
rg -n "host|model|adapter|native|generic|not_assessed|read_files|user_approval" docs/architecture/compatibility-contract.md docs/architecture/host-model-capability-matrix.md
git diff --check
```

Expected result: every term appears in a defined section, and no whitespace errors are reported.

### Exit criteria

- A reviewer can determine whether a requested integration is a host adapter, a model-provider configuration, or outside scope.
- Every later phase has a named acceptance target.

---

## Phase 2: Normalize the canonical core and remove host-specific assumptions

**Purpose:** Make the three existing agents reusable without copying their behavior into every host adapter.

**Files:**

- Create: `core/instructions/engine-orchestrator.md`
- Create: `core/instructions/engine-maintainer.md`
- Create: `core/instructions/engine-validator.md`
- Create: `core/contracts/handoff.yaml`
- Create: `core/contracts/maintenance-result.yaml`
- Create: `core/contracts/validation-result.yaml`
- Create: `core/policies/safety-boundaries.md`
- Modify: `agents/engine-orchestrator.md`
- Modify: `agents/engine-maintainer.md`
- Modify: `agents/engine-validator.md`
- Modify: `skills/README.md`

**Interfaces:**

- Consumes: Existing agent behavior and catalog fields.
- Produces: Canonical instructions with stable names and adapter-neutral tool descriptions.

### Work items

- [ ] Move routing rules into `core/instructions/engine-orchestrator.md`.
- [ ] Move pull safety rules into `core/instructions/engine-maintainer.md`.
- [ ] Move validation verdict rules into `core/instructions/engine-validator.md`.
- [ ] Replace direct assumptions about Codex-only invocation with abstract operations named `discover_engine`, `read_router`, `run_validator`, and `maintain_remote`.
- [ ] Keep the exact mutation rule: only explicit user pull authority permits `git pull --ff-only`.
- [ ] Keep the exact verdict rule: unavailable command or evidence means `NOT ASSESSED`.
- [ ] Define the handoff packet as the stable output of orchestration.
- [ ] Turn the current Codex agents into thin wrappers that point to the canonical instructions and add only Codex invocation details.
- [ ] Add frontmatter fields `canonical_id`, `version`, `required_capabilities`, and `output_contract` to each canonical instruction.
- [ ] Add a test that fails if canonical files contain Codex-only syntax such as `codex://`, plugin deeplinks, or model-specific API parameters.

### Acceptance checks

```powershell
rg -n "codex://|Responses API|Anthropic|DeepSeek|GPT-" core/instructions
python C:\Users\BIRDC\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .
git diff --check
```

Expected result: the first command reports no provider-specific matches in canonical instructions; the Codex validator passes after wrapper updates.

### Exit criteria

- There is one source of truth for each agent’s behavior.
- Codex wrappers are small enough that they cannot silently diverge from the canonical instructions.

---

## Phase 3: Add schemas, versioning, and contract validation

**Purpose:** Make catalogs, agent metadata, handoffs, and validation results machine-checkable across languages and hosts.

**Files:**

- Create: `schemas/engine-catalog.schema.json`
- Create: `schemas/agent-manifest.schema.json`
- Create: `schemas/handoff.schema.json`
- Create: `schemas/maintenance-result.schema.json`
- Create: `schemas/validation-result.schema.json`
- Create: `schemas/adapter-manifest.schema.json`
- Create: `scripts/validate-contracts.py`
- Create: `tests/fixtures/valid-handoff.yaml`
- Create: `tests/fixtures/invalid-handoff-missing-scope.yaml`
- Create: `tests/fixtures/valid-validation-result.yaml`
- Create: `tests/fixtures/invalid-validation-result.yaml`
- Modify: `catalog/engines.yaml`
- Modify: `scripts/validate-catalog.ps1`
- Modify: `tests/validate_catalog.ps1`

**Interfaces:**

- `validate-contracts.py --schema <path> --instance <path>` returns exit code `0` for valid input and `2` for schema or instance errors.
- Every schema carries a `schema_version` field.
- Verdict enums are exactly `PASS`, `FAIL`, `NOT ASSESSED`, and `PARTIAL` where the contract permits an aggregate result.

### Work items

- [ ] Define required catalog fields: `id`, `repository`, `path`, `router`, and `validators`.
- [ ] Add optional fields: `aliases`, `capabilities`, `fork_discovery`, `validation_platforms`, and `source_of_truth`.
- [ ] Define adapter manifest fields: `id`, `host`, `version`, `core_version`, `entrypoints`, `install_targets`, and `required_capabilities`.
- [ ] Define JSON Schema rejection for unknown verdict values and missing evidence fields.
- [ ] Validate all ten catalog entries against the schema.
- [ ] Add fixture tests for missing fields, invalid verdicts, and invalid repository identifiers.
- [ ] Make the PowerShell catalog test call the Python contract validator and preserve a readable failure message on Windows.
- [ ] Document schema version bump rules: patch for descriptions, minor for additive optional fields, major for required-field or enum changes.

### Acceptance checks

```powershell
python scripts\validate-contracts.py --schema schemas\engine-catalog.schema.json --instance catalog\engines.yaml
python scripts\validate-contracts.py --schema schemas\handoff.schema.json --instance tests\fixtures\valid-handoff.yaml
python scripts\validate-contracts.py --schema schemas\validation-result.schema.json --instance tests\fixtures\valid-validation-result.yaml
.\tests\validate_catalog.ps1
```

Expected result: valid fixtures pass; invalid fixtures fail with nonzero exit codes; the catalog test passes.

### Exit criteria

- A host adapter can validate the same result payload without parsing prose.
- Contract failures identify the field and source file that caused them.

---

## Phase 4: Implement capability negotiation and degraded-mode behavior

**Purpose:** Ensure the agents remain useful when a host or model lacks subagents, shell access, web access, structured output, or MCP.

**Files:**

- Create: `core/capabilities/capability-registry.yaml`
- Create: `core/capabilities/degraded-modes.md`
- Create: `core/instructions/capability-negotiator.md`
- Create: `schemas/capability-profile.schema.json`
- Create: `scripts/detect-capabilities.ps1`
- Create: `scripts/detect-capabilities.py`
- Create: `tests/fixtures/capability-profiles/readonly-generic.yaml`
- Create: `tests/fixtures/capability-profiles/codex-full.yaml`
- Create: `tests/fixtures/capability-profiles/mcp-only.yaml`
- Create: `tests/test_capability_fallbacks.ps1`
- Modify: canonical agent instructions from Phase 2

**Interfaces:**

- `detect-capabilities` returns a capability profile with booleans and a host identifier.
- The capability negotiator consumes that profile and produces an execution mode: `full`, `sequential`, `read_only`, or `not_assessed`.

### Work items

- [ ] Define the minimum profile for routing: `read_files=true` and `structured_output=false` is acceptable if the generic handoff format is used.
- [ ] Define the minimum profile for maintenance: `read_files=true`, `shell=true`, and `git=true`; otherwise maintenance is `NOT ASSESSED`.
- [ ] Define the minimum profile for validation: `read_files=true` and `shell=true`; missing validator dependencies remain `NOT ASSESSED`.
- [ ] Define the fallback when subagents are unavailable: execute independent lanes sequentially and retain the same handoff fields.
- [ ] Define the fallback when web access is unavailable: report current-source checks as `NOT ASSESSED` and do not infer freshness.
- [ ] Define the fallback when write access is unavailable: produce a patch or command plan without applying it.
- [ ] Define the fallback when structured output is unavailable: emit a Markdown table with the same field names.
- [ ] Add shell-independent JSON fixture tests for all fallback decisions.
- [ ] Add explicit user-approval capability to all mutation operations.

### Acceptance checks

```powershell
pwsh -NoProfile -File scripts\detect-capabilities.ps1 -Format Json
pwsh -NoProfile -File tests\test_capability_fallbacks.ps1
git diff --check
```

Expected result: profiles are valid JSON, readonly mode never exposes a pull operation, and all fallback fixtures pass.

### Exit criteria

- A model or host with fewer tools receives a truthful reduced workflow rather than an invented capability.
- No agent assumes that “agent” means “subagent support is available.”

---

## Phase 5: Harden the Codex adapter without changing canonical behavior

**Purpose:** Preserve the existing Codex plugin while making its relationship to the new core explicit and testable.

**Files:**

- Modify: `.codex-plugin/plugin.json`
- Modify: `agents/engine-orchestrator.md`
- Modify: `agents/engine-maintainer.md`
- Modify: `agents/engine-validator.md`
- Create: `adapters/codex/README.md`
- Create: `adapters/codex/adapter.yaml`
- Create: `tests/adapters/test_codex_adapter.ps1`
- Modify: `scripts/install.ps1`
- Modify: `README.md`

**Interfaces:**

- Codex entrypoints preserve the names `engine-orchestrator`, `engine-maintainer`, and `engine-validator`.
- `adapters/codex/adapter.yaml` maps each entrypoint to the canonical instruction ID and required capabilities.

### Work items

- [ ] Keep `.codex-plugin/plugin.json` valid under the installed Codex plugin validator.
- [ ] Add adapter documentation that explains which files are Codex-specific and which files are canonical.
- [ ] Make each Codex agent wrapper reference its canonical instruction ID and output contract.
- [ ] Add a smoke test that checks all three entrypoints exist, have descriptions, and point to real canonical files.
- [ ] Make local installation copy the complete Codex adapter and required core files into the destination.
- [ ] Add a version compatibility check between `plugin.json`, `adapter.yaml`, and the core contract version.
- [ ] Document Codex model-provider configuration as separate from plugin installation.

### Acceptance checks

```powershell
python C:\Users\BIRDC\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .
pwsh -NoProfile -File tests\adapters\test_codex_adapter.ps1
pwsh -NoProfile -File scripts\validate-catalog.ps1
```

Expected result: the Codex validator, adapter smoke test, and catalog validator all pass.

### Exit criteria

- Existing Codex users can continue installing and invoking the plugin.
- Codex behavior is covered by tests that will fail if an adapter file is renamed or detached from the core.

---

## Phase 6: Add the Claude Code adapter

**Purpose:** Package the canonical agents and skills for Claude Code’s project/user discovery conventions without duplicating their logic.

**Files:**

- Create: `adapters/claude-code/README.md`
- Create: `adapters/claude-code/adapter.yaml`
- Create: `adapters/claude-code/CLAUDE.md`
- Create: `adapters/claude-code/agents/engine-orchestrator.md`
- Create: `adapters/claude-code/agents/engine-maintainer.md`
- Create: `adapters/claude-code/agents/engine-validator.md`
- Create: `adapters/claude-code/skills/skills-engine-agents/SKILL.md`
- Create: `tests/adapters/test_claude_code_adapter.ps1`
- Modify: `scripts/install.ps1`
- Modify: `docs/distribution.md`

**Interfaces:**

- Claude adapter entrypoints map to the same canonical instruction IDs as the Codex adapter.
- `CLAUDE.md` contains only discovery and invocation guidance; domain rules remain in the canonical files and engine repositories.

### Work items

- [ ] Recheck the current Claude Code project instruction, subagent, skill, and plugin discovery rules from official Anthropic documentation before writing adapter files.
- [ ] Create the Claude project instruction that tells the host to inspect the current Git root and load the matching canonical agent.
- [ ] Create three thin Claude agent wrappers with the same output contracts as the Codex wrappers.
- [ ] Create a Claude skill entry that points to the engine catalog and capability negotiation flow.
- [ ] Define the Claude adapter’s install targets for project-local and user-level installation.
- [ ] Ensure the adapter never assumes an Anthropic model; model selection remains host configuration.
- [ ] Add a fixture for Claude Code running with a DeepSeek-compatible endpoint where the host exposes shell and file tools.
- [ ] Add a fixture for Claude Code running without shell access; expected verdict is `NOT ASSESSED` for maintenance and validation.
- [ ] Document user approval requirements for pull operations.

### Acceptance checks

```powershell
pwsh -NoProfile -File tests\adapters\test_claude_code_adapter.ps1
python scripts\validate-contracts.py --schema schemas\adapter-manifest.schema.json --instance adapters\claude-code\adapter.yaml
rg -n "engine-orchestrator|engine-maintainer|engine-validator|NOT ASSESSED" adapters\claude-code
```

Expected result: all Claude adapter files map to real canonical IDs and the manifest validates.

### Exit criteria

- A Claude Code user can install the adapter into a project and receive the same routing, maintenance, and validation contract as a Codex user.
- The adapter’s model-provider instructions are optional and do not alter the core behavior.

---

## Phase 7: Add Gemini CLI, OpenCode, and generic adapters

**Purpose:** Support hosts that use project instruction files, commands, or skill directories without pretending that all hosts share one plugin manifest.

**Files:**

- Create: `adapters/gemini-cli/README.md`
- Create: `adapters/gemini-cli/adapter.yaml`
- Create: `adapters/gemini-cli/project-instructions.md`
- Create: `adapters/gemini-cli/commands/engine-orchestrator.md`
- Create: `adapters/gemini-cli/commands/engine-maintainer.md`
- Create: `adapters/gemini-cli/commands/engine-validator.md`
- Create: `adapters/opencode/README.md`
- Create: `adapters/opencode/adapter.yaml`
- Create: `adapters/opencode/AGENTS.md`
- Create: `adapters/opencode/skills/skills-engine-agents/SKILL.md`
- Create: `adapters/generic/README.md`
- Create: `adapters/generic/engine-orchestrator.prompt.md`
- Create: `adapters/generic/engine-maintainer.prompt.md`
- Create: `adapters/generic/engine-validator.prompt.md`
- Create: `tests/adapters/test_generic_adapters.ps1`
- Modify: `scripts/install.ps1`
- Modify: `README.md`

**Interfaces:**

- Every adapter manifest identifies the host, discovery file, entrypoints, install targets, and capability requirements.
- Generic prompt files use the canonical handoff and verdict fields and do not require a plugin marketplace.

### Work items

- [ ] Confirm current Gemini CLI and OpenCode project instruction/command/skill conventions from their maintained documentation before implementing adapter paths.
- [ ] Implement Gemini command wrappers with provider-neutral language.
- [ ] Implement OpenCode project instructions and skill wrapper using the same canonical IDs.
- [ ] Implement generic prompt files that can be pasted into any model host with repository access.
- [ ] Add a command-line invocation example for each generic operation using PowerShell and Python.
- [ ] Add a “host not catalogued” mode that still permits inspection of a repository but refuses to invent engine-specific validators.
- [ ] Define adapter support status as `adapter` until each host has an installation smoke test.
- [ ] Add tests for missing host-specific directories and safe fallback to generic prompts.

### Acceptance checks

```powershell
pwsh -NoProfile -File tests\adapters\test_generic_adapters.ps1
Get-ChildItem adapters -Recurse -File | Where-Object { $_.Extension -in '.md','.yaml' } | Measure-Object
python scripts\validate-contracts.py --schema schemas\adapter-manifest.schema.json --instance adapters\gemini-cli\adapter.yaml
python scripts\validate-contracts.py --schema schemas\adapter-manifest.schema.json --instance adapters\opencode\adapter.yaml
```

Expected result: each adapter has a readable entrypoint, a valid manifest, and a generic fallback path.

### Exit criteria

- Users of supported non-Codex hosts have a documented local installation path.
- Unsupported hosts receive a useful generic workflow instead of a false compatibility claim.

---

## Phase 8: Build the optional MCP tool server

**Purpose:** Provide one typed tool surface that any MCP-capable host can use, independent of the model provider.

**Files:**

- Create: `mcp-server/package.json`
- Create: `mcp-server/tsconfig.json`
- Create: `mcp-server/src/index.ts`
- Create: `mcp-server/src/contracts.ts`
- Create: `mcp-server/src/engine-discovery.ts`
- Create: `mcp-server/src/engine-validation.ts`
- Create: `mcp-server/src/engine-maintenance.ts`
- Create: `mcp-server/src/safety.ts`
- Create: `mcp-server/README.md`
- Create: `mcp-server/tests/contracts.test.ts`
- Create: `mcp-server/tests/safety.test.ts`
- Create: `mcp-server/tests/discovery.test.ts`
- Create: `.mcp.json.example`
- Modify: `README.md`
- Modify: `docs/distribution.md`

**Interfaces:**

- `discover_engine(path)` returns `engine_identity`.
- `inspect_engine(path)` returns read-only Git and router information.
- `validate_engine(path, scope)` returns `validation_result`.
- `pull_engine_ff_only(path, confirmation_token)` returns `maintenance_result` and refuses absent or invalid confirmation.
- No MCP tool accepts a raw shell command from the model.

### Work items

- [ ] Pin the MCP SDK version in `mcp-server/package.json` after verifying the current official package and supported Node version.
- [ ] Implement typed tool schemas with bounded string, path, and enum inputs.
- [ ] Resolve repository paths through a validated Git-root discovery function.
- [ ] Restrict all paths to an explicitly supplied workspace root or a repository root returned by Git.
- [ ] Implement `discover_engine` by calling the existing catalog logic through a shared contract rather than reimplementing catalog parsing in the server.
- [ ] Implement validation as a subprocess with a fixed allowlist of catalogued validator commands.
- [ ] Implement maintenance with an explicit confirmation token generated by the host after user approval.
- [ ] Reject dirty, diverged, non-fast-forward, and unrecognised repositories without attempting a reset, merge, delete, or force-push.
- [ ] Return structured error objects with `code`, `message`, and `remediation` fields.
- [ ] Add a local stdio configuration example; do not include secrets or production URLs.
- [ ] Document that MCP standardizes tool connection, not model quality or host permissions.

### Acceptance checks

```powershell
Push-Location mcp-server
npm ci
npm test
npm run build
Pop-Location
```

Expected result: TypeScript compilation and all MCP unit tests pass. If Node or the SDK is unavailable, record `NOT ASSESSED` in the phase evidence rather than treating the phase as passed.

### Exit criteria

- An MCP-capable host can discover and validate an engine through typed tools.
- Pull remains approval-gated and fast-forward-only at the tool boundary.

---

## Phase 9: Implement host-aware installation, updates, and fork discovery

**Purpose:** Give users one predictable installer while allowing a forked engine or forked plugin repository to work from its own checkout.

**Files:**

- Create: `scripts/install.ps1`
- Create: `scripts/install.sh`
- Create: `scripts/update.ps1`
- Create: `scripts/update.sh`
- Create: `scripts/uninstall.ps1`
- Create: `scripts/uninstall.sh`
- Create: `scripts/resolve-install-target.py`
- Create: `tests/install/test_install_targets.ps1`
- Create: `tests/install/test_fork_discovery.ps1`
- Create: `tests/install/fixtures/forked-engine/AGENTS.md`
- Create: `tests/install/fixtures/forked-engine/.git/config.fixture`
- Modify: existing install and discovery scripts
- Modify: `docs/distribution.md`

**Interfaces:**

- PowerShell: `install.ps1 -Host codex|claude-code|gemini-cli|opencode|generic|mcp -Destination <path> [-Force]`.
- POSIX shell: `install.sh --host <host> --destination <path> [--force]`.
- Update: only replaces files owned by the installer and preserves user-created files outside the managed manifest.
- Uninstall: removes only files recorded in the installation manifest and refuses an untracked target.
- Discovery: resolves current Git root, origin repository name, folder name, and local router without a hardcoded machine path.

### Work items

- [ ] Define a managed installation manifest at `<destination>/.skills-engine-agents-install.json`.
- [ ] Record source commit, adapter ID, installed files, destination, and installation timestamp.
- [ ] Add explicit `-Force`/`--force` behavior for replacing an existing managed installation.
- [ ] Refuse to overwrite an unmanaged directory unless the user explicitly supplies `-Force` and the destination contains no non-managed files.
- [ ] Use copy operations rather than Windows symlinks so installations work on machines without developer-mode symlink permissions.
- [ ] Make updates atomic by staging into a temporary sibling directory and moving only after validation.
- [ ] Add shell and PowerShell parity tests for destination resolution and manifest generation.
- [ ] Add a fork fixture whose origin repository name is not one of the ten catalogued names; expected result is safe inspection with no invented validator.
- [ ] Document how a forked engine inherits the plugin without requiring `C:\\wamp64\\www`.
- [ ] Document user-level versus project-level installation for each adapter.

### Acceptance checks

```powershell
pwsh -NoProfile -File tests\install\test_install_targets.ps1
pwsh -NoProfile -File tests\install\test_fork_discovery.ps1
pwsh -NoProfile -File scripts\install.ps1 -Host generic -Destination "$env:TEMP\skills-engine-agents-test"
```

Expected result: installation is reproducible, managed files are listed, fork discovery does not assume the catalogue, and unmanaged files are not removed.

### Exit criteria

- A user can install a host adapter without cloning the engine repositories into a fixed global directory.
- A forked engine works from its checkout and is clearly marked as uncatalogued when no validator is defined.

---

## Phase 10: Apply security, permission, and supply-chain controls

**Purpose:** Prevent the universal package from becoming a broad shell-execution or repository-destruction channel.

**Files:**

- Create: `docs/security/threat-model.md`
- Create: `docs/security/permission-model.md`
- Create: `docs/security/supply-chain-policy.md`
- Create: `schemas/approval-token.schema.json`
- Create: `scripts/audit-managed-files.ps1`
- Create: `tests/security/test_path_boundaries.ps1`
- Create: `tests/security/test_mutation_gates.ps1`
- Create: `tests/security/test_command_allowlist.ps1`
- Modify: `agents/engine-maintainer.md`
- Modify: canonical safety policy
- Modify: `.gitignore`

**Interfaces:**

- Every mutating operation has `requested_by`, `approved`, `target_repo`, `target_branch`, `operation`, and `confirmation_id`.
- Every command is either a catalogued validator or a fixed internal command; model-supplied command strings are rejected.
- Every path is resolved and checked before file or Git mutation.

### Work items

- [ ] Threat-model prompt injection from engine files, malicious fork routers, malformed catalog entries, and hostile Git remotes.
- [ ] Threat-model path traversal, junctions, symlinks, nested repositories, and temporary-directory replacement attacks.
- [ ] Threat-model malicious validator commands and dependency installation scripts.
- [ ] Define read-only, approved-write, and blocked operations.
- [ ] Require explicit confirmation for pull, install overwrite, update, uninstall, and MCP server execution that can write.
- [ ] Keep `git reset`, `git clean`, manual merge, force-push, recursive delete, and broad path deletion on the denylist.
- [ ] Add checks that the target branch is `main` for this project’s own publishing workflow.
- [ ] Pin Node/Python dependencies and add an audit command to CI.
- [ ] Add secret scanning to CI and document that API keys belong in host configuration.
- [ ] Add tests proving a path outside the approved root is rejected before any command starts.

### Acceptance checks

```powershell
pwsh -NoProfile -File tests\security\test_path_boundaries.ps1
pwsh -NoProfile -File tests\security\test_mutation_gates.ps1
pwsh -NoProfile -File tests\security\test_command_allowlist.ps1
git diff --check
```

Expected result: all denied operations are rejected with no filesystem or Git side effect.

### Exit criteria

- The package has an explicit threat model and permission model.
- The optional MCP layer cannot turn model text into arbitrary shell commands.

---

## Phase 11: Build the cross-host and cross-model evaluation suite

**Purpose:** Verify that adapters preserve behavior across hosts and expose honest limits across models.

**Files:**

- Create: `evals/README.md`
- Create: `evals/contracts/routing.yaml`
- Create: `evals/contracts/maintenance.yaml`
- Create: `evals/contracts/validation.yaml`
- Create: `evals/contracts/fork-discovery.yaml`
- Create: `evals/cases/001-route-srs.yaml`
- Create: `evals/cases/002-add-finance-cross-cutting.yaml`
- Create: `evals/cases/003-skip-dirty-pull.yaml`
- Create: `evals/cases/004-block-divergence.yaml`
- Create: `evals/cases/005-report-unavailable-validator.yaml`
- Create: `evals/cases/006-discover-fork.yaml`
- Create: `evals/cases/007-reject-prompt-injected-validator.yaml`
- Create: `evals/runners/run-contract-evals.py`
- Create: `evals/runners/run-host-smoke-tests.ps1`
- Create: `evals/reports/template.md`
- Create: `.github/workflows/validate.yml`
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`

**Interfaces:**

- Each eval case contains `id`, `input`, `required_observations`, `forbidden_actions`, and `expected_verdict`.
- The contract runner returns a machine-readable report with host, model label, adapter version, case ID, status, and evidence.
- Model labels are configuration values; the tests do not hardcode API keys or require a single provider.

### Work items

- [ ] Create at least 20 cases: ten routing cases, four maintenance cases, four validation cases, and two hostile-input cases.
- [ ] Include finance plus design plus research cross-cutting routing because those engines are additive and should not replace the domain engine.
- [ ] Include a dirty repository, diverged branch, missing dependency, forked repository, unknown repository, and malformed router fixture.
- [ ] Add deterministic tests for output shape and forbidden actions.
- [ ] Add host smoke tests that install each adapter into a temporary directory and inspect the managed manifest.
- [ ] Add model-provider runs as optional jobs; a provider outage must produce `NOT ASSESSED`, not a failed package build.
- [ ] Set release thresholds: 100% contract-shape pass, 100% forbidden-action pass, 100% safety-gate pass, and no unqualified `PASS` for missing evidence.
- [ ] Record latency and token cost only when the host exposes them; otherwise mark those fields unavailable.
- [ ] Add a regression report template that names the host, model, prompt/core version, adapter version, and failed case.
- [ ] Run the suite before and after every canonical instruction change.

### Acceptance checks

```powershell
python evals\runners\run-contract-evals.py --cases evals\cases --out evals\reports\latest.json
pwsh -NoProfile -File evals\runners\run-host-smoke-tests.ps1
```

Expected result: all deterministic cases pass; optional model runs are separately labelled `PASS`, `FAIL`, or `NOT ASSESSED` with evidence.

### Exit criteria

- A host adapter change cannot ship without proving it preserves routing, safety, and verdict contracts.
- Model differences are measured as evidence, not hidden behind a universal marketing claim.

---

## Phase 12: Documentation, release packaging, rollout, and maintenance

**Purpose:** Publish a package that users can understand, install, verify, update, and report against without knowing the internal architecture.

**Files:**

- Create: `docs/adapters/codex.md`
- Create: `docs/adapters/claude-code.md`
- Create: `docs/adapters/gemini-cli.md`
- Create: `docs/adapters/opencode.md`
- Create: `docs/adapters/generic.md`
- Create: `docs/adapters/mcp.md`
- Create: `docs/operations/upgrade-policy.md`
- Create: `docs/operations/incident-runbook.md`
- Create: `docs/operations/compatibility-report-template.md`
- Create: `CHANGELOG.md`
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `docs/distribution.md`
- Modify: `.codex-plugin/plugin.json`
- Modify: `.github/workflows/validate.yml`

**Interfaces:**

- README installation paths must link to each adapter document.
- Release metadata includes `core_version`, adapter versions, schema versions, supported hosts, and assessed model-provider configurations.
- Issue reports require host, model, adapter version, core version, operating system, capability profile, reproduction case, and evidence.

### Work items

- [ ] Rewrite the README opening so it states exactly what the package installs and what it does not install.
- [ ] Add an adapter table linking Codex, Claude Code, Gemini CLI, OpenCode, generic, and MCP instructions.
- [ ] Add separate installation examples for Windows PowerShell and POSIX shells.
- [ ] Add model-provider guidance that explains selecting DeepSeek or another provider is a host configuration step.
- [ ] Add a fork workflow with commands for cloning a fork, installing the adapter, opening the host in the fork checkout, and checking discovery output.
- [ ] Add an upgrade policy that separates core contract changes from adapter changes and schema changes.
- [ ] Add an incident runbook for bad validator commands, unsafe path detection, adapter drift, and provider incompatibility.
- [ ] Add a compatibility report template generated from the eval runner.
- [ ] Add a release checklist requiring plugin validation, catalog validation, contract tests, security tests, adapter smoke tests, evals, `git diff --check`, and a clean working tree.
- [ ] Update `CHANGELOG.md` with the first multi-host release entry and explicit breaking-change notes if any install path changed.
- [ ] Run the final anti-slop review: remove generic claims, verify every named host and URL, retain concrete commands, and keep all limitations visible.
- [ ] Commit the completed implementation in focused commits on `main`; push only after the full release checklist passes.

### Acceptance checks

```powershell
python C:\Users\BIRDC\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .
pwsh -NoProfile -File scripts\validate-catalog.ps1
pwsh -NoProfile -File tests\validate_catalog.ps1
python scripts\validate-contracts.py --schema schemas\adapter-manifest.schema.json --instance adapters\codex\adapter.yaml
pwsh -NoProfile -File tests\security\test_path_boundaries.ps1
pwsh -NoProfile -File evals\runners\run-host-smoke-tests.ps1
git diff --check
git status --short --branch
```

Expected result: all available checks pass; unavailable host or provider checks are listed as `NOT ASSESSED` with the missing dependency named; the final working tree is clean after commit.

### Exit criteria

- Users can choose a supported host adapter without confusing model selection with plugin installation.
- The package has a documented generic fallback and an optional MCP route.
- A release can be reproduced from the repository and audited from its evidence report.

---

## Dependency order and parallel work

The phases are ordered by dependency:

```text
Phase 1 compatibility contract
        |
Phase 2 canonical core ---- Phase 3 schemas
        |                         |
        +----------- Phase 4 capability negotiation
                              |
          +-------------------+-------------------+
          |                   |                   |
      Phase 5 Codex      Phase 6 Claude       Phase 7 other hosts
          |                   |                   |
          +-------------------+-------------------+
                              |
                     Phase 8 MCP server
                              |
                  Phase 9 installer and forks
                              |
                    Phase 10 security gates
                              |
                   Phase 11 evaluation suite
                              |
                 Phase 12 release and operations
                              |
                Phase 13 engine integration and publication
```

Phases 5, 6, and 7 may be implemented in parallel after Phases 2–4, provided they consume the same canonical IDs and schemas. Phases 8 and 9 may proceed in parallel after the core contracts are stable. Phase 10 must review all mutation paths before Phase 11’s release gates are finalised.

## Release gate summary

The implementation is ready for a multi-host release only when all of the following are evidenced:

- The ten-engine catalog validates.
- Canonical instructions contain no host- or provider-specific commands.
- Codex, Claude Code, Gemini CLI, OpenCode, generic, and MCP adapter manifests validate where implemented.
- Installation and update tests preserve unmanaged files and reject unsafe targets.
- Pull operations remain explicit, fast-forward-only, and blocked for dirty or diverged repositories.
- Validator gaps remain `NOT ASSESSED`.
- Security tests reject arbitrary model-supplied shell commands and out-of-bound paths.
- Deterministic evals meet the four release thresholds in Phase 11.
- Optional model-provider runs are reported with host, model, adapter, core version, and evidence.
- README, adapter guides, distribution notes, changelog, and incident runbook agree with the actual package.
- All ten engine repositories publish `.skills-engine/engine-manifest.yaml` and pass their engine-specific integration tests, or are explicitly recorded as `NOT ASSESSED`.
- The public release contains the source archive, checksums, release manifest, adapter documentation, and MCP package metadata.
- Each developer installation path identifies its host, adapter version, core version, and supported engine contract version.
- `git diff --check` is clean and the final commit is pushed to `main`.

## Known non-goals

- The package will not make every model equally capable of routing, tool use, or long-context work.
- The package will not install itself inside a model provider that has no host-side extension mechanism.
- The package will not copy the ten engines into this repository.
- The package will not run arbitrary validators supplied by an engine repository or model prompt.
- The package will not force a single provider, gateway, API key, or model name on users.
- The package will not treat a successful text response as proof that a repository mutation occurred.

---

## Phase 13: Adjust all ten engines for agent/MCP expectations and publish the developer distribution

**Purpose:** Make every skills engine explicitly consumable by the coordination agents and optional MCP server, while keeping each engine independently usable and giving other developers clear, reproducible installation paths.

This phase changes the ten engine repositories as coordinated downstream work. The repositories remain separate. The changes below add a small integration contract to each engine; they do not copy the universal agents or make any engine depend on the `skills-engine-agents` repository at runtime.

### Shared engine integration contract

Every engine repository must expose the following repository-local contract:

```yaml
engine_id: string
display_name: string
contract_version: "1.0"
router:
  path: string
  required: true
skills:
  discovery_glob: string
  frontmatter_description_required: true
validation:
  commands:
    - id: string
      command: string
      working_directory: string
      platform: windows|posix|both
      read_only: true
      required_dependencies: []
      release_gate: true|false
agent_integration:
  supported_modes: [read, validate, maintain, write_with_approval]
  local_context_files: []
  mcp_safe_tools: []
  approval_required_for: []
  forbidden_operations: []
  fork_behavior: inspect|catalogue_after_registration|reject
source_of_truth:
  router: string
  skills: string
  references: string
```

The contract must be stored at `.skills-engine/engine-manifest.yaml` in each engine repository. The file is a declaration, not executable code. The universal catalog may read it, but the engine remains valid when the plugin is absent.

### Shared files and tests for all ten engines

Each engine repository receives the following files or equivalent updates:

- Create: `.skills-engine/engine-manifest.yaml`
- Create: `.skills-engine/AGENTS-INTEGRATION.md`
- Create: `tests/agent-integration/validate_manifest.py` or the engine’s native equivalent
- Create: `tests/agent-integration/fixtures/readonly-profile.yaml`
- Create: `tests/agent-integration/fixtures/approval-required-profile.yaml`
- Modify: root `AGENTS.md`, `README.md`, or `CLAUDE.md`, whichever is the engine’s canonical router, to include a short integration section
- Modify: the engine’s existing validation baseline to include the new manifest and integration test
- Modify: the engine’s release documentation to state whether the MCP server is optional or required

The shared integration section must say, in substance:

```markdown
## Skills Engine Agents integration

This repository remains independently usable. The optional `skills-engine-agents`
coordination package may read this engine's router, discover the documented
skills, run the declared release checks, and report missing evidence as
`NOT ASSESSED`. It must not invent validators, copy domain instructions, or
perform writes without explicit user approval.

The machine-readable integration contract is `.skills-engine/engine-manifest.yaml`.
The engine's router and `SKILL.md` files remain authoritative for domain behavior.
```

### Engine-by-engine adjustment matrix

#### 13.1 `srs-skills`

**Repository:** `C:\\wamp64\\www\\srs-skills`

**Files:**

- Modify: `AGENTS.md` to expose the SRS router and requirements-document boundaries.
- Create: `.skills-engine/engine-manifest.yaml` with SRS, PRD, architecture, testing, governance, and compliance skill discovery.
- Modify: existing quality baseline to declare structural validation and routing smoke tests as release gates.
- Create: `tests/agent-integration/test_srs_agent_contract.py`.

**Contract decisions:**

- Agent mode may read requirements, references, templates, and validation results.
- Write mode requires approval before changing requirements, architecture, or compliance artifacts.
- MCP-safe tools are `discover_skills`, `read_router`, `read_skill`, and `run_documented_validator`.
- The engine must reject fabricated standards, citations, or acceptance criteria and report missing source material.

**Acceptance evidence:**

- A routing fixture selects the SRS engine for “write a software requirements specification.”
- A cross-cutting fixture adds digital research when current standards or regulations are requested.
- A write fixture proves no document is changed without approval.

#### 13.2 `business-plan-skills`

**Repository:** `C:\\wamp64\\www\\business-plan-skills`

**Files:**

- Modify: `AGENTS.md` to declare business-planning scope and cross-cutting finance routing.
- Create: `.skills-engine/engine-manifest.yaml` with business-plan, market strategy, demand, forecasting, and investor-planning discovery.
- Modify: validation baseline to include source freshness and financial-model checks where already documented.
- Create: `tests/agent-integration/test_business_plan_agent_contract.py`.

**Contract decisions:**

- Agent mode may read business context and templates but must label assumptions separately from sourced facts.
- Finance/accounting work must add `chwezi-accounting-doctrine`; the business-plan engine does not replace that cross-cutting engine.
- MCP-safe tools are read-only discovery, template inspection, and documented validation.
- Financial writes, model overwrites, and publication actions require approval and an audit record.

**Acceptance evidence:**

- A routing fixture selects business-plan skills for a market-entry plan.
- A finance fixture selects both business-plan and accounting doctrine.
- A missing market source is reported as an evidence gap, not filled from model memory.

#### 13.3 `website-skills`

**Repository:** `C:\\wamp64\\www\\website-skills`

**Files:**

- Modify: `AGENTS.md` to define website project discovery, static starters, UX, performance, and deployment boundaries.
- Create: `.skills-engine/engine-manifest.yaml` with web skill discovery and website-specific validators.
- Modify: fixture benchmark registration to expose its documented command to the universal validator.
- Create: `tests/agent-integration/test_website_agent_contract.py`.

**Contract decisions:**

- Agent mode may inspect project structure, content, assets, and performance fixtures.
- Design and visual formatting tasks must also activate `design-system-skills`.
- Deployment, hosting, domain, DNS, and production configuration changes require approval.
- MCP-safe tools are project discovery, static validation, fixture benchmarking, and read-only audit reporting.

**Acceptance evidence:**

- A routing fixture selects website skills for a landing page request.
- A design fixture adds the design engine.
- A production-deploy fixture produces an approval request instead of executing deployment.

#### 13.4 `social-media-skills`

**Repository:** `C:\\wamp64\\www\\social-media-skills`

**Files:**

- Modify: `AGENTS.md` to define content-only social strategy and platform workflow scope.
- Create: `.skills-engine/engine-manifest.yaml` with content calendar, campaign, audience, and platform-specific skill discovery.
- Modify: source-freshness and routing validators to expose their documented commands.
- Create: `tests/agent-integration/test_social_media_agent_contract.py`.

**Contract decisions:**

- Agent mode may draft content and schedules but must not publish to a social platform without explicit approval and a target/account confirmation.
- Current platform rules, features, and audience facts require digital research verification when they affect a recommendation.
- MCP-safe tools are read-only content inspection, calendar validation, and source checks.
- Credentials and account tokens remain in the publishing host, never in the engine or plugin repository.

**Acceptance evidence:**

- A content-calendar fixture selects social-media skills.
- A current platform-policy fixture adds digital research.
- A publish fixture stops at a reviewable draft and records the required approval.

#### 13.5 `linux-skills`

**Repository:** `C:\\wamp64\\www\\linux-skills`

**Files:**

- Modify: `AGENTS.md` to define Linux administration, provisioning, hardening, and incident boundaries.
- Create: `.skills-engine/engine-manifest.yaml` with distro matrix and shell-validation metadata.
- Modify: existing validator registry to mark commands requiring a Linux environment.
- Create: `tests/agent-integration/test_linux_agent_contract.py`.

**Contract decisions:**

- Agent mode may inspect configuration, logs, and documented runbooks.
- Commands that change packages, services, firewall rules, DNS, filesystems, credentials, or permissions require explicit approval and a target host.
- The universal MCP layer must not expose unrestricted shell execution; it may expose named, allowlisted diagnostics.
- Windows hosts report Linux-only validation as `NOT ASSESSED` unless WSL or a declared remote target is available.

**Acceptance evidence:**

- A Linux hardening fixture selects Linux skills and requires an execution target.
- A package-install fixture is blocked without approval.
- A Windows-only fixture reports the distro matrix check as `NOT ASSESSED`.

#### 13.6 `proposal-skills`

**Repository:** `C:\\wamp64\\www\\proposal-skills`

**Files:**

- Modify: `AGENTS.md` to define RFP/RFQ, tender, bid, grant, and compliance-matrix scope.
- Create: `.skills-engine/engine-manifest.yaml` with proposal workflow and evidence requirements.
- Modify: proposal validation documentation to expose `git diff --check` and any documented structural checks.
- Create: `tests/agent-integration/test_proposal_agent_contract.py`.

**Contract decisions:**

- Agent mode may inspect solicitation documents, templates, compliance matrices, and source registers.
- The proposal engine must require digital research verification for current donor, procurement, legal, or market claims.
- MCP-safe tools are document discovery, requirement extraction, matrix validation, and draft evidence reporting.
- Submission, email delivery, signature, and external portal actions require approval and a final human review.

**Acceptance evidence:**

- An RFP fixture selects proposal skills.
- A current procurement-rule fixture adds digital research.
- A submission fixture creates a review packet and never sends externally.

#### 13.7 `skills-web-dev`

**Repository:** `C:\\wamp64\\www\\skills-web-dev`

**Files:**

- Modify: `SKILL.md` and the canonical router to declare the agent/MCP integration contract.
- Create: `.skills-engine/engine-manifest.yaml` with AI systems, engineering, security, product, and documentation skill families.
- Modify: control-plane, routing-smoke, anti-slop, and evidence-pack gates to be machine-discoverable.
- Create: `tests/agent-integration/test_skills_web_dev_agent_contract.py`.

**Contract decisions:**

- This engine owns the general engineering and AI-system routing contract, but it does not own Codex, Claude, Gemini, or DeepSeek provider configuration.
- Agent mode must load only the smallest relevant `SKILL.md` set after routing.
- MCP-safe tools are catalog discovery, skill inspection, deterministic validation, and evidence-pack generation.
- Code changes, dependency installation, deployment, and external messages require approval.

**Acceptance evidence:**

- An AI-agent architecture fixture selects the AI skill family.
- A documentation artifact fixture runs the evidence-pack and anti-slop gates.
- A provider-integration fixture marks provider-specific assumptions as requiring current-source verification.

#### 13.8 `chwezi-accounting-doctrine`

**Repository:** `C:\\wamp64\\www\\chwezi-accounting-doctrine`

**Files:**

- Modify: `README.md` to declare accounting/IFRS/tax scope and additive cross-cutting use.
- Create: `.skills-engine/engine-manifest.yaml` with doctrine router, finance skill discovery, and strict validation metadata.
- Modify: `tools\\validate-doctrine.ps1` documentation so the universal validator can call it without guessing parameters.
- Create: `tests/agent-integration/test_accounting_agent_contract.ps1`.

**Contract decisions:**

- Agent mode may inspect doctrine, accounting source material, and financial workpapers.
- Statutory, tax, IFRS, and accounting claims require current-source verification and explicit jurisdiction/date context.
- MCP-safe tools are doctrine discovery, source inspection, and strict validation.
- Posting entries, changing ledgers, filing returns, approving close outputs, and changing controls require approval and an audit trail.

**Acceptance evidence:**

- A financial-model fixture adds accounting doctrine alongside business-plan skills.
- A tax fixture requires jurisdiction and period before routing.
- A ledger-write fixture is blocked by the approval gate.

#### 13.9 `design-system-skills`

**Repository:** `C:\\wamp64\\www\\design-system-skills`

**Files:**

- Modify: `AGENTS.md` and `doctrine/design-doctrine.md` to document agent-readable design constraints and cross-cutting activation.
- Create: `.skills-engine/engine-manifest.yaml` with design, typography, UI/UX, visual formatting, and document-rendering skill discovery.
- Modify: design validation commands to expose the anti-slop font rule and visual QA requirements.
- Create: `tests/agent-integration/test_design_agent_contract.ps1`.

**Contract decisions:**

- Agent mode may inspect design doctrine, assets, tokens, and rendered evidence.
- The design engine must remain additive to the active domain engine.
- Visual artifacts must declare typeface, colour, layout, and state decisions before generation; banned primary fonts remain rejected.
- MCP-safe tools are doctrine discovery, asset metadata inspection, rendering, and visual evidence collection. Asset replacement and publication require approval.

**Acceptance evidence:**

- A dashboard fixture selects the domain engine plus design system skills.
- A document-rendering fixture reports visual evidence requirements.
- A banned-font fixture fails the design gate with a named file and line.

#### 13.10 `digital-research-skills`

**Repository:** `C:\\wamp64\\www\\digital-research-skills`

**Files:**

- Modify: `AGENTS.md` to expose source-evaluation, source-verification, research orchestration, and evidence-discipline requirements.
- Create: `.skills-engine/engine-manifest.yaml` with research skill discovery, source registry requirements, and verification commands.
- Modify: source verification and currentness validators to expose documented commands and required fixtures.
- Create: `tests/agent-integration/test_digital_research_agent_contract.py`.

**Contract decisions:**

- Agent mode may discover, evaluate, verify, and report sources within the authorised scope.
- The engine’s no-hallucination guardrail is inherited by every research subtask and every cross-cutting current-fact route.
- MCP-safe tools are source discovery, source evaluation, URL verification, claim-support inspection, and evidence-report generation.
- Source publication, external contact, archive writes, or edits to evidence registries require approval.

**Acceptance evidence:**

- A current standards-check fixture adds digital research.
- An unsupported claim fixture remains unresolved and cannot receive `PASS`.
- A source-verification fixture reports URL, source, claim, confidence, and access-date evidence.

### Engine release and publication workflow

Each engine adjustment follows this sequence in its own repository:

1. Add `.skills-engine/engine-manifest.yaml` and the integration note.
2. Add the engine-specific integration fixtures and validator.
3. Run the engine’s existing release checks unchanged.
4. Run the new agent integration test.
5. Run the universal catalog validator against the checkout.
6. Commit the engine change to that engine’s `main` branch with a scoped message such as `feat: expose agent integration contract`.
7. Push the engine repository’s `main` branch.
8. Create a release tag only after the engine’s own maintainers approve the change; use the engine’s existing versioning policy.
9. Update `skills-engine-agents/catalog/engines.yaml` with the released contract version and validator metadata.
10. Run the universal adapter and evaluation suite against the released engine commit.

The plugin must not silently depend on unpublished engine changes. During rollout, the catalog records `integration_status: pending`, `available`, or `not_assessed` for each engine. The universal agents continue to work with older engines through the existing router and validator fields, but they report missing integration metadata as `NOT ASSESSED`.

### Developer publication channels

Publish the tools through separate channels with one source of truth:

| Channel | Published artifact | Developer experience | Authority |
|---|---|---|---|
| GitHub | `skills-engine-agents` source, tags, release notes | Clone or download a release archive | Repository `main` and signed release tag |
| Codex plugin directory | Validated Codex plugin package | Search and install from Codex when directory approval exists | Codex manifest and directory policy |
| Claude Code distribution | Claude adapter directory or supported marketplace entry | Install the adapter into a project or user scope | Claude adapter manifest and host documentation |
| Gemini/OpenCode | Host-specific adapter files and installer | Copy/install adapter into the host’s project scope | Adapter manifest and host documentation |
| Generic CLI | PowerShell, POSIX, and Python installer paths | `install.ps1`, `install.sh`, or Python package entrypoint | Tagged GitHub release |
| MCP | Versioned MCP package, stdio configuration, and source | Install the MCP package and register it with an MCP-capable host | `mcp-server` package version and lockfile |

### Recommended public package names and commands

Use names that make the separation visible:

```text
GitHub:  github.com/peterbamuhigire/skills-engine-agents
MCP:     @peterbamuhigire/skills-engine-agents-mcp
Python:  skills-engine-agents-cli
```

The package names must be checked for availability before publication. The plan does not assume that either registry name is currently unclaimed.

The public quick starts should include these concrete flows:

```powershell
# Windows generic or Codex adapter
irm https://raw.githubusercontent.com/peterbamuhigire/skills-engine-agents/main/scripts/install.ps1 | iex

# Clone a forked engine and use the installed adapter from that checkout
$forkUrl = Read-Host 'Enter the HTTPS URL of the engine fork'
$forkPath = Join-Path $env:TEMP 'skills-engine-fork-checkout'
git clone $forkUrl $forkPath
Set-Location $forkPath
skills-engine-agents discover
```

The final release documentation must warn users to inspect downloaded scripts before piping them to a shell and must provide the safer cloned-release command for security-conscious teams.

### Publication CI and provenance

**Files in the plugin repository:**

- Create: `.github/workflows/release.yml`
- Create: `.github/workflows/adapter-smoke-tests.yml`
- Create: `release/manifest.json`
- Create: `release/checksums.txt`
- Create: `release/NOTICE.txt`
- Modify: `.github/workflows/validate.yml`
- Modify: `CONTRIBUTING.md`

**Required release checks:**

- Validate the Codex plugin manifest.
- Validate every adapter manifest and every engine catalog entry.
- Run deterministic contract, security, install, fork, and host smoke tests.
- Build the MCP package with a locked dependency tree.
- Produce a release archive containing the canonical core, adapters, scripts, schemas, and documentation.
- Generate SHA-256 checksums for the release archive and MCP package tarball.
- Include the source commit, core schema version, adapter versions, and assessed engine integration commits in `release/manifest.json`.
- Upload artifacts only from a protected `main` tag or approved release workflow.
- Never publish API keys, local paths, private engine contents, or generated evidence containing credentials.

### Developer installation documentation

Every adapter guide must contain:

- prerequisites and supported operating systems;
- install command and destination;
- update command;
- uninstall command;
- how to confirm the adapter is loaded;
- how to run a read-only discovery check;
- how to run validation;
- how to request a pull safely;
- how to configure an alternative model provider in the host, without changing the plugin;
- fork behavior and the expected `NOT ASSESSED` result for an uncatalogued engine;
- troubleshooting for missing shell, missing Git, missing validator dependencies, and denied permissions;
- a link to the compatibility report template.

### Acceptance checks

Run from `skills-engine-agents` after all ten engine repositories have published their integration contract:

```powershell
python scripts\validate-contracts.py --schema schemas\engine-catalog.schema.json --instance catalog\engines.yaml
pwsh -NoProfile -File tests\adapters\test_codex_adapter.ps1
pwsh -NoProfile -File tests\adapters\test_claude_code_adapter.ps1
pwsh -NoProfile -File tests\adapters\test_generic_adapters.ps1
pwsh -NoProfile -File tests\install\test_install_targets.ps1
pwsh -NoProfile -File tests\install\test_fork_discovery.ps1
pwsh -NoProfile -File tests\security\test_path_boundaries.ps1
python evals\runners\run-contract-evals.py --cases evals\cases --out evals\reports\phase-13.json
git diff --check
```

For each engine repository, run its own documented release checks plus:

```powershell
Test-Path .skills-engine\engine-manifest.yaml
python tests\agent-integration\validate_manifest.py .skills-engine\engine-manifest.yaml
```

If an engine uses a different native test runner, the equivalent command must be recorded in that engine’s manifest; the universal package must not invent a replacement.

Expected result: every engine either passes its integration contract or is explicitly recorded as `NOT ASSESSED` with the missing file, dependency, or approval named.

### Exit criteria

- All ten engines declare what the agents may read, validate, and change.
- All ten engines declare which MCP operations are safe and which require approval.
- The universal catalog can consume engine manifests without copying domain skills.
- Developers can install the Codex plugin, a host adapter, the generic CLI, or the MCP package from documented public release channels.
- GitHub releases include checksums, version metadata, source commit, and adapter/engine compatibility information.
- A developer with a forked engine can use the tools without changing the universal package or relying on the original machine paths.

## Implementation handoff

Implement on `main` in phase order. Use one commit per completed phase when the phase creates code or tests; use a single documentation commit for this plan until implementation begins. Phase 13 requires coordinated commits in each engine repository followed by a catalog update in this repository. At each checkpoint, attach command output or a report path to the phase evidence. If a host specification changes, update the compatibility contract and adapter manifest before changing its installer.
