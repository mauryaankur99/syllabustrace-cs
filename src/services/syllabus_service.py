"""
syllabus_service.py — Service for loading, navigating, and calculating coverage over exam syllabi.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from ..core.models import SyllabusDocument


class SyllabusService:
    def __init__(self, syllabus_file: Optional[Path] = None):
        if syllabus_file is None:
            self.syllabus_file = Path(__file__).resolve().parent.parent.parent / "data" / "syllabi" / "gate_cs_syllabus.json"
        else:
            self.syllabus_file = syllabus_file
        self.syllabus: Optional[SyllabusDocument] = None
        self._load()

    def _load(self):
        if self.syllabus_file.exists():
            with open(self.syllabus_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.syllabus = SyllabusDocument(**data)
        else:
            self.syllabus = None

    def get_syllabus(self) -> Optional[Dict[str, Any]]:
        return self.syllabus.model_dump() if self.syllabus else None

    def get_subjects(self) -> List[Dict[str, Any]]:
        if not self.syllabus:
            return []
        return [s.model_dump() for s in self.syllabus.subjects]

    def get_all_topics(self) -> List[Dict[str, Any]]:
        topics = []
        if not self.syllabus:
            return topics
        for s in self.syllabus.subjects:
            for t in s.topics:
                topics.append({
                    "subject_name": s.name,
                    "subject_code": s.code,
                    "topic_id": t.id,
                    "topic_name": t.name,
                    "subtopics": t.subtopics,
                })
        return topics

    def calculate_coverage(self, question_syllabus_ids: List[str]) -> Dict[str, Any]:
        """Calculates syllabus coverage heatmap and gap analysis."""
        coverage = {}
        total_topics = 0
        covered_topics = 0

        counts: Dict[str, int] = {}
        for nid in question_syllabus_ids:
            if nid:
                counts[nid] = counts.get(nid, 0) + 1

        subject_stats = []
        for s in self.syllabus.subjects:
            subj_total = len(s.topics)
            subj_covered = 0
            topic_breakdowns = []
            for t in s.topics:
                total_topics += 1
                q_count = counts.get(t.id, 0)
                if q_count > 0:
                    covered_topics += 1
                    subj_covered += 1
                topic_breakdowns.append({
                    "topic_id": t.id,
                    "topic_name": t.name,
                    "question_count": q_count,
                    "status": "covered" if q_count > 0 else "gap",
                })
            subject_stats.append({
                "subject_name": s.name,
                "subject_code": s.code,
                "total_topics": subj_total,
                "covered_topics": subj_covered,
                "coverage_pct": round((subj_covered / subj_total * 100.0) if subj_total else 0, 1),
                "topics": topic_breakdowns,
            })

        overall_pct = round((covered_topics / total_topics * 100.0) if total_topics else 0, 1)

        return {
            "total_topics": total_topics,
            "covered_topics": covered_topics,
            "overall_coverage_pct": overall_pct,
            "subjects": subject_stats,
        }
