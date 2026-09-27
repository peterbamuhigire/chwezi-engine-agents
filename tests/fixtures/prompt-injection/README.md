# Prompt-injection fixtures

These inert text fixtures model hostile content from a fetched document, tool result and imported skill. They use the reserved `.invalid` domain, contain no credentials or real client data, and are never executed or sent to a network tool.

The expected disposition is included beside each payload: classify it as untrusted data, flag the attempted scope change/exfiltration, preserve the user's authorized task, and make no outbound submission. They are test inputs, not security controls. This repository has no deterministic agent-runtime harness for proving model behavior; runtime resistance and egress enforcement remain **NOT ASSESSED**.
