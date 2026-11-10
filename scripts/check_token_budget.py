"""Token-budget and model-class lint for repositories that carry engine or project instructions.

Runner-neutral: checks the files that Claude Code (CLAUDE.md) and Codex (AGENTS.md) load at session start.

    python scripts/check_token_budget.py REPO_DIR [REPO_DIR ...] [--strict] [--deep]

Rules:
  T-01  AGENTS.md at or under 32,768 bytes (Codex stops reading project instructions at its byte cap).
  T-02  CLAUDE.md at or under 32,000 bytes (target: at most about 8,000 tokens for anything loaded on every session).
  T-03  A repository with instructions carries the model-class block (marker MODEL-ROUTING-BLOCK) in the first 12,000 bytes.
  T-04  Subagent definitions (agents/*.md) pin a model class through a 'model:' front-matter line.
  T-06  The class block names classes only: no model version numbers or model IDs inside it.
  T-07  Plan resume or status files under docs/plans stay at or under 8,000 bytes.
  T-05  (--deep) no retired model IDs in source files.

Exit code 1 with --strict when any rule fails.
"""
import pathlib
import re
import sys

CAP_AGENTS = 32768
CAP_CLAUDE = 32000
BLOCK = re.compile(r"<!-- MODEL-ROUTING-BLOCK.*?<!-- /MODEL-ROUTING-BLOCK -->", re.S)
STALE = re.compile(r"claude-3[-\w.]*|claude-(?:opus|sonnet|haiku)-4[-\w.]*")
SRC_EXT = {".php", ".ts", ".js", ".kt", ".py", ".cs", ".json", ".toml", ".yaml", ".yml"}
SKIP = {"node_modules", "vendor", ".git", "dist", "docs", "build", "archive", "tests", "fixtures"}


def size(p):
    return p.stat().st_size if p.exists() else None


def scan_stale(root, limit=4000):
    hits, n = [], 0
    for p in root.rglob("*"):
        if any(part in SKIP for part in p.parts) or not p.is_file() or p.suffix.lower() not in SRC_EXT:
            continue
        n += 1
        if n > limit:
            break
        m = STALE.search(p.read_text(encoding="utf-8", errors="ignore"))
        if m:
            hits.append(f"{p.relative_to(root)}: {m.group(0)}")
    return hits[:5]


def check(d, deep=False):
    fails = []
    a, c = size(d / "AGENTS.md"), size(d / "CLAUDE.md")
    if a is not None and a > CAP_AGENTS:
        fails.append(f"T-01 AGENTS.md {a:,} B over {CAP_AGENTS:,}")
    if c is not None and c > CAP_CLAUDE:
        fails.append(f"T-02 CLAUDE.md {c:,} B over {CAP_CLAUDE:,}")
    blocks = []
    for doc in (d / "AGENTS.md", d / "CLAUDE.md"):
        if doc.exists():
            txt = doc.read_bytes().decode("utf-8", errors="ignore")
            m = BLOCK.search(txt)
            if m:
                blocks.append((doc, m))
    if (a is not None or c is not None) and not blocks:
        fails.append("T-03 class block missing")
    for doc, m in blocks:
        if m.start() > 12000:
            fails.append(f"T-03 block in {doc.name} starts after 12,000 bytes")
        head = m.group(0).split("Tokens, both runners")[0]
        if re.search(r"(?<![\w.])\d+\.\d+(?![\w.])", head) or "claude-" in m.group(0):
            fails.append(f"T-06 model version in block ({doc.name})")
    for pf in list(d.glob("docs/plans/*/RESUME.md")) + list(d.glob("docs/plans/*/phase-status.md")):
        if pf.stat().st_size > 8000:
            fails.append(f"T-07 {pf.relative_to(d)} is {pf.stat().st_size:,} B (over 8,000)")
    miss = [p.name for p in d.glob("agents/*.md")
            if not re.search(r"^model:", p.read_text(encoding="utf-8", errors="ignore")[:1500], re.M)]
    if miss:
        fails.append(f"T-04 {len(miss)} subagent file(s) without a model pin")
    if deep:
        st = scan_stale(d)
        if st:
            fails.append("T-05 retired model IDs: " + "; ".join(st))
    return a, c, fails


def main():
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not args:
        print(__doc__)
        return 2
    total = 0
    for arg in args:
        d = pathlib.Path(arg)
        if not d.is_dir():
            continue
        a, c, fails = check(d, "--deep" in sys.argv)
        total += len(fails)
        print(f"{'FAIL' if fails else 'ok':4} {d.name:32} AGENTS={a} CLAUDE={c}")
        for f in fails:
            print("       -", f)
    print(f"{total} finding(s)")
    return 1 if (total and "--strict" in sys.argv) else 0


if __name__ == "__main__":
    sys.exit(main())
