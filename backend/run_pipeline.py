import json
from datetime import datetime
from typing import Dict, Any

from graph_pipeline import workflow
from state_schema import PipelineState
from db.database_manager import add_note, update_note
from db.chroma_manager import update_note_in_chroma

# Utility for pretty-printing state updates
def log_step(step_name: str, state: Dict[str, Any]):
    print(f"\n🧩 Step Completed: {step_name}")
    print(f"   Current ingestion_status: {state.get('ingestion_status')}")
    print(f"   Notemaking status: {state.get('notemaking_status')}")
    print(f"   Concept extraction status: {state.get('concept_extraction_status')}")
    print(f"   Tags: {state.get('tags')}")
    print(f"   Concepts: {state.get('concepts')}\n")


def run_workflow(initial_state: PipelineState) -> PipelineState:
    print("🚀 Starting LangGraph Workflow...")

    final_state = workflow.invoke(initial_state)
    print("✅ Workflow execution completed.\n")

    # --- Log final summary ---
    print("🧠 Final State Summary:")
    print(f"  Ingestion: {final_state.get('ingestion_status')}")
    print(f"  Notemaking: {final_state.get('notemaking_status')}")
    print(f"  Concept Extraction: {final_state.get('concept_extraction_status')}")
    print(f"  Web Search: {final_state.get('web_search_status')}")
    print(f" Tag Generation: {final_state.get('tag_generation_status')}")
    print(f"  Concepts Extracted: {final_state.get('concepts')}")
    print(f"  Tags Generated: {final_state.get('tags')}")
    print(f"  Indexing Status: {final_state.get('indexing_status')}")
    print(f"  Total Score: {final_state.get('total_score')}\n")

    # --- Store in database ---
    try:
        note_id = add_note(
            title=final_state.get("rewritten_notes").split("\n")[0][:50] or "Untitled Note",
            input_source=str(final_state.get("input_source")),
            content=final_state.get("rewritten_notes") or "",
            concepts=final_state.get("concepts", []),
            tags=final_state.get("tags", []),
            resources=final_state.get("resources", {}),
            evaluation=final_state.get("evaluation", {}),
            total_score=final_state.get("total_score", 0.0),
            indexing_status=final_state.get("indexing_status", "pending"),
        )

        print(f"💾 Note saved in database with ID: {note_id}")

        update_note_in_chroma(note_id, final_state.get("rewritten_notes").split("\n")[0][:50] or "Untitled Note", final_state.get("rewritten_notes") or "")
        print("Note indexed in Chroma vector store.")
        # Optional: mark as indexed or processed
        update_note(note_id, indexing_status="completed")

    except Exception as e:
        print("⚠️ Failed to store note in database:", e)

    return final_state


def make_json_safe(obj):
    """Recursively convert complex objects (like Document) into JSON-serializable forms."""
    from langchain_core.documents import Document

    if isinstance(obj, Document):
        return {
            "page_content": obj.page_content,
            "metadata": obj.metadata
        }
    elif isinstance(obj, list):
        return [make_json_safe(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    else:
        # Fallback: convert other unknown objects to strings
        return str(obj)



# --------------------------
# Standalone test runner
# --------------------------
if __name__ == "__main__":
    print("🧪 Running pipeline test with sample state...\n")

    # Example initial pipeline state (like from frontend)
    initial_state: PipelineState = {
        "ingestion_status": "pending",
        "input_source": """Skip to content
Chat history

You said:
what is aupr in machine learning
ChatGPT said:
AUPR stands for Area Under the Precision-Recall Curve
precision, recall, thresholds = precision_recall_curve(y_true, y_scores)
aupr = auc(recall, precision)  # or directly:
aupr_alt = average_precision_score(y_true, y_scores)

print("AUPR:", aupr)
print("Average Precision (AUPR):", aupr_alt)
Model A is better at maintaining high precision while keeping recall high — meaning it’s more reliable at detecting positives without too many false alarms.
Would you like me to show you a visual Precision-Recall curve comparison (with Python code and plot) to make it more intuitive?
""",
        "documents": None,
        "ingestion_meta": {"source": "user_input"},
        "notemaking_status": "pending",
        "clean_documents": None,
        "concept_extraction_status": "pending",
        "documents_with_concepts": None,
        "concepts": [],
        "tag_generation_status": "pending",
        "documents_with_tags": None,
        "tags": [],
        "web_search_status": "pending",
        "documents_with_resources": None,
        "resources": {},
        "style_rewrite_status": "pending",
        "rewritten_notes": "Placeholder rewritten note from agent...",
        "evaluation": {"accuracy": 0.9},
        "total_score": 9.5,
        "user_choice": "save",
        "llm": None,
        "retriever": None,
        "index_data": {},
        "indexing_status": "pending",
        "user_query": "Explain Transformers in simple terms",
        "qna_output": {},
        "user_interest": "AI",
        "recommendations": None,
        "api_key": 'AIza...0Lk',
        "profile_id": "concise_beginner",
        "profile_path": 'C:\\Users\\umbar\\OneDrive\\Documents\\Agentic_AI\\ALL Notes Project\\backend\\agents\\style_profile.json',
    }

    final_state = run_workflow(initial_state)

    print("\n🎯 Final Output State:")
    print(json.dumps(make_json_safe(final_state), indent=2))
    print(final_state.get("documents_with_concepts"))
    print(final_state.get("concepts"))
    print(final_state.get("tag_generation_status"))
    print(final_state.get("tags"))
    print(final_state.get("web_search_status"))
    print(final_state.get("documents_with_resources"))
    print(final_state.get("resources"))
