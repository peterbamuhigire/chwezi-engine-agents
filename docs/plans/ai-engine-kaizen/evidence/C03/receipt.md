# AC-C03 recovery and ownership

The orchestrator links to docs/operations/ai-change-handoff.md. The K3/K4 example uses a SQLite journal with one owner per effect. The test closes and reopens its database, revalidates the source evidence, retries the accepted request, rejects a stale revision and observes exactly two effects across two independent operation keys. An absent specialist returns NOT_ASSESSED and the separate release handoff proceeds.

Independent review identified that an omitted replay key raised an exception. The corrected entry point now rejects an absent or blank key before recording any effect. Run the coordinator fixture tests. Tests exercise local restart and idempotency. The example grants no remote permissions and does not execute deployments.
