# SyllabusTrace-CS: A Source-Traceable Quality Benchmark for AI-Generated Computer Science Multiple-Choice Questions in Indian Competitive Examinations

**Author:** Ankur Maurya  
*Independent Researcher & Software Engineer, Gujarat, India*  
*Correspondence:* `mauryaankur99@gmail.com` | `https://github.com/mauryaankur99/syllabustrace-cs`  

---

## Abstract
Large Language Models (LLMs) are increasingly explored for automated question generation in digital education. However, unconstrained prompting in high-stakes competitive examinations—such as the Graduate Aptitude Test in Engineering (GATE CS) and UGC NET in India—frequently risks generating invalid items afflicted by psychometric Item-Writing Flaws (IWFs), out-of-syllabus drift, and ungrounded answer keys lacking verifiable textbook provenance. We introduce **SyllabusTrace-CS**, an open-source evaluation framework, psychometric audit engine, and research workbench designed to evaluate and trace AI-generated Computer Science multiple-choice questions (MCQs). We formulate a controlled three-condition experimental paradigm: **Condition A (Generic Baseline)**, **Condition B (Syllabus-Constrained)**, and **Condition C (Syllabus + Canonical Source-Grounded)** across five core computer science curricula (Operating Systems, DBMS, Computer Networks, Data Structures & Algorithms, and Theory of Computation). We implement deterministic heuristic detection for seven flaw categories, a multi-dimensional scoring rubric, and live API generator adapters for major providers (Google Gemini, OpenAI, Anthropic) with end-to-end provenance tracking. To validate the audit pipeline, we evaluate an initial curated baseline suite of $N=60$ illustrative prototype fixtures. On these baseline fixtures, unconstrained items deliberately exhibit high flaw prevalence (missing citations, distractor length imbalances, answer leakage), whereas structured syllabus and textbook-grounded fixtures demonstrate rigorous citation capture and balanced option profiles. We present the system architecture, reproducible test suite, and prototype fixture analysis, while transparently documenting the experimental protocol and credential prerequisites required for full-scale live frontier model benchmarking.

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

## 5. Benchmark Dataset & Fixture Construction

### 5.1 Curated Prototype Baseline Fixtures
To validate the deterministic heuristics, scoring rubrics, and web workbench prior to executing large-scale funded API runs, a curated baseline fixture suite of $N=60$ items was authored across five foundational subjects matching the official GATE CS & IT 2026 syllabus:
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

### 5.2 Provenance and Data Tier Separation
All records are explicitly partitioned by data tier:
- `data_tier = "illustrative_fixture"`: Baseline test fixtures used for pipeline validation. In accordance with scientific integrity standards, simulated/fixture records are tagged as `is_simulated = True` with `review_status = "pending"`, and are excluded by default from claims of verified live AI model performance.
- `data_tier = "experimental_run"`: Dedicated tier reserved for genuine live model generation outputs, capturing model ID, timestamp, full raw API prompts and responses, provider parameters, and reviewer validations.

---

## 6. Implementation Verification & Prototype Baseline Findings

> **Research Integrity Notice:** The evaluation framework, scoring heuristics, and live generation engine have been implemented and verified via automated testing. The baseline metrics reported below reflect the **curated prototype fixture suite ($N=60$)**, designed to validate that the automated audit rules correctly identify psychometric flaws and citation metadata. These metrics demonstrate the discriminating power of the evaluation rubric; they are **not** claimed as verified empirical measurements of commercial AI models, which remain subject to live API evaluation runs.

### 6.1 Prototype Fixture Evaluation Metrics
Table 1 summarizes the evaluation metrics across the three conditions on the prototype fixture dataset.

**Table 1: Prototype Fixture Baseline Metrics Across Conditions ($N=60$ Curated Baseline Fixtures)**

