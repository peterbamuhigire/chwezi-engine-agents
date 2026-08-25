# Distribution

The repository is the versioned source for the `skills-engine-agents` Codex plugin. It is not, by itself, a public plugin listing.

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
