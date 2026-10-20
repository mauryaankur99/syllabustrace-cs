"""
experiment_service.py — Service for running comparative experiments and generating statistical reports.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from .question_service import QuestionService
from ..core.analyzer import BenchmarkAnalyzer
from ..core.report_generator import ReportGenerator


class ExperimentService:
    def __init__(
        self,
        question_service: QuestionService,
        experiments_dir: Optional[Path] = None,
        reports_dir: Optional[Path] = None,
    ):
        self.question_service = question_service
        base = Path(__file__).resolve().parent.parent.parent / "data"
        self.experiments_dir = experiments_dir or (base / "experiments")
        self.reports_dir = reports_dir or (base / "reports")
        self.experiments_dir.mkdir(parents=True, exist_ok=True)
        self.reports_dir.mkdir(parents=True, exist_ok=True)

    def run_benchmark_analysis(self) -> Dict[str, Any]:
        """Runs statistical analysis over the active question set."""
        questions = self.question_service.questions
        metrics = BenchmarkAnalyzer.compute_metrics(questions)
        stat_tests = BenchmarkAnalyzer.compute_statistical_tests(questions)

        metrics_dict = {k: v.model_dump() for k, v in metrics.items()}

        result_payload = {
            "experiment_id": "exp-pilot-gate-2026-v1",
            "name": "SyllabusTrace-CS Pilot Benchmark Comparison",
            "total_questions": len(questions),
            "timestamp": datetime.utcnow().isoformat(),
            "metrics": metrics_dict,
            "statistical_significance": stat_tests,
        }

        # Save to experiment run file
        exp_file = self.experiments_dir / "pilot_comparison.json"
        with open(exp_file, "w", encoding="utf-8") as f:
            json.dump(result_payload, f, indent=2)

        # Generate markdown report
        report_md = ReportGenerator.generate_markdown_report(
            metrics=metrics,
            stat_tests=stat_tests,
            total_questions=len(questions),
        )
        report_file = self.reports_dir / "RESEARCH_REPORT.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report_md)

        result_payload["report_path"] = str(report_file)
        result_payload["report_markdown"] = report_md
        return result_payload

    def get_latest_results(self) -> Dict[str, Any]:
        exp_file = self.experiments_dir / "pilot_comparison.json"
        if exp_file.exists():
            with open(exp_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return self.run_benchmark_analysis()
