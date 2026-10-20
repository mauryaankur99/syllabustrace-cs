# REPRODUCIBILITY_CHECKLIST.md — SyllabusTrace-CS

This checklist follows the standard ACM/NeurIPS/ACL reproducibility guidelines to ensure complete, independent replication of all empirical findings and artifacts.

---

## 1. Code & Environment
- [x] **Repository Access:** Publicly hosted and structured under standard open-source conventions (`https://github.com/mauryaankur99/syllabustrace-cs`).
- [x] **Dependencies Documented:** Python dependencies specified in `requirements.txt` (FastAPI, Uvicorn, Pydantic, SciPy, Matplotlib, Pytest, HTTPX).
- [x] **Hardware & Platform:** Cross-platform (Windows, macOS, Linux). Requires standard commodity CPU, $< 500$ MB RAM, and zero GPU requirement.
- [x] **Execution Commands:** All pilot evaluations, baseline fixture checks, ANOVA calculations, LaTeX tables, and plots regenerate reproducibly:
  ```bash
  # 1. Execute genuine pilot study and evaluate records
  python scripts/run_pilot_study.py

  # 2. Regenerate manuscript figures and LaTeX tables from eligible pilot data
  python scripts/generate_paper_tables_and_figures.py

  # 3. Execute software pipeline checks on the baseline fixture suite
  python scripts/reproduce_experiment.py
  ```

---

## 2. Dataset & Provenance
- [x] **Data Availability:** Complete raw and evaluated pilot records included in machine-readable JSON (`data/experiments/pilot_study_dataset.json`).
- [x] **Data Provenance & Tier Separation:** Records are strictly partitioned into illustrative baseline fixtures (`data_tier: illustrative_fixture`, $N=60$) and genuine experimental runs (`data_tier: experimental_run`, $N=12$), preventing mock or fixture records from being presented as live model outputs.
- [x] **Syllabus Hierarchy:** Official curriculum mapping provided in `data/syllabi/gate_cs_syllabus.json` (GATE CS Section 5 Operating Systems).
- [x] **Source Literature Corpus:** Canonical citations, editions, ISBNs, and verified textual excerpts provided in `data/sources/canonical_cs_sources.json` and anchored to Silberschatz et al. (10th Ed., Wiley, 2018).
- [x] **Sample Size:** Explicitly reported (Pilot Study: $N=12$ total; $n=4$ per condition across 4 matched OS topics; Baseline Fixture Suite: $N=60$).

---

## 3. Evaluation & Analysis
- [x] **Deterministic Rules:** All Item-Writing Flaw (IWF) heuristics are open-source and deterministically implemented in `src/core/evaluator.py`.
- [x] **Statistical Reporting:** Exact F-statistics, p-values, t-statistics, degrees of freedom ($df=(2, 9)$), sample sizes, and standard deviations reported without manufactured claims.
- [x] **Integrity & Non-Fabrication:** All reported numbers originate directly from the evaluated pilot JSON file generated during execution.
- [x] **Automated Tests:** Comprehensive unit and integration test suite runnable via `python tests/run_tests.py` (15 passing tests).

---

## 4. Human Review & Pre-Submission Verification
- [x] **Interactive Review Workbench:** Reviewers can inspect raw stems, options, distractors, and citations via the local web UI (`uvicorn src.api.main:app`).
- [x] **Review Decisions Tracked:** Review decisions are transparently tracked as `pending` until formal double-blind faculty review is completed.
- [x] **Pariksha Integration Test:** Verified two-way transformation fidelity between SyllabusTrace-CS and Pariksha schema (`src/integrations/pariksha_adapter.py`).
- [x] **Reviewer Guide Available:** Step-by-step instructions for expert domain peer review provided in `manuscript/REVIEWER_GUIDE.md`.
