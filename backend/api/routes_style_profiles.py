from fastapi import APIRouter, Body, HTTPException
from typing import List, Dict, Any
from db.database_manager import (
    get_style_profiles,
    save_style_profiles,
    update_style_profiles
)

router = APIRouter()

@router.get("/", response_model=List[Dict[str, Any]])
def fetch_style_profiles():
    """
    Fetch all style profiles stored in the database.
    Returns the latest JSON list of profiles.
    """
    try:
        profiles = get_style_profiles()
        return profiles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch profiles: {e}")

@router.post("/", response_model=Dict[str, str])
def save_style_profiles_api(style_data: List[Dict[str, Any]] = Body(...)):
    """
    Save (replace) all style profiles.
    The incoming JSON should be a list of profile dicts.
    """
    try:
        save_style_profiles(style_data)
        return {"message": "Style profiles saved successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save profiles: {e}")

@router.put("/", response_model=Dict[str, str])
def update_style_profiles_api(style_data: List[Dict[str, Any]] = Body(...)):
    """
    Update the existing style profiles.
    The entire updated JSON array should be sent from frontend.
    """
    try:
        update_style_profiles(style_data)
        return {"message": "Style profiles updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update profiles: {e}")

@router.delete("/", response_model=Dict[str, str])
def delete_style_profiles():
    """
    Delete all style profiles (use cautiously).
    """
    from db.database_manager import delete_style_profiles  # optional if implemented
    try:
        delete_style_profiles()
        return {"message": "All style profiles deleted."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete profiles: {e}")
