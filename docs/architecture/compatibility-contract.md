# Compatibility contract

This package coordinates independent skills engines. It does not make a model
universal by itself. A host must supply instruction discovery, file access, and
the tools or scripts needed for the requested operation.

## Terms

- **Host**: the application that loads instructions, tools, and permissions. Examples are Codex, Claude Code, Gemini CLI, OpenCode, and a generic shell workflow.
- **Model**: the provider/model selected by the host. A model may be changed without changing this package.
- **Adapter**: host-specific packaging and discovery files that point to the canonical core.
- **Core**: the model-neutral catalog, policies, contracts, and deterministic operations in this repository.
- **Native**: a host loads the adapter through its documented package or extension mechanism.
- **Adapter**: a host loads a package-specific wrapper using its documented project or user files.
- **Generic**: a host loads Markdown prompts and invokes portable scripts manually.
- **Not assessed**: the required host behavior or dependency could not be verified; it is not a pass.

## Capability vocabulary

Capability flags are observations, not permissions granted by the model:

`read_files`, `write_files`, `shell`, `git`, `web`, `subagents`, `mcp`,
`structured_output`, and `user_approval`.

The package uses these minimum capabilities:

| Operation | Required capabilities | Fallback when absent |
| --- | --- | --- |
| Route | `read_files` | Return `NOT ASSESSED` and name the required router path. |
| Validate | `read_files`, `shell` | Report `NOT ASSESSED`; do not infer a pass from prose. |
| Inspect Git | `read_files`, `git` | Report `NOT ASSESSED` with the missing tool. |
| Pull or write | `read_files`, `git`, `user_approval` | Block the operation before side effects. |
| Current-source check | `web` | Report `NOT ASSESSED` and preserve the freshness gap. |
| Parallel work | `subagents` | Run independent lanes sequentially. |
| Typed tools | `mcp` | Use the portable scripts or Markdown contract. |
| Structured handoff | `structured_output` | Emit the same field names as a Markdown handoff. |

## Host and model boundary

Installation targets are hosts, not model APIs. A provider can be configured
inside a host, but a model-only API integration is outside this package unless
the host supplies file and tool orchestration. Model quality, provider access,
latency, context limits, and tool permissions can differ; this package makes no
claim of equal reasoning quality or equal tool access across providers.

## Evidence and verdicts

Every validation result names its command, exit code, evidence, and duration.
Unavailable commands, dependencies, sources, host behavior, or approval
authority are `NOT ASSESSED`, never `PASS`. A host adapter may expose a safer
fallback, but it may not silently widen capabilities.

## Re-verification sources

The following sources were checked on 2026-08-26 and must be rechecked before a
release that changes an adapter:

- [Codex plugins](https://developers.openai.com/codex/plugins/)
- [Claude Code memory](https://docs.anthropic.com/en/docs/claude-code/memory)
- [Claude Code skills](https://docs.anthropic.com/en/docs/claude-code/skills)
- [Gemini CLI extension reference](https://github.com/google-gemini/gemini-cli/blob/main/docs/extensions/reference.md)
- [OpenCode rules](https://opencode.ai/docs/rules/)
- [OpenCode skills](https://opencode.ai/docs/skills)

## Schema version rules

Schema descriptions may change in a patch release. New optional fields require
a minor version. Required-field, field-type, or enum changes require a major
version and an adapter migration note.
