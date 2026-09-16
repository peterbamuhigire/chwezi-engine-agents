# Kaizen operation: prompt engineering across the engines

Date: 2026-09-17  
Owner: Engine coordination + Digital Research Engine  
Review date: 2026-10-17

## Aim

Improve every standalone engine's ability to generate powerful, domain-specific AI prompts, including prompts for AI-powered software development, without making unsupported prompting folklore part of engine policy. The shared contract must remain portable so a user who forks only one engine still receives the capability.

## Evidence and admission rule

The seven supplied books were treated as untrusted, copyright-protected concept inputs. No raw book text was copied into an engine. Durable practices were admitted only when they added a distinct, inspectable capability and did not conflict with current primary documentation. Current, platform-specific, model-specific, pricing, performance, framework-mandate, or syntax claims required current authoritative verification. Missing or incomplete evidence stayed `NOT_ASSESSED`.

## Supplied-source intake

| Source | Completeness/use | Decision |
|---|---|---|
| Gautam/Rahul, *AI Prompt Engineering Bible: The Ultimate Guide...* | 79 bytes, title only; content unavailable | `INCOMPLETE / NOT_ASSESSED`; no synthesis admitted |
| Tomasz Dylik, *AI Prompt Engineering Bible (7 Books in 1)* | Read across text, visual, audio, video, multimodal, advanced, monetisation, and appendix sections | Admit durable structure, multimodal variables, chaining, RAG boundaries, evals, agent controls, and HITL; reject current/platform/income claims |
| Hamid Tavakoli, *Prompt Engineering for Everyone* | Read chapter map and substantive sections on human-centred prompting, diagnosis, inclusion, governance, and lifecycle | Admit clarity, audience, structure, diagnosis, accessibility, safety, governance, and feedback-loop practices; reject universal outcome claims |
| Mohamed Al-Shamey, *Prompt Engineering Mastery* | Read anatomy, techniques, advanced, cybersecurity, infrastructure/GRC, chaining, and AI-development sections | Admit task-fit techniques, structured security/GRC fields, bounded tools, stop conditions, and versioning; reject framework and current compliance/model claims |
| Majed Alahmad, *Smart Prompt Engineering* | Read essentially the complete 337-line source | Admit seven-field prompt cards, schema validation, supervised automation, tests, experiment logs, and privacy controls; reject income/ROI claims |
| AI Prompt Engineering Team, *AI Prompt Engineering: The 2026 Guide* | Read chapter map and substantive chapters/appendices | Admit 4 Cs as an optional mnemonic, context management, eval/refine, HITL, structured output, and bounded agents; reject 2026/platform/price/temperature/performance claims |
| Harper Winters, *The Prompt Engineering Playbook* | Read chapter sections on foundations, debugging, domains, ethics, libraries, HITL, and agents | Admit outcome/context/constraints/examples, iterative debugging, source verification, libraries, and agent controls; reject productivity and provider claims |

## Practices standardised

The cross-engine contract now requires an evidence-first prompt card: outcome and consumer; trusted context/source boundary and provenance; task, constraints, exclusions and non-goals; output schema; acceptance checks; fallback/refusal and escalation. It also requires a baseline-versus-variant comparison on representative fixtures, failure-slice review, and a record of prompt version, adapter/model, evaluator, result, cost/latency effect, and rollback path.

Frameworks, personas, delimiters, example counts, chain-of-thought requests, sampling parameters, token limits, and provider syntax are optional candidates. They must not be presented as universal laws. Complex reasoning prompts should request observable concise artefacts—assumptions, criteria, options, trade-offs, checks, and unresolved gaps—rather than depend on private chain-of-thought disclosure.

For AI-powered software development, the retained pattern is: scoped repository/context, desired outcome, constraints and non-goals, allowed tools/side effects, staged inspect/plan/implement/verify handoff where useful, tests and acceptance evidence, rollback, and human approval for consequential changes. For research, generated claims inherit source boundaries and verification dates. For visual, marketing, finance, Linux, Windows, proposals, SRS, and web work, domain acceptance gates remain authoritative.

## Currentness and truth gate

The Digital Research Engine verified current primary documentation on 2026-09-17:

- OpenAI prompt engineering: instruction/data separation, context/examples, code-managed prompts, tests, and rollout: [OpenAI Prompt Engineering](https://developers.openai.com/api/docs/guides/prompt-engineering).
- OpenAI evaluation workflow: test data, criteria/graders, and comparison runs: [OpenAI Evals](https://developers.openai.com/api/docs/guides/evals).
- OpenAI model-specific guidance and catalogue were checked for adapter-scoped model facts: [Latest model guidance](https://developers.openai.com/api/docs/guides/latest-model), [Models](https://developers.openai.com/api/docs/models). Account entitlement and active runtime availability remain `NOT_ASSESSED`.
- Anthropic guidance was checked for clarity, context, examples, structured boundaries, tool/research criteria, and agentic safety: [Prompt templates and variables](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables), [Claude Code best practices](https://code.claude.com/docs/en/best-practices).
- PowerShell safety/naming guidance was checked for WhatIf/Confirm/ShouldProcess and approved verbs: [ShouldProcess](https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-shouldprocess?view=powershell-7.6), [Approved verbs](https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/rules/useapprovedverbs?view=ps-modules).
- Frontend validator scope remains bounded to markup validation, not complete UX/accessibility/visual QA: [W3C validator documentation](https://validator.w3.org/docs/users.html).

The source register was updated at `skills-web-dev/docs/source-registers/skills-engine-currentness-2026-09.json` with dated source records and claim mappings. The active Codex configuration was checked with the repository model-policy gate: local policy remains `gpt-5.6-luna` with high reasoning. The official catalogue was checked, but account/runtime entitlement for Luna is `NOT_ASSESSED`; no model switch was justified or made. Configuration changes affect new sessions only.

## Files and engines touched

- Updated the identical `docs/ai-prompting/domain-prompt-compilation-contract.md` in all eleven public domain engines so standalone forks retain the evidence-first capability.
- Updated the shared AI prompt engineering skill in `skills-web-dev` with a superseding standard, including AI-development prompt controls and observable reasoning requirements.
- Updated the business-plan prompt writer, social-media prompt library/training, and Digital Research orchestration skill with domain-specific admission and evaluation rules.
- Updated engine READMEs and this coordination record so the new capability is discoverable.
- Updated the currentness source register; no supplied book was copied into the repositories.

## Validation and residuals

Required checks before release: JSON parse/source-register validation; prompt-contract equality across all eleven engines; engine prompt-capability, catalogue, routing, source-ingestion, and native skill validators; `git diff --check`; and clean, synchronized `main` branches after push. Any unavailable native check is reported as `NOT_ASSESSED`, never as a pass.

Known limitations carried forward: the first supplied book is incomplete; active account entitlement for the configured model is not established; DOCX visual rendering remains environment-dependent; and any pre-existing unrelated engine validator/link drift must remain separately labelled rather than silently repaired in this prompt-only operation.
