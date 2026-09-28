# M10-00 executor evidence — mobilisation, governance and decision records (T01–T13)

**Executor:** Claude (Opus 5.5) under the orchestrator's brief, 29 Sep 2026. **Authority:** Peter's delegated approval ("Implement the Plan!"); decisions marked "delegated" were taken by the orchestrator under that authority. **Rules observed:** zero spend; no git commit, push, stage, reset, checkout or stash; no files deleted.

Narrative record: `docs/operations/m10-kaizen-execution-2026-09-29.md`.

| Task | Status |
|---|---|
| T01 log and evidence tree | DONE |
| T02 plan-package loss record | RECORDED AS LOST (not pursued per owner, 29 Sep 2026) |
| T03 plan-package manifest | DONE_WITH_LIMITATIONS (local Git init recommended, not done) |
| T04 disposition file | DONE |
| T05 P06 addendum | DONE |
| T06 Superpowers upgrade and telemetry | DONE_WITH_LIMITATIONS (acceptance prompt NOT_ASSESSED) |
| T07 UX-15 provenance note | DONE_WITH_LIMITATIONS (third, "undetermined" statement) |
| T08 model-policy recheck | DONE (retain Luna/high) |
| T09 font-ruling record | DONE |
| T10 font-ban memory | ALREADY DONE |
| T11 dirty-worktree baseline, push counter | DONE_WITH_LIMITATIONS (digest instability from concurrent edits) |
| T12 D-M10-01 | DONE (approval recorded) |
| T13 change-class matrix | DONE |

## T01

- **Files:** `docs/operations/m10-kaizen-execution-2026-09-29.md` (new); `docs/operations/m10-kaizen-evidence/README.md` and `M10-00/README.md` … `M10-14/README.md` (new, 16 files).
- **Commands:** `Test-Path` equivalent: 15 sub-folders listed; `python -X utf8 scripts/validate-no-book-extractions.py` → `PASS: book-extraction check roots=12 findings=0` (exit 0), rerun after all edits with the same result.

## T02

- **Status:** RECORDED AS LOST — not pursued per owner (29 Sep 2026). No search made. The recorded path `C:\Users\Peter\Downloads\skills-kaizen` is absent (the Downloads listing shows only `kaizen-prompts-2026-09-23`).
- **Files:** log section "Plan-package loss record (29 Sep 2026)", listing HEADs `9c7359e`, `938ecbb`, `6ac16be`, `09b0a11`, digest `80f28c40…6641`, P02 SHA-256 `4137…481C` and every dependent EXEC claim as `NOT_ASSESSED (package lost)`.

## T03

- **Files:** `M10-00/plan-package-manifest.sha256` (37 lines; format `<sha256>  <relative path>`; SHA-256 of the manifest `07c024362a47960ccaba0a46dfb8d9c27549bbdcdfb998832def59ff6787e298`).
- **Commands:** PowerShell `Get-ChildItem -Recurse -File` → 37 files; manifest lines 37. `.git` absent in the package.
- **Open item:** local-only Git repository in the plan package — recommended to the orchestrator; needs a commit, which the executor may not make.

## T04

- **Files:** `docs/operations/third-party-tool-dispositions-2026-09-29.md` (new).
- **Commands:** pins `b05cc3b` 1, `0e4949f` 1, `d6eaa8a` 1, `8ca22db` 2, `09170ee` 1 matches; "Reversal trigger" 5; "Review by" 5.
- **Delegated decisions:** D1–D5 take the plan's recommended options. Review-by dates for D2–D5 were not given in the plan; set to 29 Dec 2026 or the named trigger, whichever comes first.

## T05

- **Files:** `docs/operations/skills-kaizen-execution-2026-09-26.md` (11 lines inserted after the P06 section, before P09).
- **Commands:** `git diff --stat` → `1 file changed, 11 insertions(+)`; deleted lines 0; "P06 addendum" heading count 1; "disposable repository copy" count 1; `git diff --check` clean. The file has mixed line endings in the working copy (index LF); inserted lines follow the neighbouring lines.

