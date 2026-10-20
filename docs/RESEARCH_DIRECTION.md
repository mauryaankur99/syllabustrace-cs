# RESEARCH_DIRECTION.md — Research Direction & Formal Hypotheses

## 1. Selected Research Focus
**Title:** SyllabusTrace-CS: A Source-Traceable Quality Benchmark for AI-Generated Computer Science Multiple-Choice Questions in Indian Competitive Examinations.

---

## 2. Refined Research Questions & Formal Hypotheses

### Primary Research Question (RQ1)
> **RQ1 (Psychometric Flaw Reduction):** To what extent does enforcing hierarchical syllabus bounds and item-writing constraints (Condition B) reduce the prevalence of psychometric Item-Writing Flaws (IWFs)—such as answer leakage, distractor length disparity, and "All/None of the above" anti-patterns—compared to generic prompting (Condition A)?

- **Hypothesis 1 (H1):** *Syllabus-constrained prompting will significantly reduce the proportion of flawed items ($\text{IWF} < 5\%$) relative to generic prompting ($\text{IWF} > 60\%$).*

---

### Secondary Research Question (RQ2)
> **RQ2 (Source Grounding & Evidence Traceability):** Does explicit grounding in canonical Computer Science textbook passages (Condition C) eliminate answer-key ambiguity and achieve verifiable citation precision without degrading conceptual difficulty?

- **Hypothesis 2 (H2):** *Condition C will achieve near-perfect citation precision (mean traceability $\ge 4.8 / 5.0$) and significantly higher Composite Quality scores compared to both Condition A and Condition B.*

---

### Exploratory Research Question (RQ3)
> **RQ3 (Domain Invariance Across CS Strata):** Do the quality improvements conferred by source grounding remain consistent across disparate Computer Science subfields (e.g., highly mathematical Theory of Computation vs. systems-oriented Computer Networks)?

---

## 3. Methodological Significance for Competitive Exam Technology
This study addresses a major real-world bottleneck in exam platforms like **Pariksha** (`pariksha.aeigs.com`):
1. **Unverified AI generation floods item banks with subtle errors** that erode student trust.
2. **Students require authoritative explanations** linked directly to official syllabi and standard textbooks (e.g., GATE CS challenges require textbook citations).
3. **Automated audits can act as an instant quality gate** before questions are published to production student test sessions.
