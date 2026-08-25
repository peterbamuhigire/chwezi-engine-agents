# Upgrade policy

Upgrade from a managed installation with the matching update script. The
installer stages the new package, validates the adapter and canonical core,
then replaces the managed tree while preserving user-created files.

Schema changes follow the compatibility contract: patch descriptions, minor
optional fields, major required fields or enum changes. Review the release
manifest and SHA-256 checksum before updating. If validation fails, keep the
existing installation and fix the staged release.

Rollback is a reinstall of the previous tagged release into the same managed
destination after confirming its checksum. Do not use reset, clean, or broad
deletion to recover an installation.
