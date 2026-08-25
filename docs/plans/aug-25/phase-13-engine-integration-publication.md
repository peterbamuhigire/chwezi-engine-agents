# Phase 13 — Ten-Engine Integration and Public Distribution Plan

> **For agentic workers:** Use executing-plans or subagent-driven-development. This phase coordinates changes across ten separate repositories and then publishes the universal package from main.

**Goal:** Make each skills engine explicitly consumable by the agents and optional MCP server, while keeping each engine independently usable and giving other developers reproducible installation paths.

**Depends on:** Phases 1–12 and current engine repository state.

**Produces:** Ten engine integration manifests, per-engine tests and router notes, catalog updates, public release artifacts, and developer installation guides.

## Shared engine contract

Each engine repository receives .skills-engine/engine-manifest.yaml with:

- engine_id
- display_name
- contract_version: 1.0
- router.path
- skills.discovery_glob
- validation.commands
- agent_integration.supported_modes
- agent_integration.local_context_files
- agent_integration.mcp_safe_tools
- agent_integration.approval_required_for
- agent_integration.forbidden_operations
- agent_integration.fork_behavior
- source_of_truth.router
- source_of_truth.skills
- source_of_truth.references

The manifest is declarative. It does not import this plugin, copy domain skills, or execute a model-supplied command.

Each engine also adds .skills-engine/AGENTS-INTEGRATION.md stating that the engine remains independently usable, the universal package may read the router and documented checks, missing evidence is NOT ASSESSED, no writes occur without approval, and the router and SKILL.md files remain authoritative.

## Required shared test contract

Each engine adds an integration test that:

1. Loads .skills-engine/engine-manifest.yaml.
2. Confirms the declared router exists.
3. Confirms the skill discovery glob finds at least one relevant SKILL.md.
4. Confirms every declared validator has a working-directory and platform field.
5. Confirms every MCP-safe tool is read-only.
6. Confirms every approval-required operation is absent from the safe-tool list.
7. Confirms the manifest engine_id matches the universal catalog.
8. Returns exit code 0 only when all available checks pass.
9. Returns a named NOT ASSESSED result when a dependency or platform is unavailable.
10. Never executes an undeclared command.

## Engine-by-engine file and behavior plan

### 13.1 srs-skills

Repository: C:\wamp64\www\srs-skills

Files:
- Modify AGENTS.md.
- Create .skills-engine/engine-manifest.yaml.
- Create tests/agent-integration/test_srs_agent_contract.py.
- Modify the existing quality baseline to expose structural and routing gates.

Required behavior:
- Read requirements, references, templates, and documented checks.
- Add digital research for current standards, regulations, or source-sensitive claims.
- Require approval before changing requirements, architecture, governance, or compliance artifacts.
- Expose discovery, router read, skill read, and documented validator tools as MCP-safe.

Acceptance:
- SRS routing fixture selects this engine.
- Standards fixture adds digital research.
- Unapproved document mutation is rejected.

### 13.2 business-plan-skills

Repository: C:\wamp64\www\business-plan-skills

Files:
- Modify AGENTS.md.
- Create .skills-engine/engine-manifest.yaml.
- Create tests/agent-integration/test_business_plan_agent_contract.py.
- Modify the existing quality baseline for source and financial-model checks.

Required behavior:
- Keep assumptions separate from sourced facts.
- Add chwezi-accounting-doctrine for accounting, IFRS, tax, or financial statements.
- Keep financial writes, model overwrites, and publication approval-gated.
- Expose read-only discovery, template inspection, and documented validation.

Acceptance:
- Market-entry fixture selects business-plan skills.
- Finance fixture selects business-plan plus accounting doctrine.
- Missing market source remains an evidence gap.

### 13.3 website-skills

Repository: C:\wamp64\www\website-skills

Files:
- Modify AGENTS.md.
- Create .skills-engine/engine-manifest.yaml.
- Create tests/agent-integration/test_website_agent_contract.py.
- Modify website registry and benchmark metadata to expose documented commands.

Required behavior:
- Inspect project structure, content, assets, and performance fixtures.
- Add design-system-skills for visual design and document appearance.
- Require approval for deployment, DNS, hosting, and production changes.
- Expose project discovery and read-only audits as MCP-safe tools.

Acceptance:
- Landing-page fixture selects this engine.
- Design fixture adds the design engine.
- Deployment fixture stops at an approval packet.

