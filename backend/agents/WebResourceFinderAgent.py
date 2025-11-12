from ddgs import DDGS
from langchain_core.documents import Document
from typing import List, Dict
import time

class WebResourceFinderAgent:
    def __init__(self, max_results_per_concept: int = 2, delay: float = 1.0):
        self.max_results = max_results_per_concept
        self.delay = delay
        self.ddg = DDGS()

    def fetch_links(self, concept: str) -> List[Dict[str, str]]:
        query = f"{concept} site:wikipedia.org OR site:medium.com OR site:towardsdatascience.com"
        links = []
        for r in self.ddg.text(query, max_results=self.max_results):
            links.append({
                "title": r.get("title", ""),
                "link": r.get("href", ""),
                "snippet": r.get("body", "")
            })
        time.sleep(self.delay)
        return links

    def run(self, documents: List[Document]) -> List[Document]:
        for doc in documents:
            concepts = doc.metadata.get("concepts", [])
            resources = {}
            for c in concepts:
                resources[c] = self.fetch_links(c)
            doc.metadata["resources"] = resources
        return documents