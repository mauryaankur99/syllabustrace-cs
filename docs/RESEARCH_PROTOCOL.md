# RESEARCH_PROTOCOL.md — Experimental Protocol & Design

## 1. Experimental Conditions
The benchmark executes a controlled comparative study across three distinct prompt-engineering and grounding conditions:

### Condition A: Generic Topic Prompting (Baseline)
- **Input:** Subject name, topic keyword, desired difficulty.
- **Prompt Structure:** Simple instruction asking the model to write a multiple-choice question on the topic.
- **Constraints:** Minimal formatting instructions only. No syllabus hierarchy or source citations required.

### Condition B: Syllabus-Constrained Prompting
- **Input:** Exact syllabus hierarchical node (Subject -> Topic -> Subtopic), exam body (e.g., GATE CS 2026), and designated Bloom's cognitive level.
- **Prompt Structure:** Explicit instructions bounding the question strictly within the syllabus scope. Mandates item-writing conventions (4 distinct options, no "all/none of the above", balanced distractor lengths).
- **Constraints:** Pedagogical and structural bounds; no explicit textbook passage provided.

### Condition C: Syllabus + Source-Grounded Prompting
- **Input:** Syllabus node + verified canonical textbook reference (title, edition, chapter, core excerpt / theorem definition).
- **Prompt Structure:** Model must derive the stem and single correct answer directly from the supplied canonical excerpt. Distractors must target documented misconceptions. Explicit output fields for citation and evidence quote.
- **Constraints:** High factual anchoring, verifiable citation requirement, distractor rationale generation.

---

## 2. Benchmark Subject Domain & Strata
To ensure representative coverage of the standard CS curriculum, experiments sample across 5 foundational subjects:
1. **Operating Systems (OS):** CPU Scheduling, Virtual Memory & Paging, Concurrency & Synchronization, Deadlocks, File Systems.
2. **Database Management Systems (DBMS):** Relational Algebra, Normalization & Normal Forms, Transaction Processing & ACID, Concurrency Control (2PL, Serializability), Indexing (B/B+ Trees).
3. **Computer Networks (CN):** OSI/TCP-IP Architecture, Flow & Error Control, Routing Algorithms, Transport Layer Protocols (TCP/UDP), Application Layer (DNS, HTTP).
4. **Data Structures & Algorithms (DSA):** Asymptotic Analysis, Tree Traversal & Balancing, Graph Algorithms (Dijkstra, Prim/Kruskal), Dynamic Programming, Sorting & Searching.
5. **Theory of Computation (TOC):** Regular Expressions & Finite Automata, Context-Free Grammars & Pushdown Automata, Turing Machines & Decidability, Chomsky Hierarchy.

---

## 3. Evaluation Metrics
Each question is evaluated along 6 quantitative and qualitative dimensions:

1. **Factual Correctness (FC) [1–5 scale & Binary %]:** Is the designated key indisputably true and factual according to standard computer science principles?
2. **Syllabus Alignment (SA) [1–5 scale & Binary %]:** Does the item test concepts strictly inside the target syllabus subtopic without out-of-scope drift?
3. **Single-Best-Answer Validity (SBAV) [Binary %]:** Is there exactly one unambiguously correct answer, with three distinctly incorrect distractors?
4. **Source Traceability & Precision (STCP) [1–5 scale]:** Does the citation accurately reference real literature, and does the excerpt directly support the key?
5. **Distractor Quality Index (DQI) [1–5 scale]:** Are distractors plausible, non-overlapping, grammatically parallel, and reflective of authentic student errors?
6. **Item-Writing Flaw Rate (IWFR) [% of questions with >= 1 flaw]:** Proportion of items displaying flaws such as answer leakage, negative stems, length mismatch, or vague terminology.

---

## 4. Statistical Analysis Plan
- **Descriptive Statistics:** Mean, Standard Deviation, and Confidence Intervals (95% CI) computed per condition and subject.
- **Hypothesis Testing:**
  - One-Way ANOVA or Kruskal-Wallis non-parametric tests across Conditions A, B, and C.
  - Pairwise post-hoc tests (Tukey HSD or Mann-Whitney U with Bonferroni correction) comparing Condition C vs A and Condition B vs A.
  - Chi-square ($\chi^2$) test for categorical flaw rates.
- **Inter-Rater Reliability:** Cohen's Kappa ($\kappa$) when secondary human review annotations are available.
