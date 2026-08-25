# Phase 8 — MCP Server Implementation Plan

> **For agentic workers:** Use executing-plans or subagent-driven-development. The server must expose typed, allowlisted operations; it must never convert model text into arbitrary shell commands.

**Goal:** Provide an optional MCP tool surface that any MCP-capable host can use with any supported model provider.

**Depends on:** Phases 1–4 and the host MCP documentation verified before implementation.

**Produces:** A versioned stdio MCP server, typed tool schemas, safety tests, and a host registration example.

## Files

- Create: mcp-server/package.json, package-lock.json, and tsconfig.json.
- Create: mcp-server/src/index.ts — server bootstrap and tool registration.
- Create: mcp-server/src/contracts.ts — shared request/response types.
- Create: mcp-server/src/engine-discovery.ts — Git-root and catalog discovery.
- Create: mcp-server/src/engine-validation.ts — allowlisted validation dispatch.
- Create: mcp-server/src/engine-maintenance.ts — approved fast-forward maintenance.
- Create: mcp-server/src/safety.ts — path, command, and approval checks.
- Create: mcp-server/tests/contracts.test.ts, safety.test.ts, and discovery.test.ts.
- Create: mcp-server/README.md and .mcp.json.example.
- Modify: README.md and docs/distribution.md.

## Tool interface

- discover_engine(path: string) -> engine_identity
- inspect_engine(path: string) -> maintenance_result(read_only=true)
- validate_engine(path: string, scope: string) -> validation_result
- pull_engine_ff_only(path: string, confirmation_token: string) -> maintenance_result

No tool accepts command, shell, or an arbitrary executable string from the model.

## Safety invariants

- Resolve and canonicalize the target path before any operation.
- Require a Git root and catalog match before running engine-specific validators.
- Allow only validator commands declared in catalog/engines.yaml or .skills-engine/engine-manifest.yaml.
- Reject dirty trees, diverged upstreams, missing upstreams, and non-main mutation targets unless the user explicitly changes scope.
- Require a host-generated confirmation token for every pull or write operation.
- Never call git reset, git clean, manual merge, force-push, recursive delete, or broad path deletion.
- Return structured errors with code, message, and remediation.

## Tasks

- [ ] Verify the current MCP SDK package and Node version before pinning dependencies.
- [ ] Add strict TypeScript types for all request and response contracts.
- [ ] Implement discovery by reusing the catalog contract rather than copying domain routing logic.
- [ ] Implement validator dispatch with a fixed allowlist and explicit working directory.
- [ ] Implement maintenance with confirmation-token validation and post-action status checks.
- [ ] Add tests for path traversal, symlink/junction targets, dirty trees, divergence, invalid tokens, and unknown engines.
- [ ] Add tests proving model-supplied command text is rejected.
- [ ] Add stdio configuration with environment-variable expansion only for non-secret paths and host-managed secrets.
- [ ] Document MCP as an optional transport, not a replacement for canonical instructions.

## Tests and evidence

Run in mcp-server:
- npm ci
- npm test
- npm run build

Expected evidence: build and tests pass. If Node or the SDK is unavailable, record execution as NOT ASSESSED while still reviewing static contract files.

## Failure handling

- A tool schema failure blocks release.
- A dependency audit failure blocks publication until the dependency is upgraded, removed, or accepted by the maintainer.
- An MCP host that cannot provide approval uses read-only tools only.

## Exit criteria

- An MCP-capable host can discover and validate an engine through typed tools.
- Pull remains approval-gated and fast-forward-only at the MCP boundary.

## Commit checkpoint

Stage the files listed above and commit:
feat: add typed MCP engine tools
