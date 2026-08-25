# Supply-chain policy

- Node dependencies are installed from `mcp-server/package-lock.json`; CI uses
  `npm ci` and builds from that lockfile.
- Python contract validation uses the host's installed `PyYAML` and
  `jsonschema`; missing dependencies are `NOT ASSESSED`, not a pass.
- Release archives exclude `.env`, API keys, credential-bearing reports,
  private engine contents, `node_modules`, and local absolute paths.
- The release workflow runs plugin, contract, catalog, adapter, installer,
  security, and deterministic evaluation checks before packaging.
- SHA-256 checksums and a source-commit provenance manifest accompany each
  release. A failed checksum or secret scan blocks publication.
- Reviewers must inspect downloaded installation scripts before executing them.
