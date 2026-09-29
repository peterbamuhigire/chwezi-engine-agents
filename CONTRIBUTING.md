# Contributing

Keep this plugin portable and conservative.

Before submitting a change:

1. Read the affected engine's `AGENTS.md` or `README.md` router.
2. Keep repository paths relative or discoverable from Git metadata.
3. Do not add a validation command unless it is documented by the target engine.
4. Treat unavailable checks as `NOT ASSESSED`, never as passing.
5. Run the plugin validator, catalog validation, adapter/install/security tests, deterministic evaluations, MCP build/tests, and `git diff --check`.
6. Inspect the complete diff and confirm no machine-specific secrets or paths were added.

Agent prompts should define scope, evidence requirements, safety boundaries, degraded behavior, and a predictable handoff format.

Provider-backed evaluations must identify the host, model label, adapter/core
versions, and evidence. A missing host, provider, key, dependency, or approval
channel is `NOT ASSESSED`; it is not a successful result.

## Multi-host implementation work

For changes related to universal host adapters, MCP tools, or engine integration, use the phase-level plan in [`docs/plans/aug-25`](docs/plans/aug-25/README.md). Work on `main` unless a branch is explicitly requested, preserve the ten engines as independent repositories, and update the relevant phase document when implementation decisions change.

## If you are an AI agent

AI agents may propose changes here, on the same terms as people plus a few more:

1. **Disclose** in the pull request your model or runtime label, the harness
   (for example Claude Code or Codex CLI) and the plugins or skill packs loaded
   in the session.
2. **Search first.** Look through open and closed pull requests and issues for
   the same problem before opening a new one, and link what you found.
3. **One problem per pull request.** Do not bundle unrelated fixes, renames or
   formatting sweeps.
4. **Run the documented validators** listed above and in the affected engine's
   router, and paste the real results. Report any check you could not run as
   `NOT ASSESSED`, with the reason.
5. **No book extractions and no copied third-party text.** Paraphrase ideas and
   attribute them with licence, URL and commit.

Model policy is not reopened by contributions: Codex runs on GPT-6 Luna with
high reasoning, Astra only when Peter selects it explicitly, and other runtimes
keep their own configuration.

The pull request template (`.github/pull_request_template.md`) carries the
disclosure block.

Adapted in paraphrase from obra/superpowers `AGENTS.md` (MIT,
https://github.com/obra/superpowers, commit
8ca22dba9a94f28898bbce59f2537ff4d87c747d). No text copied.
