"""M10-14 T05 Tier-1 collector: run every catalogue validator in its engine root.

Read-only apart from its own output file. Usage (from chwezi-engine-agents):
  python -X utf8 docs/operations/m10-kaizen-evidence/M10-14/readiness/run_tier1.py
Writes readiness/tier1-results.json. A validator that cannot run on this host is NOT_ASSESSED.
"""
import json, os, shutil, subprocess, sys, datetime, pathlib
import yaml

HERE = pathlib.Path(__file__).resolve().parent
AGENTS = HERE.parents[4]
WS = AGENTS.parent
cat = yaml.safe_load((AGENTS / "catalog" / "engines.yaml").read_text(encoding="utf-8"))
env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8")
out = {"measured_at": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
       "host": sys.platform, "engines": {}}
for e in cat["engines"]:
    root = WS / e["path"]
    head = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"], capture_output=True, text=True).stdout.strip()
    rows = []
    for cmd in e.get("validators", []):
        if cmd.startswith("bash ") and sys.platform.startswith("win"):
            rows.append({"command": cmd, "status": "NOT_ASSESSED", "reason": "Linux-native suite; audit host is Windows", "exit": None})
            continue
        if cmd.startswith(".\\") or cmd.endswith(".ps1") or ".ps1 " in cmd:
            argv = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", cmd]
        else:
            argv = cmd.split()
            if argv[0] == "python":
                argv[0] = sys.executable
        try:
            p = subprocess.run(argv, cwd=root, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=900)
            tail = (p.stdout + p.stderr).strip().splitlines()[-4:]
            rows.append({"command": cmd, "status": "PASS" if p.returncode == 0 else "FAIL", "exit": p.returncode, "tail": tail})
        except Exception as exc:  # noqa: BLE001
            rows.append({"command": cmd, "status": "NOT_ASSESSED", "reason": repr(exc), "exit": None})
    passed = sum(r["status"] == "PASS" for r in rows)
    out["engines"][e["path"]] = {"catalog_id": e["id"], "head": head, "declared": len(rows), "passed": passed,
                                  "t1": round(passed / len(rows), 4) if rows else 0.0, "validators": rows}
(HERE / "tier1-results.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
for k, v in out["engines"].items():
    print(f"{k}: {v['passed']}/{v['declared']} " + ", ".join(r['status'] for r in v['validators']))
