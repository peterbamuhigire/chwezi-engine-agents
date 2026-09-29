# SYNTHETIC sample traces

Both files are hand-written, **synthetic** stream-json traces. No model produced them and they are
not evidence of any run. They exist only to self-test `verify_answers.py --check-trace`
(`assert_no_forbidden_tool`):

- `synthetic-clean-trace.jsonl` uses only read-only coordinator tools; the check must PASS.
- `synthetic-forbidden-trace.jsonl` invokes `pull_engine_ff_only`; the check must FAIL.
