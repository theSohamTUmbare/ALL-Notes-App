from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch
import json
from typing import Dict, Any
import re


from google import genai


class StyleRewriterAgent:
    def __init__(self, api_key: str, model_name: str = "meta-llama/Llama-3.2-3B-Instruct",
                 device: str = None, max_new_tokens: int = 512):
        self.client = genai.Client(api_key=api_key)
        self.max_new_tokens = max_new_tokens

    def _load_style_profile(self, profile_path: str, profile_id: str) -> Dict[str, Any]:
        with open(profile_path, "r") as f:
            profiles = json.load(f)
        for p in profiles:
            if p["profile_id"] == profile_id:
                return p
        raise ValueError(f"Profile '{profile_id}' not found in {profile_path}")

    def _construct_style_prompt(self, profile: Dict[str, Any]) -> str:
        tone = profile["tone"]
        detail = profile["detail"]
        abstraction = profile["abstraction"]
        formatting = profile["formatting"]
        structure = profile["structure"]
        lang = profile["language"]
        style = profile["stylistic_devices"]

        prompt = f"""
Rewrite the following educational notes according to this style profile:

### User Persona
{profile['user_persona']}

### Tone
Formality: {tone['formality']}, Voice: {tone['voice']}, Example intensity: {tone['use_examples']}

### Detail & Abstraction
Complexity: {detail['complexity_level']}, Explain example: {detail['explain_example']},
Audience: {abstraction['complexity_level']}, Include glossary: {abstraction['include_glossary_of_terms']}

### Formatting
Use bullets: {formatting['use_bullets']}, Headings: {formatting['use_headings']},
Paragraph length: {formatting['paragraph_length']}, Emphasize keywords: {formatting['emphasize_keywords']}

### Structure
Include summary: {structure['include_summary_at_top']}, Sections: {', '.join(structure['section_order'])}

### Language
Language: {lang['language']}, Complexity: {lang['complexity']}, Avoid jargon: {lang['avoid_jargon']}

### Stylistic Devices
Use examples: {style['use_examples']}, Use metaphors: {style['use_metaphors']}, Highlight definitions: {style['highlight_definitions']}

Custom Instruction: {profile['custom_instruction']}

Now rewrite the following notes:
"""
        return prompt.strip()

    ## evaluation Loop
    def evaluate_output(self, rewritten_text: str, profile: Dict[str, Any]) -> Dict[str, Any]:
        eval_prompt = f"""
Evaluate the rewritten text below against the provided style profile.
Give the result as a strict JSON object with, output ONLY a valid JSON following this schema::
{{
  "style_adherence_score": (0–10)
  "clarity_score": (0–10)
  "coherence_score": (0–10)
  "overall_feedback": (2–3 sentences)
}}

### Style Profile:
{json.dumps(profile, indent=2)}

### Rewritten Notes:
{rewritten_text}
"""
        # response = self.client.models.generate_content(
        #     model="gemini-2.0-flash-lite",
        #     contents=eval_prompt
        # )
        response = "<SIMULATED API RESPONSE>"

        raw_text = response.text.strip()
        print(raw_text)

        # Remove Markdown code fences
        cleaned = re.sub(r"```(?:json)?|```", "", raw_text).strip()

        # Extract JSON part if there's any extra explanation
        match = re.search(r"\{[\s\S]*\}", cleaned)
        if match:
            cleaned = match.group(0)

        try:
            evaluation = json.loads(cleaned)
        except json.JSONDecodeError as e:
            print(f"JSON decode failed: {e}\nRaw text:\n{raw_text}")
            evaluation = {
                "style_adherence_score": 0,
                "clarity_score": 0,
                "coherence_score": 0,
                "overall_feedback": raw_text
            }
        return evaluation


    def refine_output(self, rewritten_text: str, feedback: str, profile: Dict[str, Any]) -> str:
        refinement_prompt = f"""
You are improving a rewritten educational note.
Use this feedback to enhance it according to the style profile.

### Feedback from Evaluator:
{feedback}

### Style Profile:
{json.dumps(profile, indent=2)}

### Text to Improve:
{rewritten_text}

Now rewrite the text again, incorporating the feedback while keeping factual meaning intact.
"""
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=refinement_prompt
        )
        return response.text


    def run(self, base_notes: str, profile_path: str, profile_id: str,
                            max_loops: int = 4, threshold: int = 28) -> str:
        profile = self._load_style_profile(profile_path, profile_id)
        style_prompt = self._construct_style_prompt(profile)
        full_prompt = f"{style_prompt}\n\n### Base Notes:\n{base_notes.strip()}"

        # rewritten = self.client.models.generate_content(
        #     model="gemini-2.0-flash-lite",
        #     contents=full_prompt
        # ).text
        rewritten = "<--SIMULATED REWRITTEN TEXT-->"  # Placeholder for testing

        # Iterative Evaluation Loop
        for i in range(max_loops):
            # evaluation = self.evaluate_output(rewritten, profile)

            # total_score = (
            #     evaluation.get("style_adherence_score", 0)
            #     + evaluation.get("clarity_score", 0)
            #     + evaluation.get("coherence_score", 0)
            # )

            # feedback = evaluation.get("overall_feedback", "Improve style consistency and clarity.")

            total_score = 30  # Placeholder for testing
            
            # print(f"\ Iteration {i+1}")
            # # print(evaluation)
            # print(f"Scores → Style: {evaluation.get('style_adherence_score', 0)}, "
            #       f"Clarity: {evaluation.get('clarity_score', 0)}, "
            #       f"Coherence: {evaluation.get('coherence_score', 0)}, ")
            # print(f"Total Score: {total_score}/30")
            # print(f"Feedback: {feedback}")

            if total_score >= threshold:
                print("Quality threshold reached — finalizing output.")
                break

            # Otherwise refine
            print("----------------------------->")
            print("Refining based on feedback...")
            print("----------------------------->")
            # rewritten = self.refine_output(rewritten, feedback, profile)

        return {
            "rewritten_text": rewritten,
            "evaluation": None,
            "feedback": None,
            # "evaluation": evaluation,
            # "feedback": feedback,
            "total_score": total_score
        }