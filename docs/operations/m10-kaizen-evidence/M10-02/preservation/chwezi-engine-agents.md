# Preservation map — chwezi-engine-agents (M10-02-T03)

The package had no `AGENTS.md`, so Codex sessions got no router. `AGENTS.md` is created from the former `CLAUDE.md` (47 lines), and `CLAUDE.md` becomes the portfolio bridge (`docs/operations/claude-bridge-contract.md`). Classification decided by the M10-02 executor under Peter's delegated authority, 29 Sep 2026; reviewer ticks left open.

## Hashes and sizes

| File | Pre SHA-256 | Pre bytes | Post SHA-256 | Post bytes |
|---|---|---|---|---|
| `CLAUDE.md` | `ea62efc2d356bcbd2d29250e36dc3369e085f5ed009837376f00211514b0bbfc` (HEAD blob) | 2,516 (working tree) | `1b6519b9d455cba8d12d2aeb0cf81eb9cce43adffecb57d1febc308a6e271e57` | 324 |
| `AGENTS.md` | absent | 0 | `eb929a119e733b5c377d0ee59cf8d98495f710b98754f00296bbbca238741eaa` | 4,433 |

Router effective bytes: 2,516 before (no import); 324 + 4,433 = 4,757 after (the increase is the design trigger block, T06, and the drift-control paragraph).

## Sentence table

| ID | Source line | Sentence (abridged) | Class | Destination | Reviewer |
|---|---|---|---|---|---|
| E01 | 1 | Heading `# CLAUDE.md - chwezi-engine-agents (Skills Engine Agents)` | doctrine-moved | AGENTS.md heading (`# AGENTS.md - …`) | [ ] |
| E02 | 3–4 | Coordination and maintenance layer for the eleven catalogued engines | doctrine-moved | AGENTS.md L3–4, verbatim | [ ] |
| E03 | 4 | The primary router is `README.md` | doctrine-moved | AGENTS.md L6–7, verbatim | [ ] |
| E04 | 5 | The Claude Code adapter is `adapters/claude-code/CLAUDE.md` | doctrine-moved | AGENTS.md L7–9 (widened: host adapters under `adapters/`, Claude Code and Codex named) | [ ] |
| E05 | 7 | "How to use this package under Claude Code:" | doctrine-moved | AGENTS.md "How to use this package:" (runner-neutral) | [ ] |
| E06 | 9–10 | Resolve the engine from `catalog/engines.yaml` (paths relative to `C:\wamp64\www\`) | doctrine-moved | AGENTS.md step 1, verbatim | [ ] |
| E07 | 11–12 | Read the engine's `CLAUDE.md` (falling back to `AGENTS.md` or `README.md`) before its skills | doctrine-moved | AGENTS.md step 2, order changed to `AGENTS.md` first (after M10-02 every `CLAUDE.md` imports `AGENTS.md`, so the content is the same) | [ ] |
| E08 | 13–14 | Use the three workflows in `agents/` by reading their definitions directly | doctrine-moved | AGENTS.md step 3, verbatim | [ ] |
| E09 | 15 | They are not registered with Claude Code's native `Skill` tool | Claude-mechanics | CLAUDE.md Claude-only notes, bullet 1 | [ ] |
| E10 | 16 | Canonical instructions live in `core/instructions/` | doctrine-moved | AGENTS.md step 3, verbatim | [ ] |
| E11 | 18–21 | Read-only by default; `git pull --ff-only` only on request; skip dirty repos; never reset, delete, merge manually, force-push | doctrine-moved | AGENTS.md §Safety boundaries, verbatim | [ ] |
| E12 | 22–23 | Unavailable validation commands are `NOT ASSESSED`, never a pass | doctrine-moved | same, verbatim | [ ] |
| E13 | 24–25 | Writes, submissions, external messages, publication need explicit approval | doctrine-moved | same, verbatim | [ ] |
| E14 | 26–29 | Never store book extractions in any engine or this package (folders, files, summaries) | doctrine-moved | same, verbatim | [ ] |
| E15 | 29–31 | Book knowledge enters only as paraphrased skill content with a `Sources` line | doctrine-moved | same, verbatim | [ ] |
| E16 | 31–34 | Check with `validate-no-book-extractions.py` (path-based; allowlist for exceptions) | doctrine-moved | same, verbatim | [ ] |
| E17 | 36–37 | Catalog holds eleven public engines; with this package, twelve repositories | doctrine-moved | AGENTS.md §Engine count, verbatim | [ ] |
| E18 | 38 | Private personal engines stay out of catalog, marketplace and public documents | doctrine-moved | same, verbatim | [ ] |
| E19 | 40–43 | Cross-engine handoffs: SRS / dev / design / research / finance | doctrine-moved | same paragraph, verbatim | [ ] |
| E20 | 43 | See `core/instructions/engine-orchestrator.md` | doctrine-moved | same, verbatim | [ ] |
| E21 | 45–46 | `README.md` documents Codex-specific installation and a `~/.codex/...` path | doctrine-moved | AGENTS.md "Host-specific material", verbatim | [ ] |
| E22 | 46–47 | Those apply to the Codex host only and are not expected on this machine for Claude Code | doctrine-moved | AGENTS.md "…apply to the Codex host only. Claude Code reads this file through `CLAUDE.md`." | [ ] |

Counts: doctrine-moved 21, Claude-mechanics 1, duplicate 0, obsolete 0. **Lost: 0.**

Added (not moves): the bridge-contract sentence in the opening paragraph; the "Portfolio drift control" paragraph (M10-02-T04); the design trigger block `v2` (M10-02-T06, recommended option: engine-agents carries it only through `AGENTS.md`); Claude-only bullet 2 (an engine's `CLAUDE.md` is a bridge that imports its `AGENTS.md`).

Codex-host behaviour of the new `AGENTS.md`: `NOT_ASSESSED` (no Codex session run; zero-spend rule).
