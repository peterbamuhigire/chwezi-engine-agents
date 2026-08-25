# Skills Engine Agents Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and publish a portable Codex plugin for routing, maintaining, and validating the ten skills engines.

**Architecture:** A standalone plugin contains three agent definitions, a portable engine catalog, and PowerShell bootstrap/validation scripts. Existing engines remain the source of truth for domain instructions; the plugin discovers them from the current checkout and documented repository metadata.

**Tech Stack:** Codex plugin manifest JSON, Markdown agent prompts, YAML catalog, PowerShell 5.1-compatible scripts, Git, and the local plugin validator.

## Global Constraints

- Never hard-code `C:\wamp64\www` or another machine-specific checkout root.
- Never reset, delete, force-push, or silently modify a dirty engine checkout.
- Treat missing validators as `not assessed`, never as passing.
- Keep the plugin independently useful when only one engine is cloned.

---

### Task 1: Complete plugin metadata and user documentation

**Files:**
- Modify: `.codex-plugin/plugin.json`
- Create: `README.md`
- Create: `CONTRIBUTING.md`

- [ ] **Step 1: Update the manifest**

Set the display name, descriptions, developer name, and default prompt to describe the ten-engine orchestrator, maintainer, and validator agents. Keep the manifest free of unsupported app or MCP fields.

- [ ] **Step 2: Document installation and operation**

Document local installation, optional marketplace installation, engine discovery, fork behavior, read-only defaults, and the exact write actions that require explicit authorization.

- [ ] **Step 3: Document contribution rules**

Require catalog validation, plugin validation, PowerShell parsing, and review of agent prompts before publication.

- [ ] **Step 4: Validate metadata**

Run `python C:\Users\BIRDC\.codex\skills\.system\plugin-creator\scripts\validate_plugin.py .` and confirm exit code 0.

### Task 2: Add the agent definitions and engine catalog

**Files:**
- Create: `agents/engine-orchestrator.md`
- Create: `agents/engine-maintainer.md`
- Create: `agents/engine-validator.md`
- Create: `catalog/engines.yaml`

- [ ] **Step 1: Define orchestration behavior**

Make the orchestrator classify requests into domain engines, cross-cutting engines, and validation work. Require explicit handoff packets containing scope, engine IDs, evidence, blockers, and next actions.

- [ ] **Step 2: Define maintenance behavior**

Make the maintainer inspect branch, upstream, dirty state, and ahead/behind counts. Permit `git pull --ff-only` only after an explicit pull request and skip dirty or diverged repositories.

- [ ] **Step 3: Define validation behavior**

Make the validator load the engine router, select documented checks, run only available commands, and report exit codes and unassessed checks.

- [ ] **Step 4: Create the ten-engine catalog**

Record each canonical repository name, engine ID, router path, local folder name, and documented validation commands without absolute paths.

### Task 3: Add portable discovery, installation, and catalog validation

**Files:**
- Create: `scripts/discover-engine.ps1`
- Create: `scripts/install.ps1`
- Create: `scripts/validate-catalog.ps1`

- [ ] **Step 1: Implement engine discovery**

Resolve the current Git root, origin URL, repository basename, branch, and router presence. Return structured JSON and a nonzero exit code for missing Git roots or unknown engines.

- [ ] **Step 2: Implement catalog validation**

Parse `catalog/engines.yaml` using only PowerShell-compatible logic available on the target machine, validate the ten expected engine IDs and required fields, and reject duplicate IDs or repository names.

- [ ] **Step 3: Implement installation**

Copy the plugin into a user-selected or default personal plugin directory without overwriting an existing installation unless `-Force` is supplied. Print the installed path and a next-step command.

- [ ] **Step 4: Parse-check the scripts**

Run PowerShell parser checks against all `.ps1` files and confirm no syntax errors.

### Task 4: Add deterministic tests and release evidence

**Files:**
- Create: `tests/validate_catalog.ps1`
- Create: `.gitignore`

- [ ] **Step 1: Add catalog tests**

Assert that the catalog contains exactly ten unique engine IDs and that every router path and command list is non-empty.

- [ ] **Step 2: Add clean-repository exclusions**

Ignore local test output, plugin caches, and PowerShell transient files while keeping all source, catalog, agent, and documentation files tracked.

- [ ] **Step 3: Run the full validation set**

Run the plugin validator, catalog test, PowerShell parser checks, and `git diff --check`; record the outputs in the final handoff.

### Task 5: Publish the initial draft

**Files:**
- Modify: all files created in Tasks 1–4

- [ ] **Step 1: Review scope**

Run `git status -sb`, inspect the complete diff, and confirm no unrelated files are present.

- [ ] **Step 2: Commit the plugin**

Commit the complete implementation as `feat: add skills engine agents plugin`.

- [ ] **Step 3: Push the feature branch**

Push `agent/bootstrap-plugin` to the repository with upstream tracking.

- [ ] **Step 4: Open a draft PR**

Create a draft pull request targeting `main` with the architecture, portability behavior, safety boundaries, and validation evidence.
