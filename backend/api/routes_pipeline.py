from io import BytesIO
from fastapi import APIRouter, Body, UploadFile, File, Form, HTTPException
from typing import Dict, Any
import json
from run_pipeline import run_workflow, make_json_safe
from agents.StyleLearnerAgent import StyleLearnerAgent

from db.database_manager import update_style_profiles  
from google import genai
 
router = APIRouter()

@router.post("/run")
def run_pipeline_api(state: Dict[str, Any] = Body(...)):
    """Run the LangGraph pipeline and return the final processed state."""
    print(state)
    final_state = run_workflow(state)
    return make_json_safe(final_state)

@router.post("/learn")
async def learn_style_from_input(
    current_profile: str = Form(...),
    user_text: str = Form(None),
    file: UploadFile = File(None)
):
    try:
        current_profile = json.loads(current_profile)
    except json.JSONDecodeError:
        print(current_profile)
        raise HTTPException(status_code=400, detail="Invalid JSON in 'current_profile'")

    # Extract note text
    note_text = user_text or ""
    if file:
        # Simple handling for txt or pdf files
        ext = file.filename.split(".")[-1].lower()
        content = await file.read()
        if ext == "txt":
            note_text = content.decode("utf-8", errors="ignore")
        elif ext == "pdf":
            try:
                from PyPDF2 import PdfReader
                pdf = PdfReader(BytesIO(content))
                note_text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
            except Exception:
                raise HTTPException(status_code=400, detail="Unable to read PDF file.")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Use .txt or .pdf")

    if not note_text.strip():
        raise HTTPException(status_code=400, detail="No text provided for style learning.")

    # Initialize StyleLearnerAgent 
    try:
        learner = StyleLearnerAgent(api_key="AIzaSyAgVyjlgwX89ForZ5l3mTf8dyhRF5EPg0s")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to initialize LLM: {e}")

    # Run the learner agent to get partial style JSON 
    try:
        learned_json = learner.run(note_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Style learner failed: {e}")

    new_profile = current_profile.copy()
    for key, value in learned_json.items():
        new_profile[key] = value  # overwrite sections like tone, formatting, etc.

    from datetime import datetime
    new_profile["updated_at"] = datetime.now().isoformat()

    #  Save to DB
    try:
        update_style_profiles([new_profile])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save updated style profile: {e}")

    return new_profile