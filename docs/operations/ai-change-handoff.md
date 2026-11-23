# Hand off a reviewed AI change

Use the existing version 1.0 handoff envelope. The SRS producer owns the expected observable outcome. Engineering owns the patch and its revision. The reviewer owns the test and reports the measured outcome. The release operator owns the durable effect record and decides whether to act. Keep those owners attached to their artifacts across a restart.

In the envelope's evidence list, provide a project-relative path, its SHA-256 and format `ai-evidence/1`. The referenced JSON names producer, consumer, case ID, criterion, input and output revisions, measured outcome, limitations and next action. The reviewer supplies the expected identity and outcome independently. Run the [reference verifier](../../evals/contracts/ai_evidence.py) before using any claim. Legacy text evidence remains readable and can be returned for stronger proof.

For a K3 import retry, use the event ID and compare the payload and tested patch. For K4, use the promotion ID and the complete bundle revision. On resumption, re-read the evidence, validate the digest and revisions, and consult the [operator journal example](../../evals/behavioural/ai_recovery.py). A repeated accepted operation returns its prior disposition. Changed inputs under an existing key require reconciliation. An unavailable specialist leaves the claim unassessed. Proceed with another independent artifact within its existing permissions.

Run `python -B -m unittest discover -s tests -p test_ai_coordination.py -v` to exercise stale evidence, missing evidence, restart, and route-versus-task outcomes in synthetic cases.

From the repository root, run the envelope check with python -B scripts/validate-contracts.py --schema schemas/handoff.schema.json --instance evals/contracts/ai-examples/handoff.json. Then run python -B evals/contracts/ai_evidence.py evals/contracts/ai-examples/handoff.json evals/contracts/ai-examples/expected-import.json to compare the evidence with the reviewer expectation.
