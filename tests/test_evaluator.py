"""
test_evaluator.py — Unit tests for the deterministic and rubric evaluation engine.
"""

import unittest
from src.core.models import MCQRecord
from src.core.evaluator import Evaluator


class TestEvaluator(unittest.TestCase):
    def setUp(self):
        self.evaluator = Evaluator()

    def test_evaluator_valid_item(self):
        record = MCQRecord(
            id="test-valid-01",
            stem="Which scheduling algorithm is non-preemptive?",
            options={
                "A": "First-Come First-Served",
                "B": "Round Robin",
                "C": "Shortest Remaining Time First",
                "D": "Preemptive Priority Scheduling"
            },
            correct_key="A",
            explanation="FCFS executes processes until completion without preemption.",
            condition="source_grounded",
            subject="Operating Systems",
            source_citation={
                "source_id": "src-silberschatz-os10",
                "citation_text": "Operating System Concepts, 10th Ed.",
                "chapter": "Chapter 5",
                "page": "205",
                "verified_excerpt": "Under nonpreemptive scheduling, once the CPU has been allocated to a process, the process keeps the CPU until it releases it."
            }
        )

        result = self.evaluator.evaluate(record)
        self.assertTrue(result.is_valid)
        self.assertEqual(len(result.flaw_flags), 0)
        self.assertGreaterEqual(result.scores.composite_quality, 95.0)
        self.assertEqual(result.scores.traceability, 5.0)
        self.assertEqual(result.scores.factual_correctness, 5.0)

    def test_evaluator_all_none_flaw(self):
        record = MCQRecord(
            id="test-flaw-all-none",
            stem="What causes thrashing in virtual memory?",
            options={
                "A": "Excessive page faulting",
                "B": "Low CPU utilization",
                "C": "Insufficient physical frames",
                "D": "All of the above"
            },
            correct_key="D",
            explanation="Thrashing is characterized by high paging and low CPU utilization.",
            condition="generic",
            subject="Operating Systems",
        )

        result = self.evaluator.evaluate(record)
        self.assertIn("FLAW_ALL_NONE_ABOVE", result.flaw_flags)
        self.assertLess(result.scores.distractor_quality, 5.0)

    def test_evaluator_missing_citation(self):
        record = MCQRecord(
            id="test-no-cite",
            stem="What is the worst-case time complexity of quicksort?",
            options={
                "A": "O(n log n)",
                "B": "O(n^2)",
                "C": "O(n)",
                "D": "O(log n)"
            },
            correct_key="B",
            explanation="Quicksort takes quadratic time when partitions are maximally unbalanced.",
            condition="generic",
            subject="Data Structures and Algorithms",
            source_citation=None
        )

        result = self.evaluator.evaluate(record)
        self.assertIn("FLAW_NO_CITATION", result.flaw_flags)
        self.assertLessEqual(result.scores.traceability, 1.5)

    def test_evaluator_invalid_key_and_duplicate(self):
        record = MCQRecord(
            id="test-invalid-key",
            stem="Which protocol is connection-oriented at the transport layer?",
            options={
                "A": "TCP",
                "B": "TCP",  # Duplicate
                "C": "UDP",
                "D": "IP"
            },
            correct_key="E",  # Invalid key
            explanation="TCP is connection oriented.",
            condition="generic",
            subject="Computer Networks",
        )

        result = self.evaluator.evaluate(record)
        self.assertFalse(result.is_valid)
        self.assertIn("ERR_INVALID_KEY", result.flaw_flags)
        self.assertIn("FLAW_DUPLICATE_OPT", result.flaw_flags)


if __name__ == "__main__":
    unittest.main()
