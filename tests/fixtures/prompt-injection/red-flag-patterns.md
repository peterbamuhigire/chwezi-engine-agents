# Red-flag patterns for imported setup text

Static patterns that `tests/test_prompt_injection_fixtures.py` checks against the inert fixtures in this folder. A match is a flag for human review, not a verdict. Runtime resistance of any agent to these texts remains **NOT ASSESSED**: this repository has no deterministic agent-runtime harness.

Adapted in paraphrase from the Awesome Claude Skills review (AC-07; ComposioHQ/awesome-claude-skills, no root licence, https://github.com/ComposioHQ/awesome-claude-skills). No text copied.

| ID | Behaviour | Pattern (case-insensitive regular expression) |
|---|---|---|
| RF-01 | Tells the model to discard or ignore its prior knowledge | `(ignore\|set aside\|disregard\|forget)[^.\n]{0,40}(know\|knowledge\|pretrained\|training)` |
| RF-02 | Forbids checking existing configuration or its locations | `(do not\|don't\|never)[^.\n]{0,40}(look up\|inspect\|check\|search)[^.\n]{0,40}config` |
| RF-03 | Writes a pasted credential into user-level agent or MCP configuration | `(api key\|token\|secret)[\s\S]{0,120}(~/\.mcp\.json\|~/\.claude\|~/\.codex\|user-level mcp)` |
