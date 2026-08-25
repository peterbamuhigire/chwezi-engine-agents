# Host, model, and capability matrix

This matrix records packaging and orchestration behavior. It does not certify
model quality. `not_assessed` means the behavior is not verified.

| Host | Installation | Instruction discovery | Agent entrypoints | Tool transport | Approval transport | Model configuration | Tested on | Known limits |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| codex | native | Codex plugin manifest and bundled agent files | three named agent files | scripts, optional MCP | host prompt | host_owned | Windows checkout | Plugin availability varies by Codex surface. |
| claude-code | adapter | project `CLAUDE.md`, `.claude/agents`, `.claude/skills` | three agent wrappers and routing skill | scripts, MCP | host prompt | host_owned | project-local files | Marketplace support is not assumed. |
| gemini-cli | adapter | `GEMINI.md`, extension commands and skills | command wrappers | scripts, MCP | host prompt | host_owned | extension layout | CLI version and extension policy can change. |
| opencode | adapter | project `AGENTS.md` and project skill | routing skill and rules | scripts, MCP | permission prompt | host_owned | project-local files | Current V2 behavior prefers `AGENTS.md`. |
| generic | generic | human-loaded Markdown prompts | prompt files | scripts | manual | provider_owned | PowerShell and POSIX examples | No automatic discovery or approval channel. |
| mcp | adapter | host MCP configuration | typed tools | MCP | confirmation token | host_owned | stdio server | Host must provide approval for mutations. |

## Provider examples

Provider selection stays with the host. A DeepSeek-compatible endpoint can be a
host configuration fixture, but this package does not claim that every host or
every DeepSeek model supports the same tools, context, or output behavior.

| Provider situation | Classification | Package boundary |
| --- | --- | --- |
| Model selected inside Codex | host-owned | Use the Codex adapter. |
| Claude Code using a compatible third-party endpoint | provider-owned | Test host/tool behavior; do not score model quality as an adapter property. |
| Gemini CLI selecting a model alias | host-owned | Use Gemini's documented extension and command paths. |
| Direct model API without file/tool orchestration | not_assessed | Outside the installation contract. |
