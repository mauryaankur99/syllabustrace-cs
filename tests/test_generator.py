"""
test_generator.py — Unit tests for the multi-condition question generator.
"""

import unittest
from src.core.generator import MCQGenerator


class TestGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = MCQGenerator(provider="mock")

    def test_generator_conditions(self):
        # Test Generic condition
        q_gen = self.generator.generate(
            condition="generic",
            subject="Operating Systems",
            topic="CPU Scheduling",
        )
        self.assertEqual(q_gen.condition, "generic")
        self.assertEqual(len(q_gen.options), 4)
        self.assertIn(q_gen.correct_key, {"A", "B", "C", "D"})

        # Test Syllabus-Constrained condition
        q_syl = self.generator.generate(
            condition="syllabus_constrained",
            subject="Database Management Systems",
            topic="Normalization",
            subtopic="Boyce-Codd Normal Form",
            cognitive_level="Analysis"
        )
        self.assertEqual(q_syl.condition, "syllabus_constrained")
        self.assertIsNotNone(q_syl.source_citation)
        self.assertEqual(q_syl.cognitive_level, "Analysis")

        # Test Source-Grounded condition
        source_meta = {
            "source_id": "src-cormen-clrs4",
            "title": "Introduction to Algorithms",
            "authors": ["Cormen", "Leiserson", "Rivest", "Stein"],
            "chapter": "Chapter 22",
            "section": "22.3",
            "page": "595-601",
            "verified_excerpt": "Dijkstra's algorithm solves single-source shortest-paths on weighted directed graphs with non-negative edge weights."
        }
        q_src = self.generator.generate(
            condition="source_grounded",
            subject="Data Structures and Algorithms",
            topic="Graph Algorithms",
            subtopic="Dijkstra's Algorithm",
            source_data=source_meta
        )
        self.assertEqual(q_src.condition, "source_grounded")
        self.assertEqual(q_src.source_citation["verified_excerpt"], source_meta["verified_excerpt"])


if __name__ == "__main__":
    unittest.main()
