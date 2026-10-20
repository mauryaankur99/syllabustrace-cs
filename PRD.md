# PRD.md — Product Requirements Document: SyllabusTrace-CS

## 1. Executive Summary & Research Mission
**SyllabusTrace-CS** is an independent, non-commercial scientific research project and benchmarking workbench designed to evaluate AI-generated Computer Science Multiple-Choice Questions (MCQs) in high-stakes competitive examinations (such as GATE CS and UGC NET).

The core mission is to empirically demonstrate that **syllabus-constrained and canonical source-grounded prompting paradigms** significantly reduce psychometric Item-Writing Flaws (IWFs), eliminate answer-key ambiguity, and achieve verifiable evidence traceability compared to unconstrained generative baselines.

---

## 2. Research Integrity & Non-Commercial Independence
1. **Separation from Commercial Activities:** SyllabusTrace-CS is strictly separated from commercial websites and products. While the author has previous experience building educational platforms (such as Pariksha, `pariksha.aeigs.com`), Pariksha serves solely as an external motivation and adapter case study. SyllabusTrace-CS is an independent, open-source scientific benchmark.
2. **Researcher Identity:** The project is authored by Ankur Maurya, an Independent Researcher and Computer Science & Engineering graduate from Gujarat, India. The project explicitly avoids fabricating university professorships, endorsements, or institutional appointments.
3. **Research-Access Program Alignment:** All system goals and operational workflows are designed to satisfy the strict non-commercial research criteria of programs like the OpenAI Researcher Access Program and Anthropic Research Grants.
4. **Data Tier Separation:** The framework maintains an explicit distinction between:
   - **Genuine Research Data:** $N=60$ audited items across 5 core Computer Science disciplines, with full provenance and verified experimental evaluations.
   - **Demonstration / Scratch Data:** Mock samples in `data/datasets/demo_samples.json` clearly tagged for UI testing and excluded from statistical reporting.

---

## 3. Core Research Questions
- **RQ1 (Item-Writing Flaw Elimination):** Can hierarchical syllabus constraints and item-writing rules reduce psychometric flaws (answer leakage, option length outliers, "All/None of the above") to $< 5\%$?
- **RQ2 (Canonical Evidence Traceability):** Does injecting verified textbook excerpts achieve near-perfect citation precision ($\ge 4.8 / 5.0$) and significantly superior Composite Quality scores?
- **RQ3 (Domain Invariance):** Do these quality advantages hold invariant across distinct computer science disciplines (OS, DBMS, CN, DSA, TOC)?

---

## 4. Key Functional Modules

| Module | Purpose | Status |
| :--- | :--- | :--- |
| **Research Dashboard** | Real-time overview of research hypotheses, experiment status, subject distribution, and telemetry | Complete |
| **Syllabus Explorer** | Hierarchical GATE CS / UGC NET curriculum tree, topic coverage heatmaps, and curriculum gap analysis | Complete |
| **Literature Registry** | Authoritative textbook catalog (Cormen, Silberschatz, Kurose-Ross, Sipser) with chapter indices and verified excerpts | Complete |
| **MCQ Dataset Manager**| Search, filter, inspect, and export benchmark items with provenance metadata and flaw tags | Complete |
| **AI Generation Lab** | Controlled comparison generator supporting Condition A (Generic), B (Syllabus), and C (Source-Grounded) | Complete |
| **Deterministic Auditor**| 8-rule deterministic audit engine (option counts, key validity, leakage, duplicates, length disparity) | Complete |
| **Review Workspace** | Human expert review queue for auditing questions, logging comments, and approving verified items | Complete |
| **Experiment Studio** | Automated statistical analysis (ANOVA F-statistic, p-values, Welch's t-tests, flaw distributions) | Complete |
| **Manuscript & Report** | Automated generation of academic research reports (Markdown, LaTeX, Matplotlib figures) | Complete |
| **Pariksha Adapter** | Decoupled bidirectional schema adapter for educational platform case studies | Complete |

---

## 5. Scientific Deliverables & File Structure
```text
syllabustrace-cs/
├── README.md
├── PRD.md
├── LICENSE (MIT)
├── CITATION.cff
├── requirements.txt
├── docs/
│   ├── RESEARCH_DIRECTION.md
│   ├── LITERATURE_REVIEW.md
│   ├── RESEARCH_PROTOCOL.md
│   ├── ARCHITECTURE.md
│   ├── DATA_DICTIONARY.md
│   ├── EVALUATION_RUBRIC.md
│   ├── EXPERIMENT_GUIDE.md
│   ├── LIMITATIONS.md
│   └── RESEARCH_ACCESS_COMPLIANCE.md
├── data/
│   ├── syllabi/gate_cs_syllabus.json
│   ├── sources/canonical_cs_sources.json
│   ├── datasets/
│   │   ├── benchmark_questions.json
│   │   ├── evaluated_benchmark.json
│   │   ├── evaluated_benchmark.csv
│   │   └── demo_samples.json
│   ├── experiments/pilot_comparison.json
│   └── reports/RESEARCH_REPORT.md
├── manuscript/
│   ├── manuscript.md
│   ├── manuscript.tex
│   ├── references.bib
│   ├── figures/
│   ├── tables/
│   ├── REPRODUCIBILITY_CHECKLIST.md
│   └── REVIEWER_GUIDE.md
├── src/
│   ├── api/main.py
│   ├── core/ (models, evaluator, generator, analyzer, report_generator)
│   ├── services/ (syllabus, source, question, experiment)
│   ├── integrations/pariksha_adapter.py
│   └── ui/index.html
├── scripts/
│   ├── populate_benchmark.py
│   ├── reproduce_experiment.py
│   └── generate_paper_tables_and_figures.py
└── tests/
    ├── run_tests.py
    ├── test_evaluator.py
    ├── test_generator.py
    ├── test_analyzer.py
    ├── test_pariksha_adapter.py
    └── test_api.py
```

---

## 6. Verification & Quality Assurance Contract
- All tests must execute with 0 failures via `python tests/run_tests.py`.
- All figures and LaTeX tables must regenerate via `python scripts/generate_paper_tables_and_figures.py`.
- No experimental findings, p-values, or citations may be fabricated.