### 13.4 social-media-skills

Repository: C:\wamp64\www\social-media-skills

Files:
- Modify AGENTS.md.
- Create .skills-engine/engine-manifest.yaml.
- Create tests/agent-integration/test_social_media_agent_contract.py.
- Modify source-freshness and routing validator metadata.

Required behavior:
- Draft content and schedules without publishing automatically.
- Add digital research for current platform rules, features, and audience facts.
- Require account, target, and human approval before publication.
- Keep credentials in the host, not the engine or plugin.

Acceptance:
- Calendar fixture selects this engine.
- Current platform fixture adds digital research.
- Publish fixture stops at a reviewable draft.

### 13.5 linux-skills

Repository: C:\wamp64\www\linux-skills

Files:
- Modify AGENTS.md.
- Create .skills-engine/engine-manifest.yaml.
- Create tests/agent-integration/test_linux_agent_contract.py.
- Modify distro-matrix metadata to mark Linux-only commands.

Required behavior:
- Permit read-only configuration and log inspection.
- Require target host and approval for packages, services, firewalls, DNS, filesystems, credentials, and permissions.
- Expose named diagnostics only; never unrestricted shell through MCP.
- Report Linux-only checks NOT ASSESSED on Windows without a declared Linux target.

Acceptance:
- Hardening fixture requires an execution target.
- Package install fixture is blocked without approval.
- Windows-only fixture returns NOT ASSESSED.

### 13.6 proposal-skills

Repository: C:\wamp64\www\proposal-skills

Files:
- Modify AGENTS.md.
- Create .skills-engine/engine-manifest.yaml.
- Create tests/agent-integration/test_proposal_agent_contract.py.
- Modify documented structural-check metadata.

Required behavior:
- Inspect solicitations, templates, compliance matrices, and source registers.
- Add digital research for current procurement, legal, donor, or market claims.
- Require review and approval before submission, email, signatures, or portal actions.
- Expose requirement extraction, matrix validation, and draft evidence reporting.

Acceptance:
- RFP fixture selects this engine.
- Current procurement fixture adds digital research.
- Submission fixture creates a review packet only.

### 13.7 skills-web-dev

Repository: C:\wamp64\www\skills-web-dev

Files:
- Modify SKILL.md and the canonical router.
- Create .skills-engine/engine-manifest.yaml.
- Create tests/agent-integration/test_skills_web_dev_agent_contract.py.
- Modify control-plane, routing-smoke, anti-slop, and evidence-pack metadata.

Required behavior:
- Own general engineering, AI systems, security, product, and documentation routing.
- Load only the smallest relevant SKILL.md set after routing.
- Expose catalog discovery, skill inspection, deterministic validation, and evidence-pack generation.
- Require approval for code changes, dependency installation, deployment, and external messages.

Acceptance:
- AI-agent architecture fixture selects the correct AI skill family.
- Documentation fixture runs evidence and anti-slop gates.
- Provider fixture marks current provider assumptions for source verification.

### 13.8 chwezi-accounting-doctrine

Repository: C:\wamp64\www\chwezi-accounting-doctrine

Files:
- Modify README.md.
- Create .skills-engine/engine-manifest.yaml.
- Create tests/agent-integration/test_accounting_agent_contract.ps1.
- Modify tools/validate-doctrine.ps1 documentation.

Required behavior:
- Keep finance, IFRS, IAS, tax, bookkeeping, controls, and reporting as additive cross-cutting scope.
- Require jurisdiction and period for statutory or tax routes.
- Expose doctrine discovery, source inspection, and strict validation.
- Require approval and audit evidence for ledger entries, filings, close outputs, and control changes.

Acceptance:
- Financial-model fixture adds doctrine with business-plan skills.
- Tax fixture requires jurisdiction and period.
- Ledger-write fixture is blocked.

### 13.9 design-system-skills

Repository: C:\wamp64\www\design-system-skills

Files:
- Modify AGENTS.md and doctrine/design-doctrine.md.
- Create .skills-engine/engine-manifest.yaml.
- Create tests/agent-integration/test_design_agent_contract.ps1.
- Modify design validation metadata for anti-slop fonts and visual QA.

Required behavior:
- Remain additive to the active domain engine.
- Expose doctrine, asset metadata, rendering, and visual evidence operations.
- Require typeface, color, layout, and state decisions before visual output.
- Require approval for asset replacement and publication.

