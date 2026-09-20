---
name: rules-distill
description: Scan an engine's skills for cross-cutting principles that recur in 2+ skills and are not already in rules/, and propose promoting them into rules/common/. Use periodically per engine, or after a skill-stocktake pass reveals repeated patterns.
metadata:
  origin: chwezi-engine-agents
  adapted_from: "ECC audit (kaizen-engines/ECC-audit-2026-09-20/00-MASTER-REPORT.md, I-2), applying the same deterministic-collection-plus-LLM-judgment split"
---

# Rules Distill

Scans one engine's skills, extracts principles that recur in **two or more**
skills, checks them against that engine's existing `rules/` content, and
proposes verdicts. Never edits `rules/` automatically — every promotion is
presented for explicit approval.

## When to Use

- Periodic maintenance for an engine that already has a `rules/` layer (all
  twelve Chwezi engines do, as of the 2026-09-20 Kaizen pass).
- After a skill-stocktake-style audit surfaces a pattern worth checking.
- When a rule file feels thin relative to what the skills actually assume.

## Design Principle: Deterministic Collection, LLM Judgment

`scripts/scan-skills.sh` and `scripts/scan-rules.sh` do the exhaustive,
mechanical part — listing every skill and every rule file, so nothing is missed
by sampling. The judgment of *which* candidate principles are genuinely
cross-cutting, whether they duplicate existing rules in different words, and how
to word a promotion — that stays with the agent (or the model reading the scan
output), because it requires reading intent, not counting occurrences.

## Workflow

### Phase 1 — Inventory (deterministic)

```bash
bash scripts/scan-skills.sh <engine-root>   # every SKILL.md path + description
bash scripts/scan-rules.sh <engine-root>    # every rules/**/*.md path + headings
```

### Phase 2 — Extraction and matching (judgment)

Read the collected skill descriptions and, for any principle that appears to
recur, open the actual skill files (not just descriptions) to confirm it is the
same principle stated twice, not two different things that happen to use
similar words.

Apply the same three-layer filter the source pattern specifies:

1. **Appears in 2+ skills** — a principle found in exactly one skill stays a
   skill concern, not a rule.
2. **Actionable behaviour change** — must be statable as "do X" / "don't do Y",
   not "X is important."
3. **Clear violation risk** — one sentence on what goes wrong if ignored.

For each candidate that survives the filter, check it against the full text of
`rules/**/*.md` (small enough per engine to read in full) and assign a verdict:

| Verdict | Meaning |
|---|---|
| **Append** | Add to an existing section of an existing rule file |
| **Revise** | Existing rule content is inaccurate or insufficient |
| **New Section** | Add a new section to an existing rule file |
| **New File** | Create a new rule file |
| **Already Covered** | Sufficiently covered, even if worded differently |
| **Too Specific** | Should remain at the skill level |

### Phase 3 — Present and apply only on approval

Present a table: principle, evidence (which 2+ skills), violation risk, verdict,
target file, draft text. **Never modify `rules/` automatically.** Apply only the
candidates the user approves; skip or modify the rest as directed.

## Output Format

```markdown
# Rules Distillation — <engine-name>

Skills scanned: N | Rules: M files | Candidates: K

| # | Principle | Verdict | Target | Evidence |
|---|-----------|---------|--------|----------|
| 1 | ... | Append | rules/common/security.md §... | skill-a, skill-b |
```

## Anti-Pattern

Do not promote a principle to a rule on the strength of one skill using strong
language ("always", "never") — that is still one skill's concern until a second,
independent skill assumes the same thing.

## Related

- `chwezi-dev-engine/rules/README.md` — the rules-vs-skills test this skill applies
- The twelve `rules/common/*.md` files created across the estate on 2026-09-20
  are the current baseline this skill would check future skill growth against.
