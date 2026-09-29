"""M10-14 T05: T2 coverage per engine = active skills with >= 3 positive fixtures and >= 2 owned
negatives, divided by active skills. Reads routing fixture files only; writes readiness/coverage.json.
An owned negative belongs to the skill that must NOT win (its `skill`, or the parent fixture's
expected skill when nested). Skill ids are compared by final path segment.
"""
import json, pathlib, collections
import yaml

HERE = pathlib.Path(__file__).resolve().parent
WS = HERE.parents[5]
ENGINES = {  # engine: (fixture files, active skill count from the engine's own validator on 29 Sep 2026)
    "chwezi-dev-engine": (["scripts/routing_fixtures.yml", "tests/routing/edge-fixtures.yml"], 167),
    "design-system-skills": (["tests/routing-fixtures.yml"], 101),
    "srs-skills": (["tests/routing-fixtures.json"], 159),
    "website-skills": (["tests/routing/fixtures.json"], 62),
    "digital-research-engine": (["tests/skill-engine/routing-fixtures.json"], 59),
    "proposal-skills": (["tests/fixtures/routing-fixtures.json"], 115),
    "business-plan-skills": (["tests/routing-fixtures.json"], 137),
    "social-media-skills": (["tests/routing-fixtures.json"], 191),
    "linux-skills": (["tests/fixtures/routing.json"], 48),
    "windows-admin-engine-skills": (["tests/fixtures/routing.json"], 21),
}
PROMPT = ("prompt", "task")
EXPECT = ("expected", "expect", "expected_skill")

def seg(v):
    if isinstance(v, list):
        v = v[0] if v else ""
    return str(v).rstrip("/").split("/")[-1]

def walk(node, parent_expected, pos, neg):
    if isinstance(node, dict):
        has_prompt = any(k in node for k in PROMPT)
        exp = next((node[k] for k in EXPECT if k in node), None)
        kind = str(node.get("kind") or node.get("class") or node.get("type") or "")
        if has_prompt and "owner" in node:
            target = node.get("skill") or parent_expected
            if target:
                neg[seg(target)] += 1
        elif has_prompt and exp and kind != "negative":
            pos[seg(exp)] += 1
        for k, v in node.items():
            walk(v, seg(exp) if exp else parent_expected, pos, neg)
    elif isinstance(node, list):
        for v in node:
            walk(v, parent_expected, pos, neg)

out = {}
for eng, (files, active) in ENGINES.items():
    pos, neg = collections.Counter(), collections.Counter()
    for f in files:
        p = WS / eng / f
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
        walk(data, None, pos, neg)
    full = sorted(s for s in pos if pos[s] >= 3 and neg[s] >= 2)
    out[eng] = {"active_skills": active, "skills_with_positive": len(pos), "skills_with_owned_negative": len(neg),
                "skills_ge3pos_ge2neg": len(full), "coverage": round(len(full) / active, 4),
                "positive_fixtures": sum(pos.values()), "owned_negatives": sum(neg.values()), "files": files}
    print(f"{eng}: {out[eng]}")
(HERE / "coverage.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
