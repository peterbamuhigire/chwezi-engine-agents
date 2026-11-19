# 2026-11-19: runner tools, skills on demand, and the port backlog

**For:** the engine-maintainer workflow when it updates the community `auto-agents` copy in this repository, or any other runner copy.

**Status:** the change is documented here, but this repository's copy is **not ported yet** (still 2.2.7). The port is `NOT_ASSESSED` until it is done and tested here.

## What changed upstream

The private canonical runner in `chwezi-development-engine/auto-agents` is now at **2.4.0** (commit `39da06e`). Its `auto-agents/CHANGES.md` lists every change from 2.3.0 to 2.4.0. Each entry gives the reason, the incident that proved it, the files and the porting notes. Read that file first. It is the porting source of truth.

2.4.0 in brief:
- **What:** runner sessions start without plugin skill catalogues.
  - The new config key `skills` takes `on-demand` (the default) or `preload`.
  - Claude gets a generated `--settings` file and Codex a generated profile. Each switches off every plugin the host has enabled.
  - The agent finds skills with `python auto-agents/find_skill.py "<task words>"`.
- **Engines searched:** only the canonical folders of Development, Writing, this orchestrator (`core/instructions/`, `skills/`), Accounting Doctrine and the Knowledge Bank.
- **Measured on 19 Nov 2026:**
  - Claude Code 2.1.327: 36,216 → 30,050 start-up tokens per request.
  - codex-cli 0.170.0: 165 → 11 listed skills and 25,500 → 18,792 input tokens.

## Port checklist for this copy

1. Port 2.3.0 → 2.4.0 in order, following `CHANGES.md`. Keep this copy's `config.json`, `PLAN.md` and `ENGINE.md`.
2. `find_skill.py` resolves this repository as the `orchestrator` engine, under its current or former folder name. Keep `core/instructions/*.md` described by their first paragraph or a `description`.
3. Run `python -B -m unittest discover -s auto-agents/tests`, then `python auto-agents/release.py --version 2.4.0 --add find_skill.py --add CHANGES.md --add tests/test_find_skill.py`.
4. Propagate to the authorised community copies with `propagate.py --apply`, only where no driver is live. Record the targets that are blocked or missing.

## Rule for future engine Kaizens

Whenever a Kaizen changes the runner tools in any engine:
- Add an entry to that engine's `auto-agents/CHANGES.md` covering why, what, the files, the tests and the porting notes.
- Leave a dated note here under `docs/updates/` naming the release and which copies still need the port.

Then the next maintainer, human or agent, can update the other runner tools without rereading old session transcripts.
