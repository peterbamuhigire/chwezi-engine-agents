# M10-14 follow-up: remote CI repair evidence (29 Sep 2026)

Scope: make GitHub Actions CI green on `main` for srs-skills, digital-research-engine (GitHub repo
`digital-research-skills`), proposal-skills, business-plan-skills, social-media-skills, linux-skills and
windows-admin-engine-skills (kaizen record §10–11, items 1–2), plus the dev-engine font breach (item 32).
Zero spend. No commit or push: every edit is unstaged for the orchestrator. Decisions below were taken by
the orchestrator's executor under Peter's delegated authority, 29 Sep 2026.

## 1. Root cause (reproduced)

`gh run list --limit 3` and `gh run view <id> --log-failed` for the failing runs at the M10-14 heads:

| Repo | Run | Failing step | Log finding |
|---|---|---|---|
| srs-skills | 36524777849 | `validate_skill_engine.py --baseline` | `hospitality-operating-model-srs/SKILL.md: broken_relative_link` |
| digital-research-engine | 36524782879 | `skill_contract_validator.py --baseline` | `broken_relative_link: 2` |
| proposal-skills | 36523434653 | `validate_skills.py --baseline` | `broken_links: 4` |
| business-plan-skills | 36524798785 | `validate_skill_engine.py --baseline` | 2 × dev-engine standard, 1 × DRE gate, 1 × `C:/wamp64/www/chwezi-accounting-doctrine/README.md` |
| social-media-skills | 36524287017 | `validate_skill_engine.py --baseline` | `broken_relative_link: 5` |
| linux-skills | 36524264494 | `validate_skills.py --baseline` | `../../../digital-research-engine/.../kaizen-currentness-gate.md` |
| windows-admin-engine-skills | 36524270708 | `validate_operator_manual.py` | `missing module function: Get-WseAdminActivityReport` |

Reproduction: each repository was copied (tracked + untracked, non-ignored files) into an isolated
scratch folder with no sibling engines beside it, and the failing step re-run. Six link failures
reproduced (host-absolute `C:/wamp64/...` links still resolved on this machine, which is exactly why
"every validator passes locally"). The windows failure reproduced in the real checkout too.

Why the validators passed locally: each link check did `(skill.parent / target).resolve().exists()`.
On Peter's machine `../../../<sibling-engine>/...` and `C:/wamp64/www/...` both exist; on a runner only
one repository is checked out.

Windows: `Get-WseAdminActivityReport` was already implemented (`Public/Get-WseAdminActivityReport.ps1`)
and exported in both `FunctionsToExport` (psd1) and `Export-ModuleMember` (psm1). The validator requires
every manifest export to be documented in `docs/operations/commands-and-scripts-manual.md`, and the
manual's section 19 table lacked it. Run history showed a second, hidden failure behind it: windows CI had
never been green (32 runs back to 12 Aug); before 16 Sep it failed on
`Legacy Should syntax (without dashes) is not supported in Pester 5` — runners ship Pester 5, the suites
used Pester 3 syntax, and Peter's machine has only Pester 3.4.0, so local runs hid it.

## 2. Decision: portable-link rule (approach chosen)

Options weighed: (a) sibling checkouts in CI; (b) treat sibling links as external when the sibling is
absent; (c) rewrite cross-engine links as GitHub URLs and make local link checks host-independent.

Chosen: (c). Option (b) keeps a check whose result depends on the host, the defect that hid these
failures. Option (a) couples every engine's CI to eleven other repositories. With (c):

- Cross-engine markdown links now point at `https://github.com/peterbamuhigire/<repo>/blob/main/<path>`
  (DRE maps to repo `digital-research-skills`). Every target was checked to exist on the sibling's
  `origin/main` (`git cat-file -e origin/main:<path>`) before rewriting; the rewrite script aborts otherwise.
- Each of the six validators gains `portable_link_target()` + `HOST_ABSOLUTE_LINK`: a local link that is
  host-absolute (`C:/…`, `/C:/…`, `file:`) or resolves outside the repository root is broken, even when the
  target exists on this machine. Local results now predict CI. No existing check was removed; the
  proposal validator's special case that resolved `/C:/…` links against the host was removed (host paths
  are now findings).
- Plain-text host paths in skill text (`C:\wamp64\www\<engine>\…`, including JSON-escaped forms) were
  rewritten as engine-relative names (`<engine>/…`), e.g. "Finance engine (`chwezi-accounting-doctrine`)".

## 3. Changes per repository

