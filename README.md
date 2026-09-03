# Skills Engine Agents

Portable multi-host agents for routing, validating, and maintaining the eleven `peterbamuhigire` skills engines, with a shared craft contract that keeps every engine and every product deliberate, inspectable, evidence-backed, and safe to hand over.

> **GitHub description:** Portable Codex agents for routing, maintaining, and validating eleven domain skills engines with safe discovery, quality checks, and fork-friendly installation.

## What this repository is

`skills-engine-agents` is a canonical coordination layer with Codex, Claude Code, Gemini CLI, OpenCode, generic CLI, and optional MCP adapters. It helps a host identify the right engine, preserve each engine's local operating rules, run documented validation gates, and perform safe maintenance across local checkouts.

It does not replace or duplicate the domain knowledge in the eleven engines. Each engine remains independently usable and continues to own its routers, `SKILL.md` files, references, templates, and release checks.

## The eleven skills engines

- [SRS Skills](https://github.com/peterbamuhigire/srs-skills) — software requirements, product requirements, architecture, and technical specifications.
- [Business Plan Skills](https://github.com/peterbamuhigire/business-plan-skills) — business plans, financial models, market strategy, and investor planning.
- [Website Skills](https://github.com/peterbamuhigire/website-skills) — websites, landing pages, web UX, SEO, performance, and site delivery.
- [Social Media Skills](https://github.com/peterbamuhigire/social-media-skills) — social strategy, content planning, campaigns, and platform workflows.
- [Linux Skills](https://github.com/peterbamuhigire/linux-skills) — Linux administration, servers, hardening, networking, and operations.
- [Proposal Skills](https://github.com/peterbamuhigire/proposal-skills) — proposals, tenders, bids, RFP/RFQ responses, and grant submissions.
- [Skills Web Dev](https://github.com/peterbamuhigire/skills-web-dev) — general engineering, AI systems, SaaS, security, product, UX, and technical documentation.
- [Chwezi Accounting Doctrine](https://github.com/peterbamuhigire/chwezi-accounting-doctrine) — finance, accounting, IFRS/IAS, tax, bookkeeping, controls, and reporting.
- [Design System Skills](https://github.com/peterbamuhigire/design-system-skills) — typography, visual design, UI/UX, layout, accessibility, and document presentation.
- [Digital Research Skills](https://github.com/peterbamuhigire/digital-research-skills) — research orchestration, source evaluation, evidence verification, and benchmarking.
- [Windows Administration Skills](https://github.com/peterbamuhigire/windows-admin-engine-skills) — Windows hosts, Active Directory, networking, security, storage, recovery, fleet, and hybrid administration.

The core adds three focused workflows:

- `engine-orchestrator` routes a request to the correct domain and cross-cutting engines.
- `engine-maintainer` inspects engine remotes, branches, working trees, and fast-forward updates.
- `engine-validator` runs documented engine checks and reports evidence or `NOT ASSESSED` results.

The cross-engine runtime metadata check is available at
`scripts/validate-runtime-skill-budget.py`. Run it against the exact local and
plugin skill roots exposed to a host; repository-local catalog checks do not
measure the assembled runtime budget.

The engines remain independently usable. Their own `AGENTS.md`, routers, and `SKILL.md` files remain the source of truth for domain behavior. This package supplies coordination and maintenance behavior around them. Host adapters package the same core; they do not make provider/model quality or tool access identical.

## Portfolio craft operation

The portfolio-wide craft contract is [`docs/operations/portfolio-craft-standard-2026-09-04.md`](docs/operations/portfolio-craft-standard-2026-09-04.md). It requires every engine and every kaizen operation to work in small named slices, inspect existing context, refine in place, exercise hard cases, and record structural, behavioural, render/reader, system/production, and handoff evidence. Run [`scripts/validate-portfolio-craft.ps1`](scripts/validate-portfolio-craft.ps1) to verify that all eleven engine routers carry the contract. Missing evidence remains `NOT ASSESSED`.

See the [compatibility contract](docs/architecture/compatibility-contract.md) and [host matrix](docs/architecture/host-model-capability-matrix.md) before selecting an adapter.

Host adapters are under [`adapters/`](adapters/). The optional typed MCP server
is under [`mcp-server/`](mcp-server/). Portable installers, update/uninstall
scripts, security controls, and deterministic evaluations are documented in
[`docs/distribution.md`](docs/distribution.md), [`docs/security/`](docs/security/),
and [`evals/`](evals/).

## Implementation plan

The complete multi-host implementation plan is maintained in [`docs/plans/aug-25`](docs/plans/aug-25/README.md). It contains a master overview, an index, and one detailed implementation file for each of the 13 phases, including the eleven-engine integration and public distribution phase.

The phase documents specify exact files, interfaces, host adapters, MCP tools, capability fallbacks, security controls, tests, evidence requirements, release artifacts, and developer installation paths.

## Distribution and installation

### Public plugin directory

After the plugin is accepted into the universal Codex Plugin Directory, users can search for **Skills Engine Agents** in Codex and install it without cloning this repository. Availability still depends on the user's plan, workspace settings, role, and supported Codex surface.

Publishing the GitHub repository does not itself publish the plugin to that directory; directory submission or approval is a separate product workflow.

### Workspace directory

For a private team rollout, a workspace administrator can import and publish the plugin to the workspace plugin directory. Team members then install it from the directory without cloning the repository. This keeps the plugin inside that workspace.

### Install locally

From a clone of this repository:

```powershell
.\scripts\install.ps1
```

The default destination is `%USERPROFILE%\plugins\skills-engine-agents`. Use `-Destination` to select another plugin directory and `-Force` only when intentionally replacing an existing installation.

Local installation is the fallback for development, private use, and environments that do not have access to a published directory.

## Use with a forked engine

Clone any engine fork, open Codex from that checkout, and invoke the installed agent. Discovery uses the current Git root, origin repository name, folder name, and local `AGENTS.md`; it does not assume `C:\wamp64\www` or another fixed machine path.

If the checkout is not one of the eleven catalogued engines, the agents may still inspect it, but they will not invent engine-specific validation commands.

## Safety boundaries

The agents are read-only by default. The maintainer may run `git pull --ff-only` only after the user explicitly requests a pull. It must skip dirty or diverged repositories and never reset, delete, merge manually, or force-push.

Validation commands that are unavailable are reported as `NOT ASSESSED`; unavailable evidence is never treated as a pass.

## Validate this plugin

```powershell
python C:\Users\BIRDC\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .
.\scripts\validate-catalog.ps1
.\tests\validate_catalog.ps1
git diff --check
```

## Repository layout

```text
.codex-plugin/plugin.json       Plugin manifest
agents/                         Portable agent definitions
catalog/engines.yaml            Eleven-engine registry
scripts/discover-engine.ps1     Current-checkout discovery
scripts/install.ps1             Local installation helper
scripts/validate-catalog.ps1    Registry validation
tests/validate_catalog.ps1      Deterministic catalog test
```
