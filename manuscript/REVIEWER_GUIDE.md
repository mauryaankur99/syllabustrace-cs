# REVIEWER_GUIDE.md — Human Expert Review & Pre-Submission Audit Protocol

This guide outlines the protocol for human peer reviewers, professors, and domain experts to audit the SyllabusTrace-CS benchmark and manuscript before formal conference or journal submission.

---

## 1. Quick Audit Setup (5 Minutes)
```bash
# 1. Clone the repository
git clone https://github.com/mauryaankur99/syllabustrace-cs.git
cd syllabustrace-cs

# 2. Run automated reproduction pipeline
python scripts/reproduce_experiment.py
python scripts/generate_paper_tables_and_figures.py

# 3. Launch interactive review workbench
python -m uvicorn src.api.main:app --port 8000 --reload
```
Open `http://localhost:8000` in any web browser and click the **Review Queue** tab.

---

## 2. Reviewer Checklist for Individual Assessment Items

When auditing questions in the Review Workspace, evaluate the following four dimensions:

### A. Factual Correctness & Technical Accuracy
- Is the designated correct option mathematically, algorithmically, and factually sound?
- Does the technical explanation provide a clear, indisputable rationale?
- Could any plausible alternative interpretation justify one of the distractors?

### B. Syllabus Alignment & Cognitive Depth
- Does the question test concepts strictly within the official GATE CS / UGC NET syllabus?
- Does the item match the designated Bloom's cognitive taxonomy level (e.g., Application vs. Recall)?

### C. Distractor Plausibility & Discrimination
- Are all three distractors plausible to a student who has common misconceptions?
- Are distractors grammatically parallel and approximately equal in length to the key?
- Are "All of the above" or "None of the above" completely absent?

### D. Canonical Source Grounding
- For Condition C items: Does the cited textbook (CLRS, Silberschatz, Kurose-Ross, Sipser) explicitly substantiate the correct key?
- Is the verified excerpt accurate and located on the cited page/chapter?

---

## 3. Recording Review Decisions
In the interactive review UI:
- Click **Approve Item** if the question meets all quality standards.
- Click **Reject** if the item contains uncorrectable factual errors or severe flaws.
- Click **Flag Defect** and enter specific reviewer comments if minor adjustments are needed.
All review actions are logged with timestamps and reviewer feedback.
