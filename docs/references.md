# References

The sources this package cites. They were moved here from the README on 31 October 2026 as part of the README kaizen; the entries are unchanged except for links, which are now relative to this folder. The README keeps the counts and a link to this page: 12 repositories, 13 groups of standards and official sources, 6 entries under websites and articles, and no books.

## Books

No books are cited in this repository.

## Repositories

Repositories from the my-10-kaizen study (29 Sep 2026) from which this package adapted methods. All adaptations are paraphrased or re-implemented; no text or code is copied.

- addyosmani/agent-skills — https://github.com/addyosmani/agent-skills — MIT — commit `2686b62`: the one-screen lifecycle map; the lexical routing tokeniser, stemmer, IDF and owner-outranks-self rule (`scripts/lexical_routing.py`); Tier-3 behavioural evaluation mechanics (`scripts/run_behavioural_eval.py`).
- DietrichGebert/ponytail — https://github.com/DietrichGebert/ponytail — MIT — commit `e3ba2aa`: canary-invariant and version-consistency checks (`scripts/render_host_files.py`); arm isolation and self-test discipline for behavioural runs; the honest-reporting structure of the behavioural report template.
- obra/superpowers — https://github.com/obra/superpowers — MIT — commit `8ca22db`: Windows hook failure modes recorded in the drift checker and Claude bridge contract.
- pbakaus/impeccable — https://github.com/pbakaus/impeccable — Apache-2.0 — commit `114ea1d`: the split between durable project truth and task detail, and the report-only doctor (`scripts/project_context_doctor.py`).
- Egonex-AI/Understand-Anything — https://github.com/Egonex-AI/Understand-Anything — MIT — commit `b05cc3b`: fan-in as an importance signal (`scripts/skill_fanin.py`); install rejected, see the tool dispositions.
- Graphify-Labs/graphify — https://github.com/Graphify-Labs/graphify — Apache-2.0 — commit `d6eaa8a`: provenance-tagged edges, the never-invent-an-edge rule and the shrink guard (`scripts/skill_graph.py`); host adoption rejected.
- JuliusBrussee/caveman — https://github.com/JuliusBrussee/caveman — skill text MIT — commit `2fd153c`: "measure before cutting" (`scripts/skill_usage_scan.py`); no BSL code used.
- nextlevelbuilder/ui-ux-pro-max-skill (UI UX Pro Max) — https://github.com/nextlevelbuilder/ui-ux-pro-max-skill — MIT — commit `09170ee`: BM25 defaults and calibration idea (`scripts/lib/retrieval_metrics.py`).
- ComposioHQ/awesome-claude-skills — https://github.com/ComposioHQ/awesome-claude-skills — no root licence — commit `be2a406`: red-flag patterns for imported setup text (`tests/fixtures/prompt-injection/red-flag-patterns.md`) and the seed list for the third-party skill register.
- tt-a1i/archify — https://github.com/tt-a1i/archify — commit `0e4949f`: reviewed; estate-wide install rejected (tool dispositions, D3). Its diagram ideas were adopted in `chwezi-sdlc-documentation`, not here.
- anthropics/skills — https://github.com/anthropics/skills — Apache-2.0 — commit `3337550`: the `mcp-builder` evaluation method used for the coordinator MCP tool-surface evaluation (`evals/mcp/coordinator-qa.yaml`).
- affaan-m/ECC — https://github.com/affaan-m/ECC — commit `d3b8a3e`: the ECC audit (20 Sep 2026) supplied the standalone install tier and scope choice (`scripts/install-engine.js`) and the deterministic-collection-plus-judgement split in `rules-distill`.

The [third-party skill register](security/third-party-skill-register.json) records a further 60 repositories screened by desk review on 29 Sep 2026 as sources of ideas. Nothing from them was installed.

## Standards and official sources

- JSON Schema, draft 2020-12 — https://json-schema.org/draft/2020-12/schema (all files in `schemas/`).
- Semantic Versioning (`MAJOR.MINOR.PATCH`), as applied in [`docs/distribution.md`](distribution.md).
- Model Context Protocol — https://docs.anthropic.com/en/docs/mcp; `@modelcontextprotocol/sdk` 1.30.0 in `mcp-server/package.json`.
- OWASP Application Security Verification Standard (ASVS) 5.0 — https://owasp.org/projects/asvs, https://github.com/OWASP/ASVS/releases (path-handling analogue in the plugin threat model).
- Claude Code documentation:
  - https://code.claude.com/docs/en/plugins
  - https://code.claude.com/docs/en/plugins-reference
  - https://code.claude.com/docs/en/plugins/manifest-reference
  - https://code.claude.com/docs/en/plugins/relevance
  - https://code.claude.com/docs/en/hooks
  - https://code.claude.com/docs/en/best-practices
- Anthropic documentation:
  - https://docs.anthropic.com/en/docs/claude-code/skills
  - https://docs.anthropic.com/en/docs/claude-code/memory
  - https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/prompt-templates-and-variables
- OpenAI Codex plugins — https://developers.openai.com/codex/plugins/; OpenAI API guides on prompt engineering, evals, safety best practices, models and changelog — https://developers.openai.com/api/docs/.
- Gemini CLI extension reference — https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md.
- OpenCode rules and skills — https://opencode.ai/docs/rules/, https://opencode.ai/docs/skills.
- Microsoft PowerShell guidance:
  - https://learn.microsoft.com/en-us/powershell/scripting/learn/deep-dives/everything-about-shouldprocess
  - https://learn.microsoft.com/en-us/powershell/scripting/developer/cmdlet/requesting-confirmation-from-cmdlets
  - https://learn.microsoft.com/en-us/powershell/utility-modules/psscriptanalyzer/rules/useapprovedverbs
- npm CLI v11 `npm audit` and `npm sbom` — https://docs.npmjs.com/cli/v11/commands/npm-audit/, https://docs.npmjs.com/cli/v11/commands/npm-sbom/.
- XDG Base Directory specification — https://specifications.freedesktop.org/basedir/latest/; .NET `Environment.SpecialFolder` — https://learn.microsoft.com/en-us/dotnet/api/system.environment.specialfolder.
- Official sources checked for other engines during portfolio Kaizen and recorded in this package's execution logs and the system-administration activity contract: IFRS 18; RFC 6797; OWASP ASVS; NIST SSDF 1.1; Uganda Revenue Authority PAYE and Income Tax Amendment Act 2026 pages; KCCA Local Service Tax; Google Search AI features guide; nginx, Apache httpd, Certbot, Debian, Ubuntu and Red Hat Enterprise Linux documentation; Windows Task Scheduler, Windows Update for Business and Active Directory audit-policy documentation.

## Websites and articles

- Robertson, S. and Zaragoza, H. (2009) "The Probabilistic Relevance Framework: BM25 and Beyond", *Foundations and Trends in Information Retrieval* 3(4) (cited in `scripts/lib/retrieval_metrics.py`).
- SEEK preprint, arXiv 2609.29803v1 — https://arxiv.org/abs/2609.29803v1 (source S17 in the 26 Sep 2026 Kaizen log).
- W3C Markup Validation Service user documentation — https://validator.w3.org/docs/users.html.
- DeepSeek API documentation — https://api-docs.deepseek.com/ (multi-host plan, Aug 2026).
- pytest cache documentation — https://docs.pytest.org/en/stable/how-to/cache.html.
- [Chwezi Engine Agents source repository](https://github.com/peterbamuhigire/chwezi-engine-agents).

The [third-party skill register](security/third-party-skill-register.json) records a further 60 repositories screened by desk review on 29 Sep 2026 as sources of ideas. Nothing from them was installed.
