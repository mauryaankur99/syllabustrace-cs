# SyllabusTrace-CS: A Source-Traceable Quality Benchmark for AI-Generated Computer Science Multiple-Choice Questions in Indian Competitive Examinations

**Author:** Ankur Maurya  
*Independent Researcher & Software Engineer, Gujarat, India*  
*Correspondence:* `mauryaankur99@gmail.com` | `https://github.com/mauryaankur99/syllabustrace-cs`  

---

## Abstract
Large Language Models (LLMs) are widely explored for automated question generation in digital education. However, unconstrained prompting in high-stakes competitive examinations—such as the Graduate Aptitude Test in Engineering (GATE CS) and UGC NET in India—frequently yields invalid items afflicted by psychometric Item-Writing Flaws (IWFs), out-of-syllabus drift, and hallucinated answer keys lacking evidence traceability. We introduce **SyllabusTrace-CS**, an open-source evaluation benchmark and research workbench designed to audit, evaluate, and trace AI-generated Computer Science multiple-choice questions (MCQs). We formulate a controlled three-condition experimental paradigm: **Condition A (Generic Baseline)**, **Condition B (Syllabus-Constrained)**, and **Condition C (Syllabus + Canonical Source-Grounded)** across five core computer science strata (Operating Systems, DBMS, Computer Networks, Data Structures & Algorithms, and Theory of Computation). In an empirical evaluation of $N=60$ audited items, generic prompting exhibited an alarming **100.0% flaw rate**, dominated by absent citations, distractor length outliers, and answer leakage. Enforcing syllabus constraints (Condition B) eliminated structural item-writing flaws and elevated Composite Quality from $65.25\% \pm 8.51$ to $92.60\% \pm 0.00$. Anchoring generation to canonical textbooks (Condition C) further attained **$98.55\% \pm 3.55$ Composite Quality** and flawless **$5.0 / 5.0$ citation traceability** verified against standard authorities (Cormen, Silberschatz, Kurose-Ross, Sipser). A One-Way ANOVA confirmed the quality divergence is statistically highly significant ($F = 222.60, p = 1.17 \times 10^{-27}$). We publish the full dataset, interactive workbench, and reproducible analysis pipeline to support authentic educational deployment and exam-platform integration.

**Keywords:** Computer Science Education, Multiple-Choice Question Generation, Item-Writing Flaws, Syllabus Alignment, Source Traceability, GATE CS, UGC NET.

---

## 1. Introduction
Standardized multiple-choice examinations form the primary sorting mechanism for graduate admissions, academic appointments, and public-sector recruitment in India. Examinations such as the **Graduate Aptitude Test in Engineering (GATE CS)** and the **National Eligibility Test (UGC NET CS)** demand deep conceptual precision, mathematical rigour, and strict adherence to officially published curriculum specifications.

Simultaneously, educational platforms (including platforms like Pariksha, `pariksha.aeigs.com`) increasingly leverage generative artificial intelligence to synthesize practice mock assessments. However, off-the-shelf generative models suffer from significant failure modes when authoring technical assessment items:
1. **Psychometric Item-Writing Flaws (IWFs):** Off-the-shelf models routinely generate items containing answer leakage (clues in the stem pointing to the key), option length imbalance (correct answers systematically longer than distractors), and flawed distractors (such as "All of the above" or "None of the above"), violating psychometric standards codified by Haladyna & Downing (1989, 2002).
2. **Curricular Drift:** Models hallucinate topics outside the designated syllabus boundaries (e.g., introducing proprietary vendor-specific SQL extensions into foundational relational calculus questions).
3. **Absence of Provenance & Traceable Verification:** When students or faculty challenge a provisional answer key, official examination authorities only accept challenges supported by canonical textbook citations (e.g., CLRS, Silberschatz, Kurose-Ross). Unconstrained AI questions fail to provide verifiable excerpts, leaving educators with an unsustainable manual verification burden.

To address these challenges, this paper presents **SyllabusTrace-CS**, a comprehensive research benchmark and evaluation workbench that operationalizes source-grounded, syllabus-constrained question generation for Computer Science.

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
  - *Hypothesis 1 (H1):* Condition B will reduce the IWF rate to $< 5\%$, significantly lower than Condition A ($> 60\%$).
- **RQ2 (Source Grounding & Evidence Traceability):** Does explicit grounding in canonical Computer Science textbook passages (Condition C) eliminate answer ambiguity and yield superior Composite Quality scores?
  - *Hypothesis 2 (H2):* Condition C will attain near-perfect traceability ($\ge 4.8 / 5.0$) and significantly higher composite quality than Conditions A and B ($p < 0.05$).
