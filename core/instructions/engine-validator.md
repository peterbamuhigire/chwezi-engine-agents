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

## Session diagnosis

Use this procedure when someone reports that an agent session went wrong (a
skill did not load, a plan was abandoned, a check was claimed but not run) and
asks why. It reads transcripts; it never replays or edits them.

1. **Intake.** Record the symptom in the reporter's words, the session date,
   and the engine or engines involved. Without a symptom there is nothing to
   test; ask for one.
2. **Locate.** Find the local transcript read-only: Claude Code keeps
   `~/.claude/projects/<project>/<session>.jsonl`; Codex session logs where
   present. Match on date and working directory. If no transcript can be read,
   the whole diagnosis is `NOT ASSESSED`.
3. **Analyse** along fixed dimensions, one pass each:
   - skill and route timeline (which router and `SKILL.md` files were read,
     and when);
   - plan adherence (steps planned against steps done);
   - repeated work (the same file read or command run again without a reason);
   - tool errors and how they were handled;
   - evidence claims against evidence produced (every "passes", "done" or
     "verified" matched to a command result in the transcript);
   - request conflicts (instructions that contradicted each other or the
     engine router).
4. **Findings.** Every finding cites `path:line` of the transcript (JSONL line
   number) or of the repository file it concerns. A finding without a citation
   is discarded, not softened.
5. **Redaction before sharing.** Remove secrets and tokens, client names,
   private paths beyond the project folder name, and anything from
   `political-essay-skills`. The raw report stays on the local machine; only a
   redacted summary may be committed.
6. **Output.** Return the validation-result contract. Each dimension is a
   check with `PASS`, `FAIL` or `NOT ASSESSED` (for example, an unreadable or
   truncated transcript), and the evidence field carries the citations.

Adapted in paraphrase from obra/superpowers `diagnosing-superpowers` (MIT,
https://github.com/obra/superpowers, commit
8ca22dba9a94f28898bbce59f2537ff4d87c747d). No text copied.

## Portable links

A validation run fails any link that resolves only on the author's host (host-absolute `C:/`, `/C:/`, `file:` links, or links escaping the repository). Cross-engine links are GitHub URLs. See `docs/operations/portable-links-rule.md`.
