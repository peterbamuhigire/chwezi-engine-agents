# M10-12 — skill-graph defect remediation (evidence)

Executor scope: repair the actionable candidate defects that the committed M10-12 GR-01 spike report
(`docs/operations/m10-kaizen-evidence/M10-12/skill-graph-report.json`, generator `scripts/skill_graph.py`) found and that no
existing guardrail catches. Date: 29 Sep 2026. Edits are unstaged; nothing was committed or pushed.

## Before and after

| Report section | Before (committed spike report) | After (`graph-remediation-after/skill-graph-report.json`) |
|---|---|---|
| `missing_skill_paths` | 155 (business-plan 151, dev 3, website 1) | **1** (website-skills, out of scope) |
| `retired_alias_mentions` | 237 (dev 196, digital-research 24, design 9, srs 6, agents 1, website 1) | **20** (see "Left in place" below) |
| `renamed_engine_mentions` | 5 | **1** (website-skills, out of scope) |
| `mentioned_but_unrouted` | 0 | 0 |
| nodes / edges | 1,183 / 12,198 | 1,183 / 12,268 (mentions 9,214 → 9,282, defers_to 529 → 531: prose now names live skills) |

Command: `python -X utf8 scripts/skill_graph.py --workspace-root C:\wamp64\www --out docs/operations/m10-kaizen-evidence/M10-12/graph-remediation-after`
(written to the evidence folder; the committed `docs/skill-graph/skill-graph.json` was not touched).
SHA-256: `skill-graph-report.json` 49fda6d295382d01a8a18ef931067dc561510df693633ca726422904ea6e5442;
`skill-graph.json` 46586007e0e0431dd2dd15f09f671ecc18cf6a61efd62e59b5166b2f0a8de9f0.

## Task 1 — business-plan dangling `skills/NN-...` paths — DONE

244 path occurrences in 54 business-plan files (the report's 151 lines, plus every other stale token in the same files) were
repointed to their real location (`skills/pipeline/NN-...`, `skills/meta-finance/...`, `skills/meta-strategy/...`,
`skills/meta-reporting/...`, `skills/meta-pricing-gtm/...`, `skills/saas/...`). Every replacement target was verified to exist
before writing; zero unresolved paths, so no rewording was needed. Line counts balanced (249 +/249 −), line endings preserved.

Also fixed in dev (in scope, same defect class): `skills/sdlc-meta/reliability-engineering` → `skills/devops-cloud/reliability-engineering`;
`skills/feature-planning/references/prompting-patterns.md` → `skills/product-business/product-discovery/references/feature-planning/references/prompting-patterns.md`;
`skills/experiment-engineering/...` → `skills/ai/ai-feature-rollout-and-experimentation/SKILL.md` plus the retained template path in the
retired alias folder.

## Task 2 — retired alias slugs — DONE_WITH_LIMITATIONS

Only the exact flagged lines were edited (207 lines in dev, digital-research and srs), then 24 hand edits removed duplicates and
self-references created by the substitution. Canonical names come from `chwezi-dev-engine/docs/skill-aliases.yml`
(`inactive_skill_aliases`). Where the canonical skill lives in another engine, the engine is named in brackets. Slugs consolidated
into references of `ai-agent-compliance-controls` became `ai-agent-compliance-controls/references/<slug>`. Where the substitution
would have made a skill point at itself (mysql-engineering, postgresql-engineering, saas-entitlements-and-plan-gating,
world-class-engineering, dpia-generator, mobile-platform-operations, saas-maturity-matrix), the line was reworded to say the work
routes to this skill and that the retired slug is an inactive alias. Historical records (docs/audits, docs/updates, CHANGELOG,
plans, evidence) were not touched.

Decisions taken under Peter's delegated authority (decided by orchestrator under Peter's delegated authority, 29 Sep 2026):
- `ux-for-ai` → `ai-agent-ux` (design-system-skills). The dev alias map names `design-system/skills/ai-ux`, which does not exist.
- `ux-principles-101` → `ux-psychology` (design-system-skills). The dev alias map names `design-system/skills/ux-foundations`, a
  consolidation that `skill-aliases.yml` marks `status: planned` and that was never created. `ux-psychology` is the existing
  design skill on that absorb list.
- `pos-sales-ui-design`, `pos-restaurant-ui-standard` → `finance-ui-pattern-library` (chwezi-accounting-doctrine), as the alias map says.
- `mobile-reports` → `professional-word-output`, as the alias map says.