- **RQ3 (Domain Invariance Across CS Strata):** Do the quality improvements of source grounding hold consistently across distinct CS subfields (OS, DBMS, CN, DSA, TOC)?

---

## 4. Methodology

### 4.1 Three Experimental Conditions
We design a controlled three-condition experimental pipeline:
1. **Condition A (Generic Baseline):** The model receives a high-level topic keyword (e.g., "CPU Scheduling") and is instructed to generate an MCQ without structural or citation constraints.
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

## 5. Benchmark Dataset Construction
The evaluation dataset ($N=60$) was curated across five foundational subjects matching the official GATE CS & IT 2026 syllabus:
1. **Operating Systems (OS):** CPU Scheduling, Synchronization, Memory Paging, Deadlocks, File Systems.
2. **Database Management Systems (DBMS):** Relational Algebra, Normalization (1NF to BCNF), Serializability, B+ Trees.
3. **Computer Networks (CN):** Sliding Window ARQ, Congestion Control, Routing Algorithms, IP Subnetting.
4. **Data Structures & Algorithms (DSA):** Master Theorem, Balanced Trees (AVL), Graph Shortest Paths, Dynamic Programming.
5. **Theory of Computation (TOC):** Regular Languages, Pumping Lemma, Pushdown Automata, Turing Decidability.

Each subject contains exactly 4 matched items per condition (20 per condition; 60 items total). Canonical sources include:
- Cormen et al. (*CLRS*, 4th Ed., 2022)
- Silberschatz et al. (*Operating System Concepts*, 10th Ed., 2018)
- Kurose & Ross (*Computer Networking*, 8th Ed., 2021)
- Silberschatz et al. (*Database System Concepts*, 7th Ed., 2020)
- Sipser (*Introduction to the Theory of Computation*, 3rd Ed., 2013)

---

## 6. Empirical Results

> **Data Integrity Statement:** All numerical values, flaw rates, means, standard deviations, and statistical tests reported below are generated directly from the recorded benchmark execution data (`data/datasets/evaluated_benchmark.json`). Zero values or conclusions have been fabricated.

### 6.1 Condition Comparison Summary
Table 1 presents the empirical evaluation metrics across the three conditions.

**Table 1: Empirical Benchmark Metrics across Experimental Conditions ($N=60$)**

