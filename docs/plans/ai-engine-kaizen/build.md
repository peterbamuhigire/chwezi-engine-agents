# skills-engine-agents · AI capability implementation

**Current handoff.** Committed task evidence: C01. Remaining: C02, C03, C04.
**Accountable owner** Peter. **Execution role** Coordination maintainer. **Observed starting revision** `9b87cbc19de0c5927f4bb66c959157b32c152777`. Recheck the revision on staging. Apply ordinary commits to the isolated JAD branch. Link a receipt for each criterion. All tasks begin pending.

**User journey** discover owner → transfer contract → accept or return evidence. The owner's named scope covers this repository's own contracts, fixtures and README. D-11 keeps private Development's runner canonical. Do not propagate runner code or add an implicit private dependency.

**Entry condition** Obtain accepted SRS and engineering receipts, or replay a clearly labeled synthetic substitute for the isolated fixture. C04 requires the actual cross-engine receipt reconciliation.

**Inputs** Use [casebook.md](casebook.md) for the fixture data and expected outcomes and [sources.json](sources.json) for external evidence. B1 Joel Grus, B2 Thomas Nield, B3 Albrecht/Ramachandran/Winkler, B4 Parikh/Johri, B5 Neroda/Escaravage/Peters, B6 David Foster, B7 Sanseviero/Cuenca/Passos/Whitaker, B8 Brousseau/Sharp. R IDs refer to primary sources in the register. Use the latest verified source for any new API, model version, security or vendor-specific claim. Close the capability through its normal route.

## Ordered tasks

### C01 · Extend coordination evidence compatibly

**Depends on** Entry condition only. **Owned surfaces** `schemas`, `evals/contracts`, `tests`. **Basis** B4 B5 B8 R01 R09.

Use the existing handoff 1.0 fields to reference a versioned AI evidence record. Give it producer, intended consumer, case ID, input and output revisions, measured outcome, limitations and next action. Bind its digest to the evidence file. Add a new optional typed record only if existing fields cannot express the requirement.

**AC-C01.** A legacy handoff remains valid. Positive data, code and evaluation handoffs are parsed. A wrong digest, unknown revision or missing evidence yields a blocked claim and a specific next action. A schema-valid envelope alone cannot mark a task accepted.

**Evidence.** Commit the fixture, result and failures under `docs/plans/ai-engine-kaizen/evidence/C01/`. Record source revision, receipt digest, exact command or review procedure, inputs, limitations and the acceptance ID. Update the sidecar with the observed result.

### C02 · Measure route choice and downstream behavior separately

**Depends on** C01. **Owned surfaces** `scripts/lib/retrieval_metrics.py`, `evals/behavioural`, `evals/routing`, `tests`. **Basis** B1 B2 B3 R05 R09.

Reuse the existing ranked metrics conventions and behavioural harness. Add disjoint original query families for ML triage, code review, release recovery and ambiguous/no-route requests. Capture routing rank, completion and abstention as separate decisions.

Preserve source evidence for each labeled case. Include an ambiguous family, an out-of-scope request, a near duplicate and a held-out intent. Label the retrieval harness as a proxy for actual task execution.

**AC-C02.** For ranked IDs X,Y with only Y relevant, reciprocal rank is 0.5. Empty permitted corpus yields the specified no-route result. A correct top route followed by an incorrect output counts as a routing success and execution failure, with denominators recorded. Deduplicating query families changes the denominator explicitly. The report never converts a retrieval proxy into a live execution pass.

**Evidence.** Commit the fixture, result and failures under `docs/plans/ai-engine-kaizen/evidence/C02/`. Record source revision, receipt digest, exact command or review procedure, inputs, limitations and the acceptance ID. Update the sidecar with the observed result.

### C03 · Coordinate a bounded AI-built change and preserve recovery evidence

**Depends on** C01. **Owned surfaces** `agents`, `docs/operations`, `evals/behavioural`, `tests`. **Basis** B4 B5 B8 R09 R10.

Add a coordination card with the SRS, engineering, reviewer and operator handoffs for K3/K4. Include task-to-revision identity, replay keys, evidence rejection, approved scope and one owner per mutable artifact. Keep runner maintenance with private Development.

**AC-C03.** A stopped handoff resumes without accepting a stale test receipt, writing twice or broadening permissions. An unavailable specialist leaves its result NOT_ASSESSED while independent tasks proceed. Legacy coordination remains valid.

**Evidence.** Commit the fixture, result and failures under `docs/plans/ai-engine-kaizen/evidence/C03/`. Record source revision, receipt digest, exact command or review procedure, inputs, limitations and the acceptance ID. Update the sidecar with the observed result.

### C04 · Exercise both cross-engine journeys at the accepted revisions

**Depends on** C02, C03. **Owned surfaces** `evals/cases`, `tests`, `docs/operations`. **Basis** B3 B4 B5 B8 R05 R09 R12.

Replay a synthetic AI-feature request and a deterministic code-maintenance request against the SRS, public engineer and private Development receipts. Exchange only public-safe case IDs and synthetic records. Keep any private bundle in local evidence. Record exact producing revisions and whether a transfer was simulated.

**AC-C04.** The classifier journey reaches the documented prediction and outcome checks. The coding journey catches the bad patch through K3. Missing provider evidence stays missing. The coordinator reports which route, producer, artifact and criterion failed if a receipt is removed.

**Evidence.** Commit the fixture, result and failures under `docs/plans/ai-engine-kaizen/evidence/C04/`. Record source revision, receipt digest, exact command or review procedure, inputs, limitations and the acceptance ID. Update the sidecar with the observed result.

## Verification, replay and handoff

Preserve the repository's configured slice and final checks. Run the narrow check for the changed behavior as well. Exercise a negative control by removing a required input or introducing the named defect. Record which assertion fails. Repeat on the repaired revision. Existing tests cover only their actual scope. A documentation example may be validated by an independent walkthrough with observed outputs. A trained-model, hosted or production claim requires that environment's evidence.

Keep an independent test oracle and the frozen synthetic case IDs. Use original product-safe work in public repositories. The book files and window receipts stay outside all engines. Link any additional task-specific code, catalogue, generated projections and test fixtures to the ownership decision in the evidence record. Avoid unrelated edits.

For interruption, inspect JAD status, branch, plan and the verification receipt. A matching digest can identify an existing artifact. Reconcile partial effects by their operation ID. Resume the existing lane after confirming the saved intent. Never reissue an uncertain external action. A gate failure retains its log and remains failed until repaired and rerun. Continue independent tasks. Enter a blocked result only if no permitted work remains.

**Handoff at staging.** Current task is C01. No implementation or README evidence has been submitted. Update the next-ready IDs, blockers, tested revision and receipt paths after each slice. Once all criteria genuinely pass, place `STATUS: DONE` on the first line and commit the completion candidate and complete sidecar. The independent JAD final verification must still succeed. Local integration and cross-engine receipts are recorded separately.
