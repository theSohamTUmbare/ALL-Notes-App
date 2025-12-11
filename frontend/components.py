import streamlit as st
import requests
from datetime import datetime

def format_datetime(dt):
    """Handle both datetime and string timestamps."""
    if isinstance(dt, str):
        try:
            dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # fallback if format slightly different
            return dt
    return dt.strftime("%b %d, %Y")

# --- Base API URL ---
API_BASE = "http://localhost:8000"

# ----------------------------- SESSION INIT --------------------------------
def init_session_state():
    """Initialize session state variables"""
    if 'notes' not in st.session_state:
        # Fetch notes from backend
        try:
            res = requests.get(f"{API_BASE}/notes")
            if res.status_code == 200:
                st.session_state.notes = res.json()
            else:
                st.session_state.notes = []
        except requests.exceptions.ConnectionError:
            st.warning("⚠️ Backend not reachable — using local fallback notes.")
            st.session_state.notes = [
                {
                    'id': 1,
                    'title': 'Welcome to All Notes',
                    'content': 'This is your first note. Click on any note to read or edit it.',
                    'created': datetime.now().isoformat(),
                    'modified': datetime.now().isoformat(),
                    'tags': ['welcome'],
                    'attachments': []
                }
            ]

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': 'User',
            'email': 'user@example.com',
            'theme': 'light',
            'notifications': True
        }

    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'

    if 'current_note_id' not in st.session_state:
        st.session_state.current_note_id = None

# ----------------------------- NOTE FUNCTIONS --------------------------------
def get_note_by_id(note_id):
    """Get a note by ID from backend"""
    try:
        res = requests.get(f"{API_BASE}/notes/{note_id}")
        if res.status_code == 200:
            return res.json()
    except requests.exceptions.RequestException:
        st.error("Failed to fetch note from backend.")
    return None

def get_style_profiles():
    """Fetch and return the active style profile JSON."""
    try:
        res = requests.get(f"{API_BASE}/style_profiles/")
        if res.status_code == 200:
            profiles = res.json()
            if profiles:
                return profiles[0]  # Return first (active) profile
            else:
                raise ValueError("No style profiles found in database.")
        else:
            raise RuntimeError(f"Backend returned {res.status_code}: {res.text}")
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Failed to reach backend: {e}")


def create_note(title, content, instructions="", attachments=None):
    """Create a new note via pipeline"""
    if attachments is None:
        attachments = []
    
    # Create pipeline input state
    state = {
        "ingestion_status": "pending",
        "input_source": content,
        "user_instruction": instructions,
        "document": None,
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
        "rewritten_notes": "Pending",
        "evaluation": None,
        "total_score": None,
        "user_choice": None,
        "llm": None,
        "retriever": None,
        "index_data": {},
        "indexing_status": "pending",
        "user_query": None,
        "qna_output": {},
        "user_interest": "AI",
        "recommendations": None,
        "api_key": 'AI....k',
        "profile_id": None,
        "profile_path": None,
        "style_profile": get_style_profiles(),
        
    }

    try:
        res = requests.post(f"{API_BASE}/pipeline/run", json=state)
        if res.status_code == 200:
            new_note = res.json()
            st.session_state.notes.append(new_note)
            return new_note.get("id", len(st.session_state.notes))
        else:
            st.error(f"Pipeline error: {res.text}")
    except requests.exceptions.RequestException:
        st.error("Backend not reachable during note creation.")
    return None


def update_note(note_id, **kwargs):
    """Update a note in session (for now; could be PUT to backend if added)"""
    note = next((n for n in st.session_state.notes if n['id'] == note_id), None)
    if note:
        note.update(kwargs)
        note['updated_at'] = datetime.now().isoformat()
        return True
    return False


def delete_note(note_id):
    """Delete a note via backend"""
    try:
        res = requests.delete(f"{API_BASE}/notes/{note_id}")
        if res.status_code == 200:
            st.session_state.notes = [n for n in st.session_state.notes if n['id'] != note_id]
            st.success(f"🗑️ Note {note_id} deleted successfully.")
            return True
    except requests.exceptions.RequestException:
        st.error("Failed to delete note — backend unreachable.")
    return False


def refresh_notes():
    """Reload all notes from backend"""
    try:
        res = requests.get(f"{API_BASE}/notes")
        if res.status_code == 200:
            st.session_state.notes = res.json()
    except requests.exceptions.RequestException:
        st.error("⚠️ Failed to refresh notes from backend.")


# ----------------------------- CHAT FUNCTIONS --------------------------------
def add_chat_message(role, content):
    """Add message locally to chat history"""
    st.session_state.chat_history.append({
        'role': role,
        'content': content,
        'timestamp': datetime.now().isoformat()
    })


def clear_chat_history():
    """Clear all chat messages"""
    st.session_state.chat_history = []


# ----------------------------- UTILITIES --------------------------------
def format_date(date_str):
    """Format ISO date string for display"""
    try:
        date_obj = datetime.fromisoformat(date_str)
    except Exception:
        return str(date_str)

    now = datetime.now()
    diff = now - date_obj

    if diff.days == 0:
        if diff.seconds < 60:
            return "just now"
        elif diff.seconds < 3600:
            mins = diff.seconds // 60
            return f"{mins}m ago"
        else:
            hours = diff.seconds // 3600
            return f"{hours}h ago"
    elif diff.days == 1:
        return "yesterday"
    elif diff.days < 7:
        return f"{diff.days}d ago"
    return date_obj.strftime("%b %d, %Y")


def search_notes(query):
    """Search notes locally"""
    query = query.lower()
    results = []
    for note in st.session_state.notes:
        if query in note['title'].lower() or query in note['content'].lower():
            results.append(note)
    return results


def get_notes_sorted(sort_by='modified'):
    """Get notes sorted by specified field"""
    key_func = lambda n: n.get(sort_by) or ""
    reverse = sort_by in ['modified', 'created']
    try:
        return sorted(st.session_state.notes, key=key_func, reverse=reverse)
    except Exception:
        return st.session_state.notes
    
    