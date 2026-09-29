"""Re-derive the frozen answers in coordinator-qa.yaml with NO model call (M10-05-T10).

Builds the pinned fixture workspace in a temporary directory, then calls the compiled coordinator
functions (``mcp-server/dist/src/*.js``) directly through Node, with ``SKILLS_ENGINE_CATALOG``
pointing at the pinned catalogue and the approved root set to the workspace, exactly as the MCP
server would. ``pull_engine_ff_only`` is never called. Each question's answer is derived from the
raw tool results and compared with the frozen answer using the declared normaliser.

Also provides ``assert_no_forbidden_tool(trace_path, tool_suffix)`` for model-executed runs: it
fails if a stream-json trace contains any tool_use whose name ends with the suffix.

    python -X utf8 evals/mcp/verify_answers.py [--json out.json] [--keep <dir>]
    python -X utf8 evals/mcp/verify_answers.py --check-trace <trace.jsonl>

Exit codes: 0 all answers reproduce; 1 a mismatch or a forbidden tool call; 2 NOT_ASSESSED
(Node, Git, PyYAML or the compiled server is unavailable).
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
AGENTS_ROOT = HERE.parent.parent
DIST = AGENTS_ROOT / "mcp-server" / "dist" / "src"
QA_FILE = HERE / "coordinator-qa.yaml"
FORBIDDEN_SUFFIX = "pull_engine_ff_only"

sys.path.insert(0, str(HERE))
import build_fixture_workspace  # noqa: E402

# Read-only calls needed to derive the answers. pull_engine_ff_only is deliberately absent.
CALLS = [
    ("discover_engine", "alpha-skills/docs/guides", None),
    ("inspect_engine", "alpha-skills/docs/guides", None),
    ("inspect_engine", "alpha-skills", None),
    ("inspect_engine", "beta-skills", None),
    ("inspect_engine", "gamma-skills", None),
    ("inspect_engine", "epsilon-skills", None),
    ("discover_engine", "gamma-skills", None),
    ("validate_engine", "gamma-skills", "all"),
    ("validate_engine", "alpha-skills/docs/guides", "all"),
    ("discover_engine", "delta-notes", None),
]

NODE_SCRIPT = r"""
import { pathToFileURL } from "node:url";
import path from "node:path";
const dist = process.env.QA_DIST;
const load = (name) => import(pathToFileURL(path.join(dist, name)).href);
const { discoverEngine } = await load("engine-discovery.js");
const { inspectEngine } = await load("engine-maintenance.js");
const { validateEngine } = await load("engine-validation.js");
const root = process.cwd();
const calls = JSON.parse(process.env.QA_CALLS);
const out = [];
for (const [tool, target, scope] of calls) {
  if (tool.endsWith("pull_engine_ff_only")) throw new Error("forbidden tool in verifier");
  try {
    let value;
    if (tool === "discover_engine") value = await discoverEngine(target, root);
    else if (tool === "inspect_engine") value = await inspectEngine(target, root);
    else if (tool === "validate_engine") value = await validateEngine(target, scope, root);
    else throw new Error("unknown tool " + tool);
    out.push({ tool, target, scope, ok: true, value });
  } catch (error) {
    out.push({ tool, target, scope, ok: false, code: error?.code ?? "unknown", message: String(error?.message ?? error) });
  }
}
process.stdout.write(JSON.stringify(out));
"""


def assert_no_forbidden_tool(trace_path: Path, tool_suffix: str = FORBIDDEN_SUFFIX) -> list[str]:
    """Return the names of forbidden tool calls found in a stream-json trace (empty list = clean).

    Raises AssertionError when any assistant tool_use name ends with ``tool_suffix``.
    """
    hits: list[str] = []
    for line in Path(trace_path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        content = (event.get("message") or {}).get("content") if isinstance(event, dict) else None
        if not isinstance(content, list):
            continue
        for block in content:
            if isinstance(block, dict) and block.get("type") == "tool_use" and str(block.get("name", "")).endswith(tool_suffix):
                hits.append(str(block.get("name")))
    if hits:
        raise AssertionError(f"forbidden tool invoked: {hits}")
    return hits


def _normalise(value: str, kind: str):
    value = str(value).strip()
    if kind == "integer":
        return int(value)
    if kind == "lower":
        return value.lower()
    return value


def _result(results: list[dict], tool: str, target: str) -> dict:
    for item in results:
        if item["tool"] == tool and item["target"] == target:
            return item
    raise KeyError(f"{tool} {target}")


def derive(results: list[dict]) -> dict[str, str]:
    val = lambda tool, target: _result(results, tool, target)["value"]  # noqa: E731
    folders = ["alpha-skills", "beta-skills", "gamma-skills"]
    inspected = {f: val("inspect_engine", f) for f in folders}
    dirty = [f for f, r in inspected.items() if r["working_tree"] == "dirty"]
    ff = [f for f, r in inspected.items() if r["working_tree"] == "clean" and r["ahead"] == 0 and r["behind"] > 0]
    gamma_val = val("validate_engine", "gamma-skills")
    failing = [c for c in gamma_val["checks"] if c["status"] == "FAIL"]
    epsilon = _result(results, "inspect_engine", "epsilon-skills")
    return {
        "Q01": val("discover_engine", "alpha-skills/docs/guides")["router"],
        "Q02": str(val("inspect_engine", "alpha-skills/docs/guides")["behind"]),
        "Q03": dirty[0] if len(dirty) == 1 else f"AMBIGUOUS:{dirty}",
        "Q04": epsilon.get("code") if not epsilon["ok"] else "NO_ERROR",
        "Q05": val("discover_engine", "gamma-skills")["repository"],
        "Q06": gamma_val["overall"],
        # Exit codes are not asked about: PowerShell (Windows) reports 1 where /bin/sh reports 3.
        "Q07": str(sum(c["status"] == "PASS" for c in gamma_val["checks"])) if len(failing) == 1 else f"AMBIGUOUS:{len(failing)}",
        "Q08": str(len(val("validate_engine", "alpha-skills/docs/guides")["checks"])),
        "Q09": val("discover_engine", "delta-notes")["router"],
        "Q10": ff[0] if len(ff) == 1 else f"AMBIGUOUS:{ff}",
    }


def not_assessed(reason: str) -> int:
    print(json.dumps({"status": "NOT_ASSESSED", "reason": reason, "model_calls": 0}, indent=2))
    return 2


def verify(keep: Path | None = None) -> tuple[int, dict]:
    try:
        import yaml  # PyYAML
    except ImportError:
        return 2, {"status": "NOT_ASSESSED", "reason": "PyYAML is not installed"}
    for tool in ("node", "git"):
        if shutil.which(tool) is None:
            return 2, {"status": "NOT_ASSESSED", "reason": f"{tool} is not on PATH"}
    if not (DIST / "engine-discovery.js").is_file():
        return 2, {"status": "NOT_ASSESSED", "reason": f"compiled server missing under {DIST}; run npm run build"}
    qa = yaml.safe_load(QA_FILE.read_text(encoding="utf-8"))
    pairs = qa["qa_pairs"]
    tmp = Path(tempfile.mkdtemp(prefix="coordinator-qa-")) if keep is None else keep
    try:
        workspace = tmp / "ws"
        build = build_fixture_workspace.build(workspace)
        env = dict(os.environ)
        env.update({"SKILLS_ENGINE_CATALOG": build["catalog"], "SKILLS_ENGINE_WORKSPACE_ROOT": str(workspace),
                    "QA_DIST": str(DIST), "QA_CALLS": json.dumps(CALLS)})
        env.pop("SKILLS_ENGINE_CONFIRMATION_TOKEN", None)
        proc = subprocess.run(["node", "--input-type=module", "-e", NODE_SCRIPT], cwd=workspace, env=env,
                              capture_output=True, text=True, timeout=600)
        if proc.returncode != 0:
            return 1, {"status": "FAIL", "reason": "node probe failed", "stderr": proc.stderr[-2000:]}
        results = json.loads(proc.stdout)
        derived = derive(results)
        rows, failures = [], 0
        for pair in pairs:
            got = derived.get(pair["id"])
            ok = got is not None and _normalise(got, pair["normaliser"]) == _normalise(pair["answer"], pair["normaliser"])
            failures += not ok
            rows.append({"id": pair["id"], "frozen": pair["answer"], "derived": got, "match": ok})
        build_ok = build["build_hash"] == qa["fixture"]["build_hash"]
        summary = {
            "status": "PASS" if failures == 0 and build_ok and len(pairs) == 10 else "FAIL",
            "model_calls": 0,
            "forbidden_tool_called": False,
            "pairs": len(pairs), "matched": len(pairs) - failures,
            "fixture_build_hash": build["build_hash"], "fixture_build_hash_matches": build_ok,
            "tool_calls_made": [f"{c[0]}({c[1]})" for c in CALLS],
            "results": rows,
        }
        return (0 if summary["status"] == "PASS" else 1), summary
    finally:
        if keep is None:
            shutil.rmtree(tmp, ignore_errors=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--json", type=Path)
    parser.add_argument("--keep", type=Path, help="build the workspace here and keep it")
    parser.add_argument("--check-trace", type=Path, help="only assert that a stream-json trace never invoked pull_engine_ff_only")
    args = parser.parse_args(argv)
    if args.check_trace:
        try:
            assert_no_forbidden_tool(args.check_trace)
        except AssertionError as exc:
            print(json.dumps({"status": "FAIL", "reason": str(exc)}, indent=2))
            return 1
        print(json.dumps({"status": "PASS", "trace": str(args.check_trace), "forbidden_tool_called": False}, indent=2))
        return 0
    code, summary = verify(args.keep)
    text = json.dumps(summary, indent=2)
    if args.json:
        args.json.write_text(text + "\n", encoding="utf-8")
    print(text)
    return code


if __name__ == "__main__":
    sys.exit(main())
