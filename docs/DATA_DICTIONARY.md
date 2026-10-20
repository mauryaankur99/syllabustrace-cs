# DATA_DICTIONARY.md — Data Schemas & Entity Definitions

## 1. Syllabus Schema (`SyllabusNode`)
Represents the hierarchical breakdown of an exam syllabus.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | string | Unique node identifier (e.g., `gate-cs-os-concurrency`) |
| `exam` | string | Standardized exam code (`GATE_CS`, `UGC_NET_CS`, `GPSC_CS`) |
| `subject` | string | Primary subject (`Operating Systems`, `DBMS`, etc.) |
| `topic` | string | Major topic heading (`Concurrency & Synchronization`) |
| `subtopic` | string | Fine-grained conceptual subtopic (`Deadlock Prevention & Avoidance`) |
| `cognitive_level` | string | Target Bloom's tier (`Recall`, `Comprehension`, `Application`, `Analysis`) |
| `official_doc_ref`| string | Official syllabus document section or notification link |

---

## 2. Canonical Source Schema (`SourceRecord`)
Represents an authoritative academic textbook, research paper, or official specification.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | string | Unique source identifier (e.g., `src-silberschatz-os10`) |
| `title` | string | Full textbook or publication title |
| `authors` | array[string]| List of authors |
| `edition` | string | Published edition (e.g., `10th Edition`) |
| `year` | integer | Publication year |
| `publisher` | string | Publishing house or journal |
| `isbn` | string | ISBN-10/13 or DOI |
| `domain` | string | Relevant CS discipline |
| `chapters` | array[object]| Chapter index mapping topics to verified page ranges |

---

## 3. Multiple-Choice Question Schema (`MCQRecord`)
The core benchmark entity.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | string | UUID (e.g., `mcq-os-cond-c-001`) |
| `stem` | string | The question prompt |
| `options` | object | Dictionary mapping keys `A`, `B`, `C`, `D` to option strings |
| `correct_key` | string | Designated correct answer (`A`, `B`, `C`, or `D`) |
| `explanation` | string | Pedagogical explanation justifying why the key is correct |
| `condition` | string | Experimental generation condition (`generic`, `syllabus_constrained`, `source_grounded`) |
| `syllabus_node_id`| string | Foreign key referencing `SyllabusNode.id` |
| `subject` | string | CS Subject domain |
| `source_citation` | object | `{ "source_id": str, "citation_text": str, "chapter": str, "page": str, "verified_excerpt": str }` |
| `model_metadata` | object | `{ "provider": str, "model": str, "temperature": float, "prompt_version": str }` |
| `review_status` | string | `pending`, `approved`, `rejected`, `flagged` |
| `flaw_flags` | array[string]| Detected flaw codes (e.g., `ANSWER_LEAKAGE`, `IMPLAUSIBLE_DISTRACTORS`) |
| `scores` | object | Normalized evaluation scores `{ "factual_correctness": 1-5, "syllabus_alignment": 1-5, "distractor_quality": 1-5, "traceability": 1-5, "composite_quality": 0-100 }` |
| `reviewer_notes` | string | Free-form review comments |
| `created_at` | string | ISO-8601 timestamp |
| `updated_at` | string | ISO-8601 timestamp |

---

## 4. Experiment Run Schema (`ExperimentRun`)
Represents an auditable comparative trial.

| Field | Type | Description |
| :--- | :--- | :--- |
| `id` | string | Experiment identifier (e.g., `exp-pilot-gate-2026-v1`) |
| `name` | string | Human-readable experiment title |
| `status` | string | `planned`, `running`, `completed` |
| `sample_size` | integer | Total question count across all conditions |
| `conditions` | array[string]| Conditions evaluated (`generic`, `syllabus_constrained`, `source_grounded`) |
| `metrics_summary` | object | Aggregated scores and statistical significance outputs |
| `timestamp` | string | Execution completion timestamp |