Acceptance:
- Dashboard fixture selects domain plus design.
- Rendering fixture reports visual evidence.
- Banned-font fixture fails with file and line evidence.

### 13.10 digital-research-skills

Repository: C:\wamp64\www\digital-research-skills

Files:
- Modify AGENTS.md.
- Create .skills-engine/engine-manifest.yaml.
- Create tests/agent-integration/test_digital_research_agent_contract.py.
- Modify source verification and currentness validator metadata.

Required behavior:
- Preserve source evaluation, source verification, evidence discipline, and research orchestration.
- Require real source traces for claims and current-source checks.
- Expose source discovery, evaluation, URL verification, claim support, and evidence reports.
- Require approval for external contact, archive writes, source publication, and evidence-registry edits.

Acceptance:
- Current standards fixture adds this engine.
- Unsupported claims remain unresolved.
- Verification fixture reports source, claim, confidence, and access date.

## Engine publication sequence

For each engine repository:

1. Add the manifest and integration note.
2. Add the engine-specific fixture and test.
3. Run the engine’s existing release checks unchanged.
4. Run the integration test.
5. Run the universal catalog validator against the checkout.
6. Commit to that engine’s main branch with message: feat: expose agent integration contract.
7. Push that engine’s main branch.
8. Tag only under the engine’s existing release policy.
9. Record the released commit and contract version in this repository’s catalog.
10. Run universal adapter and evaluation tests against the released commit.

The plugin must not depend silently on unpublished engine changes. During rollout, catalog status is pending, available, or not_assessed. Older engines remain usable through existing router and validator fields, but missing integration metadata is NOT ASSESSED.

## Public distribution

Publish the tools through these channels:

- GitHub source and tagged release: peterbamuhigire/chwezi-engine-agents.
- Codex plugin directory: the validated Codex package after directory approval.
- Claude Code, Gemini CLI, and OpenCode: host-specific adapter directories or supported marketplaces.
- Generic CLI: PowerShell, POSIX, and Python installation paths.
- MCP: versioned package, stdio configuration, and locked dependency tree.

Proposed package names require registry availability checks before publication:
- @peterbamuhigire/skills-engine-agents-mcp
- skills-engine-agents-cli

## Release artifacts

Create in this repository:

- .github/workflows/release.yml.
- .github/workflows/adapter-smoke-tests.yml.
- release/manifest.json.
- release/checksums.txt.
- release/NOTICE.txt.

release/manifest.json must include source commit, release version, schema versions, adapter versions, engine integration commits, build timestamp, artifact names, and checksum reference. Do not publish API keys, private engine content, local paths, or credential-bearing reports.

## Developer installation documentation

Every adapter guide must contain prerequisites, supported operating systems, install/update/uninstall commands, loading confirmation, read-only discovery, validation, safe pull flow, model-provider boundary, fork behavior, NOT ASSESSED cases, troubleshooting, and a compatibility-report link.

Provide a safer cloned-release path in addition to any remote script convenience. Tell users to inspect downloaded scripts before piping them to a shell.

## Tests and evidence

Run from this repository:

- python scripts\validate-contracts.py --schema schemas\engine-catalog.schema.json --instance catalog\engines.yaml
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\adapters\test_codex_adapter.ps1
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\adapters\test_claude_code_adapter.ps1
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\adapters\test_other_host_adapters.ps1
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\install\test_install_targets.ps1
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\install\test_fork_discovery.ps1
- powershell -NoProfile -ExecutionPolicy Bypass -File tests\security\test_path_boundaries.ps1
- python evals\runners\run-contract-evals.py --cases evals\cases --out evals\reports\phase-13.json
- git diff --check

Run in each engine:

- the engine’s documented release checks;
- its integration test;
- its manifest validator.

Expected evidence: every engine passes or is explicitly recorded NOT ASSESSED with the missing file, dependency, or approval named.

## Exit criteria

- All ten engines declare what agents may read, validate, and change.
- All ten engines declare MCP-safe operations and approval-required operations.
- The catalog consumes engine manifests without copying domain skills.
- Developers can install Codex, host adapters, generic CLI, or MCP artifacts.
- Releases include checksums, version metadata, source commits, and compatibility information.
- Forked engines work without changing the universal package or relying on original machine paths.

## Commit checkpoint

Commit the universal catalog, publication workflow, and documentation after all engine repositories have released their integration manifests with:
release: publish ten-engine agent integration contract
