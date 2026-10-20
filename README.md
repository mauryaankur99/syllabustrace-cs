# SyllabusTrace-CS: A Source-Traceable Quality Benchmark for AI-Generated Computer Science Multiple-Choice Questions in Indian Competitive Examinations

[![License: MIT](https://img.shields.io/badge/License-MIT-violet.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Tests: 13 Passed](https://img.shields.io/badge/Tests-13%20Passed-emerald.svg)](tests/)
[![Status: Prototype Workbench](https://img.shields.io/badge/Status-Prototype%20Workbench-amber.svg)](manuscript/)

---

## 1. Overview
**SyllabusTrace-CS** is an open-source scientific research evaluation framework and audit workbench designed to evaluate the psychometric quality, item-writing flaws (IWFs), syllabus alignment, and source traceability of AI-generated Computer Science Multiple-Choice Questions (MCQs) for high-stakes Indian competitive examinations (such as **GATE CS & IT** and **UGC NET CS**).

### Core Research Question
> *Does enforcing hierarchical syllabus constraints (Condition B) and authoritative canonical textbook citations (Condition C) eliminate Item-Writing Flaws (IWFs), distractor ambiguity, and answer-key drift in AI-generated Computer Science MCQs compared with unconstrained generative baselines (Condition A)?*

---

## 2. Key Contributions & Implemented Architecture
1. **Three-Condition Comparative Paradigm:** Structured experimental comparison across:
   - **Condition A (Generic Baseline):** Zero-shot topic prompt without structural constraints.
   - **Condition B (Syllabus-Constrained):** Bounded by official GATE CS syllabus nodes, Bloom's cognitive taxonomy, and negative formatting constraints.
   - **Condition C (Syllabus + Canonical Source-Grounded):** Condition B bound to verifiable excerpts from canonical textbooks (Cormen, Silberschatz, Kurose-Ross, Sipser).
2. **Deterministic Psychometric Flaw Detector:** Heuristic identification of:
   - Prohibited "All/None of the above" shortcuts (`FLAW_ALL_NONE_ABOVE`).
   - Clue and clang associations between stem and answer (`FLAW_ANSWER_LEAKAGE`).
   - Distractor length disparity ($>2.3\times$ ratio) (`FLAW_LENGTH_OUTLIER`).
   - Missing canonical citations (`FLAW_NO_CITATION`).
   - Malformed options or invalid answer keys (`ERR_OPTION_COUNT`, `ERR_INVALID_KEY`).
3. **Genuine Live Provider Integrations:** Provider clients in `src/core/generator.py` for Google Gemini (`gemini-1.5-pro`), OpenAI (`gpt-4o`), and Anthropic (`claude-3-5-sonnet`) with explicit error handling (`ProviderMissingCredentialsError`) and raw response provenance capture.
4. **Interactive Research Workbench:** Full-featured local application with a research dashboard, syllabus coverage heatmap, literature explorer, review queue, generation lab, and automated report generation.
5. **Decoupled Platform Adapter:** Offline bridge for educational platforms (such as Pariksha, `pariksha.aeigs.com`), providing an automated pre-publish quality gate for student test banks.

---

## 3. Benchmark Dataset Status & Prototype Baseline Findings

> **Research Integrity Notice on Benchmark Data:**
> The current baseline dataset ($N=60$) consists of **curated illustrative prototype fixtures** (`data_tier = "illustrative_fixture"`) across 5 core Computer Science disciplines (OS, DBMS, CN, DSA, TOC).
> These records are designed to validate that the deterministic flaw detection heuristics, scoring rubrics, and reporting scripts operate correctly. They are **not** claimed as verified empirical performance measurements of live AI models, which remain subject to forthcoming live API experimental runs.

### Prototype Fixture Baseline Summary ($N=60$)

All reported numbers are calculated directly from the baseline fixture dataset (`data/datasets/evaluated_benchmark.json`):

| Experimental Condition | Sample ($N$) | Composite Quality (%) | Factual Correctness (1–5) | Syllabus Alignment (1–5) | Traceability (1–5) | Flaw Rate (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Condition A (Generic Fixtures)** | 20 | $65.25\% \pm 8.51$ | $4.20 \pm 0.00$ | $5.00 \pm 0.00$ | $1.20 \pm 0.00$ | **100.0%** |
| **Condition B (Syllabus Fixtures)** | 20 | $92.60\% \pm 0.00$ | $4.70 \pm 0.00$ | $5.00 \pm 0.00$ | $3.60 \pm 0.00$ | **0.0%** |
| **Condition C (Source-Grounded Fixtures)** | 20 | **$98.55\% \pm 3.55$** | **$5.00 \pm 0.00$** | **$5.00 \pm 0.00$** | **$5.00 \pm 0.00$** | **15.0%** |

- **Pipeline ANOVA Check:** $F = 222.60, p = 1.17 \times 10^{-27}$ (Verifies statistical tool sensitivity on baseline cohorts).
- **Flaw Heuristics:** The audit engine detected uncited claims (100%), prohibited options ("All/None of above", 40%), and answer leakage (20%) in Condition A test fixtures, and verified their absence in Condition B and C fixtures.
- *(Note: Condition C recorded a 15% flaw flag due to length outlier heuristics on detailed mathematical proofs, while exhibiting 0% structural flaws and 0% factual errors.)*

---

## 4. Quickstart: Reproducing Experiments & Artifacts

### A. Clone the Repository
```bash
git clone https://github.com/mauryaankur99/syllabustrace-cs.git
cd syllabustrace-cs
```

### B. Run the Headless Benchmark Pipeline
```bash
python scripts/reproduce_experiment.py
```
This regenerates evaluated datasets (`data/datasets/evaluated_benchmark.json` and `.csv`) and re-computes all statistical metrics and the Markdown research report.

### C. Regenerate Publication Figures & LaTeX Tables
```bash
python scripts/generate_paper_tables_and_figures.py
```
This writes publication-quality figures (`manuscript/figures/*.png`) and LaTeX tables (`manuscript/tables/*.tex`).

### D. Run Automated Test Suite
```bash
python tests/run_tests.py
```
Executes all 13 unit and integration tests across evaluator rules, generator conditions, analyzer statistics, and platform adapters.

### E. Configuring Live Model Generation (Optional)
To execute genuine live API generation experiments rather than the baseline fixtures, export your provider API key:
```bash
# For Google Gemini (gemini-1.5-pro, gemini-2.0-flash)
export GEMINI_API_KEY="your-gemini-key"

# For OpenAI (gpt-4o, gpt-4o-mini)
export OPENAI_API_KEY="your-openai-key"

# For Anthropic (claude-3-5-sonnet)
export ANTHROPIC_API_KEY="your-anthropic-key"
```
When configured, requests via the Web Workbench Generation Lab or `MCQGenerator.generate_live()` will dispatch live API calls and record complete model provenance (model ID, timestamps, raw responses, parameters). Without credentials, the system raises an explicit `ProviderMissingCredentialsError`.

---

## 5. Launching the Interactive Web Workbench

Start the FastAPI application:
```bash
python -m uvicorn src.api.main:app --port 8000 --reload
```
Navigate to `http://localhost:8000` in your browser. The embedded Single-Page Application provides:
- **Dashboard:** Telemetry cards, research question summary, condition score distributions.
- **Experiments:** Detailed statistical comparisons, ANOVA F-statistic, Welch's t-test breakdowns.
- **MCQ Dataset:** Searchable data table with filters for condition, subject, and defect flags.
- **Review Queue:** Human expert inspection view with option highlighting and approval logging.
- **Syllabus & Heatmap:** Interactive curriculum tree covering all 5 core CS subjects.
- **Literature Registry:** Canonical textbook catalog with verified excerpts.
- **AI Generation Lab:** Interactive generation sandbox testing conditions A, B, and C.
- **Research Report:** Live Markdown preview and export buttons.

Interactive API Swagger documentation is available at `http://localhost:8000/docs`.

---

## 6. Project Architecture

```
syllabustrace-cs/
├── README.md                          # Project documentation
├── PRD.md                             # Formal Product Requirements Document
├── LICENSE                            # MIT Open Source License
├── CITATION.cff                       # Citation metadata
├── requirements.txt                   # Minimal Python dependencies
├── docs/                              # Research documentation & protocols
│   ├── RESEARCH_DIRECTION.md          # Refined research questions & hypotheses
│   ├── LITERATURE_REVIEW.md           # Verifiable academic literature review
│   ├── RESEARCH_PROTOCOL.md           # Controlled experimental design
│   ├── ARCHITECTURE.md                # System components & dataflow
│   ├── DATA_DICTIONARY.md             # Pydantic schemas & entity definitions
│   ├── EVALUATION_RUBRIC.md           # Multi-stage rubric & flaw taxonomy
│   ├── EXPERIMENT_GUIDE.md            # Reproduction walkthrough
│   ├── LIMITATIONS.md                 # Threats to validity & scope
│   └── RESEARCH_ACCESS_COMPLIANCE.md  # Non-commercial research compliance
├── data/                              # Data corpora & experiment records
│   ├── syllabi/                       # GATE CS official syllabus hierarchy
│   ├── sources/                       # Canonical CS textbook corpus
│   ├── datasets/                      # Benchmark datasets (evaluated & raw)
│   ├── experiments/                   # Serialized experiment run outputs
│   └── reports/                       # Generated research report
├── manuscript/                        # Academic paper draft & artifacts
│   ├── manuscript.md                  # Complete paper in Markdown
│   ├── manuscript.tex                 # Compilable paper in LaTeX
│   ├── references.bib                 # Verified BibTeX citations
│   ├── figures/                       # Publication figures (Matplotlib)
│   ├── tables/                        # Generated LaTeX tables
│   ├── REPRODUCIBILITY_CHECKLIST.md   # ACM/NeurIPS-style checklist
│   └── REVIEWER_GUIDE.md              # Peer reviewer audit protocol
├── src/                               # Application source code
│   ├── core/                          # Evaluator, generator, analyzer, models
│   ├── services/                      # Question, syllabus, source, experiment
│   ├── integrations/                  # Pariksha decoupled platform adapter
│   ├── api/                           # FastAPI backend REST service
│   └── ui/                            # Interactive web workbench SPA
├── scripts/                           # Reproducible CLI automation scripts
└── tests/                             # Automated test suite (13 tests)
```

---

## 7. Research Access & Non-Commercial Compliance
- **Independent Governance:** SyllabusTrace-CS is an independent, non-commercial scientific research project authored by Ankur Maurya (Independent Researcher, Gujarat, India).
- **Non-Commercial Nature:** The project contains no commercial monetization, advertisements, or paid access walls.
- **External Adapter Decoupling:** The Pariksha adapter (`src/integrations/pariksha_adapter.py`) functions strictly as an external research case study, verifying how psychometric audits can prevent flawed questions from entering mock assessment platforms.
- **Data Integrity:** All citations (Cormen, Silberschatz, Kurose-Ross, Sipser, Haladyna) are verified academic works. Zero credentials, affiliations, or findings are fabricated.

---

## 8. Citation
If you use this benchmark, workbench, or dataset in your academic work, please cite:

```bibtex
@article{maurya2026syllabustrace,
  author    = {Ankur Maurya},
  title     = {SyllabusTrace-CS: A Source-Traceable Quality Benchmark for AI-Generated Computer Science Multiple-Choice Questions in Indian Competitive Examinations},
  year      = {2026},
  url       = {https://github.com/mauryaankur99/syllabustrace-cs}
}
```

---

## 9. License
Distributed under the **MIT License**. See `LICENSE` for details.
