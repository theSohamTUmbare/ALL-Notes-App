from typing import List, Optional, Dict, Any
from langchain_core.documents import Document
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import re

from google import genai

class NotemakingAgent:
    """
    NotemakingAgent:
    - Cleans noisy raw text while preserving relevant, detailed information.
    - Removes junk text (ads, buttons, author info, chat meta, etc.).
    - Uses open-source models for semantic filtering.
    """

    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash-lite"):
        print(f"[INFO] Initializing NotemakingAgent with Google Gemini model: {model_name}")
        self.model_name = model_name
        self.client = genai.Client(api_key=api_key)


    def heuristic_clean(self, text: str) -> str:
        text = re.sub(r"http\S+", "", text)
        text = re.sub(r"(click here|login|sign up|advertisement|follow us|©|copyright)", "", text, flags=re.I)
        text = re.sub(r"(you said:|chatgpt said:|assistant:|user:)", "", text, flags=re.I)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def semantic_clean(self, text: str, user_instruction: Optional[str] = None) -> str:
        system_prompt = (
            "You are a professional notemaking AI. "
            "Clean the following text by removing irrelevant or noisy parts "
            "(ads, links, UI elements, chat markers, or unrelated content). "
            "Make concise but highly detailed notes that preserve all important factual information. "
            "Ensure clarity, coherence, and structure."
        )

        if user_instruction:
            system_prompt += f" Follow the user’s instruction carefully: {user_instruction.strip()}"

        full_prompt = (
            f"{system_prompt}\n\n"
            "### Input Text ###\n"
            f"{text}\n\n"
            "### Output: High-quality cleaned and detailed notes ###"
        )

        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=full_prompt
            )
            cleaned_text = response.text.strip()
            # cleaned_text = "SIMULATED CLEANED TEXT"  # Placeholder for actual API call
        except Exception as e:
            print(f"[ERROR] Gemini API call failed: {e}")
            cleaned_text = text  # Fallback: return the pre-cleaned text

        cleaned_text = re.sub(r"\s+", " ", cleaned_text).strip()
        return cleaned_text


    def run(self, documents: List[Document], user_instruction: Optional[str] = None) -> List[Document]:
        cleaned_docs = []
        for i, doc in enumerate(documents):
            print(f"[PROCESSING] Cleaning chunk {i+1}/{len(documents)}...")
            preclean = self.heuristic_clean(doc.page_content)
            cleaned_text = self.semantic_clean(preclean, user_instruction=user_instruction)
            cleaned_docs.append(
                Document(page_content=cleaned_text, metadata=doc.metadata)
            )

        print(f"[INFO] Cleaning completed for {len(cleaned_docs)} chunks.")
        return cleaned_docs