# Skill Lifecycle and Invocation Contract

## Purpose

Keep promoted runtime catalogues separate from experimental, deprecated, and reference-only content,
and preserve the invocation intent of canonical skills across host adapters.

## Lifecycle states

| State | Runtime treatment |
| --- | --- |
| `promoted` | May appear in an exposed runtime skill root after native validation |
| `experimental` | Isolated from promoted roots; requires behavioural evaluation before promotion |
| `deprecated` | Excluded from promoted roots; retains migration target and review/removal date |
| `reference-only` | Loaded only through a promoted skill pointer; never independently routed |

Absent lifecycle metadata means `promoted` for backward compatibility. A non-promoted `SKILL.md`
inside an exposed root is a release failure. Inactive compatibility routes use `ALIAS.md` and a
machine-readable target owned by the engine.

## Invocation states

| State | Meaning |
| --- | --- |
| `implicit` | Model may select the skill when its trigger matches; default |
| `explicit` | Direct user request is required and must be stated in the description |
| `both` | Direct and model-selected entry are both intended |

Adapters may map these semantics to host fields but may not broaden `explicit` to automatic entry.
If a host cannot enforce invocation, report enforcement `NOT ASSESSED` and retain the semantic state.
Invocation never replaces action-specific approval.

## Promotion gate

Promotion requires a positive route, neighbour negative, degraded-capability case, failure/stop case,
output/evidence check, source/currentness review, safety review, runtime budget, and rollback. A
deprecated skill names the replacement and preserves useful knowledge before removal.

## Validator

```powershell
python scripts\validate-skill-lifecycle.py --root <exact-exposed-skill-root>
```

Pass every root the host exposes. Repository-local success does not certify an assembled runtime.

This contract adapts promoted, in-progress, miscellaneous/reference, deprecated, and invocation
mechanisms studied in Matt Pocock's `mattpocock/skills` repository at commit `3cca18b`.
