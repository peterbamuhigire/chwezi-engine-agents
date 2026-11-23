import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "evals/cases"))
from replay_ai_journeys import replay


class CrossEngineJourneyTests(unittest.TestCase):
    def test_accepted_journeys_and_missing_dependencies(self):
        live = ROOT / "docs/plans/ai-engine-kaizen/evidence/incoming"
        pins = json.loads((ROOT / "evals/cases/ai-producer-pins.json").read_bytes())
        good = replay(live, pins)
        self.assertEqual(good["hosted_provider"], "NOT_ASSESSED")
        self.assertTrue(
            all(j["status"] == "ACCEPTED" for j in good["journeys"].values())
        )
        with tempfile.TemporaryDirectory() as temp:
            dst = Path(temp)
            for p in live.glob("*.json"):
                shutil.copyfile(p, dst / p.name)
            (dst / "chwezi-dev-engine.json").unlink()
            broken = replay(dst, pins)
            step = broken["journeys"]["coding"]["steps"][-1]
            self.assertEqual(
                (step["status"], step["producer"], step["artifact"], step["criterion"]),
                ("BLOCKED", "chwezi-dev-engine", "chwezi-dev-engine.json", "AC-E05"),
            )
            self.assertEqual(broken["journeys"]["classifier"]["status"], "BLOCKED")
            stale = {k: dict(v) for k, v in pins.items()}
            stale["srs-skills"]["revision"] = "old"
            self.assertEqual(
                replay(live, stale)["journeys"]["classifier"]["steps"][0]["status"],
                "BLOCKED",
            )
