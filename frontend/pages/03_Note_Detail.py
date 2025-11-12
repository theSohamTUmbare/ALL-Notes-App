import streamlit as st
from datetime import datetime
from styles import page_header, apply_global_styles, success_message, error_message
from components import init_session_state, get_note_by_id, update_note, delete_note, format_date

apply_global_styles()
init_session_state()

if st.session_state.current_note_id is None:
    st.warning("No note selected. Please select a note from the All Notes page.")
    st.stop()

note = get_note_by_id(st.session_state.current_note_id)

if note is None:
    st.error("Note not found")
    st.stop()

col1, col2 = st.columns([3, 1])

with col1:
    page_header(note['title'], f"Last modified: {format_date(note['modified'])}")

with col2:
    if st.button("← Back", use_container_width=True):
        st.session_state.current_note_id = None
        st.switch_page("pages/02_All_Notes.py")

tab1, tab2, tab3 = st.tabs(["View", "Edit", "Attachments"])

with tab1:
    st.markdown(f"""
    <div style="background-color: #ffffff; padding: 20px; ; line-height: 1.8;">
        {note['content'].replace(chr(10), '<br>')}
    </div>
    """, unsafe_allow_html=True)

    if note.get('instructions'):
        st.markdown("### Special Instructions")
        st.info(note['instructions'])

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #0066cc; text-align: center;">
            <small style="color: #666666; display: block; margin-bottom: 8px;">Created</small>
            <strong style="color: #0066cc;">{note['created'].strftime('%b %d, %Y')}</strong>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #0066cc; text-align: center;">
            <small style="color: #666666; display: block; margin-bottom: 8px;">Modified</small>
            <strong style="color: #0066cc;">{note['modified'].strftime('%b %d, %Y')}</strong>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #0066cc; text-align: center;">
            <small style="color: #666666; display: block; margin-bottom: 8px;">Length</small>
            <strong style="color: #0066cc;">{len(note['content'])} chars</strong>
        </div>
        """, unsafe_allow_html=True)

with tab2:
    st.markdown("### Edit Note")

    edited_title = st.text_input("Title", value=note['title'])
    edited_content = st.text_area("Content", value=note['content'], height=300)
    edited_instructions = st.text_area("Instructions", value=note.get('instructions', ''), height=100)

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        if st.button("💾 Save Changes", use_container_width=True):
            update_note(
                note['id'],
                title=edited_title,
                content=edited_content,
                instructions=edited_instructions
            )
            success_message("Note updated successfully!")
            st.rerun()

    with col2:
        if st.button("🔄 Discard", use_container_width=True):
            st.rerun()

    with col3:
        if st.button("🗑️ Delete", use_container_width=True):
            delete_note(note['id'])
            st.success("Note deleted")
            st.switch_page("pages/02_All_Notes.py")

with tab3:
    st.markdown("### Attachments")

    if note.get('attachments'):
        for attachment in note['attachments']:
            st.markdown(f"""
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <strong>📄 {attachment['name']}</strong>
                        <br>
                        <small style="color: #999999;">{attachment['size']} bytes</small>
                    </div>
                    <button style="padding: 8px 16px; background-color: #0066cc; color: white; border: none; border-radius: 4px; cursor: pointer;">Download</button>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No attachments yet. Upload files from the Home page to attach them to notes.")

    st.markdown("---")
    st.markdown("### Add New Attachment")
    new_attachment = st.file_uploader("Choose a file", key=f"attach_{note['id']}", label_visibility="collapsed")

    if new_attachment:
        if st.button("📎 Attach File"):
            if 'attachments' not in note:
                note['attachments'] = []

            note['attachments'].append({
                'name': new_attachment.name,
                'size': new_attachment.size,
                'type': new_attachment.type
            })
            update_note(note['id'], attachments=note['attachments'])
            success_message(f"File '{new_attachment.name}' attached!")
            st.rerun()

st.markdown("---")

st.markdown("""
<div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px;">
    <p style="color: #666666; margin: 0; font-size: 0.9rem;">
        <strong>Note ID:</strong> {0} |
        <strong>Words:</strong> {1} |
        <strong>Paragraphs:</strong> {2}
    </p>
</div>
""".format(note['id'], len(note['content'].split()), len(note['content'].split('\n'))), unsafe_allow_html=True)