## T06

- **Files changed on Peter's machine (not in any repository):** `~/.claude/plugins/installed_plugins.json` (by the plugin manager), plugin cache `superpowers/6.4.2`, marketplace clone `superpowers-marketplace`; user environment variable `SUPERPOWERS_DISABLE_TELEMETRY=1`. Backups: `C:\Users\Peter\.claude\backups\m10-00-2026-09-29\` (`installed_plugins.json` `8d16ac7e9e67926dcc920a4893acedc33db6150533e813d7310b961eafd99672`; `known_marketplaces.json` `14f776579377c99176b49392a50b308e5b567931cbbc3090f35bd3f24647bc9b`; `settings.json` `110aee8a69f4422ef742fd357bdf74e1aa1b5f46c26457a22d336941aa90a4be`). Backups kept outside this public repository on purpose (user-profile data).
- **Commands and results:**
  - `claude --version` → `2.1.284 (Claude Code)`.
  - `claude plugin marketplace update superpowers-marketplace` → "Successfully updated marketplace", exit 0.
  - `claude plugin update superpowers@superpowers-marketplace --json -y` → `{"outcome":"ok",…,"oldVersion":"4.3.1","newVersion":"6.4.2"}`.
  - `installed_plugins.json` → `"version": "6.4.2"`, `"gitCommitSha": "8ca22dba9a94f28898bbce59f2537ff4d87c747d"`.
  - `setx SUPERPOWERS_DISABLE_TELEMETRY 1` → SUCCESS; `[Environment]::GetEnvironmentVariable('SUPERPOWERS_DISABLE_TELEMETRY','User')` → `1`.
  - 6.4.2 `hooks/hooks.json`: `"command": "\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" session-start"`, `"shell": "bash"`. Local run with `CLAUDE_PLUGIN_ROOT` set → exit 0, valid `SessionStart` JSON.
  - `skills/brainstorming/scripts/server.cjs` reads `SUPERPOWERS_DISABLE_TELEMETRY` (also `DISABLE_TELEMETRY`).
- **NOT_ASSESSED (zero-spend rule):** the "Let's make a react todo list" acceptance prompt in a clean session. Owner: Peter. Restart Claude Code first; running sessions keep 4.3.1.
- `~/.claude/settings.json` was not edited.

## T07

- **Files:** `C:\wamp64\www\design-system-skills\docs\continuous-improvement\design-catalog-provenance-2026-09-29.md` (new).
- **Commands:** `python -X utf8 scripts/validate_engine.py --baseline tests/quality-baseline.json` → `skills=101 fully_compliant=101`, exit 0 (after the file was added). `PROVENANCE: UNDETERMINED` count 1; `PROVENANCE: UUPM-INTERFACE|INDEPENDENT` count 0. Pre-existing search of the design repository for `ui-ux-pro-max|uupm|nextlevelbuilder` found nothing.
- **Limitation:** the acceptance line names two phrases; the brief's position ("convergent … attribution added as a precaution") is the plan's third, risk-register statement. Delegated decision, 29 Sep 2026. The attribution sits in the provenance note; no `catalog.py` or catalogue documentation change was made (out of scope; M10-10).

## T08

- **Commands:** WebFetch `https://developers.openai.com/api/docs/models` → Astra, Sol, Luna listed as flagship; no newer general model. WebFetch `https://developers.openai.com/api/docs/changelog` → latest GPT-6 item 2026-09-25 (Sol/Luna image-encoding fix); 2026-09-22 Sol/Luna release; 2026-09-03 Astra release. `codex --version` → `codex-cli 0.156.0`; `codex debug models` → `gpt-6-astra`, `gpt-6-sol`, `gpt-6-luna` visible (`list`), Luna efforts low–max including `high`; also `gpt-5.6-*`, `gpt-5.5` listed and `gpt-reserve`, `codex-auto-review` hidden. `~/.codex/config.toml` → `model = "gpt-6-luna"`, `model_reasoning_effort = "high"`.
- **Decision:** retain Luna/high (within 7 days of the 28 Sep review; no change). Retain line appended to the running log; no new DRE review file; no policy file changed.
- **Note:** the 27 Sep P06 record cites Codex 0.157.1; the `codex` on this shell's PATH reports 0.156.0. Not investigated (possibly a different install); no policy effect.

