# Distribution

The repository is the versioned source for the `skills-engine-agents` core and
its host adapters. It is not, by itself, a public plugin listing.

Support is host-based. The selected model and provider remain the host's
configuration boundary; this package does not promise equal model quality or
tool access.

See the [compatibility contract](architecture/compatibility-contract.md) and
[host matrix](architecture/host-model-capability-matrix.md).

Adapter guides are available for [Codex](adapters/codex.md), [Claude Code](adapters/claude-code.md), [Gemini CLI](adapters/gemini-cli.md), [OpenCode](adapters/opencode.md), [generic CLI](adapters/generic.md), and [MCP](adapters/mcp.md). Operational policy is in [upgrade-policy.md](operations/upgrade-policy.md) and [incident-runbook.md](operations/incident-runbook.md).

## Public directory

1. Validate the plugin and review the final diff.
2. Publish the plugin through the Codex plugin-directory workflow.
3. Users search for `Skills Engine Agents` and install it from Codex.

Users do not need to clone the GitHub repository for this path. Product availability may vary by plan, workspace settings, role, region, and supported surface.

## Workspace directory

1. A workspace administrator imports the plugin package or repository source.
2. The administrator reviews permissions and publishes it to the workspace directory.
3. Members install it from the workspace directory.

Workspace publication is private to that workspace and is distinct from universal public-directory publication.

## Local fallback

For development or private environments, clone the repository and run:

```powershell
.\scripts\install.ps1
```

The local installer is intentionally explicit and never overwrites an existing installation unless `-Force` is provided.

Host-specific installation targets are documented in the adapter guides added
in later release phases. When a host convention is unavailable, use the
generic Markdown prompts and run the portable scripts manually; missing shell,
Git, web, or approval capabilities remain `NOT ASSESSED`.

## Versions and release tags (M10-02-T08)

Each engine's `.skills-engine/engine-manifest.yaml` `version` is the single
version source. `python -X utf8 scripts/render_host_files.py --render --engine <path>`
copies it into `.claude-plugin/plugin.json`, the engine's own
`.claude-plugin/marketplace.json` entry and `.codex-plugin/plugin.json` where one
exists; `--check` fails when any of those, or the engine's entry in this
package's suite marketplace, disagrees. This package has no engine manifest; its
version source is `.claude-plugin/plugin.json`, which the suite `chwezi-suite`
entry and `.codex-plugin/plugin.json` must match.

Versions follow semantic versioning (`MAJOR.MINOR.PATCH`). The first real
version, set on 29 Sep 2026, is `1.1.0` for every public repository, because all
twelve changed during the my-10-kaizen phases M10-00 to M10-02 (proposed rule:
`1.1.0` for repositories changed in M10, `1.0.1` otherwise; decided by the
orchestrator under Peter's delegated authority, 29 Sep 2026).

Tagging rule:

1. Tag `v<version>` on the pushed `main` commit at a push checkpoint, once per
   repository whose version changed since its last tag.
2. Cut and push tags only with Peter's authority for that checkpoint; the
   orchestrator performs it. Executors never create tags.
3. Before tagging, run `render_host_files.py --check --workspace-root .. --tag v<version>`
   for the repository; a mismatch between tag and version fails.
4. Bump the manifest `version` (then `--render`) in the same change that is
   released; never retag a published version.

Until a tag exists, tag checks are recorded as `NOT_ASSESSED (awaiting release authority)`.

## Suite marketplace source pinning (M10-02-T10 decision record)

Question: should the URL sources in `.claude-plugin/marketplace.json` pin a
`sha` (or a release tag) instead of `ref: main`?

Decision (29 Sep 2026; recommended option, decided by the orchestrator under
Peter's delegated authority): stay on `ref: main` until the first `v1.1.0` tags
exist. At the push checkpoint that creates them, pin each URL source to its
release tag (`"ref": "v<version>"`) and set `catalog/engines.yaml`
`integration.released_commit` to the tagged commit, both from the same version
source, and add a check that every pinned `ref` equals the tag of the commit in
`released_commit`. Reason: pinning before tags exist would either freeze
installs on an arbitrary commit or break them.

Related clean-up in the same change:

- `catalog/engines.yaml` `released_commit` values were 21 to 59 commits behind;
  they were refreshed to each repository's `origin/main` tracking ref as seen
  locally on 29 Sep 2026 (no fetch was run). They move to the tagged commit at
  the next release.
- `.codex-plugin/plugin.json` `homepage` and `repository` now name
  `chwezi-engine-agents`. Its `name` stays `skills-engine-agents` on purpose:
  it is the Codex plugin identity that existing installs and the release
  archive (`release.yml`) use, and renaming it needs its own migration.
