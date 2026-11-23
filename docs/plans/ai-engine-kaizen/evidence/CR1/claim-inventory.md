# CR1 claim inventory

**Date:** 2026-11-23  
**Coordinator source revision:** `e9adbe7ca9de9c6c238999067f932b79a6c4d7d5`  
**Scope:** Claims added or brought forward on the README front door. This record contains public-safe case IDs and does not copy private producer packets, test data or local paths.

| Claim and owner | Real entry point | Revision or date | Result and environment | Limit |
|---|---|---|---|---|
| K1 triage acceptance; SRS case owner | `docs/plans/ai-engine-kaizen/casebook.md`, K1; README Capabilities | Frozen synthetic casebook at the coordinator source revision above | Candidate emits five alerts against a two-review capacity; reject that profile. Fixture arithmetic is recorded in the casebook. | Expected fixture behavior, not a measured production model. The more permissive profile still needs an owner and representative evidence. |
| K3 assisted code-change acceptance; engineering and independent reviewer | `docs/plans/ai-engine-kaizen/casebook.md`, K3; `docs/operations/ai-change-handoff.md` | Frozen synthetic casebook at the coordinator source revision above | E7 replay has one effect and E8 is distinct; the casebook gives the other failure and recovery oracles. | The public README describes the oracle. It does not claim production rollout or a private source diff. |
| Non-AI routing; engine owner | `core/instructions/engine-orchestrator.md`; `catalog/engines.yaml` | Files at the coordinator source revision above | The catalogue and router identify a domain owner; missing or ambiguous engines are `NOT ASSESSED`. | Availability and validators must be checked in the selected engine checkout. |
| Handoff shape validation; coordinator maintainer | `schemas/handoff.schema.json`; `tests/fixtures/valid-handoff.yaml`; `scripts/validate-contracts.py` | Files at the coordinator source revision above | Schema validation is reproducible locally; the versioned-evidence verifier separately checks digest, case, expected identity and revisions. | A schema pass alone does not accept an evidence claim. See the C01 receipt and fixture tests. |
| JAD runner ownership; private Development owner | The D-11 decision recorded in `docs/plans/ai-engine-kaizen/build.md`; README Capabilities | Decision in the accepted build plan, 2026-11-23 | The README distinguishes this package's optional local runner from JAD's canonical private Development runner. | The private runner's revision and internals are intentionally not reproduced in this public record. |
| Historical coordinator and portfolio measurements; coordinator maintainer | README Validation, Open findings and the dated source records linked there | Dates remain attached to each historical measurement | The 2026-11-16 test result, 2026-11-16 drift/hygiene results and 2026-10-31 assessment are explicitly dated. | They are not represented as current 2026-11-23 measurements. Current README-lane checks are reported in CR3. |

The owner's local integration report records four build packets as integrated on 2026-11-23. This public record does not reproduce its private Development revision or packet contents. The README makes no claim that hosted inference, production deployment, provider behavior or private operational details were independently verified here.

## Verification

- Source inventory: README, the plan casebook and build plan, handoff card, schema, fixture, validator and existing dated records.
- Public-safe evidence rule: only synthetic case IDs and outcomes appear here; private bundles, private test inputs and workstation paths are excluded.
- Remaining limitation: the private Development evidence is represented only by the owner's local integration status; its source revision and detail are not published.