### srs-skills
- Links → GitHub URLs: `02-requirements-engineering/hospitality-operating-model-srs/SKILL.md` (lines 156–157).
- Host paths → engine-relative: `01-strategic-vision/02-business-case/references/ai-business-case-addendum.md`,
  `02-requirements-engineering/retail-operating-model-srs/SKILL.md`, `06-deployment-operations/01-deployment-guide/SKILL.md`,
  `09-governance-compliance/04-risk-assessment/SKILL.md`, `09-governance-compliance/05-formal-review-gates/SKILL.md`,
  `09-governance-compliance/05-formal-review-gates/references/uganda-public-sector-and-ngo-delivery-constraints.md`,
  `domains/retail/INDEX.md`.
- Validator: `scripts/validate_skill_engine.py`. Tests: `tests/test_validate_skill_engine_tier1.py`
  (+3: sibling link broken even when present; host-absolute link broken even when target exists; GitHub URL accepted).
  Both negative tests fail against the HEAD validator and pass against the new one.

### digital-research-engine
- Links → GitHub URLs: `skills/ai-slop-audit/SKILL.md`, `skills/anti-ai-slop/SKILL.md`.
- Host path → engine-relative: `skills/source-evaluation/references/book-driven-source-admission-and-currentness.md`.
- Validator: `scripts/skill_contract_validator.py` (both the skill-relative and root-relative candidates must stay inside the repo).
- Fonts: `skills/professional-word-output/SKILL.md`, `references/typography-layout.md`, `references/word-features.md` (see §4).

### proposal-skills
- Links → GitHub URLs: `skills/meta/ai-slop-audit/SKILL.md`, `skills/meta/anti-ai-slop/SKILL.md`,
  `skills/meta/kaizen-improvement-system/SKILL.md`, `skills/profiles-sectors/sectors/hospitality-hotel-restaurant/SKILL.md`.
- Host paths → engine-relative: `skills/language/language-standards/references/english-collocations-and-lexical-precision-2026-09-02.md`,
  `skills/pipeline/06-methodology/references/technical-approach-figures.md` ("on the reference host `C:\…\srs-skills`" →
  "resolved against the local portfolio root"), `skills/profiles-sectors/sectors/hospitality-hotel-restaurant/SKILL.md`,
  `skills/profiles-sectors/sectors/ppda-uganda/references/{contract-management-and-payment-linkage,local-government-procurement,ngo-and-donor-procurement}.md`.
- Validator: `scripts/validate_skills.py`.

### business-plan-skills
- Links → GitHub URLs: `skills/industry-guides/hospitality-hotel-restaurant/SKILL.md`, `skills/meta-strategy/kaizen-improvement-system/SKILL.md`,
  `skills/meta-strategy/references/marketing-plan-handbook-operating-loop.md`, `skills/meta-utility/ai-slop-audit/SKILL.md`,
  `skills/meta-utility/anti-ai-slop/SKILL.md`.
- Host paths → engine-relative: the seven `skills/advisory-deliverables/*/SKILL.md` and their `references/document-blueprint.md`,
  `skills/industry-guides/retail/references/retail-operating-model-and-engine-plan.md`,
  `skills/language/writing-quality/references/english-collocations-and-lexical-precision-2026-09-02.md`,
  `skills/pipeline/00-plan-assembly/references/plan-figures.md`.
- Validator: `scripts/validate_skill_engine.py`. New test: `tests/test_portable_links.py` (4 tests).

### social-media-skills
- Links → GitHub URLs: `skills/ai-marketing/ai-generative-search-optimisation/SKILL.md`, `skills/ai-marketing/ai-slop-audit/SKILL.md`,
  `skills/ai-marketing/anti-ai-slop/SKILL.md`, `skills/sectors/hospitality-hotel-restaurant/SKILL.md`, `skills/seo-discovery/seo-geo-optimisation/SKILL.md`.
- Host paths → engine-relative: `skills/language/language-standards/references/english-collocations-and-lexical-precision-2026-09-02.md`,
  `skills/meta-utility/kaizen-improvement-system/SKILL.md`.
- Validator: `scripts/validate_skill_engine.py` (`local_link_exists` now takes the repo root). New test: `tests/test_portable_links.py` (4 tests).

### linux-skills
- Link → GitHub URL: `meta/kaizen-improvement-system/SKILL.md`. Validator: `scripts/validate_skills.py`.

### windows-admin-engine-skills
- `docs/operations/commands-and-scripts-manual.md`: section 19 rows for `Add-WseAdminActivity` and `Get-WseAdminActivityReport`.
- `scripts/validate_operator_manual.py`: required functions are now read from the manifest's `FunctionsToExport` block
  (previously a verb regex `Get|Test|Invoke|Write` that silently skipped `Add-WseAdminActivity`); an empty/missing block is a finding.