Left in place on purpose (9 hits):
- 3 × "Consolidated from skills/ai/<slug>/SKILL.md" provenance headers in `ai-agent-compliance-controls/references/*/entrypoint.md:1` (historical provenance).
- 3 × `ai-agent-compliance-controls/references/routing.md:12-14`: rows that name the consolidated reference entries and link to them.
- `ai-assisted-development/SKILL.md:159`: second line of a provenance sentence ("absorbed from the retired `inherit-legacy-style` skill"); the scanner reads one line at a time.
- `implementation-status-auditor/references/plan-implementation.md:35`: the reference's own boilerplate.
- `srs-skills/.../system-orientation-guide.md:87`: a valid file path (`doc-architect/references/code-tour.md`), a scanner false positive.

Out of scope, reported (11 hits): design-system-skills 9 (`ux-for-ai` ×2, `android-data-persistence` ×2, `pos-sales-ui-design` ×2,
`ux-principles-101` ×1, `dual-auth-rbac` ×2); website-skills 1 (`seo/references/analytics-event-map.md:290`, `uganda-dppa-compliance`;
M10-11 owns website); chwezi-engine-agents `README.md:55` (a valid `world-class-engineering/references/verification-loop.md`
path, a scanner false positive).

## Task 3 — renamed engine folders — DONE (4 of 5; 1 reported)

- `C:\wamp64\www\digital-research-skills\docs\...` → `C:\wamp64\www\digital-research-engine\docs\...` in the language references of
  business-plan-skills, proposal-skills and social-media-skills. The target file exists. The catalogue id `digital-research-skills` was not changed anywhere.
- `srs-skills/.../book-driven-kaizen-wave-3-2026-09-02.md:5`: `skills-web-dev/docs/continuous-improvement/` → `chwezi-dev-engine/docs/continuous-improvement/` (exists).
- website-skills `skills/content-copy/language-standards/references/english-collocations-and-lexical-precision-2026-09-02.md:3`: same
  fix needed. **Not edited** (M10-11 scope). Its missing-path hit (`brand-voice/references/voice-profile-schema.md:6`) is an ECC
  attribution line, which is a historical record, so no fix is recommended.

## Verification (all run 29 Sep 2026, zero spend)

| Repo | Command | Result |
|---|---|---|
| chwezi-dev-engine | `scripts/skill_catalog_guardrails.py` | exit 0; skill-bytes warnings are report-only and existed before this change (CRLF working copy vs LF blob) |
| chwezi-dev-engine | `scripts/routing_smoke_test.py --min-rank1 88 --lint-fixtures` | p@1 173/191 (90.6%), p@3 100%, 0 negative failures, 0 lint; floor 88 met |
| chwezi-dev-engine | `scripts/routing_smoke_test.py --collisions --collision-gate --threshold 0.5` | 1 allow-listed pair; gate 0 errors |
| chwezi-dev-engine | `validate_engine_control_plane.py`; `contract_gate.py --all`; `source_ingestion_guardrail.py` | PASS; 161 scanned 0 errors; 0 findings |
| chwezi-dev-engine | `python -m pytest tests -q` | 207 passed, 3 skipped |
| chwezi-dev-engine | active SKILL.md count (`skills` + `00-meta-initialization`) | **167** (unchanged) |
| business-plan-skills | `validate_skill_engine.py --baseline ...`; `routing_smoke_test.py --threshold 1.0`; `routing_link_check.py`; `source_ingestion_guardrail.py`; unittest | 137/137 compliant; 61/61 (100%); 0 failures; 0 findings; exit 0 |
| digital-research-engine | `validate_engine.py`; `skill_contract_validator.py --baseline ...`; `routing_smoke_test.py --min-rank1 84 --lint-fixtures`; `check_no_book_extractions.py` | exit 0; 59/59; p@1 25/29 (86.2%), floor 84 met; OK |
| srs-skills | `validate_skill_engine.py --baseline ...`; `routing_smoke_test.py --min-rank1 83 --lint-fixtures`; `python -m engine validate-skills`; pytest owned-negatives + tier1; guardrail | exit 0; p@1 47/55 (85.5%), floor 83 met; SKILLS OK; 12 passed; 0 findings |
| proposal-skills | `validate_skills.py --baseline ...`; `routing_smoke_test.py` | 115 skills 0 findings; 25 fixtures 100% |
| social-media-skills | `validate_skill_engine.py --baseline ...`; `routing_smoke_test.py` | 191/191; 56/56 |
| chwezi-engine-agents | `render_host_files.py --check --workspace-root C:\wamp64\www` | 12 repositories, 0 findings |

## Open items

