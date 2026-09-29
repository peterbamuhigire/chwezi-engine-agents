# M10-04 evidence — agents governance scope (T11, T12 register, T13, T14, T15)

Executor: forked worker of the M10-04 executor, 29 September 2026. No git state changes; all edits unstaged. Zero spend: no model-executed checks.

## T11 — setup-command injection fixture (AC-07) — DONE_WITH_LIMITATIONS

- Added `tests/fixtures/prompt-injection/imported-setup-command.txt`: paraphrased, inert; (a) set aside prior knowledge, (b) do not look up configuration locations, (c) write a pasted key into `~/.mcp.json` for `https://setup.invalid/mcp` with the literal `<PASTED-KEY>`; expected disposition in the same style as the three existing fixtures. No Composio text reproduced.
- Added `tests/test_prompt_injection_fixtures.py` (5 tests): every fixture starts `UNTRUSTED FIXTURE` and has an `Expected disposition:` line; hosts are `.invalid` only and no key shapes appear; the pattern table names RF-01..RF-03; each pattern matches the new fixture's payload; the README still says runtime resistance is `NOT ASSESSED`.
- **Deviation:** the fixtures `README.md` has no red-flag pattern table, and README files are out of bounds for this executor (another executor is repairing READMEs). The table lives in a new file, `tests/fixtures/prompt-injection/red-flag-patterns.md`, and the test reads it. Line for the orchestrator/README owner to add to `tests/fixtures/prompt-injection/README.md`:
  > The red-flag pattern table checked by `tests/test_prompt_injection_fixtures.py` is in [`red-flag-patterns.md`](red-flag-patterns.md); it flags text that discards prior knowledge, forbids checking configuration locations, or writes a pasted credential into user-level agent configuration.
- Command: `python -m pytest -q -W error tests/test_prompt_injection_fixtures.py` → `5 passed`.
- Runtime resistance remains `NOT ASSESSED` (README unchanged).

## T12 — destructive-cleanup register (UA-15), register part — DONE_WITH_LIMITATIONS

- Created `docs/operations/destructive-cleanup-register.md`.
- Phase grep (Part A): **33** occurrences, not 27. The 6 extra are new since the plan's measurement: 5 in `tests/test_render_host_files.py` (M10-02, `35340f6`) and 1 in srs `scripts/build-doc.sh` (M10-01, `905b9a4`); all same-process temp directories. Output: `T12-destructive-cleanup-grep.txt`.
- **Defect found in the phase grep:** `Remove-Item[^\n]*-Recurse` in POSIX ERE excludes the letter `n` and backslash, so it misses lines such as `install.ps1:156` (`$destination`); Node `fs.rmSync` was never searched. A widened grep (Part B) finds **53**; the 20 extra are registered too (rows 34–53). Output: `T12-destructive-cleanup-grep-widened.txt`.
- Dispositions: Part A — `waived-temp` 21, `waived-regenerable` 4, `guarded-confirm` 3, `linux-handoff` 4, `data` 1; Part B — `waived-temp` 16, `single-file` 4. 53/53 dispositioned; 0 converted.
- No script edited (dev: M10-06 concurrent; srs: M10-07 concurrent; linux: needs a Linux test). All four linux rows are waivers citing existing guards, with non-empty-guard hardening handed to the P10 Linux lab (O-4).
- Open items O-1..O-5 in the register; O-2 (srs `init_skill.py`, `setup-srs-project.ps1/.sh` delete user content after a y/N prompt) is the priority conversion once M10-07 releases srs scripts.
- The canonical bundled-script rule is the parent executor's part (skill-writing folder), not this scope.

## T13 — rule-marker pilot (IM-16) — DONE