- Pester: `powershell/WindowsSkills.Engine/Tests/WindowsSkills.Engine.Tests.ps1` gains
  "keeps manifest exports, Public files, loaded exports and the operator manual in step"; all four suites
  (`…/Tests/AdminActivity.Tests.ps1`, `…/Tests/WindowsSkills.Engine.Tests.ps1`, `tests/powershell/Install-WindowsAdmin.Tests.ps1`,
  `tests/powershell/Kaizen-Semantics.Tests.ps1`) converted to Pester 5 syntax (`Should -Be/-Match/-BeLike/-Throw`).
- `scripts/test-powershell.ps1`: requires Pester ≥ 5 and fails loudly otherwise (previously it silently ran whatever
  Pester was present); uses `Invoke-Pester -Path`.
- Same-class fixes: `docs/operations/system-admin-activity.md` sibling link → GitHub URL;
  `engine/source-register.yaml` and `skills/meta/windows-portability-doctrine/SKILL.md` host paths → engine-relative.

### chwezi-dev-engine (item 32)
See §4. Files: `skills/product-business/professional-word-output/{SKILL.md, references/typography-layout.md, references/word-features.md,
references/python-document-generation/entrypoint.md, references/python-document-generation/references/{branding-system,pdf-reportlab,pdf-weasyprint,performance}.md,
scripts/create-reference-docx.py, templates/reference.docx}`. Active `SKILL.md` count unchanged at 167.

## 4. Font breach (dev) and the DRE copy

Chosen type (stated per the design charter): **Source Serif 4** headings, **Public Sans** body, **JetBrains Mono** code —
the design engine's DOCX baseline pairing (`docx-report-and-document-formatting`) and its approved monospace; all SIL OFL,
so embeddable and subsettable. Word-safe fallbacks, from `doctrine/references/system-font-fallbacks.md`: Georgia for
Source Serif 4; Segoe UI then Calibri for Public Sans; Consolas for JetBrains Mono — to be named in the delivery note
(silent substitution is a defect).

- Removed: `Inter` as the brand default (`Brand.font_family`, tenant fallback, xlsxwriter title format, ReportLab/WeasyPrint
  TTF registrations → `PublicSans-*.ttf`), `Arial` (typography principle, watermark font, xlsxwriter fallback advice),
  the Calibri/Calibri Light reflex table (SKILL.md and typography-layout.md), and the ReportLab `Helvetica-Bold` heading
  (watchlist face; now the registered brand bold).
