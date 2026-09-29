# Decision: canonical host for the `skill-writing` standard

**Status:** Accepted for commit by the orchestrator under Peter Bamuhigire's delegated authority, 29 September 2026. Peter's ratification of the doctrine-class change is still required before the public push gate.
**Phase:** my-10-kaizen M10-04-T01 (SP-04).
**Change class:** doctrine, with workflow-routing (engine stubs) and runtime-configuration (drift register).

## Decision

The canonical Chwezi skill-authoring standard is **`chwezi-dev-engine/skills/sdlc-meta/skill-writing`**. Six engines (`digital-research-engine`, `website-skills`, `business-plan-skills`, `social-media-skills`, `proposal-skills`, `linux-skills`) keep a `skill-writing` **pointer stub** with the same `name`, a portable minimum, an engine-local delta and a degraded mode, plus **byte mirrors** of the canonical scripts they call. `chwezi-engine-agents` owns the drift register (`catalog/shared-assets.yaml`) and the check (`scripts/render_host_files.py --check`), not the authoring content.

## Reasons

1. **It is already the declared canonical in the engines that cite one.**
   - `srs-skills/AGENTS.md` l.81 (l.76 when the plan was measured): "Skill authoring or upgrades: use `sdlc-meta/skill-writing` in the engineering catalog engine".
   - `srs-skills/docs/skill-authoring-standard.md` l.40 and `srs-skills/CONTRIBUTING.md` l.44 run the dev `skill-writing/scripts/quick_validate.py`.
   - `design-system-skills/governance/skill-authoring-standard.md` l.4 cites the "canonical `skill-writing`, `skill-composition-standards`, and `skill-engine-audit` rules".
2. **Only the dev copy carries the accepted Pocock and lean-metadata work:** five references (context pointers, two-load context budget, invocation ownership, leading words and trigger design, completion and handoff), the 350-character description cap and the "no implementation steps" rule (`2258714`), and `contract_gate.py`, which dev CI runs. It was also the largest and most recent copy (353 lines, `eb7972e`).
3. **`chwezi-engine-agents` is coordination-only.** Its `skills/README.md` states that domain skills are never duplicated there, and it has no Tier-1 skill validator. It hosts the drift register and checks, not the authoring content.
4. **No active skill is added.** The dev copy already exists; dev stays at 167 active skills.

## Consequences

- Authoring rules change in one place. A stub changes only when its portable minimum or engine delta changes.
- Each mirrored script is byte-checked: `skill-writing-quick-validate`, `skill-writing-init-skill`, `skill-writing-package-skill`, `skill-writing-upgrade-dual-compat` (research engine only) and `skill-writing-license`, plus the social-media copy of `references/skill-authoring-best-practices.md`, which a dated Kaizen record links. The stubs are registered variants with owner and reason. The canonical `SKILL.md` is deliberately not hashed, so it can evolve. Re-sync the mirrors after any change to a canonical script.
- `quick_validate.py` and `upgrade_dual_compat.py` now locate the engine root by walking up to a `.git` entry or an `AGENTS.md` router, instead of a fixed `parents[4]`. One byte-identical file therefore works at every folder depth (`meta/skill-writing` in linux; `skills/skill-writing` in research).
- The research engine's rule that research-skill revisions pass the replay gate stays an engine-local delta in its stub. The canonical `SKILL.md` names it.
- Every stub passes its own engine's Tier-1 validator and routing smoke test. No engine needed the full-mirror fallback.

## Rollback

The pre-change preservation map (`m10-kaizen-evidence/M10-04/preservation/skill-writing-preservation-map.{md,json}`) records every file of all seven copies with its SHA-256 and the engine HEAD. To restore a copy, check out its folder from that HEAD, register its hash as a variant and drop its byte rows. Each engine can be reverted independently.

## Out of scope

- Nineteen uncontrolled copies in client project folders under `C:\wamp64\www` (for example `AgroDB/skills/skill-writing`, `dynapharm-website/.claude/skills/skill-writing`). They are listed in the M10-04 evidence for Peter's decision: refresh from canonical, or leave frozen with the project.
- Content convergence of the other duplicated meta-skills (`skill-safety-audit`, `anti-ai-slop`, `ai-slop-audit`, `kaizen-improvement-system`). That is a later wave, which can follow this stub pattern.
