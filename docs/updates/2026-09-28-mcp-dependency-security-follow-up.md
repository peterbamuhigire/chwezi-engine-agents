# Coordinator MCP dependency security follow-up

**Date:** 2026-09-28
**Scope:** `mcp-server/package.json` and its exact `package-lock.json` only.

The baseline lock audit found one critical and four moderate advisories among
Vitest, `@vitest/mocker`, `yaml`, Hono, and `qs`. The Vitest critical advisory
requires the UI/browser-mode server conditions described by the advisory; this
package runs `vitest run` and does not declare Vitest UI. I upgraded to patched
versions anyway, including Vitest 4.1.11 because the separate `@vitest/mocker`
advisory does not list a fixed 3.x release. I also updated `tsx` to 4.23.15 so
its esbuild dependency satisfies the Vite peer range brought in by Vitest 4.

The resulting exact lock audit reports zero vulnerabilities across 196
packages. `npm ci --ignore-scripts`, `npm ls --all`, `npm run build`, and the
five MCP tests pass on Node.js 24.8.0. A lockfile-only CycloneDX 1.5 SBOM with
193 components is retained at
[`docs/security/sbom/coordinator-mcp-server.cdx.json`](../security/sbom/coordinator-mcp-server.cdx.json).
The supply-chain register records this narrow dependency review.

This does not review every MCP tool behavior, prove package provenance, or
establish a complete SBOM or security review for the 12-engine estate. Other
engine ecosystems and consumer lockfiles remain unassessed. P19's broad
distribution security verdict remains conditional.

**Sources:** npm CLI v11 [`npm audit`](https://docs.npmjs.com/cli/v11/commands/npm-audit/)
and [`npm sbom`](https://docs.npmjs.com/cli/v11/commands/npm-sbom/) documentation;
GitHub advisories GHSA-5xrq-8626-4rwp, GHSA-82fw-gwwq-j7x9,
GHSA-48c2-rrv3-qjmp, GHSA-gqvv-2mrq-wpjv, GHSA-g6gw-c38x-mqfc,
GHSA-crvj-82cr-hjcx, GHSA-x5fp-wj9c-mxmx, and GHSA-4mjr-xmp4-gh2g.
