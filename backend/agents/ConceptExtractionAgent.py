from typing import List, Dict, Any
from langchain_core.documents import Document
from keybert import KeyBERT
import yake
import re

class ConceptExtractionAgent:
    def __init__(self, max_keywords: int = 10, yake_lang: str = "en", yake_max_ngram: int = 3, model_name: str = "all-MiniLM-L6-v2"):
        self.max_keywords = max_keywords

        ## keybert
        self.yake_extractor = yake.KeywordExtractor(
            lan=yake_lang,
            n=yake_max_ngram,
            top=max_keywords
        )

        self.keybert_model = KeyBERT(model_name)

    def clean_text(self, text: str) -> str:
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def extract_candidates(self, text: str) -> List[str]:
        keywords = self.yake_extractor.extract_keywords(text)
        candidates = [kw for kw, score in keywords]
        return candidates

    def rank_candidates(self, text: str, candidates: List[str]) -> List[str]:
        """Rank candidate keyphrases using KeyBERT embeddings"""
        if not candidates:
            return []
        # KeyBERT semantic ranking
        ranked = self.keybert_model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 3),
            top_n=10,
            candidates=candidates,
            use_mmr=True,  # Maximal Marginal Relevance for diversity
            diversity=0.2
        )
        return [kw for kw, score in ranked]

    def run(self, documents: List[Document]) -> List[Document]:
        processed_docs = []

        for i, doc in enumerate(documents):
            print(f"[PROCESSING] Extracting concepts from chunk {i+1}/{len(documents)}...")
            text = self.clean_text(doc.page_content)
            candidates = self.extract_candidates(text)
            concepts = self.rank_candidates(text, candidates)

            # Append concepts to document metadata
            metadata = doc.metadata.copy()
            metadata["concepts"] = concepts

            processed_docs.append(Document(page_content=doc.page_content, metadata=metadata))

        print(f"[INFO] Concept extraction completed for {len(processed_docs)} chunks.")
        return processed_docs

