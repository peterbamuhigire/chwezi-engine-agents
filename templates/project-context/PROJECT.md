---
# PROJECT.md — durable project truth and pointers (contract: chwezi-engine-agents
# docs/operations/project-context-contract.md; schema: schemas/project-context.schema.json).
# Keep values short. Detail stays in the engine folders the pointers name; those folders are
# authoritative, so a conflict is fixed there and this file is corrected to match.
# No typeface, colour or per-surface mode here: those belong to the design brief and tokens.
project_schema: 1
project_id: example-project
display_name: Example Project
client: Example Client Ltd
owner: Named accountable person
platform: Multi-tenant web application with an offline-capable mobile client
users_and_jobs:
  - "Clinic receptionist: register a patient and start a visit in under two minutes"
  - "Facility manager: close the month and file the statutory report"
purpose_and_success: One sentence on the outcome and how success is measured (the SRS vision holds the detail).
positioning: One sentence on who it is for and what it replaces.
operating_context: Where and how it is used (connectivity, power, devices, languages).
constraints:
  - Hard constraint stated once, with its source named in the SRS context
voice_commitments:
  - Plain, respectful language; no jargon without an explanation
evidence_on_hand:
  present:
    - SRS context folder
  absent:
    - Brand brief (not yet written)
accessibility_baseline: WCAG 2.2 AA for every public and staff surface
jurisdiction:
  country: Uganda
  statutes:
    - Data Protection and Privacy Act, 2019
srs_context: chwezi-sdlc-documentation/projects/ExampleProject/_context
research_context: digital-research-engine/projects/example-project/_context
code_repository: example-project
project_brief: example-project/PROJECT_BRIEF.md
website_repository: example-project-website
design_tokens: example-project-website/docs/design-tokens.md
design_brief: example-project-website/docs/design-brief.md
last_reviewed: "2026-09-29"
review_due: "2026-12-29"
---

# Example Project

## Users and jobs

Who uses it and the job each person hires it for. One line per role; personas live in the SRS
context.

## Purpose and success

The outcome and how it is measured. The SRS vision and metrics files hold the targets.

## Positioning and operating context

Who it is for, what it replaces, and the conditions it must survive.

## Constraints and jurisdiction

Hard constraints and the statutes that apply, named rather than summarised.

## Voice

The commitments any engine writing for this project must keep. The brand brief holds the full
voice guide when one exists.

## Evidence on hand

What exists and what is known to be missing, so an absence is stated rather than implied.

## Pointers

Each pointer names the engine folder that stays authoritative for its detail. Where a pointer is
omitted, the absence is listed under evidence on hand.
