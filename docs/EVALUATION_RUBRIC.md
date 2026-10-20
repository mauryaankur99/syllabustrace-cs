# EVALUATION_RUBRIC.md — Multi-Stage Evaluation Rubric & Flaw Taxonomy

## 1. Quality Dimensions (1–5 Likert Scale)

### 1. Factual Correctness (FC)
- **Score 5 (Flawless):** The designated answer is scientifically, mathematically, and empirically accurate according to canonical CS references. Explanation is rigorous and contains zero conceptual flaws.
- **Score 4 (Minor Nit):** The designated answer is correct, but explanation contains minor stylistic ambiguity or imprecise notation.
- **Score 3 (Debatable / Context-Dependent):** The key is valid only under specific implicit assumptions not stated in the stem (e.g., assumes 32-bit architecture without specifying).
- **Score 2 (Erroneous Key or Explanation):** The explanation contradicts standard definitions, or another option is equally or more correct.
- **Score 1 (Factual Hallucination):** The key is blatantly false, refers to non-existent algorithms/protocols, or miscalculates fundamental quantities.

### 2. Syllabus Alignment (SA)
- **Score 5 (Directly on Target):** Exactly targets the intended subtopic within the official GATE CS / UGC NET syllabus at the appropriate depth.
- **Score 4 (Broadly Aligned):** Belongs to the broader subject area, though slightly tangential to the designated subtopic.
- **Score 3 (Marginal / Prerequisite):** Covers basic high-school prerequisites or advanced graduate research outside the core competitive syllabus.
- **Score 2 (Out of Scope):** Asks about irrelevant proprietary technologies, vendor specific syntax (e.g., Oracle PL/SQL quirks rather than standard relational algebra).
- **Score 1 (Domain Mismatch):** Asks about completely unrelated domains (e.g., mechanical hardware or general trivia).

### 3. Single-Best-Answer Validity (SBAV) & Distractor Plausibility
- **Score 5 (Optimal Discrimination):** Exactly one unambiguously correct answer. All three distractors are plausible, non-overlapping, and represent authentic student misconceptions.
- **Score 4 (Good Distractors):** Clear single answer; 2 of 3 distractors are strong, 1 is slightly easy to eliminate.
- **Score 3 (Partial Ambiguity):** One distractor could be argued as partially correct depending on terminology.
- **Score 2 (Multiple Correct or All Implausible):** Two options are virtually indistinguishable in validity, or 2+ distractors are nonsensical.
- **Score 1 (Fatal Item Design):** No correct answer exists, or all four options are correct.

### 4. Source Traceability & Precision (STCP)
- **Score 5 (Verifiable Citation):** Explicit canonical textbook name, edition, chapter, and verified excerpt directly corroborating the answer.
- **Score 4 (Accurate Reference):** Correct book and chapter cited, but excerpt is slightly generalized.
- **Score 3 (Vague / General):** Cites a standard book title with no chapter, page, or corroborating quote.
- **Score 2 (Mismatched Source):** Cites a book that does not cover the topic (e.g., citing Kurose-Ross for Relational Normalization).
- **Score 1 (Hallucinated Source):** Fabricated author, non-existent book, or falsified quotation.

---

## 2. Automated Item-Writing Flaw (IWF) Taxonomy
Automated regex and lexical heuristics flag the following defect codes:

| Flaw Code | Description | Rule Heuristic |
| :--- | :--- | :--- |
| `ERR_OPTION_COUNT` | Non-standard format | Options count != 4 (missing A, B, C, or D) |
| `ERR_INVALID_KEY` | Corrupt answer key | Key is not one of `['A', 'B', 'C', 'D']` |
| `FLAW_DUPLICATE_OPT`| Duplicate choices | Any two options are identical (case-insensitive) |
| `FLAW_ALL_NONE_ABOVE`| "All/None of the above" | Option contains "All of the above" or "None of the above" |
| `FLAW_ANSWER_LEAKAGE`| Clue in stem | Key contains distinctive n-gram (>4 chars) repeated exclusively from stem |
| `FLAW_LENGTH_OUTLIER`| Unbalanced length | Correct option is >2.5x longer or shorter than average distractor length |
| `FLAW_NO_CITATION` | Untraced evidence | Missing source reference or empty verified quote |
| `FLAW_STEM_TOO_SHORT`| Underspecified stem | Stem length < 25 characters |
