# Frozen baseline

Windows checkout at `ab1039c30184b954dc03c3985d3ad6bdda3cd5f0`. Working tree clean before the cycle. Inventory from tracked paths under `skills/`, `scripts/` and `tests/` respectively. One live skill, zero files in a references directory, 45 script files, 97 test and fixture files, 77 contract cases. Generated and ignored files excluded.

The following judgemental scores apply to the stated coverage. 100 requires direct proof across supported paths. 75 means the primary path has evidence with gaps. 50 means substantial failure or indirect coverage. 25 means minimal evidence or major failure. Partial coverage is stated explicitly. Security, privacy, data-loss and licensing blockers stand outside the average.

| Dimension | Score | Confidence | Status | Evidence |
| --- | ---: | --- | --- | --- |
| Routing | 77 | Medium | FAIL | 30/39 gated lexical primary@1, 33/39 engine@1, 3/4 cross-engine activations. 42 lexical cases including 3 declared defects. Live agents NOT_ASSESSED. |
| Skill quality | 80 | Medium | PASS | `skills/rules-distill/SKILL.md` and `core/instructions/engine-orchestrator.md#procedure` define manifest-first discovery, constraints, evidence and handoff. |
| Duplication and drift | 55 | High | FAIL | `scripts/refresh_released_commits.py` exits 1. Marketplace and hook-copy checks report drift. Canonical community runtime ownership declared in `AGENTS.md`. |
| Evidence and currentness | 63 | Medium | FAIL | README has dated historical cases and stated scopes. Two overdue standards listed under maintainer decisions, with live behavioural runs pending. |
| Validators and tests | 72 | High | FAIL | 77 contract shapes pass, malformed neighbouring YAML aborts lexical report generation. Scratch mixed-case test captures traceback and missing JSON. |
| Token cost | 90 | High | PASS | Strict token lint returns 0. AGENTS 11,421 bytes, CLAUDE 324, README 63,787, skill 5,356. Exact startup tokenizer across hosts NOT_ASSESSED. |
| Security and safety | 65 | Medium | FAIL | Project-only public hygiene and hook-copy checks return 1. README F-01 optional MCP dependency issue is separately a blocker. Hook behavior and source inspection are scoped evidence. |
| Install and platform | 52 | Medium | FAIL | README documents fresh-clone update failure and historical Windows gaps. Native installs and Linux runtime NOT_ASSESSED. |
| English and readability | 73 | Medium | PASS | README places Capabilities and start steps early, preserves measured historical results and carries a long calendar and backlog. |
| Kaizen | 75 | High | PASS | `docs/kaizen/2026-11-16-portfolio-drift.md` substantiates 24 local closures and defers 11 pins; unresolved findings carry evidence links. |

Raw mean **70.2**. Published baseline **65**. Critical finding F-01 and any release blocking security or hygiene result must be judged independently of the score. No model-quality, licensing or absence-of-secrets conclusion follows from this run.

## Representative routing trials

Run `python -X utf8 evals/runners/run-contract-evals.py --cases evals/cases --route-oracles --workspace-root <engine-root> --out <scratch-report>`. The table uses literal fixture phrasings from the same fixed report. Rank is the expected skill's position. This is deterministic lexical routing, with twelve acceptance prompt cases scored separately from the 42 lexical oracles. Behavioural execution is NOT_ASSESSED.

| Case | Request | Expected | First result / rank |
| --- | --- | --- | --- |
| `023-route-business-case-roi` | Write a business case with ROI, payback period and NPV for replacing our ERP. | `chwezi-sdlc-documentation/02-business-case` | `chwezi-sdlc-documentation/02-business-case` / 1 / cross-engine miss |
| `024-route-business-case-erp` | Write a business case with ROI for the new ERP. | `chwezi-sdlc-documentation/02-business-case` | `chwezi-sdlc-documentation/02-business-case` / 1 |
| `025-route-lighthouse-cwv` | Run a Lighthouse audit on the company website and fix the Core Web Vitals failures before launch. | `website-skills/deploy` | `website-skills/deploy` / 1 / cross-engine hit |
| `026-route-invoice-typeface` | Pick the typeface and type scale for the invoice PDF. | `chwezi-design-engine/pdf-proposal-and-bankable-document-design` | `chwezi-design-engine/pdf-proposal-and-bankable-document-design` / 1 |
| `027-route-generic-srs` | Write the SRS for the patient billing module. | `chwezi-sdlc-documentation/01-initialize-srs` | `chwezi-sdlc-documentation/20-hr-module-srs` / 2 |
| `028-route-game-srs` | Specify requirements for our mobile puzzle game: levels, player progression, in-app purchases and store certification. | `chwezi-sdlc-documentation/19-game-software-requirements-specification` | `chwezi-sdlc-documentation/19-game-software-requirements-specification` / 1 |
| `029-route-validation-contract` | Assemble the release evidence bundle across the seven evidence categories before we ship the payments feature. | `chwezi-dev-engine/validation-contract` | `chwezi-dev-engine/validation-contract` / 1 |
| `041-route-rest-contract` | Design the REST API contract for the orders service before any code is written. | `chwezi-dev-engine/api-design-first` | `chwezi-dev-engine/api-design-first` / 1 / cross-engine hit |
| `048-route-source-verification` | Verify these market-size claims against primary sources and record the access dates. | `digital-research-skills/source-verification` | `digital-research-skills/source-verification` / 1 |
| `051-route-prd` | Write a PRD for the new customer self-service portal. | `chwezi-sdlc-documentation/01-prd-generation` | `chwezi-dev-engine/new-project` / 4 |
| `053-route-word-report` | Format the Word report with named styles, captions and an automatic table of contents. | `chwezi-design-engine/docx-report-and-document-formatting` | `digital-research-skills/professional-word-output` / 2 |
| `064-route-firewall` | Configure the firewall and install a Let's Encrypt certificate on our Ubuntu web server. | `linux-skills/linux-firewall-ssl` | `linux-skills/linux-firewall-ssl` / 1 |
