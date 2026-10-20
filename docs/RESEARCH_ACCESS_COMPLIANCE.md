# Research Purpose, Governance, and Access Program Clarification

## 1. Research Purpose & Intended Use
**SyllabusTrace-CS** is an open-source scientific research evaluation framework and audit workbench designed to investigate the psychometric quality, item-writing flaws (IWFs), syllabus alignment, and source traceability of AI-generated multiple-choice questions (MCQs) in higher-education Computer Science (targeting curricula such as GATE CS and UGC NET).

The primary purpose of this project is non-commercial academic inquiry and methodology development:
- To establish reproducible metrics for evaluating psychometric validity and hallucination in technical assessment items.
- To compare generation conditions (zero-shot baseline, syllabus-constrained, and evidence-grounded retrieval generation).
- To provide an open-source, reproducible workbench for educators and researchers to inspect, audit, and benchmark synthetic assessment items.

---

## 2. Researcher Status & Institutional Affiliations
- **Author / Lead Developer:** Ankur Maurya
- **Status:** Independent Researcher and Computer Science & Engineering Graduate (Gujarat, India).
- **Affiliation Disclaimer:** The author is an independent researcher and does **not** claim an active university faculty appointment, formal doctoral/postdoctoral appointment, institutional grant award, or formal institutional endorsement from any university or academic institution.
- **Independence:** While the author has independently built web and educational software tools (such as Pariksha), SyllabusTrace-CS is maintained separately as an open-source scientific workbench.

---

## 3. Clear Distinction: Project Design vs. Grant/Program Eligibility Requirements
Many computational research-access programs (such as the OpenAI Researcher Access Program, Anthropic Research Grants, and Google Cloud Research Credits) maintain stringent criteria for subsidized model access or research grants. 

**Important Clarification on Eligibility:**
1. **No Guarantee of Eligibility:** Structuring SyllabusTrace-CS as an open-source, non-commercial GitHub repository **does not** guarantee eligibility, acceptance, or compute grants from any external research-access provider.
2. **Institutional Affiliation Requirements:** Most major academic access programs explicitly require primary affiliation with an accredited degree-granting academic institution (e.g., full-time faculty, PhD candidate, or recognized post-doctoral fellow). Independent researchers who do not hold active institutional credentials may not qualify under the terms of those specific institutional programs.
3. **Transparent Positioning:** This project does not misrepresent its author's standing or claim institutional backing to meet third-party grant criteria. If grant applications are made, they will truthfully represent the independent status of the researcher and the open-source nature of the work.

---

## 4. Project-Level Non-Commercial Architecture
While project design cannot substitute for institutional credentials, the repository adheres strictly to non-commercial open-source scientific principles:
1. **Public & Open Source:** Licensed under the MIT License for public reproducibility and peer review.
2. **Decoupled from Commercial Systems:** The repository contains no monetization, paywalls, premium subscriptions, or user ad tracking.
3. **Adapter Isolation:** Any external system bridges (such as the Pariksha adapter in `src/integrations/pariksha_adapter.py`) exist strictly as offline case-study export/import conduits to evaluate how research benchmarks interface with real-world LMS/question-bank formats. SyllabusTrace-CS operates independently of production student databases or commercial operations.
4. **Reproducible Artifacts:** Experimental configurations, pipeline code, fixture datasets, figures, and manuscripts are version-controlled openly.

---

## 5. Scope of Contributions & Limitations
- **Current Artifacts:** The current repository includes the complete evaluation engine, psychometric IWF detector, automated report generators, and a pilot benchmark fixture suite ($N=60$ items across 5 CS disciplines).
- **Model Experiment Execution:** Automated generation pipelines for live LLM providers (Google Gemini, OpenAI, Anthropic) are fully architected in `src/core/generator.py` with structured provenance tracking. Full-scale empirical evaluation runs depend on user-provided API credentials. Baseline pilot data are clearly labeled as illustrative prototype fixtures pending funded or provisioned live model execution.
