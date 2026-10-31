# Supply-chain policy

- Node dependencies are installed from `mcp-server/package-lock.json`; CI uses
  `npm ci` and builds from that lockfile.
- Python contract validation uses the host's installed `PyYAML` and
  `jsonschema`; missing dependencies are `NOT ASSESSED`, not a pass.
- Release archives are built with `git archive`, so they hold tracked files only.
  `scripts/check_public_hygiene.py` fails the build when a tracked file is a
  local settings file, an `.env` or key file, a credential-shaped string or a
  path on one workstation. It is the secret and path scan; it recognises the
  patterns listed in its docstring and nothing else.
- The release workflow first calls the validate workflow (plugin, contract,
  catalogue, adapter, installer, security, deterministic evaluation, hook, MCP,
  portfolio drift and hygiene checks) and packages only if it passes. It then
  repeats the catalogue schema check, the contract evaluations and the MCP
  build and tests, packages the archive and writes a SHA-256 checksum.
- Not yet true, and not claimed: the workflow does not generate
  `release/manifest.json` (it is a static template), does not verify the
  checksum after writing it, does not sign the archive and has no publication
  step. A release that needs a provenance manifest, a signature or a
  publication gate must add them first.
- Reviewers must inspect downloaded installation scripts before executing them.
