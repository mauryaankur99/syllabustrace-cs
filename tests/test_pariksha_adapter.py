"""
test_pariksha_adapter.py — Tests the external platform schema conversion and bridge.
"""

import unittest
from src.core.models import MCQRecord, EvaluationScores
from src.integrations.pariksha_adapter import ParikshaAdapter


class TestParikshaAdapter(unittest.TestCase):
    def test_pariksha_export_and_import(self):
        original = MCQRecord(
            id="mcq-test-pk-01",
            stem="What is conflict serializability in DBMS transactions?",
            options={
                "A": "Equivalence to a serial schedule via non-conflicting swap operations",
                "B": "Execution of transactions strictly one at a time",
                "C": "Buffering write operations until checkpointing",
                "D": "Eliminating all read-write lock contention"
            },
            correct_key="A",
            explanation="A schedule is conflict serializable if it can be transformed into a serial schedule by swapping non-conflicting instructions.",
            condition="source_grounded",
            subject="Database Management Systems",
            syllabus_node_id="dbms-transactions",
            cognitive_level="Comprehension",
            source_citation={
                "source_id": "src-silberschatz-dbms7",
                "citation_text": "Database System Concepts, 7th Edition",
                "chapter": "Chapter 17",
                "page": "780-792",
                "verified_excerpt": "A schedule S is conflict serializable if it is conflict equivalent to a serial schedule."
            },
            scores=EvaluationScores(factual_correctness=5.0, syllabus_alignment=5.0, distractor_quality=5.0, traceability=5.0, composite_quality=98.0)
        )

        # Export to Pariksha format
        pk_exported = ParikshaAdapter.export_to_pariksha_format(original)
        self.assertEqual(pk_exported["pariksha_id"], "pk-mcq-test-pk-01")
        self.assertEqual(pk_exported["exam_series"], "GATE_UGC_NET_CS")
        self.assertEqual(pk_exported["track_code"], "CS_CORE_DBMS")
        self.assertEqual(pk_exported["correct_answer"], "A")
        self.assertEqual(len(pk_exported["options"]), 4)

        # Import back to SyllabusTrace-CS record
        imported = ParikshaAdapter.import_from_pariksha_format(pk_exported)
        self.assertEqual(imported.id, "mcq-test-pk-01")
        self.assertEqual(imported.stem, original.stem)
        self.assertEqual(imported.correct_key, "A")
        self.assertEqual(imported.options["A"], original.options["A"])
        self.assertEqual(imported.source_citation["chapter"], "Chapter 17")


if __name__ == "__main__":
    unittest.main()
