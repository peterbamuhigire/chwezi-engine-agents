# Degraded modes

Capability detection selects the narrowest mode supported by observed evidence.

| Mode | Requirements | Behaviour |
| --- | --- | --- |
| `full` | read, write, shell, Git, structured output, approval | Run declared checks and approved mutations. Web, subagents, and MCP remain optional. |
| `sequential` | read, shell, structured output; no subagents | Run independent routing and validation lanes one at a time. |
| `read_only` | read; no approval or no write authority | Discover and inspect; block pulls, installs, updates, and writes. |
| `not_assessed` | read unavailable or detection failed | Return the required path/tool and preserve `NOT ASSESSED`. |

Specific fallbacks:

- Missing shell makes validation and maintenance `NOT ASSESSED`; it does not
  permit a prose-only pass.
- Missing Git makes repository inspection and pull `NOT ASSESSED`.
- Missing approval blocks all writes and pulls, even when the directory is
  writable.
- Missing web access preserves a freshness gap.
- Missing subagents changes parallel lanes to sequential execution.
- Missing MCP changes typed tools to portable scripts.
- Missing structured output changes serialization to Markdown with the exact
  contract field names.
