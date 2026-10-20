"""
test_api.py — Integration tests for FastAPI endpoints in SyllabusTrace-CS.
"""

import unittest
from fastapi.testclient import TestClient
from src.api.main import app


class TestAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_api_overview(self):
        res = self.client.get("/api/overview")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["project"], "SyllabusTrace-CS")
        self.assertGreaterEqual(data["total_questions"], 60)
        self.assertIn("counts_by_condition", data)
        self.assertIn("counts_by_subject", data)

    def test_api_syllabi(self):
        res = self.client.get("/api/syllabi")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["exam"], "GATE_CS")
        self.assertEqual(len(data["subjects"]), 5)

    def test_api_syllabus_coverage(self):
        res = self.client.get("/api/syllabi/coverage")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("overall_coverage_pct", data)
        self.assertGreater(data["overall_coverage_pct"], 50.0)

    def test_api_sources(self):
        res = self.client.get("/api/sources")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(len(data), 5)
        self.assertTrue(any("Silberschatz" in s["title"] or any("Silberschatz" in a for a in s["authors"]) for s in data))

    def test_api_questions_crud(self):
        # 1. Fetch questions list
        res = self.client.get("/api/questions?limit=10")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertGreaterEqual(data["total"], 60)

        # 2. Direct evaluation endpoint
        eval_payload = {
            "id": "temp-test-item",
            "stem": "What is the complexity of binary search on sorted array?",
            "options": {
                "A": "O(log n)",
                "B": "O(n)",
                "C": "O(n log n)",
                "D": "O(1)"
            },
            "correct_key": "A",
            "explanation": "Binary search halves the search space at each iteration.",
            "condition": "source_grounded",
            "subject": "Data Structures and Algorithms"
        }
        eval_res = self.client.post("/api/evaluate", json=eval_payload)
        self.assertEqual(eval_res.status_code, 200)
        eval_data = eval_res.json()
        self.assertTrue(eval_data["is_valid"])
        self.assertIn("scores", eval_data)

    def test_api_experiments_and_pariksha(self):
        res = self.client.get("/api/experiments/results")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("metrics", data)
        self.assertIn("statistical_significance", data)

        # Pariksha export
        pk_res = self.client.get("/api/pariksha/export?min_score=80.0")
        self.assertEqual(pk_res.status_code, 200)
        pk_data = pk_res.json()
        self.assertEqual(pk_data["status"], "success")
        self.assertGreater(pk_data["exported_count"], 0)


if __name__ == "__main__":
    unittest.main()
