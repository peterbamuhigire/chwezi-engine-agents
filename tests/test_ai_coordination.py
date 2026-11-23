import hashlib
import json
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "evals/contracts"), str(ROOT / "evals/behavioural")]
from ai_evidence import inspect_evidence
from ai_routes import evaluate
from ai_recovery import record


class CoordinatorCases(unittest.TestCase):
    def setUp(self):
        root = tempfile.TemporaryDirectory()
        self.addCleanup(root.cleanup)
        self.base = Path(root.name)

    def fixture(self, case, observed):
        expected = {
            "producer": "engineering",
            "consumer": "reviewer",
            "case_id": case,
            "criterion": "AC-" + case,
            "input_revision": "fixture-1",
            "output_revision": "patch-2",
            "expected_outcome": observed,
        }
        payload = {k: v for k, v in expected.items() if k != "expected_outcome"}
        if case == "K2":
            expected["producer"] = payload["producer"] = "evaluation-reviewer"
        payload.update(
            observed=observed,
            limitations="Synthetic examples only",
            next_action="Inspect the reviewed change.",
        )
        path = self.base / (case + ".json")
        path.write_bytes(json.dumps(payload).encode())
        return expected, {
            "format": "ai-evidence/1",
            "path": path.name,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        }

    def test_data_code_eval_and_failed_handoffs(self):
        for case, observed in [
            ("K1", "hold"),
            ("K2", "unsupported"),
            ("K3", "once"),
            ("K4", "restored"),
        ]:
            expected, ref = self.fixture(case, observed)
            self.assertEqual(
                inspect_evidence(self.base, ref, expected)["status"], "ACCEPTED"
            )
            for broken in [
                {**ref, "sha256": "0" * 64},
                {**ref, "path": "missing.json"},
            ]:
                result = inspect_evidence(self.base, broken, expected)
                self.assertEqual(result["status"], "BLOCKED")
                self.assertTrue(result["next_action"])
            self.assertEqual(
                inspect_evidence(
                    self.base, ref, {**expected, "output_revision": "unknown"}
                )["status"],
                "BLOCKED",
            )
            self.assertEqual(
                inspect_evidence(
                    self.base, ref, {**expected, "expected_outcome": "incorrect"}
                )["status"],
                "BLOCKED",
            )
        self.assertEqual(
            inspect_evidence(self.base, "legacy router path", expected)["status"],
            "NOT_ASSESSED",
        )

    def test_missing_or_null_measurement_is_blocked(self):
        exp, ref = self.fixture("K2", "unsupported")
        p = self.base / ref["path"]
        data = json.loads(p.read_bytes())
        del data["observed"]
        p.write_bytes(json.dumps(data).encode())
        ref["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
        self.assertEqual(
            inspect_evidence(self.base, ref, {**exp, "expected_outcome": None})[
                "status"
            ],
            "BLOCKED",
        )

    def test_ranks_and_execution_are_distinct(self):
        result = evaluate(
            json.loads((ROOT / "evals/behavioural/ai-route-cases.json").read_bytes())
        )
        self.assertEqual(result["rank_control"], 0.5)
        self.assertTrue(all(r["label_source"] for r in result["rows"]))
        self.assertEqual((result["request_count"], result["family_count"]), (8, 7))
        self.assertEqual((result["task_passed"], result["task_assessed"]), (1, 2))
        self.assertEqual(result["route_matches"], 8)
        self.assertEqual(
            next(x for x in result["rows"] if x["id"] == "deny")["ranked"], []
        )
        first = result["rows"][0]
        self.assertTrue(first["route_match"])
        self.assertEqual(first["execution"], "FAIL")

    def test_restart_conflict_and_absent_specialist(self):
        from contextlib import closing

        exp, ref = self.fixture("K3", "once")
        path = self.base / "effects.db"
        with closing(sqlite3.connect(path)) as db:
            self.assertEqual(record(db, None, exp, self.base, ref), "BLOCKED")
            self.assertEqual(record(db, "E7", exp, self.base, ref), "APPLIED")
        with closing(sqlite3.connect(path)) as db:
            self.assertEqual(record(db, "E7", exp, self.base, ref), "ALREADY_APPLIED")
            stale = {**exp, "output_revision": "patch-3"}
            self.assertEqual(record(db, "E7", stale, self.base, ref), "BLOCKED")
            self.assertEqual(
                record(db, "E8", exp, self.base, ref, available=False), "NOT_ASSESSED"
            )
            next_exp, next_ref = self.fixture("K4", "restored")
            self.assertEqual(
                record(db, "promote-42", next_exp, self.base, next_ref), "APPLIED"
            )
            self.assertEqual(
                db.execute("SELECT count(*) FROM effects").fetchone()[0], 2
            )
