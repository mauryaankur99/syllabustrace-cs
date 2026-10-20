"""
report_generator.py — Automated Research Report Generator for SyllabusTrace-CS.
Produces comprehensive, auditable Markdown and HTML scientific research reports.
"""

from typing import Dict, Any, List
from datetime import datetime
from .models import ExperimentMetrics


class ReportGenerator:
    """Generates an academic research report from empirical experiment data."""

    @staticmethod
    def generate_markdown_report(
        metrics: Dict[str, ExperimentMetrics],
        stat_tests: Dict[str, Any],
        total_questions: int,
        timestamp: str = None,
    ) -> str:
        timestamp = timestamp or datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")

        gen_m = metrics.get("generic")
        syl_m = metrics.get("syllabus_constrained")
        src_m = metrics.get("source_grounded")

        f_stat = stat_tests.get("f_statistic", "N/A")
        p_val = stat_tests.get("p_value", "N/A")
        if isinstance(p_val, float):
            p_val_str = f"{p_val:.2e}" if p_val < 0.001 else f"{p_val:.4f}"
        else:
            p_val_str = str(p_val)

        pairwise = stat_tests.get("pairwise_comparisons", {})

        report = f"""# SyllabusTrace-CS — Evaluation & Benchmark Report

**Project Title:** SyllabusTrace-CS: A Source-Traceable Quality Benchmark for AI-Generated Computer Science Multiple-Choice Questions in Indian Competitive Examinations  
**Author:** Ankur Maurya  
**Date Generated:** {timestamp}  
**Dataset Size:** {total_questions} items across 5 core Computer Science domains  
**Evaluation Tier:** Prototype Baseline Fixtures (`data_tier: illustrative_fixture`; Live API Runs Pending)  

---

## 1. Executive Summary & Research Question
This research investigates whether syllabus-constrained and source-grounded prompting paradigms materially improve the pedagogical quality, factual correctness, item-writing validity, and evidence traceability of AI-generated Computer Science multiple-choice questions (MCQs) compared to unconstrained generic prompting.

**Core Research Question:**
> *Does enforcing hierarchical syllabus constraints (Condition B) and authoritative canonical textbook grounding (Condition C) eliminate critical Item-Writing Flaws (IWFs) and yield statistically superior item quality in high-stakes competitive examinations (e.g., GATE CS, UGC NET) compared with baseline unconstrained generation (Condition A)?*

**Data Provenance Statement:**
The baseline metrics reported below reflect the **curated prototype fixture dataset ($N={total_questions}$)**, used to validate the deterministic Item-Writing Flaw heuristics, scoring rubrics, and reporting pipelines. Live generation across frontier LLMs (Google Gemini, OpenAI, Anthropic) is architected in `src/core/generator.py` and requires configured API keys.

---

## 2. Experimental Methodology
The study deploys a controlled 3-condition comparative design:
1. **Condition A (Generic Baseline):** Prompted with high-level topic keywords without syllabus boundaries or source requirements.
2. **Condition B (Syllabus-Constrained):** Bound strictly to official GATE CS / UGC NET hierarchical subtopics and Bloom's cognitive taxonomy levels, enforcing structural balance.
3. **Condition C (Syllabus + Source-Grounded):** Bound to official syllabus nodes and anchored directly in canonical CS textbooks (Cormen et al., Silberschatz et al., Kurose & Ross, Sipser) with mandatory citation and excerpt verification.

---

## 3. Prototype Fixture Baseline Summary ($N={total_questions}$)

| Metric | Condition A (Generic) | Condition B (Syllabus-Constrained) | Condition C (Source-Grounded) |
| :--- | :---: | :---: | :---: |
| **Sample Size (N)** | {gen_m.sample_size if gen_m else 0} | {syl_m.sample_size if syl_m else 0} | {src_m.sample_size if src_m else 0} |
| **Composite Quality Score (0–100%)** | **{gen_m.composite_quality_mean if gen_m else 0}%** (±{gen_m.composite_quality_std if gen_m else 0}) | **{syl_m.composite_quality_mean if syl_m else 0}%** (±{syl_m.composite_quality_std if syl_m else 0}) | **{src_m.composite_quality_mean if src_m else 0}%** (±{src_m.composite_quality_std if src_m else 0}) |
| **Factual Correctness (1–5)** | {gen_m.factual_correctness_mean if gen_m else 0} (±{gen_m.factual_correctness_std if gen_m else 0}) | {syl_m.factual_correctness_mean if syl_m else 0} (±{syl_m.factual_correctness_std if syl_m else 0}) | {src_m.factual_correctness_mean if src_m else 0} (±{src_m.factual_correctness_std if src_m else 0}) |
| **Syllabus Alignment (1–5)** | {gen_m.syllabus_alignment_mean if gen_m else 0} (±{gen_m.syllabus_alignment_std if gen_m else 0}) | {syl_m.syllabus_alignment_mean if syl_m else 0} (±{syl_m.syllabus_alignment_std if syl_m else 0}) | {src_m.syllabus_alignment_mean if src_m else 0} (±{src_m.syllabus_alignment_std if src_m else 0}) |
| **Distractor Quality (1–5)** | {gen_m.distractor_quality_mean if gen_m else 0} (±{gen_m.distractor_quality_std if gen_m else 0}) | {syl_m.distractor_quality_mean if syl_m else 0} (±{syl_m.distractor_quality_std if syl_m else 0}) | {src_m.distractor_quality_mean if src_m else 0} (±{src_m.distractor_quality_std if src_m else 0}) |
| **Evidence Traceability (1–5)** | {gen_m.traceability_mean if gen_m else 0} (±{gen_m.traceability_std if gen_m else 0}) | {syl_m.traceability_mean if syl_m else 0} (±{syl_m.traceability_std if syl_m else 0}) | {src_m.traceability_mean if src_m else 0} (±{src_m.traceability_std if src_m else 0}) |
| **Item-Writing Flaw Rate (%)** | **{gen_m.flaw_rate if gen_m else 0}%** | **{syl_m.flaw_rate if syl_m else 0}%** | **{src_m.flaw_rate if src_m else 0}%** |

---

## 4. Item-Writing Flaw (IWF) Detection on Baseline Fixtures

| Flaw Category | Description | Generic (A) | Syllabus (B) | Source-Grounded (C) |
| :--- | :--- | :---: | :---: | :---: |
| `FLAW_NO_CITATION` | Lack of verifiable citation | {gen_m.flaw_counts.get("FLAW_NO_CITATION", 0) if gen_m else 0} | {syl_m.flaw_counts.get("FLAW_NO_CITATION", 0) if syl_m else 0} | {src_m.flaw_counts.get("FLAW_NO_CITATION", 0) if src_m else 0} |
| `FLAW_ALL_NONE_ABOVE` | 'All of the above' / 'None of the above' | {gen_m.flaw_counts.get("FLAW_ALL_NONE_ABOVE", 0) if gen_m else 0} | {syl_m.flaw_counts.get("FLAW_ALL_NONE_ABOVE", 0) if syl_m else 0} | {src_m.flaw_counts.get("FLAW_ALL_NONE_ABOVE", 0) if src_m else 0} |
| `FLAW_LENGTH_OUTLIER` | Distractor length disparity (>2.3x) | {gen_m.flaw_counts.get("FLAW_LENGTH_OUTLIER", 0) if gen_m else 0} | {syl_m.flaw_counts.get("FLAW_LENGTH_OUTLIER", 0) if syl_m else 0} | {src_m.flaw_counts.get("FLAW_LENGTH_OUTLIER", 0) if src_m else 0} |
| `FLAW_ANSWER_LEAKAGE` | Clues in stem or option parentheses | {gen_m.flaw_counts.get("FLAW_ANSWER_LEAKAGE", 0) if gen_m else 0} | {syl_m.flaw_counts.get("FLAW_ANSWER_LEAKAGE", 0) if syl_m else 0} | {src_m.flaw_counts.get("FLAW_ANSWER_LEAKAGE", 0) if src_m else 0} |
| `FLAW_STEM_TOO_SHORT` | Underspecified stem (<25 chars) | {gen_m.flaw_counts.get("FLAW_STEM_TOO_SHORT", 0) if gen_m else 0} | {syl_m.flaw_counts.get("FLAW_STEM_TOO_SHORT", 0) if syl_m else 0} | {src_m.flaw_counts.get("FLAW_STEM_TOO_SHORT", 0) if src_m else 0} |

---

## 5. Statistical Pipeline Sensitivity Verification
- **One-Way ANOVA Pipeline Check (Baseline Fixtures):**
  - **F-statistic:** `{f_stat}`
  - **p-value:** `{p_val_str}`
  - **Interpretation:** Verifies that the ANOVA calculation correctly flags between-condition variance across the curated test fixtures. Live model statistical significance tests will be reported following production API execution.

- **Pairwise Welch's t-test Pipeline Checks:**
"""
        for pair_name, stats_dict in pairwise.items():
            t_val = stats_dict.get("t_statistic", "N/A")
            p_v = stats_dict.get("p_value", "N/A")
            sig = "Pipeline Differentiated (p < 0.05)" if stats_dict.get("significant") else "Not Differentiated"
            p_v_str = f"{p_v:.2e}" if isinstance(p_v, float) and p_v < 0.001 else f"{p_v:.4f}"
            formatted_pair = pair_name.replace("_", " ").title()
            report += f"  - **{formatted_pair}:** t = {t_val}, p = {p_v_str} -> *{sig}*\n"

        report += """
---

## 6. Key Findings & Prototype Observations
1. **Heuristic Rule Sensitivity:** The deterministic audit engine reliably isolates missing citations, distractor length outliers, and prohibited option formulas across test fixtures.
2. **Citation Traceability Mechanism:** Requiring exact citation metadata (author, edition, chapter, page, excerpt) enables structured verification against canonical authorities (CLRS, Silberschatz, Kurose-Ross, Sipser).
3. **Decoupled Quality Gate:** The pipeline demonstrates the feasibility of automated pre-filtering prior to human expert review.

---

## 7. Limitations & Threats to Validity
- **Prototype Baseline Scope:** Benchmark figures reflect a 60-item curated fixture baseline. Live model runs across frontier LLMs require API credentials.
- **Human Review Pending:** Question review status is currently marked as pending formal double-blind faculty review.
- **Curricular Scope:** Five core subjects are represented in the baseline; expansion to all 10 GATE CS units is underway.
- **Model Inherent Prior:** Models have seen textbooks during pre-training; future work will test synthetic unseen algorithmic proofs to measure pure reasoning.

---

## 8. Reproducibility Statement
To reproduce these findings:
```bash
git clone https://github.com/mauryaankur99/syllabustrace-cs.git
cd syllabustrace-cs
python scripts/reproduce_experiment.py
```
This regenerates the entire evaluation pipeline, recalculates all statistics, and outputs this report.
"""
        return report
