# M10-14 evidence: Uganda Computer Misuse legal currency across engines

- **Date:** 29 September 2026.
- **Scope:** correct stale Uganda Computer Misuse citations in engines other than `social-media-skills`, which another executor is editing and which was not touched.
- **Status:** DONE_WITH_LIMITATIONS. The limitation is that the judgment itself was not read; see Limitations.
- **Verified position used:** the `UG-CMA-2022-VOID-2026`, `UG-CMA-SECTIONS-STRUCK-2026`, `UG-CMA-AG-DIRECTIVE-2026` and `UG-CMA-S25-2023` records added on 29 Sep 2026 to `social-media-skills/docs/source-registers/source-register.json`, and `social-media-skills/docs/kaizen/consolidation-2026-09-29/evidence/S10/S10-T01-legal-currency-evidence.md`. The wording keeps the S10-T01 precision rules. The text never says the whole Computer Misuse Act was voided. Section numbers are given as "per secondary reports; verify against the judgment".

## Position as written into the engines

On 17 Mar 2026 the Constitutional Court declared the whole Computer Misuse (Amendment) Act 2022 void because of a quorum defect (Rule 24(3) of the Rules of Procedure; Articles 88 and 89 of the Constitution). Per secondary reports, it also struck ss.11, 23 and 26 to 29 of the principal Act (2023 revised edition numbering) and criminal libel (Penal Code ss.162 and 163). Section 25 had already been struck on 11 Jan 2023. The Attorney General halted prosecutions under the struck provisions. The rest of the principal Act remains in force. Sources were cited with access date 29 Sep 2026: CPJ, CIPESA, The Independent and Daily Monitor. The cross-engine link to the register uses its GitHub URL.

## Sweep

`git grep -n -i "computer misuse"` was run in every repo under `C:\wamp64\www` matching `chwezi-*`, `*-skills` and `digital-research-engine`, including `political-essay-skills`. `social-media-skills` was skipped. A working-tree `grep -rIl` was also run for "computer misuse", "criminal libel", "criminal defamation" and "misuse (amendment)".

| Hit | Classification | Action |
|---|---|---|
| `business-plan-skills/skills/pipeline/14-ai-integration/references/uganda-ict-ip-guidelines.md` L37 and part 8.2 | Live guidance: it presented the void 2022 Amendment objectives as the Act's current objectives | Corrected |
| `business-plan-skills/skills/pipeline/10-financial-projections/references/uganda-ip-framework.md` L310 and L419 | Live guidance: generic mentions | Scoped to the principal Act; dated legal-currency note added in part 11.1 |
| `srs-skills/domains/uganda/references/regulations.md` L14 | Live guidance | Row scoped to the principal Act; dated note added under the table |
| `digital-research-engine/docs/plans/2026-04-26-upf-cris-design.md` L197 | Historical plan | Left unchanged, as instructed |
| `digital-research-engine/projects/upf-cris/**` (about 25 files) and `srs-skills/projects/BIRDC-ERP/09-governance-compliance/05-dppa-annex/01-front-matter.md` | Git-ignored client project workspaces, not engine guidance; most already record the March 2026 nullification | Not edited (out of scope). Reported: `upf-cris/02-research/security-legal-governance/research/04-evidence-act-and-digital-evidence.md` L31 heading "Computer Misuse Act 2011 (Amended 2022)" and `.../14-sources.md` L27 "amended 2022" are stale if that research is reused |
| `chwezi-*`, `design-system-skills`, `linux-skills`, `political-essay-skills`, `proposal-skills`, `website-skills`, `windows-admin-engine-skills` | No hits | None |

## Files changed

- `C:\wamp64\www\business-plan-skills\skills\pipeline\14-ai-integration\references\uganda-ict-ip-guidelines.md`
- `C:\wamp64\www\business-plan-skills\skills\pipeline\10-financial-projections\references\uganda-ip-framework.md`
- `C:\wamp64\www\srs-skills\domains\uganda\references\regulations.md`

## Verification (29 Sep 2026)

| Repo | Command | Result |
|---|---|---|
| business-plan-skills | `python -X utf8 scripts/validate_skill_engine.py --baseline docs/quality/skill-quality-baseline.json` | exit 0; 137 active skills, 137 fully compliant |
| business-plan-skills | `python -X utf8 scripts/routing_smoke_test.py --threshold 1.0` | exit 0; 61/61 (100%) |
| business-plan-skills | `python -X utf8 scripts/source_ingestion_guardrail.py` | exit 0; 0 findings, 0 content warnings |
| business-plan-skills | `python -X utf8 scripts/routing_link_check.py` | exit 0; 7 surfaces, 0 failures |
| business-plan-skills | `quick_validate.py` on `14-ai-integration` and `10-financial-projections` | Both valid |
| business-plan-skills | `python -X utf8 -m pytest -q tests` | 66 passed, 50 subtests passed |
| srs-skills | `python -X utf8 scripts/source_ingestion_guardrail.py` | exit 0; 0 findings |
| srs-skills | `python -X utf8 scripts/validate_skill_engine.py --baseline tests/skill-quality-baseline.json` | exit 0 (4 pre-existing report-only byte warnings on unrelated skills) |
| srs-skills | `python -X utf8 scripts/routing_smoke_test.py` | exit 0; owned negatives 13 pass, 0 fail, 3 NOT_ASSESSED (cross-engine) |
| srs-skills | `python -X utf8 -m engine validate-skills` | SKILLS OK |
| srs-skills | `python -X utf8 -m pytest` (engine/tests, coverage gate) | 432 passed, 2 skipped; coverage 96.86% (gate 90%) |
| srs-skills | `python -X utf8 -m pytest --no-cov -o addopts="" -q tests` | 27 passed |

After the edits, `git grep "Amendment) Act 2022"` in both repos shows that every Computer Misuse hit presents the Amendment Act as void. The one other hit is the unrelated Companies (Amendment) Act 2022.

## Limitations and open items

- The judgment on ULII was not read (NOT_ASSESSED, as in S10-T01), so the section list rests on secondary reports. Any appeal or re-enactment bill is also NOT_ASSESSED.
- The GitHub register link points to records that are unstaged in `social-media-skills`. The link resolves only after the orchestrator commits and pushes S10-T01.
- The stale lines in the git-ignored `upf-cris` client research files were not edited (see Sweep).
