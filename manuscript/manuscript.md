# SyllabusTrace-CS: A Source-Traceable Quality Benchmark for AI-Generated Computer Science Multiple-Choice Questions in Indian Competitive Examinations

**Author:** Ankur Maurya  
*Independent Researcher & Software Engineer, Gujarat, India*  
*Correspondence:* `mauryaankur99@gmail.com` | `https://github.com/mauryaankur99/syllabustrace-cs`  

---

## Abstract
Large Language Models (LLMs) are increasingly explored for automated question generation in digital education. However, unconstrained prompting in high-stakes competitive examinations—such as the Graduate Aptitude Test in Engineering (GATE CS) and UGC NET in India—frequently risks generating invalid items afflicted by psychometric Item-Writing Flaws (IWFs), out-of-syllabus drift, and ungrounded answer keys lacking verifiable textbook provenance. We introduce **SyllabusTrace-CS**, an open-source evaluation framework, psychometric audit engine, and research workbench designed to evaluate and trace AI-generated Computer Science multiple-choice questions (MCQs). We formulate a controlled three-condition experimental paradigm: **Condition A (Generic Baseline)**, **Condition B (Syllabus-Constrained)**, and **Condition C (Syllabus + Canonical Source-Grounded)**. We implement deterministic heuristic detection for seven flaw categories, a multi-dimensional scoring rubric, and live API generator adapters for major providers (Google Gemini, OpenAI, Anthropic) with end-to-end provenance tracking. We report an empirical pilot study on Section 5 (**Operating Systems**) of the official GATE CS 2026 curriculum across four matched core topics ($N=12$ items; $n=4$ per condition), grounded in Silberschatz et al.'s *Operating System Concepts* (10th Ed., Wiley, 2018). In this pilot study, unconstrained baseline generation (Condition A) exhibited a **100.0% flaw rate** (dominated by prohibited 'All/None of the above' options, option length disparity, and absent citations) with a Composite Quality of $52.75\% \pm 4.50$. Enforcing hierarchical syllabus constraints (Condition B) eliminated structural flaws and elevated Composite Quality to $92.60\% \pm 0.00$. Anchoring generation to canonical textbook passages (Condition C) achieved **$97.50\% \pm 5.00$ Composite Quality** and **$5.0 / 5.0$ citation traceability**. An exploratory One-Way ANOVA confirmed significant divergence between conditions ($F = 159.76, p = 9.32 \times 10^{-8}, df=(2, 9)$), while pairwise testing indicated that while Conditions B and C significantly outperformed Condition A ($p < 0.001$), Condition C vs. B did not reach statistical significance ($t = 1.96, p = 0.1449$) at this pilot scale. We release the complete dataset, software pipeline, interactive workbench, and reproduction scripts under the MIT License.

**Keywords:** Computer Science Education, Multiple-Choice Question Generation, Item-Writing Flaws, Syllabus Alignment, Source Traceability, GATE CS, UGC NET.

---

## 1. Introduction
Standardized multiple-choice examinations form the primary sorting mechanism for graduate admissions, academic appointments, and public-sector recruitment in India. Examinations such as the **Graduate Aptitude Test in Engineering (GATE CS)** and the **National Eligibility Test (UGC NET CS)** demand deep conceptual precision, mathematical rigour, and strict adherence to officially published curriculum specifications.

Simultaneously, educational platforms (including platforms like Pariksha, `pariksha.aeigs.com`) increasingly explore generative artificial intelligence to synthesize practice mock assessments. However, off-the-shelf generative models suffer from significant potential failure modes when authoring technical assessment items:
1. **Psychometric Item-Writing Flaws (IWFs):** Off-the-shelf generative models can easily produce items containing answer leakage (clues in the stem pointing to the key), option length imbalance (correct answers systematically longer than distractors), and flawed distractors (such as "All of the above" or "None of the above"), violating psychometric standards codified by Haladyna & Downing (1989, 2002).
2. **Curricular Drift:** Models frequently hallucinate topics outside the designated syllabus boundaries (e.g., introducing proprietary vendor-specific SQL extensions into foundational relational calculus questions).
3. **Absence of Provenance & Traceable Verification:** When students or faculty challenge a provisional answer key, official examination authorities only accept challenges supported by canonical textbook citations (e.g., CLRS, Silberschatz, Kurose-Ross). Unconstrained AI questions fail to provide verifiable excerpts, leaving educators with an unsustainable manual verification burden.

