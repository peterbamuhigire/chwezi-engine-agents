"""Render the M10-04-T03 skill-writing pointer stubs for six engines."""
import pathlib
import sys

W = pathlib.Path(r"C:/wamp64/www")
GH = "https://github.com/peterbamuhigire/chwezi-dev-engine/blob/main/skills/sdlc-meta/skill-writing/SKILL.md"
ACK = "Acknowledgement: Shared by Peter Bamuhigire, techguypeter.com, +256 784 464178."
LOCAL = r"C:\wamp64\www\chwezi-dev-engine\skills\sdlc-meta\skill-writing\SKILL.md"
META2 = "metadata:\n  portable: true\n  compatible_with:\n  - claude-code\n  - codex\n"
META4 = "metadata:\n  portable: true\n  compatible_with:\n    - claude-code\n    - codex\n"
LINUX_META = ('license: Complete terms in LICENSE.txt\nmetadata:\n  author: Peter Bamuhigire\n  author_url: techguypeter.com\n'
              '  author_contact: "+256784464178"\n  portable: true\n  compatible_with:\n    - claude-code\n    - codex\n')

ENGINES = {
    "digital-research-engine": dict(
        path="skills/skill-writing", scripts="skills/skill-writing/scripts",
        desc="Use when creating or upgrading a skill in this research engine with portable frontmatter, progressive disclosure, reference-file strategy and validation under the canonical chwezi-dev-engine skill-writing standard; use skill-composition-standards to normalise house style and skill-safety-audit for read-only review.",
        use="Creating or upgrading a reusable research-engine skill: portable frontmatter, progressive disclosure, reference-file strategy, permissions and validation.",
        neighbour="Use `skill-composition-standards` to normalise an existing skill against house style, and `skill-safety-audit` for a read-only safety review.",
        validators="`python -X utf8 scripts/skill_contract_validator.py --baseline tests/skill-engine/quality-baseline.json` and `python -X utf8 scripts/routing_smoke_test.py`",
        delta=["Every active skill carries the 13 contract sections that `scripts/skill_contract_validator.py` enforces; keep runner-specific tool names out of the body.",
               "Revise a research skill only through the replay gate: a separate candidate, a frozen baseline and historical replay, recorded in `evals/seek-research/revision-register.jsonl` (see [replay-gated skill revision](../ai-evaluation-and-data-flywheel/references/replay-gated-skill-revision.md))."],
        example="For a new source-analysis capability, inspect `source-evaluation` and `source-verification` first, define the distinct trigger and stop boundary, then add one positive, one negative and one collision fixture before activation.",
        refs=["[Skill composition standards](../skill-composition-standards/SKILL.md)", "[Skill safety audit](../skill-safety-audit/SKILL.md)",
              "[Replay-gated skill revision](../ai-evaluation-and-data-flywheel/references/replay-gated-skill-revision.md)"],
        meta=META2, ack=True),
    "social-media-skills": dict(
        path="skills/meta-utility/skill-writing", scripts="skills/meta-utility/skill-writing/scripts",
        desc="Use when creating or upgrading portable social-media skills with routing, contracts and validation under the canonical chwezi-dev-engine skill-writing standard; use `skill-safety-audit` when a read-only safety review is the closer match.",
        use="Creating or upgrading a portable social-media skill, its routing fixtures, contracts or validation.",
        neighbour="Use `skill-safety-audit` for a read-only safety review; do not publish, spend or change a live account.",
        validators="`python -X utf8 scripts/validate_skill_engine.py --baseline quality-baseline.json` and `python -X utf8 scripts/routing_smoke_test.py`",
        delta=["Write for the stated client market and currency; never publish, spend, change a live account or certify compliance while authoring.",
               "Apply [anti-AI slop](../../ai-marketing/anti-ai-slop/SKILL.md) while writing and [the slop audit](../../ai-marketing/ai-slop-audit/SKILL.md) at the release checkpoint; follow the [local authoring standard](../../../docs/standards/skill-authoring-standard.md)."],
        example="Given a request for a LinkedIn carousel skill, inspect the closest content and platform skills, name the neighbour that wins on a pure copy request, then add positive and collision fixtures before activation.",
        refs=["[Local authoring standard](../../../docs/standards/skill-authoring-standard.md)",
              "[Skill authoring practices (canonical mirror)](references/skill-authoring-best-practices.md)",
              "[Skill safety audit](../skill-safety-audit/SKILL.md)"],
        meta=META2, ack=True),
    "website-skills": dict(
        path="skills/meta/skill-writing", scripts="skills/meta/skill-writing/scripts",
        desc="Use when creating or upgrading portable website-engine skills, triggers, contracts, references, validators, or routing fixtures under the canonical chwezi-dev-engine skill-writing standard; use skill-safety-audit for independent safety review and update-claude-documentation for router-only changes.",
        use="Creating a reusable portable website skill, repairing a legacy skill's contract, or updating routing fixtures and validators.",
        neighbour="Use `skill-safety-audit` for independent safety review and `update-claude-documentation` for router-only changes.",
        validators="`python -X utf8 scripts/validate-skill-contracts.py --baseline quality/skill-contract-baseline.json` and `python -X utf8 scripts/routing-smoke-test.py`",
        delta=["Follow the [website authoring standard](../../../docs/skill-authoring-standard.md); the acknowledgement line sits directly under the title.",
               "Compare the closest page, form and launch skills before adding a route; a skill created to improve catalogue metrics is refused."],
        example="For a new form workflow, compare `page-builder` and the external form-design route, declare the distinct output and permissions, then add positive and neighbour-collision fixtures before activation.",
        refs=["[Website authoring standard](../../../docs/skill-authoring-standard.md)", "[Skill safety audit](../skill-safety-audit/SKILL.md)"],
        meta=META2, ack=True),
    "business-plan-skills": dict(
        path="skills/meta-utility/skill-writing", scripts="skills/meta-utility/skill-writing/scripts",
        desc="Use when creating, normalising, reviewing, or releasing a reusable business-plan skill under the canonical chwezi-dev-engine skill-writing standard; distinguishes skill authoring from `skill-safety-audit`, which inspects safety without redesigning the skill contract.",
        use="Creating or normalising a skill for a repeatable business-planning, advisory, finance, pitch or execution workflow.",
        neighbour="Use `skill-safety-audit` instead for a read-only safety inspection; use the domain skill when the task is to produce a plan artefact.",
        validators="`python -X utf8 scripts/validate_skill_engine.py --baseline docs/quality/skill-quality-baseline.json` and `python -X utf8 scripts/routing_smoke_test.py`",
        delta=["Draft from the [dual-compatible skill template](references/dual-compatible-skill-template.md) and respect the [dual-surface migration rules](references/dual-surface-migration-rules.md); inventory `skills/` and `country-context/` for neighbours.",
               "Verify financial figures, thresholds and accounting treatments, or assign them to professional review under the finance engine; apply `anti-ai-slop` while writing and `ai-slop-audit` before release."],
        example="Asked for a lender-readiness review skill, first search `meta-bankability-scoring`, `11-funding-request` and `meta-accounting-finance-review`; update the owner that already scores bankability instead of adding a duplicate reviewer.",
        refs=["[Dual-compatible skill template](references/dual-compatible-skill-template.md)",
              "[Dual-surface migration rules](references/dual-surface-migration-rules.md)", "[Skill safety audit](../skill-safety-audit/SKILL.md)"],
        meta=META4, ack=False),
    "linux-skills": dict(
        path="meta/skill-writing", scripts="meta/skill-writing/scripts",
        desc="Use when creating or upgrading a portable Linux operations skill in this engine under the canonical chwezi-dev-engine skill-writing standard; distinguishes authoring contracts from executing `linux-sysadmin` workflows and from the read-only `skill-safety-audit` review gate.",
        use="Creating a specialist Linux skill or changing an existing skill's trigger, contract, references or routing fixtures.",
        neighbour="Execute Linux administration through `linux-sysadmin`; use `skill-safety-audit` for a read-only review of unsafe instructions.",
        validators="`python -X utf8 scripts/validate_skills.py --baseline quality-baseline.json` and `python -X utf8 scripts/routing_smoke_test.py` (Linux-native tests run on Linux)",
        delta=["Keep `## Distro support` as the first H2 of every specialist skill; route family differences through `common.sh` primitives in `sk-*` guidance; manual commands stay the baseline and scripts are optional.",
               "Never mutate a server while writing a skill; keep the author metadata keys; follow the [local authoring standard](../../docs/engine-design/skill-authoring-standard.md) and [skill template](../../templates/skill-template.md)."],
        example="For slow PostgreSQL queries, inspect `linux-postgresql` and `linux-perf-profiling`; route query diagnosis to the former and host-wide attribution to the latter, and add a collision fixture for the ambiguous prompt.",
        refs=["[Local authoring standard](../../docs/engine-design/skill-authoring-standard.md)", "[Skill template](../../templates/skill-template.md)",
              "[Skill safety audit](../skill-safety-audit/SKILL.md)"],
        meta=LINUX_META, ack=False),
    "proposal-skills": dict(
        path="skills/meta/skill-writing", scripts="skills/meta/skill-writing/scripts",
        desc="Use when creating or normalising reusable proposal skills, trigger routes, contracts, references, or authoring automation under the canonical chwezi-dev-engine skill-writing standard; use skill-safety-audit instead for a read-only security review.",
        use="Creating or upgrading an active proposal skill, its trigger description or its directly linked resources.",
        neighbour="Use `skill-safety-audit` for a read-only inspection of unsafe instructions or bundled resources.",
        validators="`python -X utf8 scripts/validate_skills.py`, `python -X utf8 scripts/routing_smoke_test.py`, `python -X utf8 scripts/source_ingestion_guardrail.py` and `git diff --check`",
        delta=["Follow the [proposal authoring standard](../../../docs/skill-authoring-standard.md); frontmatter holds only `name`, `description` and `metadata`, and the acknowledgement sits under the title.",
               "Run the source-ingestion guardrail whenever a book or other copyrighted source informs the work, and apply [anti-AI slop](../anti-ai-slop/SKILL.md) before release."],
        example="When `financial-proposal` overlaps `work-plan`, keep pricing and fee assumptions in `financial-proposal` and route staffing days to `work-plan`; a fixture asking for a price schedule must rank the financial skill in the top three.",
        refs=["[Proposal authoring standard](../../../docs/skill-authoring-standard.md)", "[Skill safety audit](../skill-safety-audit/SKILL.md)",
              "[Anti-AI slop](../anti-ai-slop/SKILL.md)"],
        meta=META4, ack=True),
}


