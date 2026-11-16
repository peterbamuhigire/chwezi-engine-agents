# Portfolio drift repair - 16 November 2026

Peter authorised repair of the outstanding drift findings, then explicitly held
commits and pushes. This change preserves that hold. No source policy, model
selection, permission, release threshold or application data is changed here.

## Result and scope

The full host check initially reported 35 findings across 12 public repositories.
The repair clears 24 content and registration findings. Eleven release-pin
findings remain: nine lagging pins and two pins absent from local history.
The separate marketplace check also exposed three stale suite descriptions;
these are corrected from the inspected local plugin manifests.
The full drift check still exits 1. It is not an all-green release result.

## Repairs

- Point the SDLC ISO-quality and proposal missing-evidence canaries at their
  unchanged text in `docs/agents-reference.md`, using the validator's existing
  `files` field. Their wording and mandatory status are retained.
- Return the canonical design trigger to the social engine's root router;
  replace its reference-file duplicate with a link. Both hosts read the router.
- Remove the business-plan country-context exclusion: all three country skills
  are already explicitly listed in its plugin. No skill is removed.
- Correct the development marketplace to 168 skills. Correct the suite's SDLC,
  development and design descriptions to 160, 168 and 109 respectively.
- Register the design shell installer as a deliberate variant. Its executable
  lines match the shared template; only a comment replaces a drive-path example
  with portable prose. The variant retains exact digest checking; the other ten
  shell copies retain byte equality with the canonical template.

## Deliberate-variant review

For each of the 17 mismatches, locate the exact registered CRLF-normalised digest
in the owning repository's Git history, compare that version with the working
file, and inspect the semantic change before updating the register. All 17
registered baselines were recovered. No source file in this table was changed
by the repair; each retains its existing owner and exact new digest check.
Checks establish the inspected local behaviour, not broad quality certification.

| Variant | Registered baseline commit | Retained change |
|---|---|---|
| `chwezi-design-engine/scripts/install-engine.js` | `c9b334d770c4` | Keep the source entry-limit check before install writes. |
| `chwezi-sdlc-documentation/rules/common/core.md` | `360854a9fa24` | Keep upstream attribution in place of a workstation-only file path. |
| `website-skills/rules/common/core.md` | `b8c9edf3992d` | Keep device-resolved research routing instead of a fixed checkout path. |
| `social-media-skills/rules/common/core.md` | `3416d0b5c1f3` | Keep the catalogue research-engine ID and unchanged research duty. |
| `linux-skills/rules/common/core.md` | `41dc74ebb107` | Keep the existing owner-directed short user-command handoff and machine-command exception. |
| `website-skills/skills/meta/skill-writing/SKILL.md` | `74d085518f29` | Keep the portable canonical skill-writing pointer; retain the engine-specific authoring contract and degraded behaviour. |
| `digital-research-engine/skills/skill-writing/SKILL.md` | `95f69eadc8a7` | Keep the portable canonical skill-writing pointer; retain the engine-specific authoring contract and degraded behaviour. |
| `proposal-skills/skills/meta/skill-writing/SKILL.md` | `cb0b23668978` | Keep the portable canonical skill-writing pointer; retain the engine-specific authoring contract and degraded behaviour. |
| `business-plan-skills/skills/meta-utility/skill-writing/SKILL.md` | `5f5e17df7cfa` | Keep the portable canonical skill-writing pointer; retain the engine-specific authoring contract and degraded behaviour. |
| `social-media-skills/skills/meta-utility/skill-writing/SKILL.md` | `3416d0b5c1f3` | Keep the portable canonical skill-writing pointer; retain the engine-specific authoring contract and degraded behaviour. |
| `chwezi-design-engine/scripts/generate-plugin-manifest.js` | `c9b334d770c4` | Keep the entry-limit check before manifest generation. |
| `chwezi-dev-engine/scripts/routing_smoke_test.py` | `ca226ae79846` | Keep coverage reporting and the optional zero-positive ceiling; fixture checks remain separate. |
| `chwezi-sdlc-documentation/scripts/routing_smoke_test.py` | `702a5ab32ea2` | Keep coverage/floor reporting, separate local versus cross-engine negatives, and explicit missing-dependency failure. |
| `proposal-skills/scripts/routing_smoke_test.py` | `3905b5408592` | Keep owned-negative primary exclusion and distinguish top-three hits from primary precision. |
| `business-plan-skills/scripts/routing_smoke_test.py` | `21f38e3e7617` | Keep unreadable-skill failures, coverage reporting and the optional primary-precision floor. |
| `linux-skills/scripts/routing_smoke_test.py` | `3baac6798807` | Keep duplicate/absent fixture ID failures, expected/forbidden checks and separate rank metrics. |
| `windows-admin-engine-skills/scripts/routing_smoke_test.py` | `053aec14e550` | Keep primary-rank/forbidden checks and the 11-specialist coverage floor. |

