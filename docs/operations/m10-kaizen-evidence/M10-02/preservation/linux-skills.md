# Preservation map — linux-skills (M10-02-T02)

Contract: `docs/operations/claude-bridge-contract.md`. Pilot template: `preservation/design-system-skills.md`.
Classification decided by the executor under Peter's delegated authority, 29 Sep 2026; reviewer ticks left open for the
independent reviewer.

## Hashes and sizes

| File | Pre SHA-256 | Pre bytes | Post SHA-256 | Post bytes |
|---|---|---|---|---|
| `CLAUDE.md` | `ef7f886a30388dc1a433c83e334afbbd245a15df60cddb52644004fbd6514c54` | 10,502 (LF) | `937ff7e40a04988a685db64a66cfd429911e525c521bfd8b60c4d96a6e38cfbf` | 362 (LF) |
| `AGENTS.md` | `b6f557c0c55ee0958fe7831c2278c4cecf0709d304a99d7fafabebb1dbc0f853` | 16,633 (CRLF working copy) | `fd2a62ceda9ee76ea69bea1e9d3d655d66f0fb3b3e3e8b3b80ece50360996b5d` | 21,182 (LF) |

Router effective bytes (`CLAUDE.md` plus `@`-imported files): before 10,502 (no `@AGENTS.md` import, so Claude loaded only
`CLAUDE.md`); after 362 + 21,182 = 21,544. Claude now loads the full runner-neutral router, including the Codex-only
section it is told to skip. `AGENTS.md` was rewritten with LF endings; `git diff --stat` shows +60/−0 for it.

Design trigger block: the `CLAUDE.md` copy (L152–170) and the `AGENTS.md` copy (L210–228 pre-change) are byte-identical
`v2` after CRLF normalisation (`diff` empty), so the `CLAUDE.md` copy is a duplicate. The earlier drifted runner-neutral
`v1` noted in the baseline is gone.

## Sentence table

Headings (`# Linux Skills Knowledge Base`, `## Two-family engine`, `## Structure`, `## Skills`, `## Engine design`,
`## Key Rules`) are structural; their content moves to the named `AGENTS.md` sections.

