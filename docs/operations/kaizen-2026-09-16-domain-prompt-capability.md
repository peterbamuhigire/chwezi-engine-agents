# Kaizen Record: Domain AI Prompt Capability

Date: 2026-09-16
Owner: skills-engine maintainers
Scope: eleven public skills engines and the coordination layer
Source input: `C:\Users\Peter\Downloads\AI_Image_Prompting_Verification_Report.docx`
Additional source inputs: eight supplied book markdown files under
`C:\Users\Peter\Downloads\aigen_markdown\` (read 2026-09-16; concept-only).

## Aim

Make every public engine able to generate a powerful, domain-appropriate AI
prompt when a prompt handoff is the correct output, while preserving direct
execution, safety, evidence, and deterministic-tool boundaries.

## Observe and baseline

The supplied report found a useful image-prompt pattern: name the outcome and
subject, add only relevant composition/execution detail, rank constraints,
separate generation from editing, preserve references explicitly, and inspect
the result. It also found that long prompts, lens terminology, negative
instructions, exact text, reference fidelity, and cross-model universality are
not guarantees.

Repository observation: business-plan and social-media engines already contain
prompt-related skills, but the portfolio had no shared contract or deterministic
check proving that all eleven engine routers exposed prompt-generation guidance.

## Currentness gate

Current claims were checked against primary OpenAI sources on 2026-09-16:

| Claim | Source and scope | Status |
|---|---|---|
| Image prompting should specify subject, composition, style, constraints; edits should state the change and preservation rules; inspect and refine | https://developers.openai.com/api/docs/guides/image-prompting | verified for the current OpenAI image-prompting guide; provider-specific |
| Image generation supports iterative multi-turn workflows | https://developers.openai.com/api/docs/guides/image-generation | verified for the current OpenAI API guide; provider-specific |
| Current model catalogue includes GPT-6 Astra, GPT-5.6 Sol/Terra/Luna, and image models | https://developers.openai.com/api/docs/models | verified as catalogue content accessed 2026-09-16; account entitlement and runtime availability are NOT_ASSESSED |
| Current Codex runner model | Local `C:\Users\Peter\.codex\config.toml` and `skills-web-dev/.codex/ensure_model_policy.py --runtime codex --check` | configured `gpt-5.6-luna`, high reasoning; policy check passed; actual account entitlement remains NOT_ASSESSED because local TUI availability hints list Sol/Astra but not Luna |

Additional currentness checks used for this wave:

| Claim | Source and scope | Status |
|---|---|---|
| Prompt quality improves when identity/instructions, examples, and relevant context are separated; production prompt builders should be code-managed, tested, and rolled out deliberately | https://developers.openai.com/api/docs/guides/prompt-engineering | verified for OpenAI's current guidance; provider-specific |
| Prompt/model changes should use test data and graders rather than demos alone | https://developers.openai.com/api/docs/guides/evals | verified for OpenAI's current eval workflow; grader quality and cross-provider portability remain qualified |
| AI applications need safety measures and human oversight | https://developers.openai.com/api/docs/guides/safety-best-practices | verified within OpenAI application guidance; control design remains product/threat-model specific |
| Coding agents benefit from verification evidence, explore-plan-code separation, specific context, and controlled context/delegation | https://code.claude.com/docs/en/best-practices | verified for current Claude Code guidance; runner-specific |
| PowerShell mutation prompts should account for WhatIf/Confirm, ShouldProcess, and approved verbs; nested operations must be tested explicitly | https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-shouldprocess?view=powershell-7.6 and https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/rules/useapprovedverbs?view=ps-modules | verified for documented PowerShell guidance; command/module implementation still matters |
| Generated markup should be checked with a validator as one part of broader frontend QA | https://validator.w3.org/docs/users.html | verified for W3C validator scope; not a substitute for accessibility, browser, visual, or content review |

Decision: retain the authorised Luna model policy. No model change is justified
by this prompt-capability Kaizen cycle; model quality, cost, latency, and
account availability are not a reason to alter the pins without a separate
verified evaluation and Peter's authorisation.

## Select and experiment

Standardise one shared contract with thin adapters in each router. The contract
uses a nine-part prompt envelope, five modes, a ten-step compiler, risk routing,
visual extensions, an agentic inspect/plan/implement/verify/review-recover
lifecycle, and a required prompt package. Each router adds a domain adapter
with its own failure consequence and acceptance checks.

## Check and adoption evidence

- Central contract added:
  `docs/operations/domain-prompt-compilation-contract-2026-09-16.md`.
- Eleven engine-local contracts added under `docs/ai-prompting/`, so a
  standalone fork has the capability without the coordination checkout.
- Eleven engine routers taught the contract with domain-specific fields.
- Deterministic validator added:
  `scripts/validate-prompt-capability.ps1`.
- Source register updated in `skills-web-dev/docs/source-registers/`.
- `skills-web-dev` AI documentation strengthened for coding-agent task briefs,
  AI feature prompt contracts, prompt/agent evaluation, and prompt-injection
  safety. Obsolete model recommendation examples were removed in favour of
  currentness-gated selection.
- All eleven engine READMEs now advertise the capability and link to their
  local runtime copy.
- The eight books were read as a cross-domain study. Durable contributions were
  admitted as synthesis: explicit objective/context/output, examples,
  one-variable refinement, explore-plan-implement-verify, safe PowerShell
  mutation controls, semantic/accessibility/browser validation, and agent
  evaluation/recovery. Version, price, API, feature, and platform claims were
  withheld unless independently verified.
- DOCX text and tables were extracted successfully. Visual render QA is
  `NOT_ASSESSED`: the packaged renderer lacked `pdf2image`, and LibreOffice
  (`soffice`) was unavailable. The DOCX contains no embedded media.

Validation evidence on 2026-09-16:

- `validate-prompt-capability.ps1`: PASS, 11 engines, identical local contracts.
- `validate-portfolio-craft.ps1`: PASS, 11 engines.
- Coordination catalog and catalog tests: PASS.
- Native checks: SRS, Business Plan, Website, Social Media, Digital Research,
  Accounting, Proposal, Skills Web Dev, Design System, and Windows Admin passed
  their applicable structural/routing gates. Linux routing passed, but its
  native validator retains one pre-existing broken link to
  `digital-research-skills`; this Kaizen did not alter that unrelated finding.
- Codex policy checks passed for 10 engines. Business Plan remains
  `NOT_ASSESSED`/drift because its managed AGENTS policy was already out of sync
  before this change; no model-policy repair was authorised.
- JSON parsing of the updated source register: PASS. Local contract hashes remain
  identical across all eleven engines after the lifecycle update.

## Re-measure and release gates

Run the portfolio validator, each engine's native validator, and `git diff
--check`. A future behavioural evaluation should compile one representative
prompt per engine, then score: intent match, constraint coverage, safety and
permission fidelity, output usability, and failure recovery. No behavioural
pass is claimed by this structural Kaizen record.

## Recovery and next review

Rollback is additive: remove the router sections, central contract, validator,
source entries, and this record while preserving unrelated user changes. Review
on 2026-10-16 or sooner if a receiving model, image workflow, or engine routing
contract changes.
