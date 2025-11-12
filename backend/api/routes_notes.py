from fastapi import APIRouter
from db.database_manager import get_all_notes, get_note_by_id, delete_note
from typing import Dict, Any

router = APIRouter()

@router.get("/", response_model=list[Dict[str, Any]])
def fetch_notes():
    return get_all_notes()

@router.get("/{note_id}", response_model=Dict[str, Any])
def fetch_note_by_id(note_id: int):
    return get_note_by_id(note_id)

@router.delete("/{note_id}")
def remove_note(note_id: int):
    delete_note(note_id)
    return {"message": f"Note {note_id} deleted successfully."}
