"""Verify M10-14 traceability closure against backlog section 1 (read-only)."""
import re, sys, collections
BACKLOG = r"C:/Users/Peter/Documents/my-10-kaizen/05-traceability-backlog.md"
CLOSURE = r"C:/wamp64/www/chwezi-engine-agents/docs/operations/m10-kaizen-evidence/M10-14/traceability-closure.md"
ID = re.compile(r"\b(?:(?:SP|PT|UX|GR|CV|AO|UA|AC|AR|IM)-\d{2}|BL-\d{2}[a-z])\b")
ALLOWED = {"DONE", "DONE_WITH_LIMITATIONS", "PARTIAL", "NOT_ASSESSED", "DEFERRED",
           "DROPPED-AT-EXECUTION", "DONE (M10-14, commit pending orchestrator)"}
HASH = re.compile(r"\b[0-9a-f]{7}\b")
text = open(BACKLOG, encoding="utf-8").read()
sec1 = text.split("## 1. Assignment by phase", 1)[1].split("### 1.1", 1)[0]
backlog_ids = set()
for line in sec1.splitlines():
    if line.startswith("| **M10"):
        backlog_ids.update(ID.findall(line.split("|")[2]))
table = open(CLOSURE, encoding="utf-8").read().split("## 2. Traceability table", 1)[1].split("## 3.", 1)[0]
rows = [l for l in table.splitlines() if l.startswith("| ") and not l.startswith("| ID ")]
seen = collections.Counter(); status = collections.Counter(); errors = []
for r in rows:
    c = [x.strip() for x in r.strip().strip("|").split("|")]
    rid, st, commits = c[0], c[3], c[4]
    seen[rid] += 1; status[st] += 1
    if st not in ALLOWED: errors.append(f"{rid}: bad status {st!r}")
    if st in ("DONE", "DONE_WITH_LIMITATIONS") and not HASH.search(commits):
        errors.append(f"{rid}: {st} without commit hash")
    if st.startswith("DROPPED") and len(c[6]) < 10: errors.append(f"{rid}: dropped without reason")
missing = sorted(backlog_ids - set(seen)); extra = sorted(set(seen) - backlog_ids)
dups = sorted(k for k, v in seen.items() if v != 1)
print(f"backlog_section1_ids={len(backlog_ids)} table_rows={len(rows)} unique_table_ids={len(seen)}")
print(f"missing={missing} extra={extra} not_exactly_once={dups}")
print("status_counts=" + "; ".join(f"{k}: {v}" for k, v in sorted(status.items())))
print(f"rows_without_status={sum(1 for r in rows if not r.split('|')[4].strip())} errors={errors}")
ok = not (missing or extra or dups or errors) and len(rows) == len(backlog_ids)
print("RESULT: PASS" if ok else "RESULT: FAIL"); sys.exit(0 if ok else 1)