Full baseline and new hashes, source diffs and command logs are retained in the
local maintenance evidence. The register links this review and records the new
hashes. Re-review on any variant edit; the scheduled register review remains
29 December 2026. Hash equality alone is not semantic approval.

## Verification

- Coordinator: `python -X utf8 -m pytest -q -p no:cacheprovider tests`:
  **378 passed, 24 subtests passed** in 209.67 seconds.
- The six reviewed routing scripts pass their engine-native smoke checks.
  Social routing also passes `--min-rank1 92 --lint-fixtures`; its machine-path
  check passes after the trigger relocation.
- Design: `node --test tests/file-count.test.js`: **4 passed**, including
  oversized-source rejection before installer or manifest writes.
- Marketplace: **23 checked entries, zero drift, zero unassessed** after repair.
  The earlier failed marketplace run is retained in local evidence.
- Full host check: **11 findings, zero unassessed**, all release-pin findings.
  The read-only pin survey confirms all 11 engines have dirty-tree blockers.
- Coordinator public-hygiene check: **zero findings**. README metrics pass all
  six limits. Diff whitespace checks pass across all six touched repositories.
- Actual-diff review confirms exact variant digests, unchanged owners/discovery
  rules/exemptions, unchanged non-comment installer lines, ten remaining
  canonical shell copies, preserved moved-rule wording and router references.

The review inspected the actual source-history diffs and final repair diff.
No new implementation code or tests were introduced. These checks do not prove
live host behaviour, current external doctrine, market value or production
readiness. Independent second-reviewer assessment for this repair was not run.


## Release-pin dependency

Do not manually substitute hashes or permit dirty trees merely to clear this
check. `scripts/refresh_released_commits.py --write` deliberately refuses dirty
engines. The two unknown pins are not proven releases and must not be described
as ancestors. No historical lineage has been invented or rewritten.

After Peter reauthorises commits, review and commit each approved domain-engine
worktree on `main`, rerun required checks, then run the existing pin updater and
full host check. Commit the coordinator last so its catalogue names the final
engine commits. A later push requires current user authority and the normal
repository/privacy checks. No commit, tag, push, live deployment or cache refresh
was performed by this repair.

## Model-currentness check

Decision: retain the owner-selected Codex `gpt-6.1-terra`/medium default and
explicit-only `gpt-6-astra`/high option; leave Claude selection unchanged.
The account cache refreshed at 2026-11-16T17:27:25.335963600Z lists both IDs and
the relevant reasoning levels. Six affected engine policy checks pass. This
does not establish which model a running root uses or change that session.

Primary pages rechecked on 16 November 2026:

- [OpenAI Terra release](https://openai.com/index/introducing-gpt-6-1-terra/),
  coding and pricing/availability sections: vendor positioning supports routine
  work; standard API input/cache/output prices are USD 1/0.05/5 per million
  tokens. Exact publication day was not established from the inspected body.
- [Anthropic Fable/Mythos 5.2 release](https://www.anthropic.com/claude-fable-and-mythos-5-2),
  published 9 November 2026, introduction and task-fit guidance: newer specialist
  models do not imply replacement of the existing daily coding configuration.

These are vendor claims, not a controlled local cost, latency or quality trial.
Claude account availability and comparative task performance remain NOT_ASSESSED.
No evidence justifies a policy change for this metadata repair. Recheck on the
next model decision or new Kaizen; no future-currentness guarantee is made.

## Additional hygiene repair, 16 November 2026

The subsequent full hygiene scan found 14 issues beyond the host-drift findings
above. Repairs made Linux examples portable, replaced workstation routing paths
in Linux and Design, withheld one workstation root in each of two dated records,
and removed Linux's per-user settings file from the Git index while preserving
the local file byte-for-byte and adding its ignore entry. No permission settings
were edited. The index removal is staged; no commit, push or history rewrite ran.
All four affected checkouts now report zero hygiene findings. Shell syntax/help
checks pass. Linux's registered skill-writing variant was updated only after
verifying that the pointer replacement was the sole normalized byte change
against its prior registered hash. Policy ceilings were not increased. The repeated host-drift check
still has only the 11 release-pin findings awaiting authorised clean commits.
The final registered-variant change passed all 57 host-rendering tests.
