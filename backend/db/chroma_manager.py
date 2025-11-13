import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHROMA_PATH = "db/chroma_store"

# Initialize embedding model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Initialize splitter
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

def get_vector_store():
    """Load or create the persistent Chroma vector store"""
    os.makedirs(CHROMA_PATH, exist_ok=True)
    return Chroma(
        collection_name="notes",
        embedding_function=embeddings,
        persist_directory=CHROMA_PATH,
    )

def update_note_in_chroma(note_id: int, title: str, content: str):
    """Split note and store embeddings"""
    vector_store = get_vector_store()

    # Split text into chunks
    chunks = splitter.split_text(content)

    # Delete previous entries for same note (if any)
    vector_store.delete(where={"note_id": note_id})

    # Add new embeddings
    vector_store.add_texts(
        texts=chunks,
        metadatas=[{"note_id": note_id, "title": title}] * len(chunks)
    )

    vector_store.persist()
    print(f"✅ Indexed note {note_id} ({len(chunks)} chunks) in Chroma.")

def search_notes(query: str, k: int = 5):
    """Semantic search across all notes"""
    vector_store = get_vector_store()
    results = vector_store.similarity_search(query, k=k)
    return results

def search_notes_with_scores(query: str, k: int = 3):
    vector_store = get_vector_store()
    results = vector_store.similarity_search_with_score(query, k=k)
    return results

def search_within_note(note_id: int, query: str, k: int = 3):
    """Search only within a single note"""
    vector_store = get_vector_store()
    results = vector_store.similarity_search(
        query,
        k=k,
        filter={"note_id": note_id}
    )
    return results
