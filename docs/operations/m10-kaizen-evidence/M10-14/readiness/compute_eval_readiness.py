"""M10-14 T05: Engine Eval Readiness from stored inputs (deterministic; no engine is read).

Readiness = 30*T1 + 40*mean(p@1, owned-negative pass, coverage, collision cleanliness) + 30*T3.
NOT_ASSESSED (null / absent) = 0 in its slot. Rubric: chwezi-dev-engine
skills/sdlc-meta/skill-engine-audit/references/scoring-rubric.md "Engine Eval Readiness (measured)".
Usage: python -X utf8 compute_eval_readiness.py  -> writes ../eval-readiness.json
"""
import json, pathlib, hashlib

H = pathlib.Path(__file__).resolve().parent
t1 = json.loads((H / "tier1-results.json").read_text(encoding="utf-8"))
cov = json.loads((H / "coverage.json").read_text(encoding="utf-8"))
col = json.loads((H / "collision-scan.json").read_text(encoding="utf-8"))
t2 = json.loads((H / "t2-inputs.json").read_text(encoding="utf-8"))

ENGINES = ["chwezi-dev-engine", "design-system-skills", "srs-skills", "website-skills", "digital-research-engine",
           "proposal-skills", "business-plan-skills", "social-media-skills", "linux-skills",
           "chwezi-accounting-doctrine", "windows-admin-engine-skills", "chwezi-engine-agents"]
ALIAS = {"digital-research-engine": "digital-research-skills"}  # catalogue id used in the union scan

def r4(x): return round(x, 4)

undeclared = {}
for p in col.get("cross_engine_pairs", []):
    if p["score"] >= col["thresholds"]["error"]:
        for s in p["skills"]:
            e = s.split("/")[0]
            undeclared.setdefault(e, [0, 0])
            undeclared[e][1] += 1
            if not p.get("declared"):
                undeclared[e][0] += 1

out = {"formula": "30*T1 + 40*mean(T2_p1, T2_neg, T2_cov, T2_clean) + 30*T3; NOT_ASSESSED = 0",
       "label": t2["label"], "engines": {}}
for e in ENGINES:
    slots, na = {}, []
    if e == "chwezi-engine-agents":
        a = t2["agents_tier1"]; slots["T1"] = r4(a["passed"] / a["declared"])
    else:
        slots["T1"] = t1["engines"][e]["t1"]
        na += [f"T1 {v['command']}" for v in t1["engines"][e]["validators"] if v["status"] == "NOT_ASSESSED"]
    p = t2["p_at_1"].get(e)
    slots["T2_p1"] = r4(p["hits"] / p["total"]) if p else 0.0
    if not p: na.append("T2_p1 (harness reports p@3 only, or no routing harness)")
    n = t2["owned_negatives"].get(e)
    slots["T2_neg"] = r4((n["pass_local"] + n["mirror_pass"]) / n["total"]) if n else 0.0
    if not n: na.append("T2_neg (no owned negatives)")
    c = cov.get(e)
    slots["T2_cov"] = c["coverage"] if c else 0.0
    if not c: na.append("T2_cov (no routing fixtures)")
    key = ALIAS.get(e, e)
    u = undeclared.get(key, [0, 0])
    if key in col.get("skills_per_engine", {}):
        slots["T2_clean"] = r4(1 - u[0] / u[1]) if u[1] else 1.0
    else:  # not in the union scan: NOT_ASSESSED, never clean by default
        slots["T2_clean"] = 0.0
        na.append("T2_clean (engine not in the union collision scan)")
    slots["T3"] = r4(t2["t3"]["executed_runs"] / t2["t3"]["planned_runs"]) if t2["t3"]["executed_runs"] else 0.0
    na.append("T3 (zero-spend rule; 0 grading.json files)")
    t2mean = (slots["T2_p1"] + slots["T2_neg"] + slots["T2_cov"] + slots["T2_clean"]) / 4
    points = {"T1": round(30 * slots["T1"], 2), "T2": round(40 * t2mean, 2), "T3": round(30 * slots["T3"], 2)}
    out["engines"][e] = {"slots": slots, "points": points, "readiness": round(sum(points.values()), 1),
                          "not_assessed": na, "cross_engine_pairs_ge_0_75": u[1], "undeclared": u[0]}
body = json.dumps(out, indent=2, sort_keys=True)
out["inputs_sha256"] = {f: hashlib.sha256((H / f).read_bytes()).hexdigest() for f in
                        ["tier1-results.json", "coverage.json", "collision-scan.json", "t2-inputs.json"]}
(H.parent / "eval-readiness.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8")
for e, v in out["engines"].items():
    print(f"{e:30s} R={v['readiness']:5.1f}  T1={v['points']['T1']:5.2f} T2={v['points']['T2']:5.2f} T3={v['points']['T3']:4.1f}  {v['slots']}")
