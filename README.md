# Chwezi Engine Agents

`chwezi-engine-agents` is not a domain skill engine. It carries no independent domain-skill content worth installing on its own — no SRS skills, no accounting doctrine, no design system, nothing a consulting or engineering task would reach for directly. What it is instead is the coordination layer that sits across the eleven Chwezi domain engines: it routes a request to the right engine (or engines, for cross-cutting work), installs and updates local checkouts through a shared installer, generates each engine's plugin manifest from its actual skill tree, validates engine claims against documented checks, and vendors a shared destructive-command safety gate to every engine in the estate. Use this repository if you manage several Chwezi engines at once and want one place to route, install, validate, and maintain them, or if you want the shared installer/governance tooling without duplicating it into each engine. If you only need one domain's skills, skip this repository entirely and install that engine directly — see below.

## Install

This repository is the Chwezi suite marketplace: its [`.claude-plugin/marketplace.json`](.claude-plugin/marketplace.json) lists the coordination core plus all eleven domain engines as independently installable plugins. Add the marketplace once, then install only what you need:

```
/plugin marketplace add peterbamuhigire/chwezi-engine-agents
/plugin install chwezi-suite@chwezi        # this coordination core (optional)
/plugin install srs@chwezi                 # SRS Skills
/plugin install business-plan@chwezi       # Business Plan Skills
/plugin install website@chwezi             # Website Skills
/plugin install social@chwezi              # Social Media Skills
/plugin install linux@chwezi                # Linux Skills
/plugin install proposal@chwezi            # Proposal Skills
/plugin install engineering@chwezi         # Skills Web Dev (engineering catalogue)
/plugin install accounting@chwezi          # Chwezi Accounting Doctrine
/plugin install design-system@chwezi       # Design System Skills
/plugin install research@chwezi            # Digital Research Skills
/plugin install windows-admin@chwezi       # Windows Administration Skills
```

**Installing a domain engine standalone works with zero dependency on this coordinator.** Each engine also publishes its own repository and its own `/plugin marketplace add <that-engine-repo>` command, and none of the eleven engines requires `chwezi-suite` to be installed, present, or even known about. This repository is a convenience — one marketplace, one set of shared tooling — never a requirement. For local, non-plugin installation (project-scoped, CI, or hosts without the plugin system), use the shared installer directly: `node scripts/install-engine.js install --engine <path-to-engine>` (see the header comment in [`scripts/install-engine.js`](scripts/install-engine.js) for `--scope`, `--dry-run`, and `uninstall`/`doctor` modes).

The eleven domain engines this package coordinates, with their repositories (from [`catalog/engines.yaml`](catalog/engines.yaml)):

- [SRS Skills](https://github.com/peterbamuhigire/srs-skills) — software requirements, product requirements, architecture, and technical specifications.
- [Business Plan Skills](https://github.com/peterbamuhigire/business-plan-skills) — business plans, financial models, market strategy, investor planning.
- [Website Skills](https://github.com/peterbamuhigire/website-skills) — websites, landing pages, web UX, SEO, performance, site delivery.
- [Social Media Skills](https://github.com/peterbamuhigire/social-media-skills) — social strategy, content planning, campaigns, platform workflows.
- [Linux Skills](https://github.com/peterbamuhigire/linux-skills) — Linux administration, servers, hardening, networking, operations.
- [Proposal Skills](https://github.com/peterbamuhigire/proposal-skills) — proposals, tenders, bids, RFP/RFQ responses, grant submissions.
- [Skills Web Dev](https://github.com/peterbamuhigire/skills-web-dev) — general engineering, AI systems, SaaS, security, product, technical documentation (the engineering catalogue).
- [Chwezi Accounting Doctrine](https://github.com/peterbamuhigire/chwezi-accounting-doctrine) — finance, accounting, IFRS/IAS, tax, bookkeeping, controls, reporting.
- [Design System Skills](https://github.com/peterbamuhigire/design-system-skills) — typography, visual design, UI/UX, layout, accessibility, document presentation.
- [Digital Research Skills](https://github.com/peterbamuhigire/digital-research-engine) — research orchestration, source evaluation, evidence verification, benchmarking.
- [Windows Administration Skills](https://github.com/peterbamuhigire/windows-admin-engine-skills) — Windows hosts, Active Directory, networking, security, storage, recovery, fleet, and hybrid administration.

## Capabilities

| Component | What it does |
|---|---|
| `agents/engine-orchestrator.md` | Routes a request to the correct domain engine(s), including cross-cutting activation (finance, design, research) alongside a domain engine. |
| `agents/engine-maintainer.md` | Inspects engine remotes, branches, and working trees; runs `git pull --ff-only` only on explicit request; skips dirty or diverged checkouts; never resets, deletes, or force-pushes. |
| `agents/engine-validator.md` | Runs each engine's documented validation commands (from `catalog/engines.yaml`) and reports evidence or `NOT ASSESSED` — never treats missing evidence as a pass. |
| `scripts/install-engine.js` | Shared installer runtime: installs, updates, and uninstalls any one engine standalone, with a per-file content-hash install-state record so updates only ever touch files it wrote. |
| `scripts/generate-plugin-manifest.js` | Regenerates an engine's `.claude-plugin/plugin.json` from its actual `SKILL.md` tree, across the three skill-root shapes found in the estate. |
| `hooks/destructive-bash-gate.js` | PreToolUse hook on Bash/PowerShell: a DENY-then-ALLOW gate on destructive commands (`rm -rf`, `git reset --hard`, `git push --force`, `DROP TABLE`, etc.), vendored identically to all twelve Chwezi engines. |
| `skills/rules-distill/SKILL.md` | Scans one engine's skills for principles that recur in two or more skills and are not yet in `rules/`, and proposes promotions for explicit approval — never edits `rules/` automatically. |
| `catalog/engines.yaml` | The eleven-engine registry: repository, router file, manifest path, and validator commands per engine. |

## References

Mustafa, A. et al. *Everything Claude Code (ECC)*. GitHub: affaan-m/ECC, 2026.

Three pieces of this package's own tooling are explicitly adapted from ECC's audit findings, and each file's own header comment carries the specific citation:

- `scripts/install-engine.js` implements the "Tier 1 — STANDALONE" installation model documented in the ECC audit's installation report.
- `scripts/generate-plugin-manifest.js` follows the explicit-path-array manifest form and the constraints recorded in ECC's `.claude-plugin/PLUGIN_SCHEMA_NOTES.md` (mandatory `version`, `skills` as an array, no invented `agents` or `hooks` fields).
- `hooks/destructive-bash-gate.js` is modelled on the DENY → FORCE → ALLOW pattern in ECC's gateguard skill.
- `skills/rules-distill/SKILL.md` is adapted from the ECC audit (`kaizen-engines/ECC-audit-2026-09-20/00-MASTER-REPORT.md`, finding I-2), applying the same deterministic-collection-plus-LLM-judgment split.
