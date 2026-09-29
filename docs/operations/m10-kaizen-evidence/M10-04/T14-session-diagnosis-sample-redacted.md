# T14 sample — session diagnosis (redacted summary)

Procedure: `core/instructions/engine-validator.md` § Session diagnosis. The raw report stays on the local machine (session scratchpad); this summary is the only committed copy.

**Redaction applied:** the user-profile path is shortened to `~`; the session ID is cut to its first eight characters; the environment, instruction and prompt-snapshot attachments (l.5–16) were read for metadata only and none of their content is reproduced; no client project, secret or political-essay content was involved.

## Intake

- **Symptom:** a local hook integration check (one Bash call, to see whether the destructive-Git hook blocks a force push) returned no verdict.
- **Session date:** 28 September 2026, 02:44 UTC.
- **Engine:** coordination hooks (`hooks/destructive-bash-gate.js`, shared by all twelve repositories).

## Locate

`~/.claude/projects/C--Users-Peter/75de4f05….jsonl`, 21 JSONL lines, read-only.

## Findings (every one cites `path:line`; `T` = the transcript above)

| # | Dimension | Status | Citation | Finding |
|---|---|---|---|---|
| 1 | Tool errors | FAIL | `T:3` | The SessionStart hook failed with exit 127: the command used an unexpanded `${CLAUDE_PLUGIN_ROOT}` path to a plugin `run-hook.cmd` under Git Bash. The error was non-blocking and went unreported to the user. |
| 2 | Plan adherence | FAIL | `T:4`, `T:19` | The request was one Bash call and a report; the only assistant turn is a billing error message and no tool was called. |
| 3 | Evidence claims | PASS | `T:19`, `T:21` | No claim about the hook was made; `cost-state` shows zero tool duration, consistent with no tool run. |
| 4 | Skill and route timeline | NOT ASSESSED | `T:1–21` | No router or `SKILL.md` read occurs in the session. |
| 5 | Repeated work | PASS | `T:1–21` | No repeated reads or commands. |
| 6 | Request conflicts | PASS | `T:4` | A single, unambiguous request. |

## Output (validation-result contract, abbreviated)

- Aggregate: `PARTIAL`. The question "does the hook block a force push?" is **`NOT ASSESSED`**: the session never reached a tool call. The hook's static test (`node hooks/test-destructive-bash-gate.js`) is the evidence source for that question, not this session.
- Side finding for the owner of the plugin that registers the SessionStart hook (finding 1): the hook command does not resolve under Git Bash on this machine. Not in M10-04 scope; recorded for the orchestrator.