## T09

- **Files:** log section "Font ruling record (29 Sep 2026)".
- **Commands:** `node hooks/test-banned-font-gate.js` (design) → `18/18 passed`, exit 0. `validate_engine.py` → 101/101. Per-engine `git log -1` and `git rev-parse --short origin/main` → all ten sweep commits are HEAD and equal `origin/main`. `fonts/02-editorial-literary/fraunces` absent. Trigger-block copies: 16 in the portfolio (14 engine router copies plus two in design `integration/`) contain "Fraunces, IBM Plex" and still carry marker `v1`.
- **Found outside scope:** `C:\wamp64\www\techguy-website\vendor\website-skills\{CLAUDE,AGENTS}.md` carry the old v1 block without Fraunces/IBM Plex.

## T10

- **ALREADY DONE.** `memory/project_design_system_engine.md` line 27 records the 29 Sep HOUSE ruling, replacements and watchlist; `MEMORY.md` line 10 mentions "Fraunces/IBM Plex banned" (`Select-String 'Fraunces'` → 1 match). No memory file changed.

## T11

- **Files:** `M10-00/baseline-snapshot.json` (first run; SHA-256 `7b61d10f45022c9e97e7eb2839db983c7c6924574b46c9d72a97d6ddae5f4f00`); log section with "M10 push counter: 0".
- **Commands:** `python -X utf8 scripts/kaizen_portfolio_snapshot.py --workspace-root C:/wamp64/www --coordination-root C:/wamp64/www/chwezi-engine-agents --output-dir <scratchpad>/snapA..D --as-of 2026-09-29`, four runs: 11 engines, 1,174 raw skill files, 3 coordination skill files each time. `skill-inventory.jsonl` equal within each back-to-back pair (A=B `43a8b227…`, C=D `981aa76c…`); `baseline.json` A `7b61d10f…` ≠ B `9722c425…` (srs `scripts/diagram-render/package.json` appeared), C ≠ D (dev and srs edits in flight). Two-run equality `NOT_ASSESSED (concurrent executor edits)`.
- **Defect for the orchestrator:** `kaizen_portfolio_snapshot.py` line 49 returns `result.stdout.strip()`, which removes the leading space of the first `--porcelain` line; the first dirty path per repository loses its first character (`EADME.md`, `atalog/engines.yaml`). Not fixed here (outside M10-00 scope).
- **Observation:** srs-skills has an untracked `scripts/diagram-render/node_modules/` tree (thousands of files) from another executor; check it is ignored before staging.

## T12

- Log records Peter's answer as relayed ("D-M10-01 APPROVED: stop-the-line repairs may be pushed ahead of the 3-phase push gate"), dated 29 Sep 2026, disposition `ACCEPT WITH DOCUMENTED DEVIATION`, not backdated. Peter's exact words were not available to the executor. The brief says "stop-the-line repairs"; the plan package says "the M10-01 dev CI repair". Scope for the SRS build guard needs the orchestrator's confirmation.

## T13

- Log section "M10 change-class matrix": five rows (metadata, workflow-routing, doctrine, runtime-configuration, external-release) with proposer, implementer and acceptor; verdict vocabulary `ACCEPT`, `ACCEPT_WITH_DOCUMENTED_LIMITATIONS`, `REJECT`. `grep` of the "Change classes involved" rows in all 15 phase files finds only these five class names.

## Other verification

- `python -X utf8 scripts/validate-kaizen-cards.py` → exit 1: `README does not link agentic-h2-readiness-card.md`, `three-horizon-ai-adoption-card.md`, `task-runbook-and-integration-evidence.md`. Pre-existing (README and the cards are unchanged in this phase); not fixed here.
- Independent review of M10-00: `NOT_ASSESSED` (pending).
