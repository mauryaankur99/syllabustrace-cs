"""
models.py — Data models for SyllabusTrace-CS using Pydantic.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime


class SyllabusTopic(BaseModel):
    id: str
    name: str
    subtopics: List[str] = Field(default_factory=list)


class SyllabusNode(BaseModel):
    id: str
    exam: str = "GATE_CS"
    subject: str
    topic: str
    subtopic: Optional[str] = None
    cognitive_level: str = "Comprehension"
    official_doc_ref: Optional[str] = None


class SyllabusSubject(BaseModel):
    id: str
    name: str
    code: str
    topics: List[SyllabusTopic] = Field(default_factory=list)


class SyllabusDocument(BaseModel):
    exam: str
    title: str
    version: str
    official_source: str
    subjects: List[SyllabusSubject] = Field(default_factory=list)


class VerifiedPassage(BaseModel):
    subtopic: str
    chapter: str
    section: Optional[str] = None
    page: str
    text: str


class SourceRecord(BaseModel):
    id: str
    title: str
    authors: List[str] = Field(default_factory=list)
    edition: str
    year: int
    publisher: str
    isbn: str
    domain: str
    canonical_status: str = "gold_standard"
    verified_passages: List[VerifiedPassage] = Field(default_factory=list)


class SourceCitation(BaseModel):
    source_id: Optional[str] = None
    citation_text: str
    authors: Optional[str] = None
    chapter: Optional[str] = None
    section: Optional[str] = None
    page: Optional[str] = None
    verified_excerpt: Optional[str] = None


class ModelMetadata(BaseModel):
    provider: str = "mock"
    model: str = "deterministic-baseline"
    temperature: float = 0.2
    prompt_version: str = "v1"


class EvaluationScores(BaseModel):
    factual_correctness: float = Field(ge=1.0, le=5.0)
    syllabus_alignment: float = Field(ge=1.0, le=5.0)
    distractor_quality: float = Field(ge=1.0, le=5.0)
    traceability: float = Field(ge=1.0, le=5.0)
    composite_quality: float = Field(ge=0.0, le=100.0)


class MCQRecord(BaseModel):
    id: str
    stem: str
    options: Dict[str, str]  # Must contain 'A', 'B', 'C', 'D'
    correct_key: str  # 'A', 'B', 'C', or 'D'
    explanation: str
    condition: str = "source_grounded"  # 'generic', 'syllabus_constrained', or 'source_grounded'
    subject: str
    syllabus_node_id: Optional[str] = None
    cognitive_level: str = "Comprehension"  # 'Recall', 'Comprehension', 'Application', 'Analysis'
    source_citation: Optional[Dict[str, Any]] = None
    model_metadata: Optional[Dict[str, Any]] = None
    review_status: str = "pending"  # 'pending', 'approved', 'rejected', 'flagged'
    flaw_flags: List[str] = Field(default_factory=list)
    scores: Optional[EvaluationScores] = None
    reviewer_notes: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class EvaluationResult(BaseModel):
    mcq_id: str
    is_valid: bool
    flaw_flags: List[str] = Field(default_factory=list)
    scores: EvaluationScores
    feedback: List[str] = Field(default_factory=list)


class ExperimentMetrics(BaseModel):
    condition: str
    sample_size: int
    factual_correctness_mean: float
    factual_correctness_std: float
    syllabus_alignment_mean: float
    syllabus_alignment_std: float
    distractor_quality_mean: float
    distractor_quality_std: float
    traceability_mean: float
    traceability_std: float
    composite_quality_mean: float
    composite_quality_std: float
    flaw_rate: float  # Percentage of items having >= 1 flaw
    flaw_counts: Dict[str, int] = Field(default_factory=dict)