1. Dev `docs/skill-aliases.yml` maps `skills/ai/ux-for-ai` → `design-system/skills/ai-ux` and `skills/frontend-ux/ux-principles-101` →
   `design-system/skills/ux-foundations`; neither target exists. The alias map should be corrected by the dev engine's owner (not edited here).
2. The design-system-skills (9) and website-skills (2) hits above need their owners' fixes.
3. Scanner refinements for `skill_graph.py`: add "consolidated" to `RETIREMENT_WORDS`; do not flag a slug that is the stem of an
   existing `references/<slug>.md` path. These would remove 5 known false positives.
4. The mapping `mobile-reports` → `professional-word-output` reads oddly in mobile report-UI contexts; the dev owner may want a better target.

## Changed files

### business-plan-skills (55 files)

- `C:/wamp64/www/business-plan-skills/skills/language/writing-quality/references/english-collocations-and-lexical-precision-2026-09-02.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-finance/meta-agent-bankability-and-investor-readiness/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-finance/meta-agent-revenue-recognition-policy/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-finance/meta-agent-sla-financial-controls/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-finance/meta-agent-valuation-adjustments/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-finance/meta-agent-valuation-overlay-for-sla/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-finance/meta-agent-valuation-overlay-for-sla/references/saas-agent-sla-valuation-adjustments.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-finance/meta-ai-bankability-and-investor-readiness/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-finance/meta-ai-valuation-adjustments/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-finance/meta-bankability-scoring/references/saas-agent-bankability-checklist.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-finance/meta-bankability-scoring/references/saas-agent-sla-bankability-checklist.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-finance/meta-bankability-scoring/references/saas-bankability-scorecard.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-finance/meta-financial-stress-test/references/saas-agent-sla-stress-test-scenarios.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-finance/meta-valuation/references/saas-agent-sla-valuation-adjustments.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-finance/meta-valuation/references/saas-agent-valuation-adjustments.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-reporting/meta-agent-board-and-investor-reporting/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-reporting/meta-agent-board-and-investor-reporting/references/saas-agent-sla-board-block.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-reporting/meta-board-and-investor-reporting/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/meta-strategy/meta-due-diligence/references/saas-agent-sla-data-room-contents.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/01-executive-summary/references/saas-agent-sla-executive-summary-paragraph.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/03-products-services/saas-agent-product-strategy-and-roadmap/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/03-products-services/saas-ai-product-strategy-and-roadmap/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/06-competitive-analysis/references/ai-moats-vs-false-moats.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/06-competitive-analysis/references/saas-moats-and-defensibility.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/06-competitive-analysis/saas-agent-moat-and-wrapper-risk/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/06-competitive-analysis/saas-ai-moat-and-defensibility/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/07-marketing-sales-strategy/references/ai-feature-pricing-and-positioning.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/07-marketing-sales-strategy/saas-agent-commercial-packaging-economics/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/07-marketing-sales-strategy/saas-agent-outcome-pricing-business-case/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/07-marketing-sales-strategy/saas-agent-pricing-strategy/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/07-marketing-sales-strategy/saas-ai-pricing-strategy/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/09-management-team/saas-agent-talent-strategy/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/10-financial-projections/saas-agent-deferred-revenue-and-credit-reserves/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/10-financial-projections/saas-agent-revenue-recognition/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/10-financial-projections/saas-agent-revenue-recognition/references/saas-agent-revenue-recognition-policy-template.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/10-financial-projections/saas-agent-sla-cogs-treatment/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/10-financial-projections/saas-agent-sla-economics-in-projection/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/10-financial-projections/saas-agent-sla-economics-in-projection/references/africa-agent-sla-context.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/10-financial-projections/saas-agent-unit-economics-and-cogs/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/10-financial-projections/saas-ai-cost-of-tenant-calculator/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/10-financial-projections/saas-ai-cost-of-tenant-calculator/references/saas-agent-cost-of-tenant-extension.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/10-financial-projections/saas-ai-unit-economics-and-cogs/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/11-funding-request/saas-agent-funding-stage-playbook/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/11-funding-request/saas-agent-investor-narrative-on-sla/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/11-funding-request/saas-agent-investor-narrative-on-sla/references/saas-agent-sla-investor-narrative.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/11-funding-request/saas-ai-funding-stage-playbook/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/12-risk-analysis/references/saas-agent-risk-register-template.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/12-risk-analysis/saas-agent-risk-and-stress-test/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/12-risk-analysis/saas-agent-sla-risk/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/12-risk-analysis/saas-agent-sla-risk/references/saas-agent-sla-risk-register.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/13-implementation-timeline/saas-agent-implementation-timeline/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/16-sustainability-strategy/saas-agent-sustainability-and-ethics/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/pipeline/16-sustainability-strategy/saas-ai-sustainability-and-ethics/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/saas/saas-bankability-and-investor-readiness/SKILL.md`
- `C:/wamp64/www/business-plan-skills/skills/saas/saas-valuation-and-fundraising-strategy/SKILL.md`

