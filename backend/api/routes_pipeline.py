from io import BytesIO
from fastapi import APIRouter, Body, UploadFile, File, Form, HTTPException
from typing import Dict, Any
import json
from run_pipeline import run_workflow, make_json_safe
from agents.StyleLearnerAgent import StyleLearnerAgent
import fitz  # PyMuPDF
from PIL import Image
import pytesseract
from db.database_manager import update_style_profiles  
from google import genai
 
router = APIRouter()

@router.post("/run")
def run_pipeline_api(state: Dict[str, Any] = Body(...)):
    """Run the LangGraph pipeline and return the final processed state."""
    print(state)
    final_state = run_workflow(state)
    return make_json_safe(final_state)

def extract_pdf_to_markdown(pdf_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid or corrupted PDF file.")

    all_fonts = []

    # First pass — collect font sizes
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" not in b:
                continue
            for line in b["lines"]:
                for span in line["spans"]:
                    all_fonts.append(span["size"])

    if not all_fonts:
        return ""  

    max_size = max(all_fonts)
    h1 = max_size * 0.90
    h2 = max_size * 0.75
    h3 = max_size * 0.60

    md = []

    # Second pass — reconstruct markdown
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if "lines" not in b:
                continue

            for line in b["lines"]:
                line_text = ""
                styled = False

                for span in line["spans"]:
                    text = span["text"].strip()
                    size = span["size"]
                    font = span["font"]

                    if not text:
                        continue

                    # Identify headings
                    if size >= h1:
                        md.append(f"# {text}")
                        styled = True
                    elif size >= h2:
                        md.append(f"## {text}")
                        styled = True
                    elif size >= h3:
                        md.append(f"### {text}")
                        styled = True
                    else:
                        if "Bold" in font:
                            line_text += f"**{text}** "
                        else:
                            line_text += text + " "

                if not styled and line_text.strip():
                    md.append(line_text.strip())

        md.append("\n")

    return "\n".join(md).strip()


def extract_scanned_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    ocr_text = []

    for page in doc:
        pix = page.get_pixmap(dpi=300)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        text = pytesseract.image_to_string(img)
        ocr_text.append(text)

    return "\n".join(ocr_text).strip()


def extract_image_to_text(image_bytes: bytes) -> str:
    try:
        img = Image.open(BytesIO(image_bytes))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid image file.")
    return pytesseract.image_to_string(img).strip()


async def extract_note_text(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1].lower()
    content = await file.read()

    # TEXT & MARKDOWN
    if ext in ["txt", "md"]:
        return content.decode("utf-8", errors="ignore")

    # IMAGES → OCR
    if ext in ["png", "jpg", "jpeg", "webp"]:
        return extract_image_to_text(content)

    # PDF → digital or scanned?
    if ext == "pdf":
        digital_md = extract_pdf_to_markdown(content)
        if len(digital_md.strip()) < 20:  # likely scanned
            return extract_scanned_pdf(content)
        return digital_md

    raise HTTPException(
        status_code=400,
        detail="Unsupported file type. Use txt, md, pdf, png, jpg, jpeg, webp."
    )


@router.post("/learn")
async def learn_style_from_input(
    current_profile: str = Form(...),
    user_text: str = Form(None),
    file: UploadFile = File(None)
):
    # Load existing style profile
    try:
        current_profile = json.loads(current_profile)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON for current_profile")

    if file:
        note_text = await extract_note_text(file)
    else:
        note_text = user_text or ""

    if not note_text.strip():
        raise HTTPException(status_code=400, detail="No text provided for learning")

    try:
        learner = StyleLearnerAgent(api_key="AIz..k")
        learned_json = learner.run(note_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Style learner failed: {e}")

    new_profile = current_profile.copy()
    for key, value in learned_json.items():
        new_profile[key] = value

    from datetime import datetime
    new_profile["updated_at"] = datetime.now().isoformat()

    try:
        update_style_profiles([new_profile])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save profile: {e}")

    return new_profile