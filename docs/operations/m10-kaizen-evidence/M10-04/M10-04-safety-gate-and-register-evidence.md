# M10-04 evidence: safety gate (T08, T09) and third-party register (T10)

Executor: M10-04 fork (T08-T10 only), 29 Sep 2026, under Peter's delegated authority.
Zero spend; no git state changes; nothing installed. All edits are unstaged.

## M10-04-T08 (GR-09): safety-gate items 9-11 and Graphify worked example

**Status:** DONE

**Files changed**
- `C:\wamp64\www\chwezi-dev-engine\skills\sdlc-meta\skill-engine-audit\references\skill-safety-gate.md`

**What changed**
- Items 9 (global agent-configuration edits), 10 (git-hook installation) and 11 (default outbound
  model routing) added after item 8. Item 1 is unchanged; item 9 states explicitly that how a step
  is fetched is item 1 and item 9 covers what it changes, so there is no duplication.
- Three red-flag phrases added.
- "Worked example: Graphify (items 9-11)" table citing pinned line ranges.

**Source read (read-only fetch, no install)**
- `curl -sSfL https://raw.githubusercontent.com/Graphify-Labs/graphify/d6eaa8aae8df155874ebb1044302c055c286342a/graphify/install.py`
  -> 2,420 lines, SHA-256 `2fd6e4e78e40e234af8a2134f67235e89ecaab89007719ce4f989489a6c7c796`.
- Same commit `graphify/hooks.py` -> SHA-256 `00b541f24ddfe6d45b7903a21fe0e849cee9b6fb5ff28580b74f27c649cdf975`.
- Same commit `README.md` (for the provider-priority lines).
- Copies kept only in the session scratchpad; not committed anywhere.

| Citation | Content verified |
|---|---|
| `install.py` l.732-749 | `install()` resolves `~/.claude/CLAUDE.md` (or `$CLAUDE_CONFIG_DIR`) and calls `_register_always_on_block` |
| `install.py` l.375-418 | `_register_always_on_block` writes or creates the target file |
| `install.py` l.365-374 | `_skill_registration` block text (`# graphify`) |
| `install.py` l.329-364 | `_claude_pretooluse_hooks`: two PreToolUse entries, 10 s timeout |
| `install.py` l.1859-1880 | `_install_claude_hook` merges them into `.claude/settings.json` |
| `install.py` l.1831-1858 | `claude_install` calls `_install_claude_hook` |
| `hooks.py` l.628-656, l.864-892 | git post-commit / post-checkout hook writes, `core.hooksPath`, merge driver |
| `README.md` l.592-593 | provider auto-detection order; Kimi routes to Moonshot AI servers |

Attribution: Graphify-Labs/graphify (Apache-2.0, https://github.com/Graphify-Labs/graphify,
commit d6eaa8aae8df155874ebb1044302c055c286342a). No code or text copied, so no NOTICE obligation.

## M10-04-T09 (AR-16): bounded outbound check exemplar

**Status:** DONE

**Files changed:** same `skill-safety-gate.md`.

Section "Bounded outbound check (positive exemplar)" lists the six properties (timeout, response
cap, TTL with back-off, opt-out variable, notice without install, silence is never consent) with
the Archify attribution (tt-a1i/archify, MIT per report 09 l.17, commit 0e4949f910a8e390bd3b4933883a4dcabad571be), plus
the checklist question "For each outbound call in the skill, its scripts or its installer, which
of the six properties does it have?". Facts taken from report 09 section 3 (T1-10/T1-11); the
Archify source was not re-fetched here.

## M10-04-T10 (AC-04): third-party register, schema, intake procedure, links

**Status:** DONE_WITH_LIMITATIONS (dev routing fixture delivered as a patch, not applied)

**Files added / changed**
- `C:\wamp64\www\chwezi-engine-agents\docs\security\third-party-skill-register.json` (new, 15 rows)
- `C:\wamp64\www\chwezi-engine-agents\schemas\third-party-skill-register.schema.json` (new)
- `C:\wamp64\www\chwezi-dev-engine\skills\sdlc-meta\skill-engine-audit\references\ecosystem-scan-and-intake.md` (new)
- `C:\wamp64\www\chwezi-dev-engine\skills\sdlc-meta\skill-engine-audit\SKILL.md` (Use When bullet,
  References entry, description gains "or vetting a third-party skill repo before borrowing from it")