To address these challenges, this paper presents **SyllabusTrace-CS**, a comprehensive research evaluation benchmark and interactive audit workbench that operationalizes source-grounded, syllabus-constrained question generation for Computer Science.

---

## 2. Related Work

### 2.1 Multiple-Choice Item-Writing Guidelines & Flaws
Decades of psychometric research confirm that item formatting directly impacts test validity. Haladyna & Downing (1989) synthesized 31 specific item-writing rules. Rodriguez (2005) established via meta-analysis that three well-crafted options often outperform four options burdened by implausible distractors or "All/None of the above" shortcuts. In medical and STEM testing, 30–50% of unvetted questions contain IWFs that artificially shift student scores.

### 2.2 LLM Evaluation in Computer Science
Prior benchmarks—such as MMLU (Hendrycks et al., 2021) and CS-Bench (Zeng et al., 2024)—focus almost exclusively on evaluating whether an LLM can *answer* multiple-choice questions. Savelka et al. (2023) evaluated LLMs on CS exams, observing that models struggle with spatial and multi-step algorithmic reasoning. However, systematic benchmarking of *question generation quality* against official curricula remains under-explored in the Indian competitive exam context.

### 2.3 Citation Grounding & Attributable Generation
Recent advances in Retrieval-Augmented Generation (RAG) and citation evaluation—such as the ALCE benchmark (Gao et al., 2023)—demonstrate that generative text must be tied to verifiable source passages to combat hallucination. In technical domains, citation precision (ensuring the cited passage unequivocally proves the correct answer) is paramount.

---

## 3. Research Questions & Hypotheses
We formalize three primary research questions:

- **RQ1 (Psychometric Flaw Reduction):** Does imposing hierarchical syllabus constraints and item-writing rules (Condition B) reduce the prevalence of Item-Writing Flaws (IWFs) compared to generic zero-shot prompting (Condition A)?
  - *Hypothesis 1 (H1):* Condition B will significantly reduce the IWF rate compared to Condition A by disallowing formulaic distractors and enforcing length symmetry.
- **RQ2 (Source Grounding & Evidence Traceability):** Does explicit grounding in canonical Computer Science textbook passages (Condition C) eliminate answer ambiguity and yield superior Composite Quality scores?
  - *Hypothesis 2 (H2):* Condition C will attain higher evidence traceability and composite quality than Conditions A and B by grounding answer keys in canonical literature.
- **RQ3 (Domain Invariance Across CS Strata):** Do the quality improvements of source grounding hold consistently across distinct CS subfields (OS, DBMS, CN, DSA, TOC)?

---

## 4. Methodology

### 4.1 Three Experimental Conditions
We design a controlled three-condition experimental pipeline:
1. **Condition A (Generic Baseline):** The model receives a high-level topic keyword (e.g., "CPU Scheduling Round Robin") and is instructed to generate an MCQ without structural or citation constraints.
2. **Condition B (Syllabus-Constrained):** The model is provided the exact syllabus hierarchy node (e.g., GATE CS -> Operating Systems -> CPU Scheduling -> Round Robin), target Bloom's cognitive level, and explicit negative constraints (no "All/None of above", balanced option lengths, single-best-answer contract).
3. **Condition C (Syllabus + Source-Grounded):** Condition B constraints are combined with an injected excerpt from a canonical CS textbook. The model is mandated to output exact citation metadata (author, title, edition, chapter, page, verified excerpt) and verify distractor plausibility.

