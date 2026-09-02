# Runtime Skill Metadata Budget

The runtime skill catalog is assembled from local filesystem skills and enabled
plugins. Each entry contributes discovery metadata before the model decides
which full `SKILL.md` body to load. A repository can therefore pass its own
per-skill checks and still overflow the runtime catalogue budget.

## Validator

Run the validator against the exact directories that Codex or another host will
discover. Mark repository-owned roots with `--catalog-root`; plugin roots still
contribute to the aggregate budget but are governed by their own publisher. The
Codex configuration helper selects enabled plugins and prefers a `latest` cache:

```powershell
python -X utf8 scripts/validate-runtime-skill-budget.py `
  --root C:\Users\Peter\.agents\skills `
  --catalog-root C:\Users\Peter\.agents\skills\skills `
  --catalog-root C:\Users\Peter\.agents\skills\00-meta-initialization `
  --config C:\Users\Peter\.codex\config.toml `
  --plugin-cache C:\Users\Peter\.codex\plugins\cache
```

Repeat `--root` for each deliberately enabled plugin skill directory. Do not
scan staging or cache directories unless the host actually exposes them.

The default release limits are:

- 200 repository-owned runtime skill entries;
- 400 characters per description;
- 50,000 total description characters;
- 60,000 total name-plus-description characters.

These are conservative engineering gates, not vendor-published Codex limits.
Tune them against observed host behaviour, but keep the validator pointed at
the same assembled runtime set used in production.

## Authoring rule

Use the description only for the user goal and activation conditions. Keep
workflow steps, output contracts, examples, and policy detail in the body or
linked `references/` files. Do not duplicate a skill name across a canonical
engine and an adapter. Preserve absorbed knowledge as reference material and
record the old slug in the routing index.

## Evidence

The validator reports the discovered count, description characters, metadata
characters, duplicate names, malformed frontmatter, and budget failures. A
release gate must retain the command, result, timestamp, and consequence in the
engine handoff or delivery evidence pack.
