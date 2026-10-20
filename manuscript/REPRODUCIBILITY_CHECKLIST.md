# REPRODUCIBILITY_CHECKLIST.md — SyllabusTrace-CS

This checklist follows the standard ACM/NeurIPS/ACL reproducibility guidelines to ensure complete, independent replication of all empirical findings and artifacts.

---

## 1. Code & Environment
- [x] **Repository Access:** Publicly hosted and structured under standard open-source conventions (`https://github.com/mauryaankur99/syllabustrace-cs`).
- [x] **Dependencies Documented:** Python dependencies specified in `requirements.txt` (FastAPI, Uvicorn, Pydantic, SciPy, Matplotlib, Pytest).
- [x] **Hardware & Platform:** Cross-platform (Windows, macOS, Linux). Deterministic baseline requires standard commodity CPU, $< 500$ MB RAM, and zero GPU requirement.
- [x] **Execution Command:** All benchmark evaluations, ANOVA calculations, LaTeX tables, and plots regenerate in a single command:
  ```bash
  python scripts/reproduce_experiment.py
  python scripts/generate_paper_tables_and_figures.py
  ```

---

## 2. Dataset & Provenance
- [x] **Data Availability:** Complete raw and evaluated benchmark datasets included in machine-readable JSON and CSV (`data/datasets/`).
- [x] **Data Provenance & Tier Separation:** Records are partitioned into illustrative baseline fixtures (`data_tier: illustrative_fixture`) and genuine experimental runs (`data_tier: experimental_run`), preventing mock or baseline fixture records from being presented as verified live model outputs.
- [x] **Syllabus Hierarchy:** Official curriculum mapping provided in `data/syllabi/gate_cs_syllabus.json`.
- [x] **Source Literature Corpus:** Canonical citations, editions, ISBNs, and verified textual excerpts provided in `data/sources/canonical_cs_sources.json`.
- [x] **Sample Size:** Explicitly reported ($N=60$ total; $n=20$ per condition across 5 subject strata).

---

## 3. Evaluation & Analysis
- [x] **Deterministic Rules:** All Item-Writing Flaw (IWF) heuristics are open-source and deterministically implemented in `src/core/evaluator.py`.
- [x] **Statistical Reporting:** Exact F-statistics, p-values, t-statistics, degrees of freedom, sample sizes, and standard deviations reported.
- [x] **Integrity & Non-Fabrication:** All reported numbers originate directly from the evaluated benchmark JSON file generated during execution.
- [x] **Automated Tests:** Comprehensive unit and integration test suite runnable via `python tests/run_tests.py`.

---

## 4. Human Review & Pre-Submission Verification
- [x] **Interactive Review Workbench:** Reviewers can inspect raw stems, options, distractors, and citations via the local web UI (`uvicorn src.api.main:app`).
- [x] **Review Decisions Tracked:** Review decisions for baseline fixtures are transparently tracked as `pending` until formal double-blind faculty review is completed.
- [x] **Pariksha Integration Test:** Verified two-way transformation fidelity between SyllabusTrace-CS and Pariksha schema (`src/integrations/pariksha_adapter.py`).
- [x] **Reviewer Guide Available:** Step-by-step instructions for expert domain peer review provided in `manuscript/REVIEWER_GUIDE.md`.