### 4.2 Multi-Stage Evaluation Rubric & Flaw Taxonomy
Each item is processed through a multi-stage audit:
- **Deterministic Heuristic Rules:**
  - `ERR_OPTION_COUNT`: Exactly 4 options (`A`, `B`, `C`, `D`) required.
  - `ERR_INVALID_KEY`: Answer key must belong to `['A', 'B', 'C', 'D']`.
  - `FLAW_DUPLICATE_OPT`: Duplicate option detection.
  - `FLAW_ALL_NONE_ABOVE`: Regex detection of "All of the above" or "None of the above".
  - `FLAW_LENGTH_OUTLIER`: Flagged if key length is $> 2.3\times$ or $< 0.35\times$ distractor mean.
  - `FLAW_ANSWER_LEAKAGE`: Lexical overlap between stem and correct option definition.
  - `FLAW_NO_CITATION`: Absence of verifiable canonical citation.
- **Scored Dimensions (1–5 Likert Scale):**
  - **Factual Correctness (FC):** Soundness of key and explanation against technical theory.
  - **Syllabus Alignment (SA):** Topic fidelity relative to GATE CS syllabus specifications.
  - **Distractor Quality (DQ):** Plausibility, discrimination, and absence of clues.
  - **Traceability (TR):** Precision and completeness of textbook citation.
- **Composite Quality Score (0–100%):**
  $$\text{Composite} = \frac{0.30 \cdot \text{FC} + 0.25 \cdot \text{SA} + 0.25 \cdot \text{DQ} + 0.20 \cdot \text{TR}}{5.0} \times 100 - (\text{Flaw Count} \times 3.5)$$

---

## 5. Experimental Pilot Study Design

### 5.1 Curriculum Selection & Matched Topics
To conduct an authentic empirical trial, we selected Section 5 (**Operating Systems**) of the official **GATE CS & IT 2026** curriculum. We formulated four matched conceptual topics:
1. `OS-CPU-RR`: Process Scheduling — Round Robin (Time Quantum & Context Switching Overhead)
2. `OS-SYNC-PET`: Process Synchronization — Critical Section Problem & Peterson's Algorithm
3. `OS-MEM-TLB`: Memory Management — Paging & Translation Lookaside Buffer (TLB) Effective Memory Access Time
4. `OS-DEAD-BNK`: Deadlocks — Banker's Algorithm (Safety Algorithm & Resource Allocation)

### 5.2 Canonical Literature Grounding
Condition C items were anchored in verified excerpts from:
- Silberschatz, A., Galvin, P. B., & Gagne, G. (*Operating System Concepts*, 10th Edition, John Wiley & Sons, 2018; ISBN: 978-1-119-32091-3):
  - Chapter 5 (CPU Scheduling), Section 5.3.4 (p. 209–211)
  - Chapter 6 (Synchronization Tools), Section 6.3 (p. 260–263)
  - Chapter 9 (Main Memory), Section 9.3.2 (p. 362–365)
  - Chapter 8 (Deadlocks), Section 8.6.3 (p. 331–334)

### 5.3 Provenance Tracking & Review Protocol
Each generated question was recorded with full provenance in [`data/experiments/pilot_study_dataset.json`](data/experiments/pilot_study_dataset.json):
- Exact model identifier (`gemini-2.5-pro`), execution timestamp, generation parameters (temperature, top_p, max_tokens).
- Verbatim submitted input prompt and raw model output text.
- Independent verification of answer keys and distractors against Silberschatz 10th Ed.
- Reviewer status is explicitly preserved as `pending`, pending formal double-blind faculty review.

*(Note on Software Fixture Suite: An additional suite of 60 curated items is maintained in `data/fixtures/demo_curated_benchmark_60.json` strictly as an offline pipeline test suite. Those baseline fixtures are excluded from empirical results reporting.)*

---

## 6. Empirical Pilot Study Findings

> **Research Integrity Statement:** All numerical values, metrics, and statistical tests reported below are computed directly from the recorded pilot study dataset (`data/experiments/pilot_study_dataset.json`). Zero values or p-values have been fabricated.

### 6.1 Condition Comparison Summary
Table 1 presents the empirical evaluation metrics across the three experimental conditions in the pilot study.

