"""
main.py — FastAPI Application for the SyllabusTrace-CS Research Workbench.
Exposes REST endpoints for syllabi, sources, MCQs, AI generation, evaluation, and experiments.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse

from ..core.models import MCQRecord, EvaluationResult
from ..core.evaluator import Evaluator
from ..core.generator import MCQGenerator, ProviderMissingCredentialsError, ProviderAPIError
from ..services.syllabus_service import SyllabusService
from ..services.source_service import SourceService
from ..services.question_service import QuestionService
from ..services.experiment_service import ExperimentService
from ..integrations.pariksha_adapter import ParikshaAdapter

app = FastAPI(
    title="SyllabusTrace-CS API",
    description="A Source-Traceable Quality Benchmark Workbench for AI-Generated Computer Science MCQs",
    version="1.0.0",
)

# Enable CORS for local dev and frontend integrations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Services
evaluator = Evaluator()
generator = MCQGenerator()
syllabus_service = SyllabusService()
source_service = SourceService()
question_service = QuestionService(evaluator=evaluator)
experiment_service = ExperimentService(question_service=question_service)


# -------------------------------------------------------------
# 1. Project Overview & Dashboard Telemetry
# -------------------------------------------------------------
@app.get("/api/overview")
def get_overview():
    questions = question_service.questions
    total_q = len(questions)

    by_condition = {"generic": 0, "syllabus_constrained": 0, "source_grounded": 0}
    by_subject = {}
    by_status = {"pending": 0, "approved": 0, "rejected": 0, "flagged": 0}

    for q in questions:
        c = q.condition.lower()
        if c in by_condition:
            by_condition[c] += 1
        s = q.subject
        by_subject[s] = by_subject.get(s, 0) + 1
        st = q.review_status.lower()
        if st in by_status:
            by_status[st] += 1

    latest_exp = experiment_service.get_latest_results()

    return {
        "project": "SyllabusTrace-CS",
        "version": "1.0.0",
        "research_question": "Can syllabus-constrained and source-grounded prompting improve factual correctness, syllabus alignment, answer validity, and evidence traceability of AI-generated Computer Science MCQs?",
        "total_questions": total_q,
        "counts_by_condition": by_condition,
        "counts_by_subject": by_subject,
        "counts_by_status": by_status,
        "data_status": "illustrative_fixtures_baseline",
        "active_provider": generator.provider,
        "is_live_provider_active": not (generator.provider in {"offline_fixture", "mock"}),
        "status_description": "Current 60 items represent illustrative test fixtures for pipeline verification. Live experimental model trials remain pending valid provider credentials.",
        "latest_experiment": latest_exp.get("metrics"),
        "active_exam_tracks": ["GATE_CS", "UGC_NET_CS", "GPSC_CS"],
        "pariksha_bridge_active": True,
    }


# -------------------------------------------------------------
# 2. Syllabus Explorer & Coverage Heatmaps
# -------------------------------------------------------------
@app.get("/api/syllabi")
def get_syllabus():
    syl = syllabus_service.get_syllabus()
    if not syl:
        raise HTTPException(status_code=404, detail="Syllabus not found.")
    return syl


@app.get("/api/syllabi/coverage")
def get_syllabus_coverage():
    all_node_ids = [q.syllabus_node_id for q in question_service.questions if q.syllabus_node_id]
    return syllabus_service.calculate_coverage(all_node_ids)


# -------------------------------------------------------------
# 3. Canonical Sources & Literature Registry
# -------------------------------------------------------------
@app.get("/api/sources")
def get_sources(search: Optional[str] = None):
    if search:
        return source_service.search_sources(search)
    return source_service.get_all_sources()


@app.get("/api/sources/{source_id}")
def get_source_detail(source_id: str):
    src = source_service.get_source_by_id(source_id)
    if not src:
        raise HTTPException(status_code=404, detail="Source record not found.")
    return src


# -------------------------------------------------------------
# 4. MCQ Dataset Management (CRUD & Review)
# -------------------------------------------------------------
@app.get("/api/questions")
def get_questions(
    condition: Optional[str] = None,
    subject: Optional[str] = None,
    review_status: Optional[str] = None,
    flaw_flag: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 100,
    offset: int = 0,
):
    return question_service.get_all(
        condition=condition,
        subject=subject,
        review_status=review_status,
        flaw_flag=flaw_flag,
        search_query=search,
        limit=limit,
        offset=offset,
    )


@app.get("/api/questions/{question_id}")
def get_question_by_id(question_id: str):
    q = question_service.get_by_id(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found.")
    return q.model_dump()


@app.post("/api/questions")
def create_question(mcq: MCQRecord):
    created = question_service.create(mcq)
    return created.model_dump()


@app.put("/api/questions/{question_id}")
def update_question(question_id: str, updates: Dict[str, Any]):
    updated = question_service.update(question_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Question not found.")
    return updated.model_dump()


@app.delete("/api/questions/{question_id}")
def delete_question(question_id: str):
    success = question_service.delete(question_id)
    if not success:
        raise HTTPException(status_code=404, detail="Question not found.")
    return {"deleted": True, "id": question_id}


@app.post("/api/questions/{question_id}/review")
def review_question(question_id: str, payload: Dict[str, Any]):
    status = payload.get("status", "approved")
    notes = payload.get("notes")
    res = question_service.update_review_status(question_id, status, notes)
    if not res:
        raise HTTPException(status_code=404, detail="Question not found.")
    return res.model_dump()


# -------------------------------------------------------------
# 5. Question Generation & Evaluation Workflows
# -------------------------------------------------------------
@app.post("/api/generate")
def generate_question(payload: Dict[str, Any]):
    condition = payload.get("condition", "source_grounded")
    subject = payload.get("subject", "Operating Systems")
    topic = payload.get("topic", "CPU Scheduling")
    subtopic = payload.get("subtopic", "Round Robin")
    cognitive_level = payload.get("cognitive_level", "Comprehension")
    source_id = payload.get("source_id")

    source_data = None
    if source_id:
        src = source_service.get_source_by_id(source_id)
        if src:
            source_data = {
                "source_id": src["id"],
                "title": src["title"],
                "authors": src["authors"],
                "chapter": src["verified_passages"][0]["chapter"] if src.get("verified_passages") else "Chapter 1",
                "section": src["verified_passages"][0]["section"] if src.get("verified_passages") else "1.1",
                "page": src["verified_passages"][0]["page"] if src.get("verified_passages") else "10-20",
                "verified_excerpt": src["verified_passages"][0]["text"] if src.get("verified_passages") else "Canonical text definition.",
            }

    try:
        generated_record = generator.generate(
            condition=condition,
            subject=subject,
            topic=topic,
            subtopic=subtopic,
            cognitive_level=cognitive_level,
            source_data=source_data,
        )
        # Save to questions dataset
        question_service.create(generated_record)
        return generated_record.model_dump()
    except ProviderMissingCredentialsError as e:
        raise HTTPException(
            status_code=422,
            detail={"error": "missing_credentials", "message": str(e)}
        )
    except ProviderAPIError as e:
        raise HTTPException(
            status_code=502,
            detail={"error": "provider_api_error", "message": str(e)}
        )


@app.post("/api/evaluate")
def evaluate_arbitrary_question(mcq: MCQRecord):
    result = evaluator.evaluate(mcq)
    return result.model_dump()


# -------------------------------------------------------------
# 6. Experiments & Statistical Comparisons
# -------------------------------------------------------------
@app.get("/api/experiments/results")
def get_experiment_results():
    return experiment_service.get_latest_results()


@app.get("/api/experiments/pilot")
def get_pilot_study_results():
    pilot_metrics_file = Path(__file__).resolve().parent.parent.parent / "data" / "experiments" / "pilot_study_metrics.json"
    if pilot_metrics_file.exists():
        with open(pilot_metrics_file, "r", encoding="utf-8") as f:
            return json.load(f)
    raise HTTPException(status_code=404, detail="Pilot study not executed yet. Run scripts/run_pilot_study.py.")


@app.post("/api/experiments/run")
def trigger_benchmark_run():
    return experiment_service.run_benchmark_analysis()


# -------------------------------------------------------------
# 7. Research Report & Export Capabilities
# -------------------------------------------------------------
@app.get("/api/reports/markdown")
def get_report_markdown():
    res = experiment_service.get_latest_results()
    return PlainTextResponse(res.get("report_markdown", ""))


@app.get("/api/export/csv")
def export_dataset_csv():
    csv_str = question_service.export_csv()
    return Response(
        content=csv_str,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=syllabustrace_benchmark.csv"},
    )


@app.get("/api/export/json")
def export_dataset_json():
    return [q.model_dump() for q in question_service.questions]


# -------------------------------------------------------------
# 8. Pariksha Platform Integration Adapter
# -------------------------------------------------------------
@app.get("/api/pariksha/export")
def export_for_pariksha(min_score: float = 75.0):
    exported = ParikshaAdapter.export_batch(question_service.questions, min_quality_score=min_score)
    return {
        "status": "success",
        "exported_count": len(exported),
        "target_platform": "Pariksha MCQ Arena (pariksha.aeigs.com)",
        "items": exported,
    }


@app.post("/api/pariksha/import")
def import_from_pariksha(payload: List[Dict[str, Any]]):
    imported_records = []
    for item in payload:
        rec = ParikshaAdapter.import_from_pariksha_format(item)
        saved = question_service.create(rec)
        imported_records.append(saved.model_dump())
    return {
        "status": "success",
        "imported_count": len(imported_records),
        "items": imported_records,
    }


# -------------------------------------------------------------
# 9. Interactive Web Workbench UI (Embedded Standalone SPA)
# -------------------------------------------------------------
# Load interactive HTML UI directly from static directory or inline
STATIC_DIR = Path(__file__).resolve().parent.parent / "ui"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
def serve_ui():
    ui_index = STATIC_DIR / "index.html"
    if ui_index.exists():
        with open(ui_index, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse("<h2>SyllabusTrace-CS Research Workbench API is Running.</h2><p>Visit <a href='/docs'>/docs</a> for API documentation.</p>")
