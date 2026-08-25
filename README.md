# Skills Engine Agents

Portable Codex agents for the ten `peterbamuhigire` skills engines.

> **GitHub description:** Portable Codex agents for routing, maintaining, and validating ten domain skills engines with safe discovery, quality checks, and fork-friendly installation.

## What this repository is

`skills-engine-agents` is a Codex plugin and coordination layer for a family of independent skills engines. It helps Codex identify the right engine, preserve the engines' local operating rules, run documented validation gates, and perform safe maintenance across local checkouts.

It does not replace or duplicate the domain knowledge in the ten engines. Each engine remains independently usable and continues to own its routers, `SKILL.md` files, references, templates, and release checks.

This plugin adds three focused agents:

- `engine-orchestrator` routes a request to the correct domain and cross-cutting engines.
- `engine-maintainer` inspects engine remotes, branches, working trees, and fast-forward updates.
- `engine-validator` runs documented engine checks and reports evidence or `NOT ASSESSED` results.

The engines remain independently usable. Their own `AGENTS.md`, routers, and `SKILL.md` files remain the source of truth for domain behavior. This plugin supplies coordination and maintenance behavior around them.

## Distribution and installation

### Public plugin directory

After the plugin is accepted into the universal Codex Plugin Directory, users can search for **Skills Engine Agents** in Codex and install it without cloning this repository. Availability still depends on the user's plan, workspace settings, role, and supported Codex surface.

Publishing the GitHub repository does not itself publish the plugin to that directory; directory submission or approval is a separate product workflow.

### Workspace directory

For a private team rollout, a workspace administrator can import and publish the plugin to the workspace plugin directory. Team members then install it from the directory without cloning the repository. This keeps the plugin inside that workspace.

### Install locally

From a clone of this repository:

```powershell
.\scripts\install.ps1
```

The default destination is `%USERPROFILE%\plugins\skills-engine-agents`. Use `-Destination` to select another plugin directory and `-Force` only when intentionally replacing an existing installation.

Local installation is the fallback for development, private use, and environments that do not have access to a published directory.

## Use with a forked engine

Clone any engine fork, open Codex from that checkout, and invoke the installed agent. Discovery uses the current Git root, origin repository name, folder name, and local `AGENTS.md`; it does not assume `C:\wamp64\www` or another fixed machine path.

If the checkout is not one of the ten catalogued engines, the agents may still inspect it, but they will not invent engine-specific validation commands.

## Safety boundaries

The agents are read-only by default. The maintainer may run `git pull --ff-only` only after the user explicitly requests a pull. It must skip dirty or diverged repositories and never reset, delete, merge manually, or force-push.

Validation commands that are unavailable are reported as `NOT ASSESSED`; unavailable evidence is never treated as a pass.

## Validate this plugin

```powershell
python C:\Users\BIRDC\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .
.\scripts\validate-catalog.ps1
.\tests\validate_catalog.ps1
git diff --check
```

## Repository layout

```text
.codex-plugin/plugin.json       Plugin manifest
agents/                         Portable agent definitions
catalog/engines.yaml            Ten-engine registry
scripts/discover-engine.ps1     Current-checkout discovery
scripts/install.ps1             Local installation helper
scripts/validate-catalog.ps1    Registry validation
tests/validate_catalog.ps1      Deterministic catalog test
```
