"""
question_service.py — Dataset management, searching, filtering, and CRUD operations for MCQs.
"""

import json
import csv
import io
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
from ..core.models import MCQRecord, EvaluationScores
from ..core.evaluator import Evaluator


class QuestionService:
    def __init__(self, data_file: Optional[Path] = None, evaluator: Optional[Evaluator] = None):
        if data_file is None:
            self.data_file = Path(__file__).resolve().parent.parent.parent / "data" / "datasets" / "benchmark_questions.json"
        else:
            self.data_file = data_file
        self.evaluator = evaluator or Evaluator()
        self.questions: List[MCQRecord] = []
        self._load()

    def _load(self):
        if self.data_file.exists():
            with open(self.data_file, "r", encoding="utf-8") as f:
                raw = json.load(f)
                self.questions = [MCQRecord(**item) for item in raw]
                # Automatically run initial evaluation if scores are missing
                for q in self.questions:
                    if not q.scores:
                        res = self.evaluator.evaluate(q)
                        q.flaw_flags = res.flaw_flags
                        q.scores = res.scores
        else:
            self.questions = []

    def save(self):
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([q.model_dump() for q in self.questions], f, indent=2)

    def get_all(
        self,
        condition: Optional[str] = None,
        subject: Optional[str] = None,
        review_status: Optional[str] = None,
        flaw_flag: Optional[str] = None,
        search_query: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> Dict[str, Any]:
        filtered = self.questions

        if condition:
            filtered = [q for q in filtered if q.condition.lower() == condition.lower()]

        if subject:
            filtered = [q for q in filtered if q.subject.lower() == subject.lower()]

        if review_status:
            filtered = [q for q in filtered if q.review_status.lower() == review_status.lower()]

        if flaw_flag:
            filtered = [q for q in filtered if flaw_flag in q.flaw_flags]

        if search_query:
            sq = search_query.lower()
            filtered = [
                q for q in filtered
                if sq in q.stem.lower() or
                   sq in q.explanation.lower() or
                   any(sq in str(v).lower() for v in q.options.values())
            ]

        total_count = len(filtered)
        paginated = filtered[offset : offset + limit]

        return {
            "total": total_count,
            "limit": limit,
            "offset": offset,
            "items": [q.model_dump() for q in paginated],
        }

    def get_by_id(self, item_id: str) -> Optional[MCQRecord]:
        for q in self.questions:
            if q.id == item_id:
                return q
        return None

    def create(self, record: MCQRecord) -> MCQRecord:
        # Run evaluator on record
        eval_res = self.evaluator.evaluate(record)
        record.flaw_flags = eval_res.flaw_flags
        record.scores = eval_res.scores
        record.created_at = datetime.utcnow().isoformat()
        record.updated_at = datetime.utcnow().isoformat()
        self.questions.insert(0, record)
        self.save()
        return record

    def update(self, item_id: str, updates: Dict[str, Any]) -> Optional[MCQRecord]:
        q = self.get_by_id(item_id)
        if not q:
            return None

        for k, v in updates.items():
            if hasattr(q, k) and k not in {"id", "created_at"}:
                setattr(q, k, v)

        # Re-evaluate
        eval_res = self.evaluator.evaluate(q)
        q.flaw_flags = eval_res.flaw_flags
        q.scores = eval_res.scores
        q.updated_at = datetime.utcnow().isoformat()
        self.save()
        return q

    def delete(self, item_id: str) -> bool:
        before = len(self.questions)
        self.questions = [q for q in self.questions if q.id != item_id]
        if len(self.questions) < before:
            self.save()
            return True
        return False

    def update_review_status(self, item_id: str, status: str, notes: Optional[str] = None) -> Optional[MCQRecord]:
        q = self.get_by_id(item_id)
        if not q:
            return None
        q.review_status = status.lower()
        if notes is not None:
            q.reviewer_notes = notes
        q.updated_at = datetime.utcnow().isoformat()
        self.save()
        return q

    def export_csv(self) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "ID", "Condition", "Subject", "Syllabus_Node", "Stem",
            "Option_A", "Option_B", "Option_C", "Option_D",
            "Correct_Key", "Explanation", "Cognitive_Level",
            "Review_Status", "Flaw_Flags", "Composite_Quality_Score"
        ])
        for q in self.questions:
            writer.writerow([
                q.id,
                q.condition,
                q.subject,
                q.syllabus_node_id or "",
                q.stem,
                q.options.get("A", ""),
                q.options.get("B", ""),
                q.options.get("C", ""),
                q.options.get("D", ""),
                q.correct_key,
                q.explanation,
                q.cognitive_level,
                q.review_status,
                ";".join(q.flaw_flags),
                q.scores.composite_quality if q.scores else "",
            ])
        return output.getvalue()
