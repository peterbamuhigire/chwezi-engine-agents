# Cross-engine negative fixtures

Date: 2026-11-07. Related actions D4.1 and R4.1.

The single-engine Dev and Research routing checks cannot compare an external
owner with a local skill. Run `scripts/check_cross_engine_negatives.py` from
this checkout with `--workspace-root` and one or more
`--fixture ENGINE_ID=PATH` arguments. Use catalogue IDs, including
`digital-research-skills` for the research engine. The helper reads native
nested Dev negatives and top-level Research negatives; no fixture copy is
needed. The domain engines do not depend on this helper at runtime.

It builds the existing public lexical index, reports supplied fixture hashes,
catalogue and effective-corpus hashes, counts local negatives left to their
native check, and evaluates every cross-engine case. Exit zero requires at
least one assessed case, no corpus read issue and every expected owner scoring
strictly above the competing skill. Ties fail. Missing owners/skills and
malformed inputs cannot disappear into a green result. Both resolved engine
roots and resolved skill-file links are checked against the public index's
private-engine exclusion.

Results cover the explicitly supplied files only. Rank is lexical ordering,
not a model choosing a skill; equal scores can have different display ranks.
The `tied_scores` field makes that distinction explicit. No model calls,
network requests, configuration changes or runtime routing are performed.

The initial six-case Dev/Research check exposed a tie between identical
validation-contract descriptions. The ownership register already assigns the
shared standard to Dev. Research's routing surface was narrowed to its local
research adapter, retaining templates while routing software releases to Dev.
The unchanged six cases then passed, with no discovery issues; the native
Research suite retained 40/40 top-three and 36/40 rank-one outcomes. Earlier
candidate wording failed one local negative and was corrected before retention.

The helper's six focused tests pass, including malformed-owner preservation,
strict ties, missing targets and a real temporary private-file symlink.
Recovery is to revert the helper/tests and resolved-path safeguards together;
do not change fixture expectations or thresholds to hide the original tie.
