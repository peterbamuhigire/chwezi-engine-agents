# Synthetic sample traces and grader outputs (SYNTHETIC — not model output)

Every file in this folder was written by hand for M10-05 to self-test
`scripts/run_behavioural_eval.py` without a model call (zero-spend rule). None
of it was produced by Claude Code or any other model, and none of it is
evidence of agent behaviour. Each event carries `"_synthetic": true` and the
model field `SYNTHETIC-not-a-model`.

- `trace-init-*.jsonl` + `.expect.json`: `system/init` events for the arm
  isolation detector (clean baseline, a baseline contaminated by a user plugin,
  a short-prompt arm that leaks the global routing table or loads the
  user-level `CLAUDE.md`, an engine arm with one and with two plugins, and an
  init without a `plugins` field, which must be `NOT_ASSESSED`).
- `trace-acceptance-*.jsonl`: first-skill detection from a `Skill` tool call
  and from a `Read` of a `SKILL.md`, plus cost extraction (present and absent).
- `trace-mcp-*.jsonl`: the forbidden `pull_engine_ff_only` assertion.
- `grader-*.json`: grader outputs for id-bound validation. `expect` is `valid`
  or `invalid`; invalid cases cover a duplicate id, a missing id, a wrong
  counter, an out-of-range id, a string `passed`, no JSON and a grader that
  returned fewer results than expectations.

The real field names of Claude Code's stream-json events must be re-verified on
the day of any executed run; an unknown shape makes a cell `NOT_ASSESSED`.
