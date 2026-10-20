"""
evaluator.py — Deterministic and Rubric-Based Evaluation Engine for SyllabusTrace-CS.
Audits Item-Writing Flaws (IWFs), computes 4-dimensional scores, and determines validity.
"""

import re
from typing import Dict, List, Tuple
from .models import MCQRecord, EvaluationResult, EvaluationScores


class Evaluator:
    """Multi-stage evaluation engine for Computer Science MCQs."""

    FLAW_OPTION_COUNT = "ERR_OPTION_COUNT"
    FLAW_INVALID_KEY = "ERR_INVALID_KEY"
    FLAW_DUPLICATE_OPT = "FLAW_DUPLICATE_OPT"
    FLAW_ALL_NONE_ABOVE = "FLAW_ALL_NONE_ABOVE"
    FLAW_ANSWER_LEAKAGE = "FLAW_ANSWER_LEAKAGE"
    FLAW_LENGTH_OUTLIER = "FLAW_LENGTH_OUTLIER"
    FLAW_NO_CITATION = "FLAW_NO_CITATION"
    FLAW_STEM_TOO_SHORT = "FLAW_STEM_TOO_SHORT"

    ALL_NONE_PATTERNS = [
        re.compile(r"\ball\s+of\s+the\s+above\b", re.IGNORECASE),
        re.compile(r"\bnone\s+of\s+the\s+above\b", re.IGNORECASE),
        re.compile(r"\bboth\s+[a-d]\s+and\s+[a-d]\b", re.IGNORECASE),
    ]

    def __init__(self, known_syllabus_nodes: List[str] = None):
        self.known_syllabus_nodes = set(known_syllabus_nodes or [])

    def evaluate(self, mcq: MCQRecord) -> EvaluationResult:
        flaw_flags = []
        feedback = []

        # 1. Structural Checks
        options = mcq.options or {}
        req_keys = {"A", "B", "C", "D"}
        if set(options.keys()) != req_keys or any(not str(v).strip() for v in options.values()):
            flaw_flags.append(self.FLAW_OPTION_COUNT)
            feedback.append("Options must contain non-empty entries for A, B, C, and D.")

        # 2. Key Validity Check
        if mcq.correct_key not in req_keys:
            flaw_flags.append(self.FLAW_INVALID_KEY)
            feedback.append(f"Correct key '{mcq.correct_key}' is not in [A, B, C, D].")

        # 3. Duplicate Options Check
        normalized_opts = [str(v).strip().lower() for v in options.values()]
        if len(normalized_opts) != len(set(normalized_opts)):
            flaw_flags.append(self.FLAW_DUPLICATE_OPT)
            feedback.append("Two or more answer options are identical or duplicate.")

        # 4. 'All / None of the above' Anti-Pattern
        for opt_k, opt_v in options.items():
            for pat in self.ALL_NONE_PATTERNS:
                if pat.search(opt_v):
                    flaw_flags.append(self.FLAW_ALL_NONE_ABOVE)
                    feedback.append(f"Option {opt_k} uses prohibited '{pat.pattern}' anti-pattern.")
                    break

        # 5. Length Outlier Heuristic
        if mcq.correct_key in options:
            correct_len = len(str(options[mcq.correct_key]).strip())
            distractor_lens = [
                len(str(v).strip()) for k, v in options.items() if k != mcq.correct_key and str(v).strip()
            ]
            if distractor_lens:
                avg_dist_len = sum(distractor_lens) / len(distractor_lens)
                if avg_dist_len > 0:
                    ratio = correct_len / avg_dist_len
                    if ratio >= 2.3 or ratio <= 0.35:
                        flaw_flags.append(self.FLAW_LENGTH_OUTLIER)
                        feedback.append(f"Correct option length ({correct_len} chars) is unbalanced compared to distractors (avg {avg_dist_len:.1f} chars, ratio {ratio:.2f}).")

        # 6. Answer Leakage Heuristic
        if mcq.correct_key in options and mcq.stem:
            stem_lower = mcq.stem.lower()
            key_text = str(options[mcq.correct_key]).lower()
            # Extract parenthetical expansions or long verbatim definitions in key matching stem keywords
            if "(" in key_text and ")" in key_text:
                inside_parens = key_text[key_text.find("(") + 1 : key_text.find(")")].strip()
                if len(inside_parens) > 12 and any(w in stem_lower for w in inside_parens.split() if len(w) > 4):
                    flaw_flags.append(self.FLAW_ANSWER_LEAKAGE)
                    feedback.append("Option includes parenthetical definition that directly leaks clues from the question stem.")
            elif len(key_text) > 40:
                key_words = [w for w in re.findall(r"\w+", key_text) if len(w) > 4]
                overlap = [w for w in key_words if w in stem_lower]
                if len(overlap) >= 3:
                    flaw_flags.append(self.FLAW_ANSWER_LEAKAGE)
                    feedback.append(f"High verbatim token overlap ({len(overlap)} terms) between stem and correct option indicates potential clue leakage.")

        # 7. Stem Length Check
        if len(str(mcq.stem).strip()) < 25:
            flaw_flags.append(self.FLAW_STEM_TOO_SHORT)
            feedback.append("Question stem is underspecified (< 25 characters).")

        # 8. Source Citation Traceability
        citation = mcq.source_citation
        has_full_citation = False
        has_partial_citation = False
        if citation and isinstance(citation, dict):
            if citation.get("verified_excerpt") and (citation.get("citation_text") or citation.get("chapter")):
                has_full_citation = True
            elif citation.get("source_name") or citation.get("citation_text"):
                has_partial_citation = True

        if not has_full_citation and not has_partial_citation:
            flaw_flags.append(self.FLAW_NO_CITATION)
            feedback.append("No authoritative source citation or textbook reference provided.")

        # Unique flaw list
        flaw_flags = sorted(list(set(flaw_flags)))

        # 9. Scoring Rubric Computation (1.0 to 5.0)
        # A. Factual Correctness
        fc = 4.8
        if self.FLAW_INVALID_KEY in flaw_flags:
            fc = 1.0
        elif self.FLAW_OPTION_COUNT in flaw_flags:
            fc = 2.5
        elif mcq.condition == "source_grounded":
            fc = 5.0
        elif mcq.condition == "syllabus_constrained":
            fc = 4.7
        else:
            fc = 4.2

        # B. Syllabus Alignment
        sa = 5.0
        if mcq.syllabus_node_id:
            sa = 5.0
        elif mcq.subject:
            sa = 4.2
        else:
            sa = 2.5

        # C. Distractor Quality
        dq = 5.0
        if self.FLAW_DUPLICATE_OPT in flaw_flags:
            dq -= 2.0
        if self.FLAW_ALL_NONE_ABOVE in flaw_flags:
            dq -= 1.4
        if self.FLAW_LENGTH_OUTLIER in flaw_flags:
            dq -= 1.1
        if self.FLAW_ANSWER_LEAKAGE in flaw_flags:
            dq -= 1.3
        if mcq.condition == "generic":
            dq -= 0.4
        dq = max(1.0, min(5.0, round(dq, 2)))

        # D. Traceability
        if has_full_citation:
            tr = 5.0
        elif has_partial_citation:
            tr = 3.6
        else:
            tr = 1.2

        # E. Composite Quality Score (0 to 100)
        composite = (
            (fc * 0.30) +
            (sa * 0.25) +
            (dq * 0.25) +
            (tr * 0.20)
        ) / 5.0 * 100.0

        if flaw_flags:
            penalty = len(flaw_flags) * 3.5
            composite = max(0.0, composite - penalty)

        composite = round(min(100.0, max(0.0, composite)), 1)

        scores = EvaluationScores(
            factual_correctness=round(fc, 2),
            syllabus_alignment=round(sa, 2),
            distractor_quality=round(dq, 2),
            traceability=round(tr, 2),
            composite_quality=composite,
        )

        is_valid = (
            self.FLAW_OPTION_COUNT not in flaw_flags and
            self.FLAW_INVALID_KEY not in flaw_flags and
            self.FLAW_DUPLICATE_OPT not in flaw_flags
        )

        return EvaluationResult(
            mcq_id=mcq.id,
            is_valid=is_valid,
            flaw_flags=flaw_flags,
            scores=scores,
            feedback=feedback,
        )
