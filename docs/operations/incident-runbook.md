# Incident runbook

## Suspected unsafe mutation

1. Stop the host session and revoke the host confirmation token.
2. Record target path, branch, before/after heads, adapter/core versions, and
   the exact tool response.
3. Do not run reset, clean, merge, or force-push as an emergency response.
4. Preserve the checkout and inspect `git status`, reflog, and the managed
   install manifest read-only.

## Failed installation

Check the staged path and manifest. If the destination changed, restore the
previous tagged package; user-created files are not owned by the installer.
Run the path-boundary and managed-file audit before retrying.

## Missing evidence

Mark the affected check `NOT ASSESSED`, name the missing command/dependency/
authority, and keep the release blocked when the missing evidence is material.

## Host or provider outage

Separate deterministic contract results from provider-backed results. Record
host, model label, adapter version, core version, outage detail, and next test
window. Do not convert an outage into PASS.
