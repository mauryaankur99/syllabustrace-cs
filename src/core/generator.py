"""
generator.py — Multi-Condition Question Generation Engine for SyllabusTrace-CS.
Supports Generic (A), Syllabus-Constrained (B), and Source-Grounded (C) conditions.
Integrates live APIs (Gemini, OpenAI, Anthropic) with explicit provenance tracking,
strict error states when credentials are unconfigured, and separate offline fixtures.
"""

import os
import uuid
import json
import re
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
import httpx

from .models import MCQRecord, ModelMetadata


class ProviderMissingCredentialsError(Exception):
    """Raised when an external AI provider is requested without configured API credentials."""
    pass


class ProviderAPIError(Exception):
    """Raised when an external model API call fails or returns an unparseable response."""
    pass


class MCQGenerator:
    """Configurable question generator comparing three experimental prompt paradigms.
    Explicitly tracks model provenance, raw prompts, and raw responses.
    """

    PROMPT_TEMPLATES = {
        "generic": (
            "Write a multiple choice question on the following Computer Science topic: {topic}.\n"
            "Include exactly 4 options (keys A, B, C, D), indicate the correct answer key (A, B, C, or D), "
            "and provide a technical explanation.\n"
            "Respond ONLY with a valid JSON object with keys: stem, options (dict of A,B,C,D), correct_key, explanation."
        ),
        "syllabus_constrained": (
            "You are an expert exam item writer for the GATE CS examination.\n"
            "Target Syllabus Node: {subject} -> {topic} -> {subtopic}.\n"
            "Target Cognitive Tier: {cognitive_level} (Bloom's Taxonomy).\n"
            "Psychometric Item-Writing Rules:\n"
            "- Write an authentic, rigorous single-best-answer multiple choice question.\n"
            "- Exactly 4 non-overlapping options (A, B, C, D).\n"
            "- Balance option lengths (no option significantly longer or shorter than others).\n"
            "- Strictly avoid 'All of the above' and 'None of the above'.\n"
            "- Avoid clue leakage (the stem must not contain giveaway clues for the correct answer).\n"
            "Respond ONLY with a valid JSON object with keys: stem, options (dict of A,B,C,D), correct_key, explanation."
        ),
        "source_grounded": (
            "You are an expert psychometric item writer grounded in canonical Computer Science literature.\n"
            "Target Syllabus Node: {subject} -> {topic} -> {subtopic}.\n"
            "Target Cognitive Tier: {cognitive_level} (Bloom's Taxonomy).\n"
            "Canonical Reference: {source_title} ({authors}), {chapter}, {section}.\n"
            "Verified Canonical Excerpt:\n"
            "\"\"\"\n{verified_excerpt}\n\"\"\"\n"
            "Guidelines:\n"
            "- Formulate a question strictly verifiable using the canonical excerpt above.\n"
            "- Provide exactly 4 plausible, distinct options (A, B, C, D).\n"
            "- Distractors must target authentic student misconceptions.\n"
            "- Include exact citation and explanation referencing the source passage.\n"
            "Respond ONLY with a valid JSON object with keys: stem, options (dict of A,B,C,D), correct_key, explanation, citation."
        ),
    }

    PROVIDER_KEY_MAP = {
        "gemini": "GEMINI_API_KEY",
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
    }

    DEFAULT_MODELS = {
        "gemini": "gemini-1.5-flash",
        "openai": "gpt-4o-mini",
        "anthropic": "claude-3-5-haiku-20241022",
        "offline_fixture": "deterministic_fixture_v1",
        "mock": "deterministic_fixture_v1",
    }

    def __init__(self, provider: Optional[str] = None, model_name: Optional[str] = None):
        self.provider = provider or os.getenv("AI_PROVIDER", "offline_fixture").lower()
        if self.provider == "mock":
            self.provider = "offline_fixture"
        default_model = self.DEFAULT_MODELS.get(self.provider, "deterministic_fixture_v1")
        self.model_name = model_name or os.getenv("MODEL_NAME", default_model)

    def generate(
        self,
        condition: str,
        subject: str,
        topic: str,
        subtopic: str = "",
        cognitive_level: str = "Comprehension",
        source_data: Optional[Dict[str, Any]] = None,
        temperature: Optional[float] = None,
    ) -> MCQRecord:
        """Generates an MCQ according to the specified condition.
        If live provider is specified, calls real API and records full provenance.
        If offline_fixture is specified, generates deterministic illustrative item labeled as simulated.
        """
        condition = condition.lower()
        if condition not in self.PROMPT_TEMPLATES:
            condition = "source_grounded"

        if temperature is None:
            temperature = 0.1 if condition == "source_grounded" else 0.7

        prompt_str = self.format_prompt(
            condition=condition,
            subject=subject,
            topic=topic,
            subtopic=subtopic,
            cognitive_level=cognitive_level,
            source_data=source_data,
        )

        item_id = f"mcq-gen-{uuid.uuid4().hex[:8]}"
        timestamp = datetime.utcnow().isoformat()

        # Offline fixture generation
        if self.provider in {"offline_fixture", "mock"}:
            item_data = self._generate_deterministic_fixture(
                condition=condition,
                subject=subject,
                topic=topic,
                subtopic=subtopic,
                cognitive_level=cognitive_level,
                source_data=source_data,
            )
            model_meta = {
                "provider": "offline_fixture",
                "model": "deterministic_fixture_v1",
                "temperature": temperature,
                "prompt_version": f"v1-{condition}",
                "is_simulated": True,
                "raw_prompt": prompt_str,
                "raw_response": json.dumps(item_data, indent=2),
                "execution_timestamp": timestamp,
            }
            data_tier = "illustrative_fixture"
        else:
            # Genuine Live Model Generation
            item_data, raw_resp = self._call_live_provider(prompt_str, condition, temperature)
            model_meta = {
                "provider": self.provider,
                "model": self.model_name,
                "temperature": temperature,
                "prompt_version": f"v1-{condition}",
                "is_simulated": False,
                "raw_prompt": prompt_str,
                "raw_response": raw_resp,
                "execution_timestamp": timestamp,
            }
            data_tier = "experimental_trial"

        return MCQRecord(
            id=item_id,
            stem=item_data["stem"],
            options=item_data["options"],
            correct_key=item_data["correct_key"],
            explanation=item_data["explanation"],
            condition=condition,
            subject=subject,
            syllabus_node_id=source_data.get("syllabus_node_id") if source_data else f"{subject.lower()[:3]}-{topic.lower()[:10]}",
            cognitive_level=cognitive_level,
            data_tier=data_tier,
            source_citation=item_data.get("source_citation"),
            model_metadata=model_meta,
            review_status="pending",
            reviewer_notes=f"Generated via {self.provider}:{self.model_name}. Review pending human expert verification.",
        )

    def format_prompt(
        self,
        condition: str,
        subject: str,
        topic: str,
        subtopic: str = "",
        cognitive_level: str = "Comprehension",
        source_data: Optional[Dict[str, Any]] = None,
    ) -> str:
        template = self.PROMPT_TEMPLATES.get(condition, self.PROMPT_TEMPLATES["source_grounded"])
        source_data = source_data or {}
        return template.format(
            subject=subject,
            topic=topic,
            subtopic=subtopic or topic,
            cognitive_level=cognitive_level,
            source_title=source_data.get("title", "Canonical CS Reference"),
            authors=", ".join(source_data.get("authors", ["Author"])),
            chapter=source_data.get("chapter", "Chapter"),
            section=source_data.get("section", "Section"),
            verified_excerpt=source_data.get("verified_excerpt", "Authoritative CS definition."),
        )

    def _call_live_provider(self, prompt: str, condition: str, temperature: float) -> Tuple[Dict[str, Any], str]:
        """Dispatches to the authenticated live provider or raises an explicit blocker."""
        key_var = self.PROVIDER_KEY_MAP.get(self.provider)
        if not key_var:
            raise ProviderConfigurationError(f"Unsupported provider '{self.provider}'. Supported: {list(self.PROVIDER_KEY_MAP.keys())}")

        api_key = os.getenv(key_var)
        if not api_key:
            raise ProviderMissingCredentialsError(
                f"Missing API credentials for provider '{self.provider}'. "
                f"Environment variable '{key_var}' is not configured. "
                f"To run genuine experimental generation, set {key_var} in your environment or .env file. "
                f"Fallback fixture output is strictly prohibited from being labeled as real model output."
            )

        if self.provider == "gemini":
            return self._call_gemini_api(prompt, api_key, temperature)
        elif self.provider == "openai":
            return self._call_openai_api(prompt, api_key, temperature)
        elif self.provider == "anthropic":
            return self._call_anthropic_api(prompt, api_key, temperature)
        else:
            raise ProviderConfigurationError(f"Unknown provider '{self.provider}'.")

    def _call_gemini_api(self, prompt: str, api_key: str, temperature: float) -> Tuple[Dict[str, Any], str]:
        """Calls Google Gemini REST API."""
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": temperature,
                "responseMimeType": "application/json",
            }
        }
        try:
            with httpx.Client(timeout=30.0) as client:
                res = client.post(url, json=payload)
                if res.status_code != 200:
                    raise ProviderAPIError(f"Gemini API returned HTTP {res.status_code}: {res.text}")
                data = res.json()
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
                parsed = self._parse_json_response(raw_text)
                return parsed, raw_text
        except httpx.RequestError as e:
            raise ProviderAPIError(f"Network error calling Gemini API: {str(e)}")

    def _call_openai_api(self, prompt: str, api_key: str, temperature: float) -> Tuple[Dict[str, Any], str]:
        """Calls OpenAI Chat Completions API."""
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "You are an expert psychometric Computer Science item writer. Always output strictly valid JSON."},
                {"role": "user", "content": prompt}
            ],
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        }
        try:
            with httpx.Client(timeout=30.0) as client:
                res = client.post(url, headers=headers, json=payload)
                if res.status_code != 200:
                    raise ProviderAPIError(f"OpenAI API returned HTTP {res.status_code}: {res.text}")
                data = res.json()
                raw_text = data["choices"][0]["message"]["content"]
                parsed = self._parse_json_response(raw_text)
                return parsed, raw_text
        except httpx.RequestError as e:
            raise ProviderAPIError(f"Network error calling OpenAI API: {str(e)}")

    def _call_anthropic_api(self, prompt: str, api_key: str, temperature: float) -> Tuple[Dict[str, Any], str]:
        """Calls Anthropic Messages API."""
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "user", "content": f"{prompt}\nRespond strictly with a JSON object."}
            ],
            "max_tokens": 1024,
            "temperature": temperature,
        }
        try:
            with httpx.Client(timeout=30.0) as client:
                res = client.post(url, headers=headers, json=payload)
                if res.status_code != 200:
                    raise ProviderAPIError(f"Anthropic API returned HTTP {res.status_code}: {res.text}")
                data = res.json()
                raw_text = data["content"][0]["text"]
                parsed = self._parse_json_response(raw_text)
                return parsed, raw_text
        except httpx.RequestError as e:
            raise ProviderAPIError(f"Network error calling Anthropic API: {str(e)}")

    def _parse_json_response(self, text: str) -> Dict[str, Any]:
        """Parses model response text, stripping markdown code fences if present."""
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned)
            cleaned = re.sub(r"\s*```$", "", cleaned)
        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ProviderAPIError(f"Failed to parse model output as JSON: {str(e)}. Raw text: {text[:200]}")

        # Basic validation of required keys
        if "stem" not in data or "options" not in data or "correct_key" not in data:
            raise ProviderAPIError(f"Model JSON response missing required keys (stem, options, correct_key). Got: {list(data.keys())}")

        return data

    def _generate_deterministic_fixture(
        self,
        condition: str,
        subject: str,
        topic: str,
        subtopic: str,
        cognitive_level: str,
        source_data: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Generates realistic illustrative baseline fixtures for testing evaluation heuristics.
        Explicitly flagged as simulated output.
        """
        if condition == "generic":
            return {
                "stem": f"In {subject}, what is the main purpose of {subtopic or topic}?",
                "options": {
                    "A": f"It handles {subtopic or topic} operations in software",
                    "B": f"It optimizes system performance through {subtopic or topic} mechanism (this is the primary purpose in modern systems)",
                    "C": "It halts all background threads immediately",
                    "D": "All of the above"
                },
                "correct_key": "B",
                "explanation": f"{subtopic or topic} is utilized to ensure efficient execution and resource utilization.",
                "source_citation": None,
            }
        elif condition == "syllabus_constrained":
            return {
                "stem": f"Consider the principles of {subtopic or topic} under the {subject} curriculum. Which of the following statements is mathematically or architecturally correct regarding its operational bounds?",
                "options": {
                    "A": f"It guarantees deterministic upper bounds on latency when configured within standard constraints",
                    "B": "It operates exclusively in user space without requiring kernel mode privilege transitions",
                    "C": "It doubles the required hardware register file for every concurrent process context",
                    "D": "It eliminates the need for mutual exclusion primitives in shared memory regions"
                },
                "correct_key": "A",
                "explanation": f"Under standard {subject} specifications, {subtopic or topic} provides bounded operational performance under designated constraints.",
                "source_citation": {
                    "source_name": f"Official {subject} Curriculum Guide",
                    "edition": "GATE CS 2026",
                    "chapter": topic,
                },
            }
        else:  # source_grounded
            ref_title = source_data.get("title", "Canonical CS Reference") if source_data else "Standard Computer Science Literature"
            ref_authors = ", ".join(source_data.get("authors", ["Leading Theorists"])) if source_data else "Domain Authorities"
            ref_chapter = source_data.get("chapter", "Foundational Principles") if source_data else "Core Principles"
            excerpt = source_data.get("verified_excerpt", "Formal domain specification.") if source_data else "Fundamental principles dictate precise invariants."

            return {
                "stem": f"According to {ref_authors} in '{ref_title}' ({ref_chapter}), which necessary condition governs {subtopic or topic}?",
                "options": {
                    "A": "All active execution paths must maintain invariant safety constraints verified by formal state transition analysis",
                    "B": "The algorithm permits unverified state rollbacks without logging undo transitions",
                    "C": "Execution is restricted to asynchronous single-core microcontrollers",
                    "D": "Memory references must bypass cache hierarchy directly to storage media"
                },
                "correct_key": "A",
                "explanation": f"As rigorously proven in '{ref_title}', safety invariants require formal preservation across all valid state transitions.",
                "source_citation": {
                    "source_id": source_data.get("source_id", "canonical-ref-01") if source_data else "canonical-ref",
                    "citation_text": f"{ref_title}, {ref_chapter}",
                    "authors": ref_authors,
                    "chapter": ref_chapter,
                    "page": source_data.get("page", "100-115") if source_data else "100-115",
                    "verified_excerpt": excerpt,
                },
            }