def render(c: dict) -> str:
    q = f"python -X utf8 {c['scripts']}/quick_validate.py <skill-dir>"
    lines = ["---", "name: skill-writing", f"description: {c['desc']}"] + c["meta"].rstrip("\n").split("\n") + ["---", "# Skill Writing"]
    if c["ack"]:
        lines.append(ACK)
    lines += [
        "",
        f"Pointer stub. The canonical standard is `chwezi-dev-engine/skills/sdlc-meta/skill-writing` ([canonical on GitHub]({GH}); local path `{LOCAL}`). Load it first; this file keeps a portable minimum and this engine's delta.",
        "", "<!-- dual-compat-start -->", "## Use When", "", f"- {c['use']}",
        "", "## Do Not Use When", "", f"- {c['neighbour']}",
        "", "## Required Inputs", "",
        "| Artefact | Source/provider | Required? | If absent |", "|---|---|---:|---|",
        "| Reusable problem, trigger prompts and neighbour descriptions | Requester and live catalogue | Yes | Stop; search the catalogue before drafting. |",
        "| Canonical skill-writing standard | chwezi-dev-engine checkout or GitHub | Yes | Apply the portable minimum and mark canonical-only checks `NOT ASSESSED`. |",
        "", "## Workflow", "",
        "1. Read the canonical standard, then this engine's delta; inspect the closest neighbours.",
        "2. Write the input, output, evidence, capability, degraded-mode and decision contracts before the procedure.",
        f"3. Run {c['validators']}, then `{q}`.",
        "4. Stop on any finding or routing collision; recover by fixing the named contract and rerun, never by weakening the gate.",
        "", "## Outputs", "",
        "| Artefact | Consumer | Acceptance condition |", "|---|---|---|",
        "| Skill directory and routing fixtures | Maintainer and router | Validators pass and the expected skill ranks in the top three. |",
        "", "## Evidence Produced", "",
        "| Evidence | Artefact and format | Consumer | Acceptance condition |", "|---|---|---|---|",
        "| Validation and routing record | Command output | Release owner | Zero findings; unrun checks marked `NOT ASSESSED`. |",
        "<!-- dual-compat-end -->", "", "## Quality Standards", "",
        "- Portable minimum, applied even when the canonical is unreachable: frontmatter uses only approved keys and `name` matches the folder.",
        "- The description starts `Use when`, stays within 350 characters and names a neighbour, with no workflow steps.",
        "- `SKILL.md` stays within 500 lines; deep detail sits in references one level deep, linked directly.",
        "- Every new or changed skill gets positive, negative and collision routing fixtures.",
        "- Bundled scripts run through their interpreter, for example `python -X utf8 scripts/<name>.py`.",
        "- No book extractions or copied third-party text; paraphrase and attribute.",
        "- British English, the imperative mood, and `NOT ASSESSED` for any check not run.",
        "", "## Engine-Local Delta", "",
    ] + [f"- {d}" for d in c["delta"]] + [
        "", "## Capability Contract", "",
        "Read and search are required. Editing files and running validators need explicit permission for the authoring task; publishing, deletion and release changes need separate authorisation.",
        "", "## Degraded Mode", "",
        "If the canonical standard is unavailable, apply the portable minimum, return the narrowest qualified result, and mark each canonical-only check `NOT ASSESSED`; never report it as passed.",
        "", "## Decision Rules", "",
        "| Condition | Action | Failure or risk avoided |", "|---|---|---|",
        "| An existing skill owns the trigger and output | Normalise it in place; put branch-only detail in a linked reference | Duplicate routes and oversized entrypoints |",
        "", "## Anti-Patterns", "",
        "- Copying the canonical body into this engine. Fix: link the canonical and keep only the delta here.",
        "- Writing only positive triggers. Fix: name the neighbour and add a collision fixture.",
        "- Treating an unrun validator as a pass. Fix: record `NOT ASSESSED` with the reason.",
        "- Granting edit rights to a review procedure. Fix: default review and audit to read-only.",
        "- Weakening a baseline to clear a finding. Fix: repair the named contract instead.",
        "", "## Worked Example", "", c["example"],
        "", "## References", "", f"- [Canonical skill-writing standard]({GH})",
    ] + [f"- {r}" for r in c["refs"]]
    compact = []
    body_started = True
    for index, line in enumerate(lines):
        if line.startswith("<!-- dual-compat-start"):
            body_started = True
        nxt = lines[index + 1] if index + 1 < len(lines) else ""
        prev = compact[-1] if compact else ""
        if body_started and line == "" and (nxt.startswith(("## ", "<!--")) or prev.startswith(("## ", "<!--"))):
            continue
        compact.append(line)
    return "\n".join(compact) + "\n"


if __name__ == "__main__":
    for engine in sys.argv[1:] or list(ENGINES):
        cfg = ENGINES[engine]
        text = render(cfg)
        fm_end = text.index("\n---\n", 4) + 5
        out = W / engine / cfg["path"] / "SKILL.md"
        out.write_text(text, encoding="utf-8", newline="\n")
        print(f"{engine}: total {text.count(chr(10))} lines, body {text[fm_end:].count(chr(10))}, desc {len(cfg['desc'])}")
