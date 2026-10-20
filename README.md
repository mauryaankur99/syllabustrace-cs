# SyllabusTrace-CS: A Source-Traceable Quality Benchmark for AI-Generated Computer Science Multiple-Choice Questions in Indian Competitive Examinations

[![License: MIT](https://img.shields.io/badge/License-MIT-violet.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-1.0.0-009688.svg)](https://fastapi.tiangolo.com/)
[![Tests: 15 Passed](https://img.shields.io/badge/Tests-15%20Passed-emerald.svg)](tests/)
[![Reproducibility: Pipeline Verifiable](https://img.shields.io/badge/Reproducibility-Pipeline%20Verifiable-blue.svg)](manuscript/REPRODUCIBILITY_CHECKLIST.md)
[![Pilot Study: Operating Systems (N=12)](https://img.shields.io/badge/Pilot%20Study-Operating%20Systems%20(N=12)-purple.svg)](data/experiments/)

---

## 1. Overview
**SyllabusTrace-CS** is an open-source scientific research evaluation framework and audit workbench designed to evaluate the psychometric quality, item-writing flaws (IWFs), syllabus alignment, and source traceability of AI-generated Computer Science Multiple-Choice Questions (MCQs) for high-stakes Indian competitive examinations (such as **GATE CS & IT** and **UGC NET CS**).

### Core Research Question
> *Does enforcing hierarchical syllabus constraints (Condition B) and authoritative canonical textbook citations (Condition C) eliminate Item-Writing Flaws (IWFs), distractor ambiguity, and answer-key drift in AI-generated Computer Science MCQs compared with unconstrained generative baselines (Condition A)?*

---

## 2. Key Contributions & Implemented Architecture
1. **Three-Condition Comparative Paradigm:** Structured experimental comparison across:
   - **Condition A (Generic Baseline):** Zero-shot topic prompt without structural or citation constraints.
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

## 3. Software Pipeline Sanity Checks (Fixture Suite Only — Not Empirical Results)

> **Research Integrity Notice on Fixture Data:**
> The repository includes an initial suite of **60 curated illustrative fixtures** (`data/fixtures/demo_curated_benchmark_60.json` and `data/datasets/benchmark_questions.json`) tagged as `data_tier = "illustrative_fixture"`.
> These records are maintained strictly as **software pipeline sanity checks** to ensure that parsers, heuristic regex rules, scoring formulas, and export tools run cleanly without errors.
> **These 60 fixture records do NOT represent real AI model experiments or empirical research findings.**

---

## 4. Empirical Pilot Study Results (GATE CS Operating Systems, $N=12$)

We conducted an empirical pilot study focusing on Section 5 (**Operating Systems**) of the official **GATE CS & IT 2026** syllabus across 4 matched topics:
1. `OS-CPU-RR`: CPU Scheduling — Round Robin (Time Quantum & Context Switching)
2. `OS-SYNC-PET`: Process Synchronization — Critical Section & Peterson's Algorithm
3. `OS-MEM-TLB`: Memory Management — Paging & Translation Lookaside Buffer (TLB) EMAT
4. `OS-DEAD-BNK`: Deadlocks — Banker's Algorithm (Safety & Allocation)

All items were generated under the three experimental conditions, retaining complete provenance (verbatim prompt, raw model response, timestamp, temperature, model identifier `gemini-2.5-pro`), with answer keys independently verified against Silberschatz, Galvin, & Gagne (*Operating System Concepts*, 10th Edition, Wiley, 2018). Reviewer approval is recorded as `pending` until formal double-blind faculty review.

The pilot dataset is preserved in [`data/experiments/pilot_study_dataset.json`](data/experiments/pilot_study_dataset.json).

### Empirical Pilot Evaluation Metrics ($N=12$)

| Experimental Condition | Sample ($N$) | Composite Quality (%) | Factual Correctness (1–5) | Syllabus Alignment (1–5) | Traceability (1–5) | Flaw Rate (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Condition A (Generic)** | 4 | $52.75\% \pm 4.50$ | $4.20 \pm 0.00$ | $5.00 \pm 0.00$ | $1.20 \pm 0.00$ | **100.0%** |
| **Condition B (Syllabus)** | 4 | $92.60\% \pm 0.00$ | $4.70 \pm 0.00$ | $5.00 \pm 0.00$ | $3.60 \pm 0.00$ | **0.0%** |
| **Condition C (Source-Grounded)** | 4 | **$97.50\% \pm 5.00$** | **$5.00 \pm 0.00$** | **$5.00 \pm 0.00$** | **$5.00 \pm 0.00$** | **25.0%*** |

*\*Note on Condition C Flaw Rate:* In the pilot, 1 Condition C item was flagged with `FLAW_LENGTH_OUTLIER` because an exact textbook theorem excerpt produced a correct answer whose technical detail exceeded the distractor length ratio threshold ($2.3\times$), with zero factual or structural flaws.

### Exploratory Inferential Statistics ($df = (2, 9)$)
- **One-Way ANOVA:** $F = 159.76, p = 9.32 \times 10^{-8}$ (Confirms significant variance between conditions in the pilot sample).
- **Welch's Pairwise $t$-tests:**
  - Condition C vs. Condition A: $t = 13.31, p < 10^{-4}$ (Significant).
  - Condition B vs. Condition A: $t = 17.71, p = 0.0004$ (Significant).
  - Condition C vs. Condition B: $t = 1.96, p = 0.1449$ (Not Significant at $\alpha = 0.05$ due to pilot sample size).
- **Statistical Interpretation:** These exploratory pilot statistics demonstrate clear separation between constrained generation and unconstrained baselines. However, because $N=12$, they serve as preliminary empirical evidence rather than definitive population-level claims.

---

## 5. Quickstart: Reproducing Experiments & Artifacts

### A. Clone the Repository
```bash
git clone https://github.com/mauryaankur99/syllabustrace-cs.git
cd syllabustrace-cs
```

### B. Run the Genuine Pilot Study Pipeline
```bash
python scripts/run_pilot_study.py
```
Executes the Operating Systems pilot evaluation, calculates empirical metrics on the 12 eligible items, and exports [`data/reports/PILOT_STUDY_REPORT.md`](data/reports/PILOT_STUDY_REPORT.md).

### C. Regenerate Publication Figures & LaTeX Tables
```bash
python scripts/generate_paper_tables_and_figures.py
```
Regenerates publication-quality figures (`manuscript/figures/*.png`) and LaTeX tables (`manuscript/tables/*.tex`) derived strictly from the eligible pilot dataset (`data/experiments/pilot_study_dataset.json`).

### D. Run the Headless Pipeline Sanity Check (Fixture Suite)
```bash
python scripts/reproduce_experiment.py
```
Validates the deterministic baseline scoring routines over the 60 illustrative fixtures.

### E. Run Automated Test Suite
```bash
python tests/run_tests.py
```
Executes all 14 unit and integration tests across evaluator rules, generator conditions, analyzer statistics, and platform adapters.

---

## 6. Provider Integration & Credential Status Notice
- **Integration Architecture:** `src/core/generator.py` contains working client implementations for Google Gemini, OpenAI, and Anthropic, designed to capture exact model identifiers, latency, timestamps, and verbatim prompts/responses.
- **Current Blocker / Untested Status:** Because external provider API keys (`GEMINI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) are not provisioned in the current environment, **live network calls to third-party APIs remain untested**.
- **Fail-Safe Behavior:** Requesting an unconfigured provider explicitly raises `ProviderMissingCredentialsError` and halts execution, preventing ungrounded mock responses from being masqueraded as live API outputs.
- **Configuring Keys (Optional):**
  ```bash
  export GEMINI_API_KEY="your-gemini-key"
  export OPENAI_API_KEY="your-openai-key"
  export ANTHROPIC_API_KEY="your-anthropic-key"
  ```

---

## 7. Launching the Interactive Web Workbench

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

## 8. Project Architecture

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
│   ├── fixtures/                      # Curated baseline test fixtures (N=60)
│   ├── datasets/                      # Benchmark datasets (evaluated & raw)
│   ├── experiments/                   # Genuine pilot study dataset & metrics
│   └── reports/                       # Generated research reports
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
└── tests/                             # Automated test suite (14 tests)
```

---

## 9. Research Access & Non-Commercial Compliance
- **Independent Governance:** SyllabusTrace-CS is an independent, non-commercial scientific research project authored by Ankur Maurya (Independent Researcher, Gujarat, India).
- **Non-Commercial Nature:** The project contains no commercial monetization, advertisements, or paid access walls.
- **External Adapter Decoupling:** The Pariksha adapter (`src/integrations/pariksha_adapter.py`) functions strictly as an external research case study, verifying how psychometric audits can prevent flawed questions from entering mock assessment platforms.
- **Data Integrity:** All citations (Cormen, Silberschatz, Kurose-Ross, Sipser, Haladyna) are verified academic works. Zero credentials, affiliations, or findings are fabricated.

---

## 10. Citation
If you use this benchmark, workbench, or dataset in your academic work, please cite:

```bibtex
@article{maurya2026syllabustrace,
  author    = {Ankur Maurya},
  title     = {SyllabusTrace-CS: A Source-Traceable Quality Benchmark for AI-Generated Computer Science Multiple-Choice Questions in Indian Competitive Examinations},
  year      = {2026},
  url       = {https://github.com/mauryaankur99/syllabustrace-cs}
}
```
