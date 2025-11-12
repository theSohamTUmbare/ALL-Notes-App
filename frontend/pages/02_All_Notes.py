import streamlit as st
from datetime import datetime
from styles import page_header, apply_global_styles
from components import (
    init_session_state, get_notes_sorted, search_notes, delete_note,
    format_date, get_note_by_id
)

apply_global_styles()
init_session_state()

# page_header("Your Notes", "Browse and manage all your notes in one place")]
st.markdown("""
    <div style="text-align: center;">
        <h1>Your Notes</h1>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    search_query = st.text_input(
        "🔍 Search notes",
        placeholder="Type to search by title or content...",
        label_visibility="collapsed"
    )

with col2:
    sort_by = st.selectbox(
        "Sort by",
        ["Recently Modified", "Recently Created", "Title (A-Z)"],
        key="sort_select",
        label_visibility="collapsed"
    )

with col3:
    view_type = st.selectbox(
        "View",
        ["Grid", "List"],
        key="view_select",
        label_visibility="collapsed"
    )

st.markdown("---")

sort_map = {
    "Recently Modified": "modified",
    "Recently Created": "created",
    "Title (A-Z)": "title"
}

notes = get_notes_sorted(sort_by=sort_map[sort_by])

if search_query:
    notes = search_notes(search_query)
    st.markdown(f"<p style='color: #666666;'><strong>Found {len(notes)} note(s)</strong> matching '{search_query}'</p>", unsafe_allow_html=True)

if not notes:
    st.markdown("""
    <div style="text-align: center; padding: 60px 20px;">
        <div style="font-size: 3rem; margin-bottom: 10px;">📝</div>
        <h3 style="color: #666666; margin-bottom: 10px;">No notes yet</h3>
        <p style="color: #999999;">Create your first note to get started!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    if view_type == "Grid":
        cols = st.columns(2)
        for idx, note in enumerate(notes):
            with cols[idx % 2]:
                st.markdown(f"""
                <div class="card" style="min-height: 220px; display: flex; flex-direction: column;">
                    <div style="flex: 1;">
                        <h3 style="margin: 0 0 8px 0; color: #0066cc; cursor: pointer;" onclick="alert('{note['id']}')">{note['title']}</h3>
                        <p style="color: #666666; margin: 8px 0; font-size: 0.95rem; line-height: 1.5; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;">{note['content'][:150]}...</p>
                    </div>
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px; padding-top: 12px; border-top: 1px solid #e0e0e0;">
                        <small style="color: #999999;">{format_date(note['modified'])}</small>
                        <div>
                            <span style="display: inline-block; margin-left: 10px; color: #0066cc; cursor: pointer; font-size: 1.1rem;">👁️</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                col1, col2 = st.columns([3, 1])
                with col1:
                    if st.button("View", key=f"view_{note['id']}", use_container_width=True):
                        st.session_state.current_note_id = note['id']
                        st.switch_page("pages/03_Note_Detail.py")
                with col2:
                    if st.button("🗑️", key=f"delete_{note['id']}", help="Delete note"):
                        delete_note(note['id'])
                        st.success("Note deleted")
                        st.rerun()

    else:
        for note in notes:
            col1, col2, col3, col4 = st.columns([3, 1, 0.8, 0.5])

            with col1:
                st.markdown(f"""
                <div style="padding: 15px 0; border-bottom: 1px solid #e0e0e0;">
                    <h4 style="margin: 0 0 5px 0; color: #0066cc;">{note['title']}</h4>
                    <p style="margin: 5px 0; color: #666666; font-size: 0.9rem;">{note['content'][:100]}...</p>
                    <small style="color: #999999;">{format_date(note['modified'])}</small>
                </div>
                """, unsafe_allow_html=True)

            with col2:
                st.markdown(f"<div style='padding: 15px 0; border-bottom: 1px solid #e0e0e0; text-align: right;'><small style='color: #0066cc; font-weight: 600;'>{len(note['content'])} chars</small></div>", unsafe_allow_html=True)

            with col3:
                if st.button("View", key=f"view_list_{note['id']}", use_container_width=True):
                    st.session_state.current_note_id = note['id']
                    st.switch_page("pages/03_Note_Detail.py")

            with col4:
                if st.button("🗑️", key=f"delete_list_{note['id']}", help="Delete"):
                    delete_note(note['id'])
                    st.rerun()

st.markdown("---")

stats_col1, stats_col2, stats_col3 = st.columns(3)

with stats_col1:
    st.markdown(f"""
    <div style="background-color: #f8f9fa; border-radius: 8px; padding: 15px; text-align: center; border-left: 4px solid #0066cc;">
        <div style="font-size: 2rem; font-weight: 700; color: #0066cc;">{len(st.session_state.notes)}</div>
        <div style="color: #666666; font-size: 0.9rem;">Total Notes</div>
    </div>
    """, unsafe_allow_html=True)

with stats_col2:
    total_chars = sum(len(n['content']) for n in st.session_state.notes)
    st.markdown(f"""
    <div style="background-color: #f8f9fa; border-radius: 8px; padding: 15px; text-align: center; border-left: 4px solid #0066cc;">
        <div style="font-size: 2rem; font-weight: 700; color: #0066cc;">{total_chars:,}</div>
        <div style="color: #666666; font-size: 0.9rem;">Total Characters</div>
    </div>
    """, unsafe_allow_html=True)

with stats_col3:
    st.markdown(f"""
    <div style="background-color: #f8f9fa; border-radius: 8px; padding: 15px; text-align: center; border-left: 4px solid #0066cc;">
        <div style="font-size: 2rem; font-weight: 700; color: #0066cc;">{len([n for n in st.session_state.notes if n['attachments']])}</div>
        <div style="color: #666666; font-size: 0.9rem;">With Attachments</div>
    </div>
    """, unsafe_allow_html=True)