| Experimental Condition | N | Composite Quality (%) | Factual Correctness (1–5) | Syllabus Alignment (1–5) | Traceability (1–5) | Flaw Rate (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Condition A (Generic Fixtures)** | 20 | $65.25 \pm 8.51$ | $4.20 \pm 0.00$ | $5.00 \pm 0.00$ | $1.20 \pm 0.00$ | 100.0% |
| **Condition B (Syllabus Fixtures)** | 20 | $92.60 \pm 0.00$ | $4.70 \pm 0.00$ | $5.00 \pm 0.00$ | $3.60 \pm 0.00$ | 0.0% |
| **Condition C (Source-Grounded Fixtures)** | 20 | $98.55 \pm 3.55$ | $5.00 \pm 0.00$ | $5.00 \pm 0.00$ | $5.00 \pm 0.00$ | 15.0%* |

*\*Note on Condition C Flaw Rate:* In the fixture baseline, 3 Condition C items received a heuristic length warning (`FLAW_LENGTH_OUTLIER`) because exact mathematical theorem formulations produced a detailed correct answer slightly exceeding the distractor length ratio threshold ($2.3\times$). This confirms that the heuristic audit rules are highly sensitive even to subtle typographical asymmetry.

### 6.2 Heuristic Flaw Detection Sensitivity
Table 2 details the distribution of detected flaws across the baseline fixture suite, illustrating the heuristic engine's ability to isolate specific psychometric defects.

**Table 2: Detection of Item-Writing Flaws (IWFs) on Prototype Fixture Baseline ($N=20$ per Condition)**

| Flaw Category | Description | Generic (A) | Syllabus (B) | Source-Grounded (C) |
| :--- | :--- | :---: | :---: | :---: |
| `FLAW_NO_CITATION` | Complete absence of source citation | 20 (100%) | 0 (0%) | 0 (0%) |
| `FLAW_ALL_NONE_ABOVE` | "All of the above" / "None of the above" | 8 (40%) | 0 (0%) | 0 (0%) |
| `FLAW_LENGTH_OUTLIER` | Correct option $> 2.3\times$ distractor length | 3 (15%) | 0 (0%) | 3 (15%) |
| `FLAW_ANSWER_LEAKAGE` | Clues in stem or parenthetical expansions | 4 (20%) | 0 (0%) | 0 (0%) |
| `FLAW_STEM_TOO_SHORT` | Underspecified stem ($< 25$ chars) | 0 (0%) | 0 (0%) | 0 (0%) |
| **Total Flawed Items** | Items with $\ge 1$ flaw | **20 (100.0%)** | **0 (0.0%)** | **3 (15.0%)** |

### 6.3 Statistical Pipeline Verification
An omnibus One-Way ANOVA and post-hoc Welch's $t$-tests were executed on the fixture baseline scores to confirm that the statistical analysis pipeline operates reliably:
- **Pipeline ANOVA Verification:** $F = 222.60, p = 1.17 \times 10^{-27}$.
- **Methodological Interpretation:** Because the fixture baseline was deliberately constructed with contrasting condition specifications (unconstrained vs. constrained vs. source-grounded), the resulting separation verifies the statistical pipeline's capacity to detect variance across experimental cohorts. Formal empirical p-values describing frontier model performance will be computed from the forthcoming live experimental runs.

### 6.4 Live Model Generation Architecture
The live model generation pipeline in `src/core/generator.py` provides complete API integration for:
- **Google Gemini** (`gemini-1.5-pro`, `gemini-2.0-flash`) via `google-generativeai`.
- **OpenAI** (`gpt-4o`, `gpt-4o-mini`) via `openai`.
- **Anthropic Claude** (`claude-3-5-sonnet-20241022`) via `anthropic`.

Each live call captures:
1. Exact model identifier and generation parameters (temperature, max tokens).
2. Complete raw request prompt and verbatim unparsed response.
3. System timestamps and latency.
4. Parsed JSON structures and validation outcomes.

If API credentials (`GEMINI_API_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`) are unconfigured, the pipeline raises an explicit `ProviderMissingCredentialsError` and refuses to produce ungrounded mock responses disguised as real outputs.

---

## 7. Discussion & Practical Implications

### 7.1 Key Takeaways from Pipeline Prototyping
1. **Automated Flaw Auditing is Feasible:** Deterministic heuristic rules effectively catch common psychometric flaws (e.g., option length outliers, forbidden "All/None" patterns, and missing citations) in fractions of a second without human fatigue.
2. **Citation Traceability Requires Explicit Grounding:** Standard generative prompts do not reliably supply verifiable textbook citations unless supplied with source passages and constrained to cite author, edition, and page.
3. **Decoupled Quality Control:** By incorporating automated pre-generation gates, educational platforms can systematically reject flawed items before manual faculty review.

### 7.2 Integration Bridge with Examination Systems
The accompanying `ParikshaAdapter` module demonstrates how SyllabusTrace-CS connects to production assessment systems (such as Pariksha, `pariksha.aeigs.com`). Acting as an offline quality filter, items achieving $\ge 75\%$ composite score and 0 structural flaws can be exported in standardized JSON format for pedagogical review.

---

## 8. Limitations & Future Experimental Roadmap
- **Prototype Baseline Scope:** The current benchmark numbers reflect a 60-item curated fixture baseline used for pipeline validation. Live model execution across frontier LLMs is architected and pending API key provisioning.
- **Human Expert Verification:** Review records currently reside in a `pending` status. Conducting formal double-blind inter-rater reliability studies with university Computer Science faculty is the immediate next experimental objective.
- **Syllabus Coverage:** The current baseline exercises five core subjects (OS, DBMS, CN, DSA, TOC). Expanding to the complete 10-subject GATE CS curriculum and state engineering syllabi represents an ongoing engineering priority.

---

## 9. Ethics & Broader Impact
- **Assessment Fairness:** Automating psychometric flaw detection helps eliminate superficial test-taking cues, ensuring examinations assess authentic conceptual mastery rather than guessing strategies.
- **Open Science & Transparency:** All evaluation algorithms, scoring rubrics, benchmark fixtures, and reproduction scripts are published openly under the MIT License to facilitate independent audit and replication.
- **Human Oversight:** The platform is explicitly designed as an assistive evaluation workbench for educators, preserving human pedagogical authority over question publication.

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
