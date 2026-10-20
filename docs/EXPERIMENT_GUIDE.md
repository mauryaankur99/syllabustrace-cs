# EXPERIMENT_GUIDE.md — Reproduction & Experimentation Guide

## 1. Quickstart: Headless Benchmark Execution
You can reproduce the baseline experiment and generate all statistical tables and charts headlessly via the CLI:

```bash
# Clone the repository
git clone https://github.com/mauryaankur99/syllabustrace-cs.git
cd syllabustrace-cs

# Run the automated reproduction script
python scripts/reproduce_experiment.py
```

This command will:
1. Load official syllabus nodes (`data/syllabi/gate_cs_syllabus.json`).
2. Load canonical sources (`data/sources/canonical_cs_sources.json`).
3. Load or generate the 60-question comparative benchmark across Conditions A, B, and C.
4. Execute deterministic audits and rubric evaluations on all questions.
5. Compute inferential statistics (Means, Standard Deviations, p-values, Flaw Rates).
6. Export the final evaluated datasets (`data/datasets/evaluated_benchmark.json` and `.csv`).
7. Generate the full academic markdown research report (`data/reports/RESEARCH_REPORT.md`).

---

## 2. Launching the Interactive Research Workbench

### Running the Backend API
```bash
# Launch FastAPI server with Uvicorn
uvicorn src.api.main:app --host 127.0.0.1 --port 8000 --reload
```
API Documentation will be live at: `http://127.0.0.1:8000/docs`

### Running the Frontend UI
The workbench frontend can be served directly by the FastAPI backend (static mount) or via a Vite dev server:
```bash
# Install frontend dependencies
npm install

# Start Vite development server
npm run dev
```
Navigate to `http://localhost:5173` (or `http://127.0.0.1:8000`).

---

## 3. Running Automated Tests
```bash
# Run backend test suite
pytest tests/ -v
```
All unit tests verify:
- API endpoint responses and serialization.
- Evaluator deterministic rules and scoring bounds.
- Generator condition compliance.
- Pariksha adapter two-way conversion fidelity.
