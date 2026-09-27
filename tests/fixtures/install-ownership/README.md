# Installer ownership fixtures

`../security/install-engine-ownership.test.js` creates disposable local repositories and `.claude` targets under a unique OS temporary directory. It exercises unowned destination collisions, a locally modified update, a locally modified uninstall, a normal update/uninstall, manifest path traversal, recorded uninstall path traversal and corrupt ownership state. Cleanup is restricted to the generated temporary test root.
