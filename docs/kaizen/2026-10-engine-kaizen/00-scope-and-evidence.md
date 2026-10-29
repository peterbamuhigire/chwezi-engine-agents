# Scope and evidence — 29 October 2026

Chwezi Core Systems coordination cycle, prompt 12 of the supplied October portfolio prompt. User authorised pulling, bounded improvements, documentation, commits and pushing main; no tags or paid model calls. Branch `kaizen/2026-10` starts from clean `77d5dc743efc78be4ba0134944cafd99712c87ec`. No pre-existing policy edits were present. Domain cycles precede this baseline; Website independent review was completing, so its final revision will be recorded again. Engines are resolved through the device catalogue, not embedded host paths.

Read the Portfolio Kaizen Standard and currentness gate in the Research engine, this router, September 26 execution record, September 29 M10 execution record and corrected re-audit. The corrected historical readiness was 37.1, not 47.7. The seven-file domain reports remain authoritative for their own limitations. Recorded baseline commands, exact exits and logs: [results](evidence/baseline-results.json); [snapshot](evidence/baseline-snapshot.json). Source logs were sanitised only for machine paths; raw originals remain in the disposable lab.

## Confirmed defects

- Critical dependency audit: 13 vulnerable package entries (six moderate, six high, one critical); see [npm audit](evidence/baseline-npm-audit.json). Reachable exploitability is not established: this server uses stdio, while several advisories concern HTTP/OAuth paths.
- Major fixture-path contract failure: `scripts/run_behavioural_eval.py:116` accepts a Windows drive path on POSIX; existing negative test fails. [Python result](evidence/baseline-3.log).
- Major Codex plugin identity mismatch: `.codex-plugin/plugin.json:2` differs from marketplace identity; native install fails. Claude local installation succeeds. MCP package version/identity and release archive retain legacy names.
- Major release and CI claims exceed actual workflow checks; release does not run all the tests promised by supply-chain policy. No release tag or public directory submission was run.
- Major stale catalogue pins for all eleven engines and eight drift findings, including the now-obsolete Business country-context exclusion. [Drift](evidence/baseline-0.log).
- Minor router includes a device-specific workspace example; bridge contract contradicts its registered Claude block.

## Precondition history

```text
77d5dc7 chore(marketplace): social-media-skills 1.2.0
4fc8784 docs(operations): Social Kaizen 2026-09-29 consolidation portfolio record (S13)
3f39de5 chore(portfolio): social marketplace text, catalogue alias gate, regenerated engine tours and skill graph (Social Kaizen S12)
9f2fbcd chore(routing): register social routing floor 92 in baseline.json; re-point oracles 044/057 to owners; ledger RC-018/RC-019 (Social Kaizen S11)
aef2dc5 chore(marketplace): social plugin count 110 -> 112 after Social Kaizen S10
c776c92 chore(catalog): re-register social skill-writing and core rules hashes after Social Kaizen S09
7398229 chore: harmonise portfolio for chwezi-sdlc-documentation and chwezi-design-engine renames
a4cf31d chore(routing): Social Kaizen S08 ledger RC-015..017, EAE mirrored-pack row, social shared-asset hashes
44a1fe1 chore(marketplace): social count 110 (Social Kaizen S07)
a038ee4 chore(marketplace): social count 117 (Social Kaizen S06)
3928669 chore(marketplace): social count 132 (Social Kaizen S05)
896ae93 chore(marketplace): social count 151 (Social Kaizen S04)
e4a8275 fix(routing): blog-ideation owner -> social-media-skills/content-ideas; social count 162 (Social Kaizen S03-T-X1)
282582d chore(marketplace): social count 176 (Social Kaizen S02)
6744eb3 docs(m10-14): cross-engine Computer Misuse legal-currency evidence
e435d6c chore(shared-assets): register social routing_smoke_test S01 variant
5fd8cea docs: portable links rule for all engines (cross-engine links are GitHub URLs; host-absolute links fail validation)
8301be9 docs(m10-14): CI repair evidence
a0b33a0 docs(m10-14): close-out - section 5 measures (9 MET, 1 NOT_MET), Engine Eval Readiness, traceability closure (161 IDs), Kaizen record, measured re-audit, independent review
86a7776 docs: rewrite README to portfolio structure (summary, installation, skills/workflows/tools capabilities, lifecycle map, references)
```