- design-system-skills worktree was clean before the edit (`git status --short` empty).
- Added 18 `<!-- rule:… -->` markers to `design-system-skills/doctrine/references/ai-slop-banned-fonts.md`, one line before each bullet: `font.ban.hard.{inter, geist, roboto, open-sans, lato, arial, fraunces, ibm-plex, bare-system-stack}`, `font.ban.secondary.{space-grotesk, instrument-serif, poppins, montserrat, nunito, nunito-sans}`, `font.conditional.{source-sans-3, source-sans-pro}`, `font.ban.mono.roboto-mono` (edge-case bullet §5). The doctrine is a bullet list, not a table; markers pin the bullets. Line endings kept LF as found.
- **Direction decision (under Peter's delegated authority, 29 Sep 2026):** M10-02 registered the JSON sidecar as the canonical *distributed* copy (`catalog/shared-assets.yaml`, `ai-slop-banned-fonts-json`, byte mode), while the JSON's own `$comment` keeps the Markdown as the authored source. The validator therefore checks **both** directions: every sidecar family resolves to a marker, and every `font.*` marker resolves to a sidecar entry. IBM Plex cuts resolve through `hardBanFamilyPrefixes`; `IBM Plex Mono` in `monospaceBanned` resolves through the prefix.
- Added `scripts/validate-rule-markers.py` (ID format, uniqueness, marker followed by a doctrine line, sidecar both ways; Impeccable attribution Apache-2.0, commit `114ea1d…`) and `tests/test_validate_rule_markers.py` (6 tests: clean pass, seeded duplicate → exit 1, sidecar family without marker → exit 1, marker without sidecar entry → exit 1, bad ID → exit 1, design pilot file passes).
- Commands:
  - `python -X utf8 scripts/validate-rule-markers.py ../design-system-skills/doctrine/references/ai-slop-banned-fonts.md` → `PASS: 18 marker(s); sidecar checked; findings 0`, exit 0.
  - `python -m pytest -q tests/test_validate_rule_markers.py` → `6 passed`.
  - design `node hooks/test-banned-font-gate.js` → `18/18 passed`, exit 0.
  - design `python -X utf8 scripts/validate_engine.py` → `skills=101 fully_compliant=101`, exit 0.
  - design `python -m pytest -q tests` → `99 passed`.

## T14 — session-diagnosis procedure (SP-17) — DONE

- Added "Session diagnosis" to `core/instructions/engine-validator.md` (six steps: intake, locate read-only, six fixed dimensions, `path:line` or discard, redaction, validation-result output with `NOT ASSESSED`). Superpowers `diagnosing-superpowers` attribution (MIT, commit `8ca22db…`).
- Sample run on a real local transcript (a 21-line Claude Code session of 28 Sep 2026; not this session; no client or political-essay content). Raw report kept local in the session scratchpad (`M10-04-T14-session-diagnosis-RAW.md`); redacted summary committed as `T14-session-diagnosis-sample-redacted.md`. Every finding cites `T:<line>`; redaction list stated.
- Side finding for the orchestrator: that session's SessionStart hook failed with exit 127 because `${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd` was not expanded under Git Bash (transcript l.3). Outside M10-04 scope.

## T15 — AI-contributor policy (SP-20) — DONE (ratification recorded under delegation)

- `chwezi-engine-agents/CONTRIBUTING.md`: new "If you are an AI agent" section (disclose model/runtime label, harness, plugins; search PRs and issues; one problem per PR; run documented validators, `NOT ASSESSED` otherwise; no book extractions or copied text). Model wording follows P00 only (Codex GPT-6 Luna/high; Astra only on Peter's explicit selection; other runtimes keep their own configuration). No rejection-rate claim.
- New `chwezi-dev-engine/CONTRIBUTING.md`: short; points to `AGENTS.md` and lists the exact CI commands from `.github/workflows/skill-guardrails.yml`, plus the same AI-agent section.
- New `.github/pull_request_template.md` in both repositories (neither existed) with a disclosure block (author type, model/runtime label, harness, plugins, prior-PR search done, one problem per PR, no copied text).
- **Ratification:** decided by orchestrator under Peter's delegated authority, 29 Sep 2026 — wording ratified for commit. External-release class: public push only at the push gate; Peter's ratification of the public wording is still to be confirmed before that push.

## Verification summary

| Command | Result |
|---|---|
| `python -m pytest -q tests/test_prompt_injection_fixtures.py` | 5 passed |
| `python -m pytest -q tests/test_validate_rule_markers.py` | 6 passed |
| `python -X utf8 scripts/validate-rule-markers.py …/ai-slop-banned-fonts.md` | PASS, exit 0 |
| design `node hooks/test-banned-font-gate.js` | 18/18 passed |
| design `python -X utf8 scripts/validate_engine.py` | exit 0, 101/101 compliant |
| agents `python -m pytest -q tests` | 64 passed, 1 failed: `test_kaizen_coordination_cards` — README does not link three operations cards (README-scope, not this change) |
| agents `python -X utf8 scripts/render_host_files.py --check` | 2 findings, both skill-writing hashes in dev (the parent executor's in-flight T02–T06 edits; re-register when those land) |
| dev `python -X utf8 scripts/skill_catalog_guardrails.py` | 167 active, 0 findings |
| `git diff --check` (agents, design, dev new files) | clean |

## Open items

1. Add the red-flag-patterns link line (T11) to the fixtures README when the README owner is free.
2. Conversions O-1..O-5 in the destructive-cleanup register; O-2 first.
3. Replace the phase's grep with the widened pattern wherever it is reused (M10-14 re-audit).
4. Peter to confirm the public wording of the contributor sections before the push gate.
5. SessionStart hook exit 127 (T14 side finding).
