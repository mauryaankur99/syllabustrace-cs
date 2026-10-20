# RESEARCH_ACCESS_COMPLIANCE.md — Research Program Eligibility & Non-Commercial Independence

## 1. Purpose & Scope
This document evaluates the design, governance, and institutional positioning of **SyllabusTrace-CS** against standard research-access program eligibility criteria (such as OpenAI Researcher Access Program, Anthropic Research Grants, and Google TPU Research Cloud).

---

## 2. Institutional & Researcher Status
- **Principal Investigator / Author:** Ankur Maurya
- **Status:** Independent Researcher and Computer Science & Engineering Graduate (Gujarat, India).
- **Integrity Rule:** Do not claim academic university appointments, professorships, or grant awards unless formally conferred and documented.
- **Independence Statement:** While the author previously developed web and educational projects (e.g., Pariksha, `pariksha.aeigs.com`), **SyllabusTrace-CS is an independent, non-commercial scientific research project and open-source benchmark**.

---

## 3. Strict Non-Commercial Separation Policy
Major AI research-access programs strictly mandate that subsidized or granted model compute be used solely for non-commercial scientific research, not commercial product operations.

To guarantee compliance:
1. **Independent Repository:** SyllabusTrace-CS is housed in its own dedicated, standalone repository (`syllabustrace-cs`) with an open MIT license.
2. **No Commercial Hosting or Monetization:** The workbench and benchmark contain zero ads, payment gateways, premium subscriptions, or user tracking.
3. **Decoupled Adapter Architecture:** The Pariksha adapter (`src/integrations/pariksha_adapter.py`) functions strictly as an **external case study and verification bridge**, demonstrating how research benchmarks translate into real-world pedagogical settings. SyllabusTrace-CS does not connect to live production databases or process live student transaction data.
4. **Public Artifact Dissemination:** All findings, benchmark datasets, evaluation rubrics, figures, and manuscripts are published openly for community replication.

---

## 4. Scientific Contribution & Novelty Boundaries
- **What this project contributes:**
  1. An empirical 3-condition benchmark ($N=60$ audited items across 5 core Computer Science disciplines: OS, DBMS, CN, DSA, TOC).
  2. A psychometric Item-Writing Flaw (IWF) heuristic audit engine tailored for Computer Science competitive exams (GATE CS, UGC NET).
  3. Evidence-anchored source traceability to canonical Computer Science textbooks (CLRS, Silberschatz, Kurose-Ross, Sipser).
  4. An interactive local evaluation workbench and reproducible analysis pipeline.
- **What this project does NOT claim:**
  - We do not claim a generalized theory of natural language generation across all educational subjects.
  - We do not claim that small-scale pilot benchmarks replace large-scale multi-thousand item psychometric field trials.
  - We distinguish between planned work, pilot benchmark experiments, and completed verified evaluations.
