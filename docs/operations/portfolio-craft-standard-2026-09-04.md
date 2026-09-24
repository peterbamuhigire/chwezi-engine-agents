# Portfolio Craft Standard

Status: mandatory cross-engine delivery contract
Owner: engineering-engine maintainer
Effective: 2026-09-04
Review: 2026-10-04

## Purpose

AI can produce a large first draft quickly. That is useful only when the team
keeps ownership of the decisions, checks the work in context, and improves it
in small units. This standard makes that behaviour explicit for every product
made by the eleven skills engines.

The user brief that triggered this standard is an internal quality signal, not
an external authority. No current technology, platform, market, legal, safety,
or benchmark claim is admitted by this document. Such claims still pass the
Digital Research `source-evaluation` and `source-verification` routes.

## Non-negotiable operating rule

Do not generate an entire product, proposal, plan, campaign, design system, or
research report as one opaque batch and call the result finished. Work through
small, named slices. Each slice must be understood, exercised, reviewed, and
refined before the next slice is admitted.

## The craft loop

For every meaningful output, record the following in the project log, evidence
pack, or delivery manifest. A lightweight task may keep the record inline.

1. **Frame.** Name the audience, job, desired decision or behaviour, constraints,
   evidence boundary, and consequence of getting it wrong.
2. **Choose one slice.** Select one user journey, screen/state, requirement,
   argument, financial assumption, content unit, research claim, or operational
   procedure. State why it is the next slice.
3. **Inspect.** Read the relevant existing code, data flow, content, references,
   visual context, or operating state before changing it. Do not replace a
   working pattern without recording the reason.
4. **Make the smallest useful change.** Give the slice a real owner, real
   content or data, explicit states, and a clear decision. Avoid scaffolding
   that has no path to use.
5. **Exercise it in context.** Check the normal path and at least one relevant
   failure, empty, denied, interrupted, or counter-case path. Render or read it
   where appearance or language is part of the result.
6. **Refine.** Compare the result with the frame. Fix one concrete defect or
   remove one unnecessary element. Preserve a deliberate choice that works.
7. **Record the proof.** Capture the command, test, render, source locator,
   reviewer observation, or explicit `NOT ASSESSED` state. Then select the next
   slice.

The loop is also mandatory for the kaizen operation itself. A portfolio audit
that only adds prose has not improved the engines.

## Product-specific craft floors

| Product family | Required evidence of care before release |
|---|---|
| Software and APIs | One critical vertical slice traced from actor to UI/API, domain rule, data store, side effect, telemetry, and recovery; code read in context; tests cover normal and failure behaviour; dependencies and APIs are verified. |
| Design and UI | A visual thesis and named rationale for type, colour, layout, density, assets, and motion; real content; all key states; keyboard/touch and reduced-motion checks; rendered review at relevant breakpoints. |
| Websites | One journey at a time from entry page to conversion or task completion; meaningful copy and assets; responsive, accessible, fast-loading, empty/error/consent states; browser/render evidence and a launch or rollback path. |
| Proposals | One decision-maker and decision per section; a clear win thesis; sourced claims; explicit assumptions, counter-case, delivery proof, risks, commercial logic, and next action; section-level revision before assembly. |
| Business plans | A model that reconciles with the narrative; customer and operating evidence; staged milestones; downside case; funding use; sensitivity or uncertainty; a readable plan whose recommendations survive challenge. |
| Social media | Audience and channel job per post; distinctive point of view; platform-fit format and length; real examples or approved evidence; purposeful visual/audio direction; moderation, correction, and measurement loop. |
| Research and analysis | Claim-level provenance, support state, uncertainty, contradiction handling, and independent verification; synthesis must add judgement rather than repeat sources. |
| Accounting and finance | Source and reporting basis; immutable and reversible treatment; reconciliations, controls, approval, audit trail, and exception handling; no invented rate or statutory value. |
| Infrastructure and administration | Exact target and ownership; staged change; preview/before state; per-target outcome; health verification; recovery and rollback; live or lab gaps marked `NOT ASSESSED`. |
| Requirements and governance | Testable requirements with actors, states, constraints, acceptance oracles, traceability, decision records, and unresolved questions; no invented stakeholder intent; no implementation choices; complete enough that engineering and design can build and test without a clarification round. |

## Release evidence

Every release record separates these evidence types rather than treating a
clean lint or polished page as proof of the whole product:

- **Structural:** files, links, schema, routing, lint, and catalogue checks.
- **Behavioural:** tests, scenarios, failure paths, calculations, moderation,
  or user-task checks.
- **Render or reader:** browser, device, document, slide, spreadsheet, or
  read-aloud review when presentation is part of the promise.
- **System or production:** integration, deployment, live/lab, performance,
  observability, recovery, or stakeholder evidence.
- **Handoff:** owner, known limits, open risks, next action, and re-audit date.

Missing evidence is `NOT ASSESSED`, not a pass. A safety, privacy, financial,
legal, accessibility, data-loss, or release blocker remains a blocker even when
the numerical score is high.

## Anti-slop interpretation

Specificity is not decoration. It means a named user, real decision, actual
state, concrete example, verified source, meaningful asset, measured criterion,
or observed failure. Remove a section, component, slide, post, abstraction, or
metric when it has no such job. Do not use polish, animation, citations, or
checklists to conceal weak substance.

The craft standard works with, and does not replace, each engine's anti-slop,
source, finance, accessibility, security, and domain gates.

## Senior-practitioner bar

Most output is drafted by AI agents. It is releasable only when a senior human
practitioner in that domain would accept it without rewriting it. Before
release, answer each question with evidence or `NOT ASSESSED`:

1. **Specific.** Could this output have been produced for a different client,
   product, or market by changing only the names? If yes, it is generic; rework
   the slice around the named user, decision, and context.
2. **Decided.** Does it make and justify choices (trade-offs, exclusions,
   thresholds) rather than listing options or restating best practice?
3. **Buildable or actionable.** Can the next owner act on it without a
   clarification round? Requirements must let engineering and design build and
   test without inventing intent; designs must specify states and evaluation;
   code must carry its tests and rollback path.
4. **Proven.** Is every claim of quality backed by the evidence types above,
   with the unperformed ones named as `NOT ASSESSED`?
5. **Reviewed.** Was the slice reviewed against the frame by someone or
   something other than its author (independent agent pass, human reviewer, or
   executable check)? Record which; a self-review alone is recorded as such.

Missing answers are gaps, not passes. `NOT ASSESSED` and `NOT_ASSESSED` are the
same verdict. Cross-engine ownership of these questions (requirements, build,
design, research, finance) is routed by
`core/instructions/engine-orchestrator.md`.

## Content integrity

No engine stores book extractions, book summaries, chapter notes, or
`book-extractions/`, `extracted-books/`, or `book-study/` folders. Book
knowledge enters only as paraphrased, task-oriented procedures, decision rules,
checklists, rubrics, and original examples with a short `Sources` line.
`scripts/validate-no-book-extractions.py` enforces this by path.

## Kaizen contract

Use `Observe -> Baseline -> Select -> Experiment -> Check -> Standardise ->
Teach -> Re-measure`. Publish the raw score, the portfolio cap of
`min(raw_score, 65)`, blockers, evidence gaps, reversible change, owner,
measure, rollback condition, and next review. A 95/100 result is a target until
the acceptance evidence exists.