### chwezi-dev-engine (109 files)

- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-agent-commercial-operations/references/ai-agent-pricing-engine/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-agent-commercial-operations/references/ai-agent-sla-and-commitments/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-agent-commercial-operations/references/ai-agent-sla-credit-automation/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-agent-compliance-controls/references/ai-agent-audit-log-integrity/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-agent-compliance-controls/references/ai-agent-hipaa-security-controls/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-agent-compliance-controls/references/ai-agent-iso27001-controls/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-agent-compliance-controls/references/ai-agent-memory-erasure-proof/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-agent-compliance-controls/references/ai-agent-soc2-controls/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-agent-compliance-controls/references/ai-agent-soc2-controls/references/trust-criteria-mapping.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-agent-governance-and-limits/references/ai-agent-cost-and-step-budgets/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-agent-runtime-architecture/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-agent-tooling-and-hitl/references/ai-agent-tool-catalogue-and-action-gating/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-agent-tooling-and-hitl/references/ai-agents-tools/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-app-architecture/references/ai-on-saas-architecture/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-cost-and-metering/references/ai-cost-modeling/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-cost-and-metering/references/ai-cost-per-tenant-attribution/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-cost-and-metering/references/ai-saas-billing/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-cost-and-metering/references/ai-usage-metering-and-billing/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-cost-and-metering/references/ai-usage-metering-and-billing/references/stripe-metered-billing-for-ai.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-incident-response/references/ai-incident-evidence-capture/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-llm-integration/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-model-gateway/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-rag-patterns/references/ai-rag-multi-tenant/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-security/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-security/references/ai-tenant-isolation-patterns/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ai/ai-web-apps/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/android/android-development/references/android-biometric-login.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/architecture/api-design-first/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/architecture/microservices-architecture/references/microservices-architecture-models.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/architecture/microservices-architecture/references/microservices-communication.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/architecture/microservices-architecture/references/microservices-fundamentals.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/architecture/microservices-architecture/references/microservices-resilience.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/architecture/validation-contract/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/architecture/validation-contract/references/evidence-categories.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/backend-databases/database-design-engineering/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/backend-databases/mysql-engineering/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/backend-databases/postgresql-engineering/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/backend-databases/postgresql-engineering/references/postgresql-patterns.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/backend-databases/postgresql-engineering/references/postgresql-patterns/references/pgvector.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/devops-cloud/cicd-pipelines/references/cicd-devsecops/references/compliance-mapping.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/devops-cloud/kubernetes-platform/references/kubernetes-saas-delivery/references/offboarding-data-deletion.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/devops-cloud/observability-monitoring/references/observability-platform.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/execution-plan-scripts/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/finance-accounting/accounting-engine/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/finance-accounting/electronic-fiscal-taxing/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/frontend-ux/pos-sales-operations-engineering/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/frontend-ux/tailwind-css/references/grid-systems/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/game-development/game-ai-behaviour-and-navigation/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/game-development/game-development-orchestration/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/gis/gis-enterprise-domain/references/real-estate-saas-integration.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/gis/gis-platform-engineering/references/gis-maps-integration/references/a11y-maps.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ios/ios-development/references/ios-project-setup.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ios/ios-development/references/skill-deep-dive.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ios/ios-monetization/references/cross-platform-entitlement-reconciliation.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ios/ios-platform-capabilities/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ios/ios-platform-capabilities/references/ios-biometric-login/skill-deep-dive.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ios/ios-platform-capabilities/references/ios-networking-advanced/offline-queue.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ios/ios-security-and-rbac/references/ios-app-security.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ios/ios-security-and-rbac/references/ios-app-security/data-protection-classes.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ios/ios-security-and-rbac/references/ios-app-security/keychain-secure-enclave.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/ios/ios-security-and-rbac/references/ios-app-security/privacy-manifest.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/languages/python-ml-predictive/references/explainability.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/mobile-cross/mobile-platform-operations/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/mobile-cross/mobile-platform-operations/references/mobile-saas-planning.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/product-business/customer-service-excellence/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/product-business/product-led-growth/references/habit-forming-products/entrypoint.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/multi-tenant-saas-architecture/references/saas-deployment-models-decision-tree.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-accounting-system/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-accounting-system/references/financial-statements.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-admin-backoffice-tooling/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-admin-backoffice-tooling/references/bulk-operations.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-admin-backoffice-tooling/references/impersonation-design.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-admin-backoffice-tooling/references/internal-roles-and-permissions.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-architecture-strategy/references/saas-maturity-matrix.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-business-metrics/references/revenue-lifecycle-data-contract.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-business-metrics/references/saas-growth-metrics/references/guardrail-metrics.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-entitlements-and-plan-gating/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-entitlements-and-plan-gating/references/entitlements-vs-feature-flags.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-erp-system-design/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-rate-limiting-and-quotas/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-sales-organization/references/hiring-rubrics.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-sales-organization/references/onboarding-ramp.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-sales-organization/references/sales-assist-product-capabilities.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-sso-scim-enterprise-auth/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-tenant-data-portability-and-erasure/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-tenant-data-portability-and-erasure/references/erasure-cascade.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-tenant-data-portability-and-erasure/references/export-format-spec.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/saas-tenant-data-portability-and-erasure/references/requester-verification.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/saas/subscription-billing/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/implementation-status-auditor/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/implementation-status-auditor/references/plan-implementation.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/sdlc-documentation/references/sdlc-design.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/sdlc-documentation/references/sdlc-design/templates/api-documentation.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/sdlc-documentation/references/sdlc-design/templates/interface-control-document.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/sdlc-documentation/references/sdlc-design/templates/system-design-document.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/sdlc-documentation/references/sdlc-maintenance.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/sdlc-documentation/references/sdlc-planning.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/sdlc-documentation/references/sdlc-testing.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/sdlc-documentation/references/sdlc-testing/templates/software-test-plan.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/skill-composition-standards/references/baseline-contract-register.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/skill-writing/references/prompting-patterns-for-skills.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/sdlc-meta/world-class-engineering/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/security/dpia-generator/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/security/network-security/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/security/network-security/references/zero-trust.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/security/web-app-security-audit/SKILL.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/security/web-app-security-audit/references/access-control-flaws.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/security/web-app-security-audit/references/auth-session-flaws.md`
- `C:/wamp64/www/chwezi-dev-engine/skills/security/web-app-security-audit/references/business-logic-flaws.md`

### digital-research-engine (6 files)

- `C:/wamp64/www/digital-research-engine/skills/capability-matrix/SKILL.md`
- `C:/wamp64/www/digital-research-engine/skills/capability-matrix/references/companion-rules.md`
- `C:/wamp64/www/digital-research-engine/skills/capability-matrix/references/domain-rationale.md`
- `C:/wamp64/www/digital-research-engine/skills/skill-composition-standards/references/baseline-contract-register.md`
- `C:/wamp64/www/digital-research-engine/skills/validation-contract/SKILL.md`
- `C:/wamp64/www/digital-research-engine/skills/validation-contract/references/evidence-categories.md`

### srs-skills (5 files)

- `C:/wamp64/www/srs-skills/01-strategic-vision/01-prd-generation/references/opportunity-and-product-risk-evidence.md`
- `C:/wamp64/www/srs-skills/02-requirements-engineering/fundamentals/during/05-conceptual-data-modeling/references/data-quality-nfr-catalogue.md`
- `C:/wamp64/www/srs-skills/03-design-documentation/01-high-level-design/references/solution-design-views-and-controls.md`
- `C:/wamp64/www/srs-skills/09-governance-compliance/31-kaizen-engine-and-product-improvement/references/book-driven-kaizen-wave-3-2026-09-02.md`
- `C:/wamp64/www/srs-skills/AGENTS.md`

### proposal-skills (1 files)

- `C:/wamp64/www/proposal-skills/skills/language/language-standards/references/english-collocations-and-lexical-precision-2026-09-02.md`

### social-media-skills (1 files)

- `C:/wamp64/www/social-media-skills/skills/language/language-standards/references/english-collocations-and-lexical-precision-2026-09-02.md`
### chwezi-engine-agents (evidence only)

- `C:/wamp64/www/chwezi-engine-agents/docs/operations/m10-kaizen-evidence/M10-12/M10-12-graph-defect-remediation.md`
- `C:/wamp64/www/chwezi-engine-agents/docs/operations/m10-kaizen-evidence/M10-12/graph-remediation-after/skill-graph-report.json`
- `C:/wamp64/www/chwezi-engine-agents/docs/operations/m10-kaizen-evidence/M10-12/graph-remediation-after/skill-graph.json`
