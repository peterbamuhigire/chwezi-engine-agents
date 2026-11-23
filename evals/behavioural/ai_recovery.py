"""Apply accepted K3/K4 handoffs once, using an operator-owned local SQLite journal."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "contracts"))
from ai_evidence import inspect_evidence


def record(conn, key, expected, root, reference, available=True):
    if not isinstance(key, str) or not key.strip():
        return "BLOCKED"
    if not available:
        return "NOT_ASSESSED"
    review = inspect_evidence(root, reference, expected)
    if review["status"] != "ACCEPTED":
        return "BLOCKED"
    identity = json.dumps(expected, sort_keys=True)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS effects (operation TEXT PRIMARY KEY, identity TEXT NOT NULL)"
    )
    with conn:
        n = conn.execute(
            "INSERT OR IGNORE INTO effects VALUES (?,?)", (key, identity)
        ).rowcount
        actual = conn.execute(
            "SELECT identity FROM effects WHERE operation=?", (key,)
        ).fetchone()[0]
        if actual != identity:
            return "BLOCKED"
    return "APPLIED" if n else "ALREADY_APPLIED"
