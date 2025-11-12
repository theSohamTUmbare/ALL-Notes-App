from langchain_community.document_loaders import WebBaseLoader, TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from typing import Dict, Any, Union, List
import os

class IngestionAgent:
    def __init__(self, use_semantic: bool = False, chunk_size: int = 800000, chunk_overlap: int = 8000):
        self.use_semantic = use_semantic
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2") if self.use_semantic else None


    def load_content(self, sources: Union[str, os.PathLike, list]) -> str:
        # Normalizing sources to a list
        if not isinstance(sources, list):
            sources = [sources]

        combined_texts = []

        for source in sources:
            if isinstance(source, str) and source.startswith("http"):
                loader = WebBaseLoader(source)
                docs = loader.load()
                text = " ".join([d.page_content for d in docs])
                combined_texts.append(text)

            elif str(source).endswith(".pdf"):
                loader = PyPDFLoader(source)
                docs = loader.load()
                text = " ".join([d.page_content for d in docs])
                combined_texts.append(text)

            elif os.path.exists(source):
                loader = TextLoader(source)
                docs = loader.load()
                text = " ".join([d.page_content for d in docs])
                combined_texts.append(text)

            else:
                combined_texts.append(str(source))

            ## Further integration - OCR
            # elif str(source).endswith(self,".png", ".jpg", ".jpeg")):
            #     ----

        final_text = "\n".join(combined_texts)

        return final_text


    def preprocess(self, text: str) -> str:
        """For Basic text cleaning."""
        text = text.replace("\n", " ").replace("\t", " ")
        text = " ".join(text.split())
        return text


    def chunk_text(self, text: str, metadata: Dict[str, Any] = None) -> List[Document]:
        """Split text into 'semantically meaningful' or  'size-based'  chunks."""
        metadata = metadata or {}

        if self.use_semantic and self.embedding_model is not None:
            try:
                splitter = SemanticChunker(self.embedding_model)
                chunks = splitter.split_text(text)
                print(f"[SUCCESS] Semantic chunking succeeded")
            except Exception as e:
                print(f"[WARN] Semantic chunking failed: {e}. Falling back to recursive splitter.")
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=self.chunk_size,
                    chunk_overlap=self.chunk_overlap
                )
                chunks = splitter.split_text(text)
        else:
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap
            )
            chunks = splitter.split_text(text)

        documents = [
            Document(page_content=chunk, metadata={**metadata, "chunk_id": i})
            for i, chunk in enumerate(chunks)
        ]
        return documents


    def run(self, sources: Union[str, List[str]]) -> Dict[str, Any]:
      """Main callable method... (Accepts single or multiple sources.)"""
      try:
          raw_text = self.load_content(sources)
          clean_text = self.preprocess(raw_text)
          documents = self.chunk_text(clean_text, metadata={"source": str(sources[:501])})

          return {
              "status": "success",
              "source": sources,
              "documents": documents,
              "meta": {"num_chunks": len(documents)}
          }

      except Exception as e:
          return {"status": "error", "message": str(e)}
