# Portfolio count reconciliation — 26 September 2026

| Engine | Raw `SKILL.md` files | Router-reachable | Native task count | Claude plugin entries |
|---|---:|---:|---:|---:|
| SRS | 160 | 159 | 159 | 159 |
| Business Plan | 137 | 137 | 137 | 128 |
| Website | 63 | 62 | 62 | 62 |
| Social Media | 191 | 191 | 191 | 191 |
| Linux | 48 | 48 | 48 | 48 |
| Proposal | 115 | 115 | 115 | 115 |
| Chwezi Dev | 168 | 167 | 167 | 165 |
| Accounting | 108 | 108 | 108 | 108 |
| Design System | 102 | 101 | 101 | 101 |
| Digital Research | 61 | 59 | 59 | 59 |
| Windows Administration | 21 | 20 | 19 | 20 |
| **Public domain total** | **1,174** | **1,167** | **1,166** | **1,160** |

The raw total comes from the repeatable current snapshot in `baseline.json` and
`skill-inventory.jsonl`. Router and native counts are from the same-day saved
audit evidence; P00 changed documentation only and did not change any skill
tree. Windows has one required router hub beyond its 19 native task skills.
The 1,167 and 875 figures remain historical baseline and provisional target
respectively; neither is a consolidation requirement.

Static manifest reconciliation still finds nine fewer Business Plan entries
than its 137 native active skills, and two fewer Chwezi Dev entries than its
167 active files. This phase did not validate either manifest in an installed
Claude host. Installed Claude Code and Codex profiles had no Chwezi domain
engine plugins enabled, so these static differences are not evidence that a
currently enabled Chwezi plugin is missing skills.

The coordinator has three raw skill files and is outside the public domain
denominator.

## Classification limits

The fresh JSONL assigns every raw file a path, content hash, byte/line count,
frontmatter name and a discovery classification. It marks reachability as not
assessed per file. Existing router and native-validator counts do not prove
which individual files are aliases, generated copies, semantically duplicated,
or shadowed on each host. Do not retire or merge any path from these counts.
