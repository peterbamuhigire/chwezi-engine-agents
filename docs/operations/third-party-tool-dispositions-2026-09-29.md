# Third-party tool dispositions — 29 September 2026

**Operation:** my-10-kaizen, phase M10-00 (task T04). **Records:** D1–D5 (backlog items SP-02, UA-01, AR-18, GR-13, UX-15).
**Vocabulary:** Adopt / Harden / Reference / Defer / Reject, reused from the Pocock disposition register (`chwezi-dev-engine/docs/sept-matt-pocock/03-skill-disposition-register.md`), with ABSORB meaning "keep the tool as an optional helper and absorb its patterns into engine doctrine".
**Authority:** decided by the orchestrator under Peter Bamuhigire's delegated authority, 29 Sep 2026, taking the plan's recommended option for each record. These are doctrine-class dispositions; Peter's exact-text ratification remains open and is tracked in the M10 running log.
**Location note:** UA-01 proposed `docs/architecture/decision-records/`. This single consolidated file is used instead, because P04 declined a new ADR set without a measured defect, and ADR-001 is reserved for architecture.

Evidence sources are the my-10-kaizen repository reports (`my-10-kaizen/01-repo-reports/`, plan package under `C:\Users\Peter\Documents\`). Third-party text is paraphrased, not copied.

---

## D1 — SP-02 Superpowers (obra/superpowers, MIT): ABSORB; keep as an optional helper; UPGRADE

- **Decision.** Keep Superpowers installed for coding sessions only, as an optional accelerator. Upgrade from 4.3.1 (commit `e4a2375`, installed 22 Feb 2026) to 6.4.2 (commit `8ca22dba9a94f28898bbce59f2537ff4d87c747d`, 25 Sep 2026). Set `SUPERPOWERS_DISABLE_TELEMETRY=1`.
- **Rationale.**
  - The local install was 18 releases behind.
  - Its SessionStart hook used the single-quoted `${CLAUDE_PLUGIN_ROOT}` form that upstream v5.0.2 records as failing on Windows, and v6.2.0 fixed a PowerShell parse failure that left the bootstrap unloaded without warning. The bootstrap may not have been loading on this machine.
  - The brainstorming visual companion fetches a vendor logo carrying the version string unless telemetry is disabled.
- **Conditions.**
  - No engine may name a `superpowers:*` skill as a mandatory step. SP-01 removes the two mandatory calls in M10-06 and M10-08.
  - The engines' own gates remain authoritative.
  - v6.4.1 changed `executing-plans` to run the whole plan without periodic check-ins, so M10 executors keep their own checkpoints.
  - American-English upstream text is never copied; adaptations are paraphrased with MIT attribution and the commit.
- **Execution state (29 Sep 2026).** Upgrade applied through the Claude Code plugin manager (`installed_plugins.json` now shows 6.4.2, `gitCommitSha 8ca22db…`); user environment variable set. The clean-session acceptance prompt is `NOT_ASSESSED` (zero-spend rule). See `m10-kaizen-evidence/M10-00/`.
- **Evidence.** Superpowers report §1 and §6; `~/.claude/plugins/installed_plugins.json`.
- **Review by:** the next Superpowers minor release, or 29 Dec 2026, whichever comes first.
- **Reversal trigger:** the acceptance prompt fails to invoke brainstorming, or the upgrade breaks a documented plan header. Rollback: reinstall 4.3.1 through the plugin manager and remove the environment variable.

## D2 — UA-01 Understand Anything (Egonex-AI/Understand-Anything, MIT): REJECT estate-wide install; DEFER a bounded pilot

- **Decision.** Do not install the Understand Anything plugin or its hooks on the engines or estate-wide. Inspected at commit `b05cc3b20990afca537b4fc0a49b4d7fbdc65bb0`.
- **Pilot conditions**, applied only to a client codebase where a human team needs onboarding and Peter selects it:
  - marketplace install only, never `curl | bash` or `iwr | iex`;
  - a pinned version, with `autoUpdate` off and hooks not enabled;
  - one codebase;
  - token spend logged;
  - no agents that write and execute their own scripts;
  - output rewritten in British English.
- **Exclusivity.** Never run it together with Graphify on the same repository.
- **Rationale.**
  - The installer is unpinned, and its `--update` path makes upstream changes live without review.
  - Its hooks inject an instruction not to ask the user for confirmation.
  - The `tour-builder` agent executes model-authored scripts, which the engine manifests list as the forbidden operation `arbitrary_shell`.
  - Nine `understand-*` skills would collide with `doc-architect`.
- **Borrowed instead.** Topology-ordered tours (M10-06) and deterministic engine tours (M10-12).
- **Evidence.** Understand Anything report §6.1, §6.2 and §6.4.
- **Review by:** 29 Dec 2026, or when Peter names an onboarding workload, whichever comes first.
- **Reversal trigger:** a pinned, reviewed release that removes the confirmation-suppressing hook text and the self-executing agents, **and** a named onboarding workload.

## D3 — AR-18 Archify (tt-a1i/archify): REJECT estate-wide install; personal use permitted

- **Decision.** Do not install Archify into any engine or build, and never into SRS project skill folders. Personal use for interactive HTML is permitted only at tag `v3.0.1` (commit `0e4949f910a8e390bd3b4933883a4dcabad571be`) with `ARCHIFY_UPDATE_CHECK_DISABLED=1`.
- **Rationale.**
  - Its closed schema (`additionalProperties: false`) has no field for requirement IDs, and there is no CLI image export.
  - It has no ERD or class-diagram kinds.
  - It needs Node 18+ and Chrome for `finalize`.
  - It makes a daily outbound update check.
  - Upstream moved from v2.16.0 to v3.0.1 in four weeks, including a breaking viewer change.
  - Its triggers ("architecture", "sequence", "Mermaid") would pre-empt SRS HLD/LLD routing.
- **Borrowed instead.** The typed diagram IR, closed-world checks, evidence pins and repair receipts are re-implemented in Python in SRS (M10-01 AR-01 to AR-03; M10-07).
- **Evidence.** Archify report §6.
- **Review by:** close of M10-07, or 29 Dec 2026, whichever comes first.
- **Reversal trigger:** upstream gains a CLI image export and an extensible trace field, and an SRS pilot shows lower maintenance cost than the in-house IR.

## D4 — GR-13 Graphify: REJECTED for this host (P06 stands); evidence addendum

- **Decision.** No change to the P06 rejection. The new facts are appended to P06 in `skills-kaizen-execution-2026-09-26.md` ("P06 addendum"), and the LSP-pilot workload is named. Host adoption is not re-opened; P06 remains IN_PROGRESS.
- **New evidence** (pinned at 0.9.71, commit `d6eaa8aae8df155874ebb1044302c055c286342a`):
  - the licence changed from MIT to Apache-2.0 at 0.9.25 on 22 Jul 2026;
  - the README privacy paragraph still contradicts the default-off query log at 0.9.71;
  - PHP instance-method calls produce no `calls` edge (issues #1682, #2615, #3830);
  - `.inc` files are parsed as Pascal (#2961);
  - a global `graphify install` writes into `~/.claude/CLAUDE.md` and registers PreToolUse hooks.
- **Named workload for the deferred LSP pilot.** "PHP/MySQL ERP maintenance on one disposable repository copy". This satisfies the P06 condition that the pilot is deferred until a representative workload is named. It does not start the pilot.
- **Borrowed instead.** Graph-first comprehension doctrine and evidence tags (M10-06); as-built recovery (M10-08).
- **Evidence.** Graphify report §0 and §6; P02-T03 (`ad8e050`) source review and pin; EXEC P06 section.
- **Review by:** 29 Dec 2026, or the next Graphify minor release that touches logging or PHP parsing, whichever comes first.
- **Reversal trigger:** the package and logging are reconciled **and** the PHP member-call issues are closed with a test.

## D5 — UX-15 UI UX Pro Max (nextlevelbuilder/ui-ux-pro-max-skill, MIT): REJECT install; REJECT data reuse; record provenance

- **Decision.** Do not install UI UX Pro Max (inspected at `09170eec67eefd46a7ae85de61b40c194020f997`) and do not reuse its font, palette or style data.
- **Rationale.**
  - 23 of its 74 font pairings (31 %) use a face the doctrine bans, and no row cites a human typographic authority.
  - Its skill description would route work around the ban.
  - Its "parallel searches" claim is false: the searches run in a plain loop.
- **Provenance.** Design commit `02aa6c9` (20 Sep 2026) introduced `engine/design_engine/catalog.py`, whose `DOMAINS` and `STACKS` tuples match UI UX Pro Max's 12 domains and 22 stacks exactly; no engine file named the project. Recorded position: `PROVENANCE: UNDETERMINED — attributed defensively` (convergent; MIT attribution added as a precaution) in `design-system-skills/docs/continuous-improvement/design-catalog-provenance-2026-09-29.md`.
- **Borrowed instead.** The catalogue is filled with human-sourced data and wired to skills (M10-10).
- **Evidence.** UI UX Pro Max report "Bottom line" and §5.1.
- **Review by:** M10-10 close, or 29 Dec 2026, whichever comes first.
- **Reversal trigger:** none planned; the project remains an evidence source for bans only. A firmer provenance statement from Peter is recorded as a new dated entry in the design provenance record.
