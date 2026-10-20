"""
pariksha_adapter.py — Optional Bridge and Data Adapter for Pariksha (pariksha.aeigs.com).
Enables safe, decoupled bidirectional schema transformation between SyllabusTrace-CS and Pariksha.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
from ..core.models import MCQRecord


class ParikshaAdapter:
    """Decoupled data adapter for importing from and exporting to Pariksha MCQ Arena."""

    EXAM_TRACK_MAP = {
        "Operating Systems": "CS_CORE_OS",
        "Database Management Systems": "CS_CORE_DBMS",
        "Computer Networks": "CS_CORE_CN",
        "Data Structures and Algorithms": "CS_CORE_DSA",
        "Theory of Computation": "CS_CORE_TOC",
    }

    @classmethod
    def export_to_pariksha_format(cls, record: MCQRecord) -> Dict[str, Any]:
        """Converts a benchmark MCQ record into Pariksha production exam schema."""
        track = cls.EXAM_TRACK_MAP.get(record.subject, "CS_GENERAL")

        options_list = [
            {"id": "A", "label": "A", "text": record.options.get("A", "")},
            {"id": "B", "label": "B", "text": record.options.get("B", "")},
            {"id": "C", "label": "C", "text": record.options.get("C", "")},
            {"id": "D", "label": "D", "text": record.options.get("D", "")},
        ]

        citation_meta = None
        if record.source_citation:
            citation_meta = {
                "source": record.source_citation.get("citation_text") or record.source_citation.get("source_name"),
                "chapter": record.source_citation.get("chapter"),
                "section": record.source_citation.get("section"),
                "page": record.source_citation.get("page"),
                "verified_quote": record.source_citation.get("verified_excerpt"),
            }

        return {
            "pariksha_id": f"pk-{record.id}",
            "exam_series": "GATE_UGC_NET_CS",
            "track_code": track,
            "subject": record.subject,
            "syllabus_topic_id": record.syllabus_node_id,
            "cognitive_tier": record.cognitive_level,
            "question_markdown": record.stem,
            "options": options_list,
            "correct_answer": record.correct_key,
            "solution_explanation": record.explanation,
            "source_provenance": citation_meta,
            "quality_assurance": {
                "benchmark_origin": "SyllabusTrace-CS",
                "condition": record.condition,
                "composite_quality": record.scores.composite_quality if record.scores else None,
                "review_status": record.review_status,
                "exported_at": datetime.utcnow().isoformat(),
            },
        }

    @classmethod
    def import_from_pariksha_format(cls, item: Dict[str, Any]) -> MCQRecord:
        """Converts a Pariksha item into a SyllabusTrace-CS benchmark record for auditing."""
        raw_id = item.get("pariksha_id", "")
        if raw_id.startswith("pk-"):
            item_id = raw_id[3:]
        else:
            item_id = raw_id or f"imported-{datetime.utcnow().timestamp()}"

        raw_opts = item.get("options", [])
        opts_dict = {}
        if isinstance(raw_opts, list):
            for opt in raw_opts:
                k = opt.get("id") or opt.get("label")
                opts_dict[k] = opt.get("text", "")
        elif isinstance(raw_opts, dict):
            opts_dict = raw_opts

        prov = item.get("source_provenance") or {}

        citation_dict = None
        if prov:
            citation_dict = {
                "citation_text": prov.get("source", ""),
                "chapter": prov.get("chapter", ""),
                "section": prov.get("section", ""),
                "page": prov.get("page", ""),
                "verified_excerpt": prov.get("verified_quote", ""),
            }

        return MCQRecord(
            id=item_id,
            stem=item.get("question_markdown") or item.get("stem") or item.get("question", ""),
            options=opts_dict,
            correct_key=item.get("correct_answer") or item.get("correct_key") or "A",
            explanation=item.get("solution_explanation") or item.get("explanation", ""),
            condition=item.get("quality_assurance", {}).get("condition", "imported_pariksha"),
            subject=item.get("subject", "Computer Science"),
            syllabus_node_id=item.get("syllabus_topic_id"),
            cognitive_level=item.get("cognitive_tier", "Comprehension"),
            source_citation=citation_dict,
            review_status="pending",
        )

    @classmethod
    def export_batch(cls, records: List[MCQRecord], min_quality_score: float = 75.0) -> List[Dict[str, Any]]:
        """Exports approved or high-quality questions for Pariksha intake."""
        exported = []
        for r in records:
            if r.scores and r.scores.composite_quality >= min_quality_score:
                exported.append(cls.export_to_pariksha_format(r))
        return exported
