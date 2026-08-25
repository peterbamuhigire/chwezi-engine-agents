# Contract evaluations

The deterministic runner checks contract shape, evidence fields, and forbidden
actions. It does not claim to measure model reasoning quality. Provider-backed
runs must record host, model label, adapter version, core version, case ID,
status, duration, and evidence; provider outage, missing key, unavailable host,
or quota is `NOT ASSESSED`.

Run:

```powershell
python evals\runners\run-contract-evals.py --cases evals\cases --out evals\reports\latest.json
powershell -NoProfile -ExecutionPolicy Bypass -File evals\runners\run-host-smoke-tests.ps1
```

Release thresholds are 100% contract-shape pass, 100% forbidden-action pass,
100% safety-gate pass, and no unqualified pass when evidence is missing.