| ID | Source line | Sentence (abridged) | Class | Destination | Reviewer |
|---|---|---|---|---|---|
| S01 | 3 | Repo contains Linux skills, commands, tips, and notes | doctrine-moved | AGENTS.md §Purpose (verbatim, new paragraph) | [ ] |
| S02 | 4 | Claude Code reads this repo automatically every session | Claude-mechanics | Claude-only block, bullet 1 ("the `@AGENTS.md` import loads the full router" appended) | [ ] |
| S03 | 8–10 | Two-family engine: every skill and `sk-*` script supports Debian/Ubuntu and RHEL family | duplicate | AGENTS.md §Two-Family Support, first paragraph | [ ] |
| S04 | 12–13 | Each specialist skill leads with `## Distro support` matrix mapping commands/paths/services | duplicate | AGENTS.md §Two-Family bullet 1 ("its first H2 … command/path/service") | [ ] |
| S05 | 14–17 | Never hardcode apt/ufw/apache2; use common.sh primitives incl. `require_family <debian/rhel/any>` | duplicate + doctrine-moved | Primitive list duplicates §Two-Family bullet 2; the argument form moved as new bullet "`require_family` takes `<debian\|rhel\|any>`" | [ ] |
| S06 | 18–21 | Big family differences: SELinux/AppArmor, firewalld/UFW, httpd/apache2, NM/Netplan, dnf-automatic, wheel/sudo, Kickstart | doctrine-moved | AGENTS.md §Two-Family, new bullet (verbatim) | [ ] |
| S07 | 21 | Deep-dive references live under the relevant skills | duplicate | AGENTS.md §Two-Family bullet 3 ("each lives under its owning skill's `references/`") | [ ] |
| S08 | 22 | Plan, phasing, status: `docs/multi-distro/plan.md` | duplicate | AGENTS.md §Two-Family bullet 4 | [ ] |
| S09 | 23–24 | check-distro-matrix.sh asserts every specialist skill carries a matrix; run after adding/editing | doctrine-moved | AGENTS.md §Two-Family, new bullet ("must pass" was already there) | [ ] |
| S10 | 28 | `linux-sysadmin/` hub routes to all specialist skills | doctrine-moved | AGENTS.md new §Repository structure (verbatim) | [ ] |
| S11 | 29–34 | `NN-category/linux-*/` in 15 named categories (full list) | doctrine-moved | AGENTS.md §Repository structure (verbatim) | [ ] |
| S12 | 35–41 | `16-network-equipment/` appliance skills (Cisco, Netmiko, validation), added 2026-09-20, exempt from Distro invariant | doctrine-moved | AGENTS.md §Repository structure (verbatim; §Purpose already carried the exemption) | [ ] |
| S13 | 42 | `meta/` engine-authoring skills | doctrine-moved | AGENTS.md §Repository structure | [ ] |
| S14 | 43 | `commands/` command references by topic | doctrine-moved | AGENTS.md §Repository structure | [ ] |
| S15 | 44 | `scripts/` reusable shell scripts and snippets | doctrine-moved | AGENTS.md §Repository structure | [ ] |
| S16 | 45 | `notes/` general notes and troubleshooting guides | doctrine-moved | AGENTS.md §Repository structure | [ ] |
| S17 | 49 | This repo IS the Claude Code skills directory | Claude-mechanics | Claude-only block, bullet 2 | [ ] |
| S18 | 49–50 | On a server it may be placed in the configured Claude skill root so skills load automatically | Claude-mechanics | Claude-only block, bullet 2; also covered by AGENTS.md §Purpose L73–76 | [ ] |
| S19 | 50–51 | `scripts/setup-claude-code.sh` adapter is optional, not required | duplicate | AGENTS.md §Portable entry points, Claude Code bullet ("optional … not prerequisites") | [ ] |
| S20 | 51–53 | Review its `--dry-run` plan; supply exact targets, action choices, authority flags, new recovery-file path | doctrine-moved | AGENTS.md §Portable entry points, Claude Code bullet (added sentence; "action choices" was the extra detail) | [ ] |
| S21 | 53–54 | It never pulls an existing checkout or executes a downloaded shell script | doctrine-moved | AGENTS.md §Portable entry points, Claude Code bullet (verbatim) | [ ] |
| S22 | 56–57 | Use `linux-sysadmin` as entry point; hub routes to all 41 specialist skills in 15 categories | duplicate | AGENTS.md §Routing ("default entry point") and §Baseline Skills ("routing hub"). Count checked: 41 `linux-*` specialist skills on disk, 41 names listed; §Purpose's 44/16 includes the 3 network-equipment skills | [ ] |
| S23 | 60 | `linux-bash-scripting` meta-skill; load before writing/reviewing `sk-*` scripts | duplicate | AGENTS.md §Baseline Skills bullet 2 and §Routing last paragraph; the contents summary is that skill's own `SKILL.md` description | [ ] |
| S24 | 62–130 | 40 per-skill list rows (01 Provisioning … 15 Compliance), name + one-line summary | duplicate (row group) | All 40 names appear in AGENTS.md §Routing (scripted check: 0 missing); each one-line summary is a shortened form of that skill's frontmatter `description`, the filesystem index | [ ] |
| S25 | 134 | All conventions live in `docs/engine-design/spec.md` | doctrine-moved | AGENTS.md new §Engine design (verbatim) | [ ] |
| S26 | 135–136 | Skill authoring and July 2026 release gates in `skill-authoring-standard.md` | doctrine-moved | AGENTS.md §Engine design (verbatim; §Routing linked the standard without "July 2026 release gates") | [ ] |
| S27 | 137–138 | Zero-debt gates are the two exact commands; run both after changing a contract or route | doctrine-moved | AGENTS.md §Engine design (verbatim) | [ ] |
| S28 | 139 | Script catalogue (~88 scripts) in `script-inventory.md` | doctrine-moved | AGENTS.md §Engine design | [ ] |
| S29 | 140 | Scripts install to `/usr/local/bin/` with `sk-` prefix via `install-skills-bin` | doctrine-moved | AGENTS.md §Engine design | [ ] |
| S30 | 141 | Hybrid install: `core` at setup, per-skill lazy install | doctrine-moved | AGENTS.md §Engine design | [ ] |
| S31 | 142 | Every script sources `/usr/local/lib/linux-skills/common.sh` | doctrine-moved | AGENTS.md §Engine design | [ ] |
| S32 | 146 | Two-family by default: new/edited skill MUST carry matrix as first H2; scripts MUST use primitives | doctrine-moved | AGENTS.md §Working Rules (verbatim bullet) | [ ] |
| S33 | 147 | Author attribution mandatory: credit Peter Bamuhigire in frontmatter, script headers, doc footers | doctrine-moved | AGENTS.md §Working Rules (verbatim bullet) | [ ] |
| S34 | 148 | Scripts track skills automatically; proactively update affected scripts in the same session | doctrine-moved | AGENTS.md §Working Rules (verbatim; the existing "update related script docs" bullet lacked "proactively … do not wait to be told") | [ ] |
| S35 | 149 | New repo on server must be added to `update-all-repos` and `update-repos` | doctrine-moved | AGENTS.md §Working Rules (verbatim bullet) | [ ] |
| S36 | 150 | First use on a new server: `install-skills-bin <skill>`; `core` for initial setup | doctrine-moved | AGENTS.md §Working Rules (verbatim bullet) | [ ] |
| S37 | 152–170 | Design trigger block `v2` | duplicate | AGENTS.md trigger block (byte-identical after CRLF normalisation) | [ ] |

