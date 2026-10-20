# ARCHITECTURE.md — System Architecture & Design

## 1. Architectural Principles
- **Dual Interface:** Accessible via an intuitive, responsive web workbench (Vite + React / TailwindCSS) and a headless Python CLI (`scripts/reproduce_experiment.py`) for automated and scripted benchmarks.
- **Zero-Dependency Cold Start:** Fully functional out-of-the-box with a deterministic baseline engine. Researchers can clone the repository, run tests, and inspect experiments without requiring paid API keys or external server setups.
- **Pluggable Model Providers:** Abstract model provider interface supporting offline deterministic generation, OpenAI, Anthropic Claude, and Google Gemini.
- **Auditable Provenance:** Every question record permanently stores its generation parameters, prompt snapshot, source citation, automated audit flags, and human review timestamps.

---

## 2. Component Diagram

```
+--------------------------------------------------------------------------+
|                          Web Research Workbench                          |
|  - Dashboard: Metrics & Status       - Syllabus Tree & Gap Heatmaps      |
|  - Literature & Citation Explorer    - MCQ Dataset CRUD & Review Arena   |
|  - Comparative Experiment Studio     - Markdown / PDF Report Exporter    |
+------------------------------------+-------------------------------------+
                                     | JSON REST API
                                     v
+--------------------------------------------------------------------------+
|                     FastAPI Application Backend                          |
|  /api/overview   /api/syllabi   /api/sources   /api/questions            |
|  /api/generate   /api/evaluate  /api/reviews   /api/experiments /api/pariksha
+------------------------------------+-------------------------------------+
                                     |
               +---------------------+---------------------+
               |                                           |
               v                                           v
+-----------------------------+             +------------------------------+
|     Core Domain Modules     |             |      Persistence & Data      |
| - Syllabus Engine           |             | - data/syllabi/*.json        |
| - Canonical Source Registry |             | - data/sources/*.json        |
| - Generation Engine         |             | - data/datasets/*.json       |
| - Deterministic Evaluator   |             | - data/experiments/*.json    |
| - Statistical Analyzer      |             | - data/reports/*.md          |
| - Pariksha Adapter          |             +------------------------------+
+-----------------------------+
```

---

## 3. Core Modules

### `src/core/evaluator.py`
Executes multi-stage validation:
1. **Deterministic Structural Audit:**
   - Exact 4-option presence (A, B, C, D).
   - Valid answer key check.
   - Option duplication detection.
   - Answer leakage heuristics (lexical overlap between stem and designated correct option).
   - "All of the above" / "None of the above" anti-pattern detection.
   - Distractor length disparity check (ratio > 2.5x variance).
2. **Quality Scoring Rubric:**
   - Computes Factual Correctness, Syllabus Alignment, Distractor Plausibility, and Evidence Traceability scores (1–5 scale).
   - Calculates a Composite Item Quality Index (0–100%).

### `src/core/generator.py`
Implements the 3 experimental prompt conditions:
- Condition A: Generic Prompt
- Condition B: Syllabus-Constrained Prompt
- Condition C: Syllabus + Source-Grounded Prompt
Includes deterministic algorithmic generators for all 5 core CS subjects and pluggable API caller.

### `src/core/analyzer.py`
Computes descriptive and inferential statistics:
- Means, standard deviations, confidence intervals across conditions.
- Item-writing flaw rates and breakdown.
- Hypothesis testing (ANOVA F-statistic, p-values, effect size).

### `src/integrations/pariksha_adapter.py`
Provides bidirectional data transformation between SyllabusTrace-CS and Pariksha schema:
- Maps subject slugs, topic paths, question structures, and citation metadata.
- Enables exporting validated, high-scoring questions directly into Pariksha-compatible JSON format.
