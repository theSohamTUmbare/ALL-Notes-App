from fastapi import APIRouter, Body
from typing import Dict, Any
from run_pipeline import run_workflow, make_json_safe

router = APIRouter()

@router.post("/run")
def run_pipeline_api(state: Dict[str, Any] = Body(...)):
    """Run the LangGraph pipeline and return the final processed state."""
    final_state = run_workflow(state)
    return make_json_safe(final_state)


