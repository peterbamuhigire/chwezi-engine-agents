# CR2 first-use walkthrough

**Date:** 2026-11-23

**Source:** README and walkthrough tested at coordinator revision `b9005a848a87d530ec260a869f187f6fb3020304`.

**Method:** Follow each task row from the README to the named local case or oracle, then check its stated outcome and limitation. No hosted service or private data was used.

**Frozen fixture digests (SHA-256):** K1/K3 casebook `docs/plans/ai-engine-kaizen/casebook.md` — `cb00e249cef5153b0926a03affe42e7f901d7ab906c5d52c92b656ed3bcf8921`; IFRS route task `evals/fixtures/033-route-ifrs-leases/task.md` — `9874213958c42743ff16a8aa175a283b8a3251ca22e1c0747bc94a30cb05766e`; route oracle `evals/cases/033-route-ifrs-leases.yaml` — `444fc1fc363475d227439390608f0923b189ecf65c8cc2a9257dfa49aecc86ed`; handoff fixture `tests/fixtures/valid-handoff.yaml` — `b5bcf7092d2d6f1d54cd40f96b12f30fde429b796796612510598bba29bea434`.

## AI-system feature: K1

1. Open the README's **Specify an AI feature** row and follow its link to the orchestrator and the K1 casebook entry.
2. Treat the eight rows as frozen synthetic inputs. The candidate flags five alerts while the named shift profile can review two.
3. Reject that candidate under the two-review profile. Do not treat the fixture penalty or predictions as production measurements; use a different threshold or workflow only after an owner and representative evidence are supplied.

**Observed from the casebook:** the capacity decision is explicit and the next evidence need is stated. **Not assessed:** live classifier output, production data access, and deployment.

## AI-assisted software change: K3

1. Open the README's **Review an AI-assisted code change** row and follow its link to the K3 casebook and handoff card.
2. Send E7 for ticket T1 with `review` twice. The expected observable result is one history entry and a consistent retry response.
3. Send distinct event E8 for T1 with `closed`. Expect a second entry; ticket ID alone cannot be the idempotency key.
4. Continue through the conflict, mid-transaction retry, legacy ticket and concurrency rows in the linked casebook before accepting a real patch.

**Observed from the casebook:** the public import entry point, identity key, retry result and independent acceptance cases are named. **Not assessed:** a production ticket store or deployment.

## Non-AI route: IFRS 16 lease

1. Open the README's non-AI row and follow the task fixture and route oracle.
2. The oracle expects `chwezi-accounting-doctrine/ifrs-leases` as the first skill and forbids inventing an engine or loading every engine.
3. `python -B -X utf8 evals/runners/run-contract-evals.py --route-oracles` reported 77/77 fixture oracles passing but exited 1 because sibling engines were unavailable. That validates fixture/oracle consistency only; the IFRS route was not live-run and remains `NOT ASSESSED`.

## Local non-AI handoff check

The README's **Validate an ordinary handoff** row names a fixture already in this checkout. The exact command, `python3 -X utf8 scripts/validate-contracts.py --schema schemas/handoff.schema.json --instance tests/fixtures/valid-handoff.yaml`, returned `PASS`. This checks envelope shape only; the evidence verifier must still validate the digest and expected revisions.

## Evidence and recovery

The README command validates the existing handoff envelope. The [C01 receipt](../C01/receipt.md) shows how a reviewer-owned expected identity and outcome reject stale evidence. The [AI change handoff](../../../operations/ai-change-handoff.md) uses the event ID or promotion ID to re-read and reconcile a stopped operation; JAD remains owned by private Development. The examples link to local files and mark live work `NOT ASSESSED` when its engine is unavailable.

**Limitation:** this is a documentation walkthrough against synthetic oracles, not an independent production task execution. Live assistant routing and hosted inference remain `NOT_ASSESSED`.

## Independent first-use check

The owner reports that an independent reader used the task table on this README revision, ran `python -B -X utf8 evals/cases/replay_ai_journeys.py`, and accepted the classifier and coding evidence journeys. The reader also ran the documented `python -B -X utf8 scripts/validate-contracts.py --schema schemas/handoff.schema.json --instance tests/fixtures/valid-handoff.yaml` command and observed `PASS`. This corroborates the local examples; it does not assess the live IFRS route or a hosted service. Output was observed in the independent reader?s command output and summarized here; no separate report artifact was retained. Private producer revisions and receipt digests are intentionally omitted from this public record.
