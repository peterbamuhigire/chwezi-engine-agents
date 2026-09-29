# 02 — Coverage and taxonomy

**Taxonomy and structure: 52 / 100 (judged).**

## Structure as found

| Layer | Holds | Assessment |
|---|---|---|
| `core/` | 4 canonical instructions, 3 contracts, capability registry and degraded modes, safety policy | Sound model-neutral core; the orchestrator's one-question-per-engine handoff table is the clearest artefact in the package. |
| `agents/`, `adapters/` | 3 Codex wrappers; six host adapters (Claude Code, Codex, Gemini CLI, OpenCode, generic, MCP) | Thin wrappers pointing at `core/`, as intended; still hand-written rather than rendered from `core/`. |
| `catalog/` | `engines.yaml` (11 engines, validator arrays), `shared-assets.yaml` (16 assets), content-integrity allowlist | Right place for the registry; the package does not list itself or its own validators. |
| `skills/` | `rules-distill` only | A one-skill group; the skill is about per-engine rules, which the dev engine's meta group could equally own. |
| `scripts/` | 30+ scripts: installers, generators, 12 validators, routing, graph, tour, usage scan, Tier-3 runner | Flat folder mixing install, generation, validation and analysis; only `lib/` is split out. |
| `evals/` | 77 cases, 76 fixture folders, routing register/baseline/ledger, behavioural harness, MCP QA, plugin evals | Well separated by tier. |
| `docs/` | operations (governance, contracts, Kaizen records, evidence), security, architecture, tours, skill graph | `docs/operations/` carries contracts, cards, logs and evidence side by side (about 30 files plus an evidence tree). |

## Named deficiencies

1. **No self-registration.** The package routes eleven engines but has no catalogue entry, so the
   MCP `validate_engine` tool returns `NOT ASSESSED` ("not catalogued") for the package itself, and
   its T1 denominator is chosen by an executor rather than declared.
2. **Skills layer is a single skill** whose own text says this package has no `rules/` layer. A
   group of one is an orphan by the rubric's balance test.
3. **`scripts/` is a grab-bag** of about 30 entry points with no index; the engine tour lists 10
   "gates" but the brief's validator set is 8 and CI runs a third selection.
4. **`docs/operations/` mixes classes**: binding contracts (bridge, project context, craft
   standard), cards, dated Kaizen records, a running log and raw evidence share one folder.
5. **Adapters are not generated from `core/`.** The baseline recorded this (theme k); M10-02
   single-sourced `CLAUDE.md` bridges across the portfolio, but adapter prompts, the Codex plugin
   manifest and the MCP server identity remain hand-kept, and three of them carry the old name.

## Coverage of the package's remit

| Remit | Covered by | Coverage |
|---|---|---|
| Route to the right engine(s) | orchestrator, catalogue, oracles | partial: lexical proof only |
| Keep host files and shared assets aligned | `render_host_files.py`, register | strong for bridges and registered assets; blind to Codex plugin, MCP identity, release names |
| Detect cross-engine overlap | union scan, ownership register | strong as a gate; 27 duplicate names and 21 declared pairs still unresolved |
| Prove behaviour | Tier-3 harness | built, unexecuted |
| Install and distribute | installer, marketplace, release workflow | installer and marketplace checked; release never cut |
| Govern | Kaizen records, registers, dispositions | partial: log incomplete, ratifications open |
| Orient newcomers | tours, project context, graph, fan-in | present, not yet exercised on a real project |