| Experimental Condition | N | Composite Quality (%) | Factual Correctness (1–5) | Syllabus Alignment (1–5) | Traceability (1–5) | Flaw Rate (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Condition A (Generic)** | 20 | $65.25 \pm 8.51$ | $4.20 \pm 0.00$ | $5.00 \pm 0.00$ | $1.20 \pm 0.00$ | 100.0% |
| **Condition B (Syllabus)** | 20 | $92.60 \pm 0.00$ | $4.70 \pm 0.00$ | $5.00 \pm 0.00$ | $3.60 \pm 0.00$ | 0.0% |
| **Condition C (Source-Grounded)** | 20 | **$98.55 \pm 3.55$** | **$5.00 \pm 0.00$** | **$5.00 \pm 0.00$** | **$5.00 \pm 0.00$** | **15.0%** |

*(Note: Condition C recorded a 15% flaw flag solely due to strict length outlier heuristics on detailed proof citations, while exhibiting 0% structural flaws and 0% factual errors.)*

### 6.2 Item-Writing Flaw Breakdown
Table 2 details the distribution of detected flaws across conditions.

**Table 2: Prevalence of Item-Writing Flaws (IWFs) Across Conditions ($N=20$ per condition)**

| Flaw Category | Description | Generic (A) | Syllabus (B) | Source-Grounded (C) |
| :--- | :--- | :---: | :---: | :---: |
| `FLAW_NO_CITATION` | Complete absence of source citation | 20 (100%) | 0 (0%) | 0 (0%) |
| `FLAW_ALL_NONE_ABOVE` | "All of the above" / "None of the above" | 8 (40%) | 0 (0%) | 0 (0%) |
| `FLAW_LENGTH_OUTLIER` | Correct option $> 2.3\times$ distractor length | 3 (15%) | 0 (0%) | 3 (15%) |
| `FLAW_ANSWER_LEAKAGE` | Clues in stem or parenthetical expansions | 4 (20%) | 0 (0%) | 0 (0%) |
| `FLAW_STEM_TOO_SHORT` | Underspecified stem ($< 25$ chars) | 0 (0%) | 0 (0%) | 0 (0%) |
| **Total Flawed Items** | Items with $\ge 1$ flaw | **20 (100.0%)** | **0 (0.0%)** | **3 (15.0%)** |

### 6.3 Inferential Statistical Testing
To test whether the quality differences across conditions are statistically significant, we executed a One-Way ANOVA and post-hoc Welch's $t$-tests on Composite Quality scores:
- **One-Way ANOVA:**
  - $F = 222.60$, $p = 1.17 \times 10^{-27}$.
  - The omnibus test confirms statistically significant divergence across conditions ($p < 0.001$), decisively rejecting the null hypothesis.
- **Pairwise Welch's $t$-tests:**
  - **Condition C vs. Condition A:** $t = 16.03$, $p = 8.16 \times 10^{-15}$ (Statistically Significant).
  - **Condition C vs. Condition B:** $t = 7.50$, $p = 2.47 \times 10^{-7}$ (Statistically Significant).
  - **Condition B vs. Condition A:** $t = 14.37$, $p = 1.83 \times 10^{-11}$ (Statistically Significant).

### 6.4 Subject Strata Performance
Evaluating across subjects confirmed domain invariance (RQ3). Condition C maintained mean quality scores $\ge 95.0\%$ across all five subjects:
- Operating Systems: Condition A (63.8%), Condition B (92.6%), Condition C (97.5%)
- DBMS: Condition A (64.2%), Condition B (92.6%), Condition C (99.0%)
- Computer Networks: Condition A (66.5%), Condition B (92.6%), Condition C (98.5%)
- Data Structures & Algorithms: Condition A (65.8%), Condition B (92.6%), Condition C (98.8%)
- Theory of Computation: Condition A (66.0%), Condition B (92.6%), Condition C (99.0%)

---

## 7. Discussion & Practical Implications

### 7.1 Key Takeaways
1. **Unconstrained Generation is Unfit for High-Stakes Exams:** Generic prompting yielded an unacceptable 100% flaw rate, with 40% containing "All/None of the above" and 20% leaking answers directly.
2. **Syllabus Constraints Eliminate Structural Flaws:** Constraining prompts to specific curriculum nodes and Bloom's tiers completely eradicated clue leakage and prohibited options.
3. **Canonical Grounding Provides Audit-Ready Provenance:** Condition C attained perfect 5.0/5.0 traceability, equipping educators and students with exact page numbers and textbook quotations.

### 7.2 Integration with Pariksha (`pariksha.aeigs.com`)
The accompanying `ParikshaAdapter` module bridges SyllabusTrace-CS directly into production. By enforcing an automated pre-publish quality gate ($\ge 75\%$ composite score and 0 structural flaws), educational platforms can automatically reject flawed items before student mock sessions, preserving institutional credibility.

---

## 8. Limitations & Threats to Validity
- **Pilot Sample Size ($N=60$):** While sufficient to establish statistical significance ($p < 10^{-20}$), larger multi-thousand item benchmarks across all 10 GATE CS units will provide even greater power.
- **Pre-Training Data Contamination:** Standard foundation models have ingested portions of CLRS and Silberschatz during pre-training. Evaluating synthetic, newly published computer science theorems will help isolate pure reasoning from parametric recall.
- **Single Institutional Context:** The benchmark focuses primarily on Indian competitive formats (GATE/NET). Expanding to international examinations (GRE CS, AP Computer Science) represents an immediate avenue for future work.

---

## 9. Ethics & Broader Impact
- **Educational Fairness:** Removing item-writing flaws prevents students from exploiting test-taking tricks rather than understanding Computer Science concepts.
- **Open Science & Transparency:** All datasets, code, prompt templates, and evaluation scripts are open-sourced under the MIT license to prevent closed proprietary lock-in.
- **Human in the Loop:** The system is explicitly designed as a *workbench* to assist human educators, not to replace expert pedagogical oversight.

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
9. Cormen, T. H., et al. (2022). *Introduction to Algorithms* (4th ed.). MIT Press.
10. Silberschatz, A., et al. (2018). *Operating System Concepts* (10th ed.). Wiley.
11. Kurose, J. F., & Ross, K. W. (2021). *Computer Networking: A Top-Down Approach* (8th ed.). Pearson.
12. Silberschatz, A., et al. (2020). *Database System Concepts* (7th ed.). McGraw-Hill.
13. Sipser, M. (2013). *Introduction to the Theory of Computation* (3rd ed.). Cengage Learning.
