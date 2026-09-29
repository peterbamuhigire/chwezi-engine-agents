# M10-14-T03 close-out snapshot and diff against the M10-00 baseline

- Command (run twice, 29 Sep 2026, before any M10-14 evidence was written into the repositories): `python -X utf8 scripts/kaizen_portfolio_snapshot.py --workspace-root C:/wamp64/www --coordination-root C:/wamp64/www/chwezi-engine-agents --output-dir <scratch>/snap{1,2} --as-of 2026-09-29`.
- Two-run digest equality: **PASS**. Both runs gave `baseline.json` SHA-256 `ccc9febebc91507f8a6502e7a513ceed43625aec001bfb62eef35c21df3ac512`, `skill-inventory.jsonl` `efe8529f9364e527135c9a84a53213e143cc2cec7e4556741d0bc4ccf855ee96` and `coordination-skill-inventory.jsonl` `52de683ac36881a64c0a6e86ec6a43984b4e40824b8d3490a8e4a96440178447`. This closes the M10-00-T11 limitation (digest instability from concurrent executor edits).
- Stored: `close-snapshot.json` (the first run's `baseline.json`). It now carries the CV-01 router fields (`router_bytes`, `router_import_bytes`, `router_effective_bytes`, `router_imports`).
- Freeze state: all 12 repositories clean, each local `HEAD` equal to `origin/main`.
- The M10-00 snapshot predates CV-01, so its router bytes are reconstructed here from Git at the M10-00 HEADs: `CLAUDE.md` size plus any `@`-imported file. For the eight engines whose M10-00 `CLAUDE.md` was the full router, "effective" is the `CLAUDE.md` alone, because Claude Code did not load `AGENTS.md` then.
- The M10-00 snapshot's first dirty path per engine is truncated (`EADME.md`); the snapshot defect is recorded in M10-00 and is not re-measured here.

| Repository | M10-00 HEAD | Close HEAD | Commits between | M10-00 clean | Close clean | Raw SKILL.md M10-00 → close | CLAUDE.md bytes M10-00 → close | Effective router bytes M10-00 → close |
|---|---|---|---|---|---|---|---|---|
| business-plan-skills | `ceeb240` | `8949387` | 9 | True | True | 137 → 137 | 19602 → 222 | 19602 (no imports) → 39132 |
| chwezi-accounting-doctrine | `8c1d683` | `82279fa` | 5 | True | True | 108 → 108 | 187 → 44 | 6909 (AGENTS.md) → 9197 |
| chwezi-dev-engine | `7adc9fc` | `67ae982` | 16 | False | True | 168 → 168 | 1037 → 44 | 15898 (AGENTS.md) → 15566 |
| chwezi-engine-agents | `eaa2152` | `8a438c9` | 20 | False | True | 3 → 10 | 2516 → 324 | 2516 (no imports) → 5162 |
| design-system-skills | `b7e1003` | `25ce1e6` | 12 | True | True | 102 → 102 | 4093 → 212 | 4093 (no imports) → 11850 |
| digital-research-engine | `5c4313c` | `2b9c87d` | 12 | True | True | 61 → 61 | 11455 → 889 | 11455 (no imports) → 21051 |
| linux-skills | `9443e50` | `87c6421` | 7 | True | True | 48 → 48 | 10352 → 362 | 10352 (no imports) → 22168 |
| proposal-skills | `e72dc66` | `5de27f8` | 10 | True | True | 115 → 115 | 244 → 44 | 30567 (AGENTS.md) → 31108 |
| social-media-skills | `bcf43e3` | `09eebe7` | 8 | True | True | 191 → 191 | 21436 → 44 | 21436 (no imports) → 41156 |
| srs-skills | `efa18e6` | `fa85fba` | 11 | False | True | 160 → 160 | 33533 → 44 | 33533 (no imports) → 51212 |
| website-skills | `1660bc1` | `ec72bca` | 11 | True | True | 63 → 63 | 21178 → 760 | 21178 (no imports) → 41968 |
| windows-admin-engine-skills | `132cbe9` | `55c53cc` | 4 | True | True | 21 → 21 | 1480 → 250 | 11227 (AGENTS.md) → 12617 |

Raw public SKILL.md total: 1174 → 1174; coordination: 3 → 10

## Findings

1. Every repository moved (4 to 20 commits since M10-00). Raw `SKILL.md` counts are unchanged for all eleven public engines (1,174 in total). The coordinator went from 3 to 10 raw skill files, 9 of them excluded candidates (fixtures and templates), so 1 active.
2. `CLAUDE.md` itself shrank to a bridge of 44 to 889 bytes in all twelve repositories (roadmap §5 row 7).
3. **Claude-loaded router bytes rose in 11 of 12 repositories.** The bridge imports `AGENTS.md`, which now carries the doctrine that used to be split between the two files. Examples: srs 33,533 → 51,212; website 21,178 → 41,968; social 21,436 → 41,156; business-plan 19,602 → 39,132. Only dev fell (15,898 → 15,566). No router budget was set (P04: no token target without measured waste), so this is recorded as a measured cost for the next Kaizen, not a failure.
