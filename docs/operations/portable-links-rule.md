# Portable links rule (29 September 2026)

**Rule.** Every link in a public engine must resolve on a clean CI runner that has checked out only that one repository.

- A link to another engine is a GitHub URL (`https://github.com/peterbamuhigire/<repo>/blob/main/<path>`).
  - Exception: the research engine's GitHub repository is named `digital-research-skills`, although its local folder is `digital-research-engine`.
- A link inside an engine is repository-relative. It never starts with `/C:/…`, `C:\…` or `file:`, and it never climbs out of the repository with `../..`.
- Plain host paths in prose (`C:\wamp64\www\<engine>\…`) are written as engine-relative names (`<engine>/…`). The device-specific root comes from the active runner's global routing table.
- Every engine's link validator treats host-absolute links and repository-escaping links as broken, both locally and on CI. That way a link that works only on the author's machine fails before it is pushed.

**Why.** Before 29 September 2026, remote CI was red in seven engines. Their links resolved on Peter's machine, because the sibling engines and `C:/wamp64` paths exist there, but not on a runner. The evidence is in `m10-kaizen-evidence/M10-14/ci-repair-evidence.md`.

**Known exception.** The `skill-writing` pointer stubs are hash-registered in `catalog/shared-assets.yaml`. Any change to their local-path wording must be re-registered there in the same commit.
