"""
test_analyzer.py — Unit tests for statistical aggregator and hypothesis tests.
"""

import unittest
from src.core.models import MCQRecord, EvaluationScores
from src.core.analyzer import BenchmarkAnalyzer


class TestAnalyzer(unittest.TestCase):
    def test_analyzer_metrics_and_anova(self):
        # Build sample records
        questions = []
        for i in range(10):
            questions.append(MCQRecord(
                id=f"g-{i}", stem=f"Stem {i}", options={"A": "1", "B": "2", "C": "3", "D": "4"},
                correct_key="A", explanation="Exp", condition="generic", subject="Operating Systems",
                flaw_flags=["FLAW_NO_CITATION"],
                scores=EvaluationScores(factual_correctness=4.0, syllabus_alignment=5.0, distractor_quality=3.5, traceability=1.0, composite_quality=60.0)
            ))
            questions.append(MCQRecord(
                id=f"s-{i}", stem=f"Stem {i}", options={"A": "1", "B": "2", "C": "3", "D": "4"},
                correct_key="A", explanation="Exp", condition="syllabus_constrained", subject="Operating Systems",
                flaw_flags=[],
                scores=EvaluationScores(factual_correctness=4.7, syllabus_alignment=5.0, distractor_quality=4.8, traceability=3.6, composite_quality=92.0)
            ))
            questions.append(MCQRecord(
                id=f"c-{i}", stem=f"Stem {i}", options={"A": "1", "B": "2", "C": "3", "D": "4"},
                correct_key="A", explanation="Exp", condition="source_grounded", subject="Operating Systems",
                flaw_flags=[],
                scores=EvaluationScores(factual_correctness=5.0, syllabus_alignment=5.0, distractor_quality=5.0, traceability=5.0, composite_quality=99.0)
            ))

        metrics = BenchmarkAnalyzer.compute_metrics(questions)
        self.assertIn("generic", metrics)
        self.assertIn("syllabus_constrained", metrics)
        self.assertIn("source_grounded", metrics)
        self.assertEqual(metrics["generic"].flaw_rate, 100.0)
        self.assertEqual(metrics["source_grounded"].flaw_rate, 0.0)

        stat_tests = BenchmarkAnalyzer.compute_statistical_tests(questions)
        self.assertGreater(stat_tests["f_statistic"], 50.0)
        self.assertLess(stat_tests["p_value"], 0.001)
        self.assertTrue(stat_tests["is_significant"])


if __name__ == "__main__":
    unittest.main()
