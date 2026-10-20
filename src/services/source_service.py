"""
source_service.py — Service for managing canonical academic literature and passages.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from ..core.models import SourceRecord


class SourceService:
    def __init__(self, sources_file: Optional[Path] = None):
        if sources_file is None:
            self.sources_file = Path(__file__).resolve().parent.parent.parent / "data" / "sources" / "canonical_cs_sources.json"
        else:
            self.sources_file = sources_file
        self.sources: List[SourceRecord] = []
        self._load()

    def _load(self):
        if self.sources_file.exists():
            with open(self.sources_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.sources = [SourceRecord(**item) for item in data]
        else:
            self.sources = []

    def get_all_sources(self) -> List[Dict[str, Any]]:
        return [s.model_dump() for s in self.sources]

    def get_source_by_id(self, source_id: str) -> Optional[Dict[str, Any]]:
        for s in self.sources:
            if s.id == source_id:
                return s.model_dump()
        return None

    def search_sources(self, query: str) -> List[Dict[str, Any]]:
        q = query.lower()
        matched = []
        for s in self.sources:
            if (
                q in s.title.lower() or
                q in s.domain.lower() or
                any(q in a.lower() for a in s.authors) or
                any(q in p.subtopic.lower() or q in p.text.lower() for p in s.verified_passages)
            ):
                matched.append(s.model_dump())
        return matched

    def get_passages_by_subtopic(self, subtopic_name: str) -> List[Dict[str, Any]]:
        q = subtopic_name.lower()
        results = []
        for s in self.sources:
            for p in s.verified_passages:
                if q in p.subtopic.lower() or p.subtopic.lower() in q:
                    results.append({
                        "source_id": s.id,
                        "source_title": s.title,
                        "authors": s.authors,
                        "edition": s.edition,
                        "passage": p.model_dump(),
                    })
        return results
