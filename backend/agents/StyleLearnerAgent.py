import re
import json
import statistics
from typing import Dict, Any, Tuple
from jsonschema import validate, ValidationError
from google import genai


class StyleLearnerAgent:

    STYLE_SCHEMA = {
        "type": "object",
        "properties": {
            "detail": {"type": "object"},
            "abstraction": {"type": "object"},
            "formatting": {"type": "object"},
            "structure": {"type": "object"},
            "language": {"type": "object"},
            "stylistic_devices": {"type": "object"}
        },
        "required": [
            "detail",
            "abstraction",
            "formatting",
            "structure",
            "language",
            "stylistic_devices"
        ],
    }

    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-lite"):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name


    def _extract_features(self, text: str) -> Dict[str, Any]:
        lines = text.splitlines()

        headings = [l for l in lines if l.strip().startswith("#")]
        bullets = [l for l in lines if re.match(r"^\s*[\*\-]\s+", l)]
        numbered = [l for l in lines if re.match(r"^\s*\d+\.\s+", l)]

        examples = re.findall(r"(?i)\bexample|imagine|for instance\b", text)
        metaphors = re.findall(r"(?i)\blike\b", text)

        sentences = re.split(r"[.!?]", text)
        lengths = [len(s.split()) for s in sentences if len(s.split()) > 3]
        avg_len = statistics.mean(lengths) if lengths else 10

        if avg_len < 10:
            paragraph_length = "short"
        elif avg_len < 20:
            paragraph_length = "medium"
        else:
            paragraph_length = "long"

        features = {
            "headings": headings,
            "bullets_present": bool(bullets),
            "numbered_lists_present": bool(numbered),
            "examples_present": bool(examples),
            "metaphors_present": bool(metaphors),
            "avg_sentence_length": avg_len,
            "paragraph_length": paragraph_length,
            "language": "English"
        }
        return features


    def _construct_prompt(self, features: Dict[str, Any], text: str) -> str:
        return f"""
            You are a precise JSON style learner.
            Given the features and the example note text of user on some topic, your taks is to fill 
            learn the 'general' noting style of user from the example note given and fill the style JSON according to the schema below.
            Output ONLY a valid JSON following this schema:

            {{
              "tone": {{
                "formality": "string enum ['very_formal','formal','neutral','conversational','friendly','playful']",
                "voice": "string enum ['active', 'passive']"
              }},
              "detail": {{
                "complexity_level": "string enum ['minimal','low','medium','high','exhaustive']",
                "explain_example": "string enum ['low_detail','medium_detail','high_detail']"
              }},
              "abstraction": {{
                "complexity_level": "string enum ['beginner','intermediate','expert']",
                "math_verbose": "string enum ['sparse','medium','verbose']"
              }},
              "formatting": {{
                "use_bullets": "boolean",
                "use_numbered_lists": "boolean",
                "use_headings": "boolean",
                "heading_style": "string enum ['#','##','###','bold','underline']",
                "max_bullet_length_words": "integer",
                "paragraph_length": "string enum ['short','medium','long']",
                "prefer_tables_for_data": "boolean"
              }},
              "structure": {{
                "include_title": "boolean",
                "include_summary_at_top": "boolean",
                "include_examples_section": "boolean",
                "include_actions_or_todos_at_end": "boolean",
                "section_order": "array of strings"
              }},
              "language": {{
                "language": "string",
                "avoid_jargon": "boolean"
              }},
              "stylistic_devices": {{
                "use_examples": "boolean",
                "use_metaphors": "boolean",
                "use_analogies": "boolean",
                "use_acronyms_expanded_first": "boolean",
                "use_abbreviations": "boolean",
                "show_action_items": "boolean",
                "highlight_definitions": "string enum ['none','bold','italics','quotes']"
              }}
            }}

            Return only the JSON. No commentary.

            FEATURES:
            {json.dumps(features, indent=2)}

            NOTE:
            {text}
        """

    def _call_llm(self, prompt: str) -> Dict[str, Any]:
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=prompt,
        )
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            # Try to extract the first valid JSON substring if model output includes stray text
            match = re.search(r"\{.*\}", response.text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
            raise ValueError("Model did not return valid JSON.")


    def _validate_json(self, style_json: Dict[str, Any]) -> Tuple[bool, list]:
        try:
            validate(instance=style_json, schema=self.STYLE_SCHEMA)
            return True, []
        except ValidationError as e:
            return False, [str(e)]


    def run(self, note_text: str, max_retries: int = 3) -> Dict[str, Any]:
        features = self._extract_features(note_text)

        for attempt in range(1, max_retries + 1):
            print(f"Attempt {attempt} to infer style JSON...")
            prompt = self._construct_prompt(features, note_text)
            style_json = self._call_llm(prompt)

            valid, errors = self._validate_json(style_json)
            if valid:
                print(f"JSON validated successfully on attempt {attempt}")
                return style_json
            else:
                print(f"Validation failed: {errors}")
                print("retrying...")

        raise ValueError("Failed to produce valid style JSON after multiple retries.")