## Portfolio doctrine localised (not a `CLAUDE.md` move)

| ID | Addition | Reason | Reviewer |
|---|---|---|---|
| P01 | AGENTS.md new §Never store book extractions (paragraph modelled on windows-admin's) | Linux had no book-extraction ban in any router file; the portfolio rule in chwezi-engine-agents ("Never store book extractions in any engine or in this package") already binds it. Decided under Peter's delegated authority, 29 Sep 2026 | [ ] |

No existing `AGENTS.md` sentence was rewritten. §Working Rules still says "Keep repo-level policy in `AGENTS.md` and
Claude-specific policy in `CLAUDE.md`", which remains true under the bridge contract (Claude-only mechanics only).

## Counts

| Class | Count |
|---|---|
| duplicate | 10 rows (S03, S04, S07, S08, S19, S22, S23, S24 = row group of 40, S37; plus S05 in part) |
| doctrine-moved | 24 rows (S01, S05 in part, S06, S09–S16, S20, S21, S25–S36) |
| Claude-mechanics | 3 rows (S02, S17, S18) |
| obsolete | 0 |
| **Lost** | **0** |

## Manifest additions (`.skills-engine/engine-manifest.yaml`)

- `claude_only_block`: identical to the `CLAUDE.md` section body (checked programmatically).
- `invariants`: `book-extraction-ban` ("Book extractions, book summaries and chapter-by-chapter notes must never be stored
  in this"), `not-assessed` ("Missing host, lab, source, live, or recovery evidence is `NOT ASSESSED`, never a pass.").
  Both phrases verified present in the post-change `AGENTS.md`.
- `invariant_exemptions.british-english`: no British English output rule exists in the linux router (AGENTS.md, former
  CLAUDE.md, README.md, rules/); adding one would be new doctrine.

## Validators (engine root, 29 Sep 2026)

| Command | Result |
|---|---|
| `python -X utf8 scripts/validate_skills.py --baseline quality-baseline.json` | exit 0; 48 active skills, fully compliant 48, failure counts {} |
| `python -X utf8 scripts/routing_smoke_test.py` | exit 0; 30/30 passed, precision 1.000 |
| `bash scripts/tests/check-distro-matrix.sh` (Git Bash on Windows) | exit 0; passed 41, failed 0 (structural only; Linux-native host behaviour NOT_ASSESSED) |
| `python -X utf8 tests/agent-integration/test_linux_agent_contract.py` | exit 0; PASS |
| Scripts/tests referencing `CLAUDE.md` (`grep` over `*.py`, `*.sh`, `*.js`) | none |
