# LIMITATIONS.md — Threats to Validity & Project Limitations

## 1. Threats to Internal Validity
- **Automated Flaw Detection Heuristics:** Deterministic rules (e.g., answer leakage via n-gram overlap, length disparity) provide objective, fast screening, but may occasionally flag valid technical terms that naturally require precise phrasing. Human expert review remains the gold standard.
- **Model Inherent Memorization:** Frontier foundation models have seen portions of standard textbooks (CLRS, Silberschatz) during pretraining. When tested on source-grounded conditions, performance improvements reflect both improved contextual adherence and retrieval precision, but contamination cannot be completely ruled out without synthetic novel theorems.

---

## 2. Threats to External Validity
- **Domain Specialization:** The present benchmark specifically targets Computer Science curricula (GATE CS, UGC NET CS, State PSCs). While the methodology and taxonomy generalize readily to other STEM fields (e.g., Electrical Engineering, Mathematics), empirical verification in non-CS domains is left for future work.
- **Cognitive Level Representation:** While the benchmark targets four Bloom's tiers (Recall, Comprehension, Application, Analysis), higher-order multi-concept synthesis problems (such as complex 2-mark GATE questions requiring multi-page code tracing or mathematical proofs) are underrepresented compared to standard single-concept MCQs.

---

## 3. Computational & Operational Considerations
- **Offline Deterministic Fallback:** To ensure 100% reproducibility without external API costs or credential dependencies, the repository provides an offline deterministic generator alongside cloud API adapters. The offline generator produces structurally realistic items, but full cross-model parameter comparisons require live model keys.
- **Sample Size in Pilot Phase:** The initial baseline evaluation dataset comprises 60 audited items (20 per condition across 5 subject strata). While sufficient to demonstrate statistically significant variance in flaw rates and citation precision, broader multi-thousand item scaling is slated for community expansion.
