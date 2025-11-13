from fastapi import APIRouter, Body
from google import genai
from db.chroma_manager import search_notes, search_within_note

router = APIRouter()
client = genai.Client(api_key="AIzaSyAgVyjlgwX89ForZ5l3mTf8dyhRF5EPg0s")

@router.post("/global")
def chat_global(query: str = Body(..., embed=True)):
    """Chat across all notes"""
    retrieved = search_notes(query)
    context = "\n\n".join([r.page_content for r in retrieved])

    prompt = f"""
Use the following context to answer the question as accurately as possible:
{context}

Question: {query}
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    return {"response": response.text, "matches": [r.metadata for r in retrieved]}

@router.post("/note")
def chat_with_note(note_id: int = Body(...), query: str = Body(...)):
    """Chat within a single note"""
    retrieved = search_within_note(note_id, query)
    context = "\n\n".join([r.page_content for r in retrieved])

    prompt = f"""
Using only the content from this note, answer the question:
{context}

Question: {query}
"""
    response = client.models.generate_content(
        model="gemini-2.0-flash-lite",
        contents=prompt
    )
    return {"response": response.text, "matches": [r.metadata for r in retrieved]}
