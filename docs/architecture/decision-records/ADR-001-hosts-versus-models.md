# ADR-001: Separate hosts from models

## Context

The package must work across multiple AI applications without copying domain
instructions into provider-specific prompts. Hosts own discovery, permissions,
and tools; models interpret instructions and produce decisions.

## Options

1. Publish one provider-specific prompt per model.
2. Publish one canonical core with thin host adapters.
3. Publish only a direct model API client.

## Decision

Use one canonical core and thin host adapters. Installation and support claims
are made against hosts. Provider/model configuration remains host-owned.

## Consequences

The core stays portable and contracts stay stable. Adapters must track host
discovery conventions. A model-only integration cannot be certified unless a
host supplies file access, tools, and approval handling.

## Verification

Every adapter manifest declares its host, core version, required capabilities,
and generic fallback. Canonical instructions contain no provider-specific API
parameters or model names.