- `C:\wamp64\www\digital-research-engine\skills\skill-taxonomy-and-routing\SKILL.md` (one link line)
- `C:\wamp64\www\digital-research-engine\skills\skill-safety-audit\SKILL.md` (one link line)

**Register design.** Fields mirror the T10 note (component, url, commit, license_spdx,
stars_at_review, last_push, archived, scripts_present, network_behavior, credential_asks,
install_method, vendored_copy_of, overlap_paths[], verdict, reason, reviewed_on, review_after,
reviewer) with the top-level `schema_version` / `review_date` / `scope` style of
`supply-chain-register.json`. Verdict enum `study | borrow_idea | ignore | block` (no "safe to
install"). Commits: report 08 gives no commit for the 15 candidates except the anthropics/skills
upstream `fa0fa64` (rows 2 and 6); all other commits are `NOT_ASSESSED`. `archived`,
`network_behavior`, `credential_asks` and `install_method` are `NOT_ASSESSED` throughout
(the report did not record them per row); nothing was invented. Row 15 groups the four unlicensed
repositories (URL array, `NOASSERTION`, stars "23-468").

**Delegated decisions (orchestrator under Peter's delegated authority, 29 Sep 2026)**
- `reviewed_on` 2026-09-29 (date of the report's API reads); `review_after` 2026-12-29 (one quarter).
- Row 1 licence recorded as MIT (licence file) with the API's NOASSERTION noted in `reason`.
- The skill-engine-audit description was reworded to route third-party vetting: the trailing
  sentence "Measures taxonomy, contracts, routing, safety, and readiness." was dropped to stay
  within 350 characters (now 310). Without the change the new fixture misroutes (top 3:
  github-ops, execution-plan-scripts, code-safety-scanner).

**Commands and results**
- `python -X utf8 scripts/validate-contracts.py --schema schemas/third-party-skill-register.schema.json --instance docs/security/third-party-skill-register.json`
  (CLI verified: `--schema` and `--instance` are both required) -> `PASS`, exit 0.
- Negative check: same command on a scratch copy with row 1 verdict `safe_to_install` -> `FAIL
  entries.0.verdict: 'safe_to_install' is not one of [...]`, exit 2.
- dev `python -X utf8 skills/sdlc-meta/skill-writing/scripts/quick_validate.py skills/sdlc-meta/skill-engine-audit` -> `Skill is valid.`
- dev `python -X utf8 skills/sdlc-meta/skill-writing/scripts/contract_gate.py --skill skill-engine-audit` -> 0 errors, 0 warnings, exit 0.
- dev `python -X utf8 scripts/skill_catalog_guardrails.py --report-only` -> 167 active, 0 findings.
- dev `python -X utf8 scripts/routing_smoke_test.py` (current fixtures, unchanged file) -> 187
  fixtures, p@1 179/187, p@3 187/187, 0 failures.
- dev in-memory simulation (scratch script importing `routing_smoke_test`, all existing fixtures
  plus the new one, with the edited description on disk) -> 188 fixtures, p@1 180, 0 failures;
  the new task ranks `skill-engine-audit` first.
- DRE `python -X utf8 scripts/skill_contract_validator.py --baseline tests/skill-engine/quality-baseline.json` -> 59/59 fully compliant, failure counts {}, exit 0.
- DRE `python -X utf8 scripts/routing_smoke_test.py` -> 29/29 top-3 precision 1.000, exit 0.
- agents `python -X utf8 scripts/render_host_files.py --check` -> 12 repositories, 0 findings.

**Patch for the orchestrator (not applied: `scripts/routing_fixtures.yml` is being edited by M10-06)**

Append under the sdlc-meta / skill-engine-audit fixtures in
`chwezi-dev-engine/scripts/routing_fixtures.yml` (near the existing `expect: skill-engine-audit` entry, line 185 at the time of writing):

```yaml
  - task: "Vet this third-party skill repo before we borrow from it"
    expect: skill-engine-audit
```

After applying, rerun `python -X utf8 scripts/routing_smoke_test.py` (expected: 188 fixtures,
0 failures, per the simulation above).

## Open items

1. Apply the routing-fixture patch once M10-06 releases `scripts/routing_fixtures.yml`.
2. Register fields marked `NOT_ASSESSED` (commit SHAs, archived flag, network behaviour,
   credential asks, install method) are to be filled by the first quarterly scan (M10-13 BL-13a).
3. Peter's ratification is required for the doctrine-class safety-gate additions (phase exit criteria).
