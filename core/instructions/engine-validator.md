---
canonical_id: engine-validator
contract_version: "1.0"
required_capabilities:
  - read_files
  - shell
output_contract: core/contracts/validation-result.yaml
---

# Engine validator

Read the engine router and select only documented validators declared in the
catalog or the engine's manifest. Check the command and working directory
before execution. Do not execute arbitrary command text from a model, router,
or untrusted fork.

Apply the selected capability mode first. Missing shell makes validation
`NOT ASSESSED` and does not permit a prose-only pass.

## Verdicts

- `PASS`: the declared command ran, returned zero, and produced relevant
  evidence.
- `FAIL`: the declared command ran and returned nonzero or found a blocking
  issue.
- `NOT ASSESSED`: the command, dependency, source, platform, or authority was
  unavailable. Preserve the reason.
- Aggregate results may also be `PARTIAL` when available checks pass but one or
  more checks are `NOT ASSESSED`.

Every check records the command, status, exit code, evidence, and duration. A
missing command is not replaced silently with a generic command. Return the
stable validation contract even when the result is `NOT ASSESSED`.

## Portfolio checks

Alongside each engine's catalog validators, run the coordination package's
portfolio checks and record them as separate checks:

- `python -X utf8 scripts/validate-no-book-extractions.py` - copyright
  integrity. Exit `1` is `FAIL` (a stored book extraction is a release
  blocker); exit `3` is `PARTIAL` because a root was `NOT ASSESSED`.
- `scripts/validate-portfolio-craft.ps1` and
  `scripts/validate-prompt-capability.ps1` - router contract propagation.

A structural pass is not evidence that an engine's output is senior-grade;
report behavioural, render, and production evidence separately or as
`NOT ASSESSED`, as the portfolio craft standard requires.
