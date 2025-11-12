from langchain_core.documents import Document
from typing import List
import re

class TagGenerator:
    def __init__(self, max_tags: int = 10):
        self.max_tags = max_tags

    def clean_tag(self, tag: str) -> str:
        tag = re.sub(r"[^a-zA-Z0-9\s\-]", "", tag)
        tag = re.sub(r"\s+", " ", tag).strip().lower()
        return tag.replace(" ", "_")

    def run(self, documents: List[Document]) -> List[Document]:
        for doc in documents:
            concepts = doc.metadata.get("concepts", [])
            base_text = doc.page_content.lower()

            # Generate extra tags heuristically from frequent nouns (fallback)
            if not concepts:
                words = re.findall(r"\b[a-zA-Z]{4,}\b", base_text)
                concepts = list(set(words))[:self.max_tags]

            tags = [self.clean_tag(c) for c in concepts][:self.max_tags]
            doc.metadata["tags"] = tags
        return documents

