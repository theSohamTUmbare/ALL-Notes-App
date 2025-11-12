import streamlit as st
from datetime import datetime

def init_session_state():
    """Initialize session state variables"""
    if 'notes' not in st.session_state:
        st.session_state.notes = [
            {
                'id': 1,
                'title': 'Welcome to All Notes',
                'content': 'This is your first note. Click on any note to read or edit it.',
                'created': datetime.now(),
                'modified': datetime.now(),
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


def get_note_by_id(note_id):
    """Get a note by its ID"""
    for note in st.session_state.notes:
        if note['id'] == note_id:
            return note
    return None


def create_note(title, content, instructions="", attachments=None):
    """Create a new note"""
    if attachments is None:
        attachments = []

    new_id = max([n['id'] for n in st.session_state.notes], default=0) + 1
    new_note = {
        'id': new_id,
        'title': title,
        'content': content,
        'instructions': instructions,
        'created': datetime.now(),
        'modified': datetime.now(),
        'tags': [],
        'attachments': attachments
    }
    st.session_state.notes.append(new_note)
    return new_id


def update_note(note_id, **kwargs):
    """Update a note's properties"""
    note = get_note_by_id(note_id)
    if note:
        note.update(kwargs)
        note['modified'] = datetime.now()
        return True
    return False


def delete_note(note_id):
    """Delete a note"""
    st.session_state.notes = [n for n in st.session_state.notes if n['id'] != note_id]


def add_chat_message(role, content):
    """Add a message to chat history"""
    st.session_state.chat_history.append({
        'role': role,
        'content': content,
        'timestamp': datetime.now()
    })


def clear_chat_history():
    """Clear all chat messages"""
    st.session_state.chat_history = []


def format_date(date_obj):
    """Format date for display"""
    if isinstance(date_obj, datetime):
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
        else:
            return date_obj.strftime("%b %d, %Y")
    return str(date_obj)


def search_notes(query):
    """Search notes by title and content"""
    query = query.lower()
    results = []
    for note in st.session_state.notes:
        if query in note['title'].lower() or query in note['content'].lower():
            results.append(note)
    return results


def get_notes_sorted(sort_by='modified'):
    """Get notes sorted by specified field"""
    if sort_by == 'modified':
        return sorted(st.session_state.notes, key=lambda n: n['modified'], reverse=True)
    elif sort_by == 'created':
        return sorted(st.session_state.notes, key=lambda n: n['created'], reverse=True)
    elif sort_by == 'title':
        return sorted(st.session_state.notes, key=lambda n: n['title'])
    return st.session_state.notes