- `create-reference-docx.py` constants changed and `templates/reference.docx` regenerated. Check: the HEAD script regenerates
  the committed template byte-identically in `word/styles.xml` (md5 `4a30cb19…`), so the regeneration only changes fonts:
  styles now carry `Source Serif 4` ×4, `Public Sans` ×4 (`Courier` ×2 comes from python-docx's default template, unchanged).
- DRE copy (`digital-research-engine/skills/professional-word-output`) carried the same Calibri table, Calibri watermark and
  "Calibri or Arial" advice; same edits applied. `grep -w "Inter|Arial"` over both skill folders (text files) now returns nothing.
- Left as is (not banned): `DejaVu Sans` in `references/report-print-pdf/entrypoint.md` (watchlist only; used for Unicode
  coverage in PDF engines) — candidate for the next design review.

## 5. Local CI runs (full workflow sequences, isolated copies without siblings)

All commands from each repository's `.github/workflows/*.yml`, run in the isolated copy; `[exit]` shown.

| Repo | Result |
|---|---|
| srs-skills | pytest `--cov-fail-under=90` 96.23 % [0]; `validate_engine.py` [0]; `validate_skill_engine.py --baseline` failure counts `{}` [0]; routing `--min-rank1 83 --lint-fixtures` [0]; owned-negatives + tier1 pytest 15 passed [0]; `engine validate-skills` [0]; SDD boundaries [0]; requirements decision [0]; seed demo [0]; demo validate PASS [0]; `--break-something` negative fails as required [0]; source-ingestion guardrail 0 findings [0] |
| digital-research-engine | contract validator `{}` (59/59 compliant) [0]; routing `--min-rank1 84` [0]; `test_routing_ratchet.py` 5 passed [0]; `validate_engine.py` [0]; source currency PASS [0]; guardrail 0 [0] |
| proposal-skills | `validate_skills.py --baseline` findings 0 [0]; routing top-3 100 % [0]; guardrail 0 [0] |
| business-plan-skills | validator `{}` (137/137) [0]; routing `--threshold 1.0` [0]; evidence register PASS [0]; sector gates PASS [0]; 7 workbooks verified [0]; exemplar packs PASS [0]; 4 release bundles PASS [0]; unittest discover OK [0]; compileall [0]; guardrail 0 [0] |
| social-media-skills | validator 191/191 [0]; source freshness PASS [0]; routing 56/56 [0]; unittest discover OK [0]; guardrail 0 [0] |
| linux-skills | Skill quality: `validate_skills.py --baseline` `{}` (48/48) [0]; routing [0]; `check-distro-matrix.sh` failed 0 [0]; guardrail 0 [0]. Bash suites: safe-operation fixture PASS [0]; `common-sh.test.sh` [1] on this Windows Git Bash host only (`USER: unbound variable`, `detect_distro: family 'unknown'`) — host-specific, file untouched; the remote "Bash suites" workflow is green on ubuntu at HEAD `0f6da83` (run 36524264556). `install-skills-bin.test.sh` needs `sudo` on Linux: NOT_ASSESSED locally |
| windows-admin-engine-skills | `validate_engine` 19/0 [0]; routing 19/0 [0]; guardrail 0 [0]; command tree 48/0 [0]; operator manual 48/14/12 findings=0 [0]; fleet manifest [0]; `unittest discover -s tests/python` 23 OK [0]; `test-powershell-syntax.ps1` 78 files, 0 findings [0]; `test-powershell.ps1` with Pester 5.7.1 → 6 + 4 + 4 + 2 passed, `powershell_smoke=PASS` [0] (real checkout; the scratch copy's very long path pushes the installer's proposed PATH over the 8,191-character gate, a path-length artefact); `install-windows-admin.ps1 -WhatIf` [0] (real checkout) |
| chwezi-dev-engine | `skill_catalog_guardrails.py` [0] (active SKILL.md 167); guardrail unittest OK [0]; `pytest tests` 207 passed, 3 skipped [0]; routing `--min-rank1 88` [0]; collision gate 0 errors [0]; control plane PASS [0]; hook tests 61/61, 7/7 [0]; `contract_gate.py --all` 0 errors [0] |

Negative/mutation checks:
- `portable_probe.py` (scratch) against each validator: worktree versions flag sibling and host-absolute links and accept
  in-repo and GitHub links (6/6 PASS); the HEAD versions accept both non-portable links (6/6 DIFF) — the defect.
- Windows: removing the backticked `Get-WseAdminActivityReport` row from a copy of the manual makes the new Pester test fail (5 passed, 1 failed).
- `test-powershell.ps1` on this host without Pester 5 exits 1 with "Pester 5 or later is required (found: 3.4.0)".

Pester 5.7.1 was obtained for verification only, by downloading the PSGallery nupkg into the scratch folder and
prefixing `PSModulePath` for the session; Peter's installed modules were not changed.

## 6. Limits and open items

- Remote CI result after push: NOT_ASSESSED until the orchestrator pushes (no push rights for executors).
- Windows installer `-WhatIf` step on the runner depends on the runner's user PATH length (+≈4.2k characters for 51 command
  directories under `D:\a\…`); it passes locally; runner result NOT_ASSESSED until pushed. It has never run remotely before,
  since earlier steps always failed.
- Peter's machine has Pester 3.4.0 only: `scripts/test-powershell.ps1` now stops with an install hint until he runs
  `Install-Module Pester -MinimumVersion 5.0 -Scope CurrentUser -SkipPublisherCheck`.
- Not changed (outside CI or registered elsewhere): the six `skill-writing` pointer stubs still name a local path in prose
  (`local path C:\wamp64\…`); they are hash-registered variants in `chwezi-engine-agents/catalog/shared-assets.yaml`, so
  changing them needs a paired re-registration in the agents repo. Router files `srs-skills/AGENTS.md` (lines 68, 152) and
  `proposal-skills/AGENTS.md` (lines 81–108) link to `/C:/wamp64/www/<self>/…` paths (host-dependent; repo-relative links
  would be correct). Historical records keep their original links (`digital-research-engine/docs/continuous-improvement/ai-slop-responsibility-assessment-2026-09-11.md`
  → old `skills-web-dev` name; `windows-admin-engine-skills/docs/audits/2026-09-06-kaizen*.md`; srs `docs/continuous-improvement/kaizen-wave-*`).
- Portfolio rule to record in chwezi-engine-agents (next Kaizen): "cross-engine references are GitHub URLs or plain engine
  names; validators treat host-absolute and repository-escaping links as broken". Not written into agents here (out of scope).
