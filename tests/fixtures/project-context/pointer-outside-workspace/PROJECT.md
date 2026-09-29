---
project_schema: 1
project_id: demo-clinic
display_name: Demo Clinic
client: Fictional Client
owner: Test Owner
platform: Web application (synthetic fixture)
users_and_jobs:
  - "Receptionist: register a walk-in patient"
purpose_and_success: Replace paper registers; success is a same-day month-end report.
positioning: A fictional clinic system for tests.
operating_context: Intermittent connectivity; shared desktop at the front desk.
constraints:
  - Works offline for a full clinic day
voice_commitments:
  - Plain language
evidence_on_hand:
  present:
    - SRS context folder
  absent: []
accessibility_baseline: WCAG 2.2 AA
jurisdiction:
  country: Uganda
  statutes:
    - Data Protection and Privacy Act, 2019
srs_context: ../outside/_context
research_context: demo-research/projects/demo-clinic/_context
code_repository: demo-app
project_brief: demo-app/PROJECT_BRIEF.md
website_repository: demo-site
brand_brief: demo-site/docs/brand-brief.md
design_tokens: demo-site/docs/design-tokens.md
design_brief: demo-site/docs/design-brief.md
last_reviewed: "2026-09-01"
review_due: "2099-12-31"
---

# Demo Clinic

## Users and jobs

The receptionist registers patients; detail lives in the SRS context.

## Pointers

Each pointer names the authoritative engine folder.
