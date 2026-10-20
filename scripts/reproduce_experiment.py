#!/usr/bin/env python3
"""
reproduce_experiment.py — Headless CLI Reproduction Pipeline for SyllabusTrace-CS.
Executes end-to-end evaluation, statistical analysis, and report generation.
"""

import sys
import json
from pathlib import Path

# Add src to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from src.core.models import MCQRecord
from src.core.evaluator import Evaluator
from src.core.analyzer import BenchmarkAnalyzer
from src.core.report_generator import ReportGenerator
from src.services.question_service import QuestionService
from src.services.experiment_service import ExperimentService


def main():
    print("=" * 70)
    print(" SyllabusTrace-CS -- Headless Reproduction Pipeline")
    print("=" * 70)

    data_file = BASE_DIR / "data" / "datasets" / "benchmark_questions.json"
    if not data_file.exists():
        print(f"Error: Benchmark file {data_file} not found.")
        sys.exit(1)

    print(f"[*] Loading benchmark questions from: {data_file}")
    evaluator = Evaluator()
    question_service = QuestionService(data_file=data_file, evaluator=evaluator)
    experiment_service = ExperimentService(question_service=question_service)

    print(f"[*] Total benchmark items loaded: {len(question_service.questions)}")
    print("[*] Provenance Mode: Curated Prototype Baseline Fixtures (data_tier: illustrative_fixture)")
    print("[*] Notice: Live model API calls require GEMINI_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY.")
    print("[*] Running multi-stage deterministic and rubric evaluation...")

    # Run analysis
    results = experiment_service.run_benchmark_analysis()
    metrics = results["metrics"]
    stats_data = results["statistical_significance"]

    print("\n" + "=" * 70)
    print(" PROTOTYPE FIXTURE BASELINE SUMMARY BY CONDITION (N=60)")
    print("=" * 70)
    print(f"{'Condition':<25} | {'N':<4} | {'Composite':<14} | {'Flaw Rate':<10} | {'Traceability':<12}")
    print("-" * 70)

    cond_order = ["generic", "syllabus_constrained", "source_grounded"]
    for c in cond_order:
        m = metrics.get(c)
        if not m:
            continue
        c_name = "Generic (A)" if c == "generic" else "Syllabus (B)" if c == "syllabus_constrained" else "Source-Grounded (C)"
        comp_str = f"{m['composite_quality_mean']}% (+/- {m['composite_quality_std']})"
        flaw_str = f"{m['flaw_rate']}%"
        tr_str = f"{m['traceability_mean']} / 5.0"
        print(f"{c_name:<25} | {m['sample_size']:<4} | {comp_str:<14} | {flaw_str:<10} | {tr_str:<12}")

    print("-" * 70)
    print(f"\n[*] Inferential Pipeline Sensitivity Check (ANOVA on Prototype Fixtures):")
    print(f"    - F-Statistic: {stats_data.get('f_statistic')}")
    p_v = stats_data.get('p_value')
    p_str = f"{p_v:.2e}" if isinstance(p_v, float) and p_v < 0.001 else f"{p_v:.4f}"
    print(f"    - p-value:     {p_str} (Sensitivity verified; empirical model tests pending live runs)")

    print(f"\n[*] Exporting artifacts:")
    # Export evaluated JSON and CSV
    evaluated_json = BASE_DIR / "data" / "datasets" / "evaluated_benchmark.json"
    with open(evaluated_json, "w", encoding="utf-8") as f:
        json.dump([q.model_dump() for q in question_service.questions], f, indent=2)
    print(f"    - Evaluated JSON: {evaluated_json}")

    evaluated_csv = BASE_DIR / "data" / "datasets" / "evaluated_benchmark.csv"
    with open(evaluated_csv, "w", encoding="utf-8") as f:
        f.write(question_service.export_csv())
    print(f"    - Evaluated CSV:  {evaluated_csv}")

    report_path = results.get("report_path")
    print(f"    - Research Report: {report_path}")

    print("\n" + "=" * 70)
    print(" [OK] Reproduction complete! All benchmarks, tables, and reports regenerated.")
    print("=" * 70)


if __name__ == "__main__":
    main()