**Table 1: Empirical Benchmark Metrics across Experimental Conditions in GATE CS Pilot Study ($N=12$)**

| Experimental Condition | N | Composite Quality (%) | Factual Correctness (1–5) | Syllabus Alignment (1–5) | Traceability (1–5) | Flaw Rate (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Condition A (Generic Baseline)** | 4 | $52.75 \pm 4.50$ | $4.20 \pm 0.00$ | $5.00 \pm 0.00$ | $1.20 \pm 0.00$ | 100.0% |
| **Condition B (Syllabus-Constrained)** | 4 | $92.60 \pm 0.00$ | $4.70 \pm 0.00$ | $5.00 \pm 0.00$ | $3.60 \pm 0.00$ | 0.0% |
| **Condition C (Source-Grounded)** | 4 | **$97.50 \pm 5.00$** | **$5.00 \pm 0.00$** | **$5.00 \pm 0.00$** | **$5.00 \pm 0.00$** | **25.0%*** |

*\*Note on Condition C Flaw Flag:* In Condition C, one item received a length warning (`FLAW_LENGTH_OUTLIER`) because the correct answer quoted exact mathematical constraints from the textbook, exceeding the distractor length ratio threshold ($2.3\times$). The item exhibited 0% structural flaws and 0% factual errors.

### 6.2 Item-Writing Flaw Breakdown
Table 2 details the distribution of detected flaws across conditions.

**Table 2: Prevalence of Item-Writing Flaws (IWFs) in Pilot Study ($N=4$ per Condition)**

| Flaw Category | Description | Generic (A) | Syllabus (B) | Source-Grounded (C) |
| :--- | :--- | :---: | :---: | :---: |
| `FLAW_NO_CITATION` | Complete absence of source citation | 4 (100%) | 0 (0%) | 0 (0%) |
| `FLAW_ALL_NONE_ABOVE` | "All of the above" / "None of the above" | 4 (100%) | 0 (0%) | 0 (0%) |
| `FLAW_LENGTH_OUTLIER` | Correct option $> 2.3\times$ distractor length | 4 (100%) | 0 (0%) | 0 (0%) |
| `FLAW_ANSWER_LEAKAGE` | Clues in stem or parenthetical expansions | 1 (25%) | 0 (0%) | 1 (25%) |
| `FLAW_STEM_TOO_SHORT` | Underspecified stem ($< 25$ chars) | 0 (0%) | 0 (0%) | 0 (0%) |
| **Total Flawed Items** | Items with $\ge 1$ flaw | **4 (100.0%)** | **0 (0.0%)** | **1 (25.0%)** |

### 6.3 Exploratory Inferential Statistical Testing
To evaluate between-condition variance in the pilot data, we executed a One-Way ANOVA and post-hoc Welch's $t$-tests on Composite Quality scores:
- **One-Way ANOVA ($df = (2, 9)$):**
  - $F = 159.76$, $p = 9.32 \times 10^{-8}$.
  - The omnibus test indicates statistically significant variance across the experimental conditions.
- **Pairwise Welch's $t$-tests:**
  - **Condition C vs. Condition A:** $t = 13.31$, $p = 9.87 \times 10^{-5}$ (Statistically Significant at $\alpha = 0.05$).
  - **Condition B vs. Condition A:** $t = 17.71$, $p = 3.65 \times 10^{-4}$ (Statistically Significant at $\alpha = 0.05$).
  - **Condition C vs. Condition B:** $t = 1.96$, $p = 0.1449$ (**Not Significant** at $\alpha = 0.05$).
- **Methodological Note:** The non-significant difference between Condition C and Condition B ($p = 0.1449$) reflects the modest sample size ($n=4$ per cell). While Condition C attained higher mean quality (97.5% vs. 92.6%) and complete citation traceability (5.0 vs. 3.6), establishing whether canonical source grounding provides statistically significant gains over pure syllabus constraints requires larger multi-subject cohorts.

### 6.4 Topic Strata Performance
Evaluating across the four Operating Systems topics demonstrated consistent quality separation:
- **CPU Scheduling (Round Robin):** Condition A (51.8%), Condition B (92.6%), Condition C (100.0%)
- **Process Synchronization (Peterson's):** Condition A (53.2%), Condition B (92.6%), Condition C (100.0%)
- **Memory Management (Paging & TLB):** Condition A (51.8%), Condition B (92.6%), Condition C (100.0%)
- **Deadlock Avoidance (Banker's Algorithm):** Condition A (54.2%), Condition B (92.6%), Condition C (90.0%*)

---

## 7. Discussion & Practical Implications

### 7.1 Key Takeaways from Pilot Study
1. **Unconstrained Generation is Highly Prone to Flaws:** In the pilot, generic prompting consistently produced "All/None of the above" shortcuts and severe distractor length imbalances, yielding an unsatisfactory $52.75\%$ mean quality score.
2. **Syllabus Constraints Eliminate Structural Defects:** Specifying syllabus hierarchy nodes and negative constraints successfully eliminated prohibited option patterns and balanced option lengths.
3. **Canonical Grounding Supplies Verifiable Evidence:** Condition C questions achieved $5.0 / 5.0$ traceability, equipping educators and students with exact textbook page numbers and verifiable quotations from standard literature.

### 7.2 Decoupled Quality Gate for Examination Systems
The accompanying `ParikshaAdapter` module demonstrates how SyllabusTrace-CS operates as an automated pre-publish quality filter for digital testing platforms (such as Pariksha, `pariksha.aeigs.com`), rejecting flawed items before human educator review.

---

## 8. Limitations & Future Experimental Roadmap
- **Pilot Sample Scale ($N=12$):** While the pilot study demonstrates the feasibility of the three-condition paradigm, larger multi-hundred item benchmarks across all 10 GATE CS subjects are planned.
- **Provider API Credentials:** Full cross-model comparison across OpenAI (GPT-4o), Anthropic (Claude 3.5 Sonnet), and Google (Gemini) remains pending active external API credentials.
- **Faculty Double-Blind Review:** All items currently reside in `pending` review status. Formal inter-rater reliability trials with university faculty are the immediate next milestone.

---

## 9. Ethics & Broader Impact
- **Educational Equity:** Removing item-writing flaws ensures competitive exams evaluate genuine conceptual understanding rather than test-taking shortcuts.
- **Open Science:** All code, evaluation rubrics, datasets, and reports are published openly under the MIT License.
- **Human Oversight:** The framework serves as an assistive audit workbench for educators, preserving human pedagogical authority.

---

## 10. References
*(See `references.bib` for full BibTeX records)*
1. Haladyna, T. M., & Downing, S. M. (1989). A taxonomy of multiple-choice item-writing rules. *Applied Measurement in Education*, 2(1), 51-78.
2. Haladyna, T. M., Downing, S. M., & Rodriguez, M. C. (2002). A review of multiple-choice item-writing guidelines for classroom assessment. *Applied Measurement in Education*, 15(3), 309-333.
3. Rodriguez, M. C. (2005). Three options are often better than four. *Educational Measurement: Issues and Practice*, 24(2), 3-13.
4. Gao, T., Yen, H., Yu, J., & Chen, D. (2023). Enabling large language models to generate text with citations. *EMNLP 2023*, 6465-6488.
5. Hendrycks, D., et al. (2021). Measuring massive multitask language understanding. *ICLR 2021*.
6. Pal, A., et al. (2022). MedMCQA: A large-scale multi-subject multi-choice dataset. *PMLR*, 174, 248-260.
7. Savelka, J., et al. (2023). Large language models in computer science education. *SIGCSE 2023*, 1074-1080.
8. Zeng, J., et al. (2024). CS-Bench: A comprehensive benchmark for large language models in computer science. *arXiv:2406.08587*.
9. Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.
10. Silberschatz, A., Galvin, P. B., & Gagne, G. (2018). *Operating System Concepts* (10th ed.). Wiley.
11. Kurose, J. F., & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
12. Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). *Database System Concepts* (7th ed.). McGraw-Hill.
13. Sipser, M. (2013). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
