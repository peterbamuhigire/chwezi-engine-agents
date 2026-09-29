"""Hand-computed vectors for scripts/lib/retrieval_metrics.py (M10-10-T08, UX-09).

Every expected value below was worked by hand (arithmetic shown in the comment) before the
module was run, so the tests check the formulas rather than echo the implementation.
"""
from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts" / "lib"))

import retrieval_metrics as rm  # noqa: E402


class PrecisionTests(unittest.TestCase):
    def test_precision_divides_by_k(self) -> None:
        # [a,b,c] with {a,c}: 2 relevant in top 3 -> 2/3
        self.assertAlmostEqual(rm.precision_at_k(["a", "b", "c"], {"a", "c"}, 3), 2 / 3)
        # top 1 is a -> 1/1
        self.assertEqual(rm.precision_at_k(["a", "b", "c"], {"a", "c"}, 1), 1.0)
        # short list [x,a], k=3: 1 relevant / 3 positions -> 1/3
        self.assertAlmostEqual(rm.precision_at_k(["x", "a"], {"a"}, 3), 1 / 3)

    def test_graded_mapping_ignores_zero_grades(self) -> None:
        # grade 0 is not relevant: only 'a' counts -> 1/2
        self.assertEqual(rm.precision_at_k(["b", "a"], {"a": 2, "b": 0}, 2), 0.5)

    def test_invalid_k(self) -> None:
        with self.assertRaises(ValueError):
            rm.precision_at_k(["a"], {"a"}, 0)


class RankTests(unittest.TestCase):
    def test_reciprocal_rank(self) -> None:
        # first relevant at rank 3 -> 1/3
        self.assertAlmostEqual(rm.reciprocal_rank(["x", "y", "a"], {"a"}), 1 / 3)
        # cut at k=2: not found -> 0
        self.assertEqual(rm.reciprocal_rank(["x", "y", "a"], {"a"}, 2), 0.0)
        self.assertEqual(rm.reciprocal_rank(["a"], {"a"}), 1.0)

    def test_mrr_at_k(self) -> None:
        # cases: rank 2 -> 0.5; rank 1 -> 1.0; absent -> 0.0; mean = 1.5 / 3 = 0.5
        cases = [(["x", "a"], {"a"}), (["a"], {"a"}), (["x", "y", "z"], {"a"})]
        self.assertAlmostEqual(rm.mrr_at_k(cases, 3), 0.5)
        # at k=1 only the second case scores: 1 / 3
        self.assertAlmostEqual(rm.mrr_at_k(cases, 1), 1 / 3)

    def test_typo_recovery(self) -> None:
        self.assertEqual(rm.typo_recovery_at_k(["x", "y", "a"], {"a"}, 3), 1.0)
        self.assertEqual(rm.typo_recovery_at_k(["x", "y", "a"], {"a"}, 2), 0.0)


class GainTests(unittest.TestCase):
    def test_dcg(self) -> None:
        # gains [2,1,0]: (2^2-1)/log2(2) + (2^1-1)/log2(3) + 0 = 3 + 0.6309298
        self.assertAlmostEqual(rm.dcg_at_k([2, 1, 0], 3), 3 + 1 / math.log2(3))
        # gains [1,2]: 1/1 + 3/log2(3) = 1 + 1.8927893
        self.assertAlmostEqual(rm.dcg_at_k([1, 2], 2), 1 + 3 / math.log2(3))

    def test_ndcg(self) -> None:
        grades = {"a": 2, "b": 1}
        # ideal order [a,b] -> 3 + 0.6309298 = 3.6309298; actual [b,a] -> 2.8927893
        # ratio = 2.8927893 / 3.6309298 = 0.796707...
        self.assertAlmostEqual(rm.ndcg_at_k(["b", "a"], grades, 2), 2.8927892607 / 3.6309297536, places=6)
        self.assertEqual(rm.ndcg_at_k(["a", "b"], grades, 2), 1.0)
        # nothing relevant -> 0.0, never a division error
        self.assertEqual(rm.ndcg_at_k(["a"], {}, 3), 0.0)
        # at k=1 with [b,a]: actual 1/1 = 1, ideal 3/1 = 3 -> 1/3
        self.assertAlmostEqual(rm.ndcg_at_k(["b", "a"], grades, 1), 1 / 3)


class AbstentionTests(unittest.TestCase):
    def test_abstention_rate(self) -> None:
        self.assertEqual(rm.abstention_rate([True, False, True, True]), 0.75)
        self.assertEqual(rm.abstention_rate([]), 0.0)
        self.assertEqual(rm.abstention_rate([False, False]), 0.0)


class BM25Tests(unittest.TestCase):
    def test_single_field_scores(self) -> None:
        # d0 = [a,b] (len 2), d1 = [b] (len 1); N = 2, avgdl = 1.5
        # idf(a) = ln(1 + 1.5/1.5) = ln 2 ; idf(b) = ln(1 + 0.5/2.5) = ln 1.2
        # d0,"a": norm = 0.25 + 0.75*2/1.5 = 1.25 ; 1*2.5/(1 + 1.5*1.25) = 0.8695652 ; * ln2 = 0.6027366
        # d1,"b": norm = 0.25 + 0.75*1/1.5 = 0.75 ; 2.5/(1 + 1.125) = 1.1764706 ; * ln1.2 = 0.2144960
        bm = rm.BM25().fit([{"t": ["a", "b"]}, {"t": ["b"]}])
        self.assertAlmostEqual(bm.score(["a"], 0), math.log(2) * 2.5 / 2.875)
        self.assertAlmostEqual(bm.score(["b"], 1), math.log(1.2) * 2.5 / 2.125)
        self.assertEqual(bm.score(["a"], 1), 0.0)
        # duplicate query tokens count once
        self.assertEqual(bm.score(["a", "a"], 0), bm.score(["a"], 0))

    def test_field_boosts(self) -> None:
        # doc0 tags=[a] (boost 3), body=[a,c]: tf(a) = 3 + 1 = 4 ; len = 3*1 + 2 = 5
        # doc1 body=[c]: len 1 ; avgdl = 3 ; idf(a) = ln 2
        # norm = 0.25 + 0.75*5/3 = 1.5 ; 4*2.5/(4 + 1.5*1.5) = 10/6.25 = 1.6 ; * ln2 = 1.1090355
        bm = rm.BM25(boosts={"tags": 3}).fit([{"tags": ["a"], "body": ["a", "c"]}, {"body": ["c"]}])
        self.assertAlmostEqual(bm.score(["a"], 0), 1.6 * math.log(2))
        self.assertEqual(len(bm.scores(["a"])), 2)

    def test_parameter_guard(self) -> None:
        with self.assertRaises(ValueError):
            rm.BM25(b=1.5)


if __name__ == "__main__":
    unittest.main()
