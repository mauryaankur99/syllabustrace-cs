# SyllabusTrace-CS — Evaluation & Benchmark Report

**Project Title:** SyllabusTrace-CS: A Source-Traceable Quality Benchmark for AI-Generated Computer Science Multiple-Choice Questions in Indian Competitive Examinations  
**Author:** Ankur Maurya  
**Date Generated:** 2026-10-20 10:24:36 UTC  
**Dataset Size:** 60 items across 5 core Computer Science domains  
**Evaluation Tier:** Prototype Baseline Fixtures (`data_tier: illustrative_fixture`; Live API Runs Pending)  

---

## 1. Executive Summary & Research Question
This research investigates whether syllabus-constrained and source-grounded prompting paradigms materially improve the pedagogical quality, factual correctness, item-writing validity, and evidence traceability of AI-generated Computer Science multiple-choice questions (MCQs) compared to unconstrained generic prompting.

**Core Research Question:**
> *Does enforcing hierarchical syllabus constraints (Condition B) and authoritative canonical textbook grounding (Condition C) eliminate critical Item-Writing Flaws (IWFs) and yield statistically superior item quality in high-stakes competitive examinations (e.g., GATE CS, UGC NET) compared with baseline unconstrained generation (Condition A)?*

**Data Provenance Statement:**
The baseline metrics reported below reflect the **curated prototype fixture dataset ($N=60$)**, used to validate the deterministic Item-Writing Flaw heuristics, scoring rubrics, and reporting pipelines. Live generation across frontier LLMs (Google Gemini, OpenAI, Anthropic) is architected in `src/core/generator.py` and requires configured API keys.

---

## 2. Experimental Methodology
The study deploys a controlled 3-condition comparative design:
1. **Condition A (Generic Baseline):** Prompted with high-level topic keywords without syllabus boundaries or source requirements.
2. **Condition B (Syllabus-Constrained):** Bound strictly to official GATE CS / UGC NET hierarchical subtopics and Bloom's cognitive taxonomy levels, enforcing structural balance.
3. **Condition C (Syllabus + Source-Grounded):** Bound to official syllabus nodes and anchored directly in canonical CS textbooks (Cormen et al., Silberschatz et al., Kurose & Ross, Sipser) with mandatory citation and excerpt verification.

---

## 3. Prototype Fixture Baseline Summary ($N=60$)

| Metric | Condition A (Generic) | Condition B (Syllabus-Constrained) | Condition C (Source-Grounded) |
| :--- | :---: | :---: | :---: |
| **Sample Size (N)** | 20 | 20 | 20 |
| **Composite Quality Score (0–100%)** | **65.25%** (±8.51) | **92.6%** (±0.0) | **98.55%** (±3.55) |
| **Factual Correctness (1–5)** | 4.2 (±0.0) | 4.7 (±0.0) | 5.0 (±0.0) |
| **Syllabus Alignment (1–5)** | 5.0 (±0.0) | 5.0 (±0.0) | 5.0 (±0.0) |
| **Distractor Quality (1–5)** | 3.42 (±1.08) | 5.0 (±0.0) | 4.82 (±0.45) |
| **Evidence Traceability (1–5)** | 1.2 (±0.0) | 3.6 (±0.0) | 5.0 (±0.0) |
| **Item-Writing Flaw Rate (%)** | **100.0%** | **0.0%** | **15.0%** |

---

## 4. Item-Writing Flaw (IWF) Detection on Baseline Fixtures

| Flaw Category | Description | Generic (A) | Syllabus (B) | Source-Grounded (C) |
| :--- | :--- | :---: | :---: | :---: |
| `FLAW_NO_CITATION` | Lack of verifiable citation | 20 | 0 | 0 |
| `FLAW_ALL_NONE_ABOVE` | 'All of the above' / 'None of the above' | 6 | 0 | 0 |
| `FLAW_LENGTH_OUTLIER` | Distractor length disparity (>2.3x) | 8 | 0 | 1 |
| `FLAW_ANSWER_LEAKAGE` | Clues in stem or option parentheses | 5 | 0 | 2 |
| `FLAW_STEM_TOO_SHORT` | Underspecified stem (<25 chars) | 0 | 0 | 0 |

---

## 5. Statistical Pipeline Sensitivity Verification
- **One-Way ANOVA Pipeline Check (Baseline Fixtures):**
  - **F-statistic:** `222.598`
  - **p-value:** `1.17e-27`
  - **Interpretation:** Verifies that the ANOVA calculation correctly flags between-condition variance across the curated test fixtures. Live model statistical significance tests will be reported following production API execution.

- **Pairwise Welch's t-test Pipeline Checks:**
  - **Source Grounded Vs Generic:** t = 16.152, p = 7.12e-15 -> *Pipeline Differentiated (p < 0.05)*
  - **Source Grounded Vs Syllabus Constrained:** t = 7.503, p = 4.28e-07 -> *Pipeline Differentiated (p < 0.05)*
  - **Syllabus Constrained Vs Generic:** t = 14.371, p = 1.17e-11 -> *Pipeline Differentiated (p < 0.05)*

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
