import streamlit as st
from datetime import datetime
from styles import page_header, apply_global_styles, success_message
from components import (
    init_session_state, get_note_by_id, update_note, delete_note,
    format_date, format_datetime, add_chat_message
)
import re 
import requests

st.set_page_config(
    layout="wide",
)

# ---------- Setup ----------
apply_global_styles()
init_session_state()
API_BASE = "http://localhost:8000"

# ---------- Load Note ----------
if st.session_state.current_note_id is None:
    st.warning("No note selected. Please select one from All Notes.")
    st.stop()

note = get_note_by_id(st.session_state.current_note_id)
if note is None:
    st.error("Note not found")
    st.stop()

# ---------- Page Header ----------
clean_title = re.sub(r'^#+\s*', '', note['title']).strip()

col1, col2 = st.columns([3, 1])
with col1:
    page_header(clean_title, f"Last modified: {format_date(note['updated_at'])}")
with col2:
    chat_active = st.session_state.get("chat_open", False)
    if st.button("💬 Chat", use_container_width=True):
        st.session_state.chat_open = not chat_active
        st.rerun()

# ===========================================================
# STYLED SPLIT LAYOUT USING STREAMLIT COLUMNS
# ===========================================================
chat_open = st.session_state.get("chat_open", False)

if chat_open:
    main_col, chat_col = st.columns([2.2, 1.4])
else:
    main_col = st.container()
    chat_col = None

# ---- CSS Styling ----
st.markdown("""
    <style>
        .main-panel {
            background-color: #ffffff;
            padding: 1px;
            border-radius: 1px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            border-right: 2px solid #e8e8e8;
            height: 2px;
        }
        .chat-panel {
            background-color: #fafbfc;
            padding: 1px;
            border-radius: 1px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            height: 2px;
            position: fixed;
            top: 10px;
            z-index: 9999;
        }
        .chat-header {
            text-align: center;
            margin-bottom: 15px;
        }
        .chat-bubble {
            border-radius: 12px;
            padding: 10px 14px;
            margin-bottom: 8px;
            max-width: 85%;
            word-wrap: break-word;
        }
        .user-bubble {
            background-color: #0066cc;
            color: white;
            align-self: flex-end;
        }
        .assistant-bubble {
            background-color: #f1f3f5;
            color: #333;
            align-self: flex-start;
        }
    </style>
""", unsafe_allow_html=True)

# ===========================================================
# LEFT PANEL (NOTE VIEWER)
# ===========================================================
with main_col:
    st.markdown("<div class='main-panel'>", unsafe_allow_html=True)

    # --- Display Top 3 Tags ---
    if note.get('tags'):
        top_tags = note['tags'][:3]  # 
        tags_html = " ".join(
            [f"<span style='background-color:#e0f0ff; color:#0066cc; padding:6px 12px; border-radius:12px; font-size:1rem; margin-right:6px;'>{tag}</span>"
            for tag in top_tags]
        )
        st.markdown(f"""
        <div style="text-align:right; margin-bottom:15px;">
            {tags_html}
        </div>
        """, unsafe_allow_html=True)


    # st.markdown(f"""
    # <div style="background-color: #ffffff; padding: 20px; ; line-height: 1.8;">
    #     {note['content'].replace(chr(10), '<br>')}
    # </div>
    # """, unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown(note["content"])

    if note.get('instructions'):
        st.markdown("### Special Instructions")
        st.info(note['instructions'])

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #0066cc; text-align: center;">
            <small style="color: #666666; display: block; margin-bottom: 8px;">Created</small>
            <strong style="color: #0066cc;">{format_datetime(note['created_at'])}</strong>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #0066cc; text-align: center;">
            <small style="color: #666666; display: block; margin-bottom: 8px;">Modified</small>
            <strong style="color: #0066cc;">{format_date(note['updated_at'])}</strong>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #0066cc; text-align: center;">
            <small style="color: #666666; display: block; margin-bottom: 8px;">Length</small>
            <strong style="color: #0066cc;">{len(note['content'])} chars</strong>
        </div>
        """, unsafe_allow_html=True)


    # --- Concepts & Resources Section ---
if note.get('concepts') or note.get('resources'):
    st.markdown("### Additional Information")

    # Concepts
    if note.get('concepts'):
        st.markdown("""
        <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; margin-top:10px;">
            <strong style="color:#0066cc;">Concepts detected:</strong>
        """, unsafe_allow_html=True)

        for c in note['concepts']:
            st.markdown(
                f"<li style='margin-left:20px; color:#444; line-height:1.6;'>{c}</li>",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

    # Resources      
    if note.get('resources'):
        st.markdown("""
        <div style="background-color:#f8f9fa; padding:15px; border-radius:10px; margin-top:15px;">
            <strong style="color:#0066cc; font-size:1.1rem;">🔗 Resources</strong>
        """, unsafe_allow_html=True)

        resources = note["resources"]

        # resources is expected to be a dict like:
        # { "Data": [ {title, link, snippet}, ... ], "ML": [...], ... }

        for topic, items in resources.items():
            st.markdown(
                f"<h4 style='color:#333; margin-bottom:6px;'>{topic}</h4>",
                unsafe_allow_html=True
            )

            # each item inside topic is: {title, link, snippet}
            for item in items:
                title = item.get("title", "Untitled")
                link = item.get("link", None)
                snippet = item.get("snippet", "")

                st.markdown(
                    f"""
                    <div style="margin-left:20px; margin-bottom:12px; padding:10px 12px; background:#ffffff; border-radius:6px; border:1px solid #e0e0e0;">
                        <div style="font-weight:600; color:#0056b3; font-size:0.95rem;">
                            {f"<a href='{link}' target='_blank'>{title}</a>" if link else title}
                        </div>
                        <div style="color:#555; margin-top:4px; font-size:0.85rem; line-height:1.4;">
                            {snippet}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("</div>", unsafe_allow_html=True)



    st.markdown("</div>", unsafe_allow_html=True)

# ===========================================================
# RIGHT PANEL (CHAT)
# ===========================================================
if chat_col:
    with chat_col:
        st.markdown("""
                    <div class='chat-panel'>
        """, unsafe_allow_html=True)
        if st.button("❌ Close Chat", use_container_width=True):
            st.session_state.chat_open = False
            st.rerun()
        st.markdown("""
            <div class='chat-header' style="border: 2px solid #e0e0e0; border-radius: 8px;">
                <h3>💬 Chat with this Note</h3>
                <p style="color:#666; font-size:0.9rem;">Ask questions about this note</p>
            </div>
        """, unsafe_allow_html=True)

        note_chat_key = f"chat_history_{note['id']}"
        if note_chat_key not in st.session_state:
            st.session_state[note_chat_key] = []

        chat_area = st.container()
        with chat_area:
            if not st.session_state[note_chat_key]:
                st.info("No conversation yet. Start chatting below 👇")
            else:
                for msg in st.session_state[note_chat_key]:
                    bubble_class = "user-bubble" if msg["role"] == "user" else "assistant-bubble"
                    st.markdown(f"<div class='chat-bubble {bubble_class}'>{msg['content']}</div>", unsafe_allow_html=True)

        st.markdown("---")
        query = st.text_input("Ask something...", key=f"chat_input_{note['id']}")
        if st.button("Send", key=f"send_btn_{note['id']}") and query.strip():
            st.session_state[note_chat_key].append({"role": "user", "content": query, "timestamp": datetime.now()})
            with st.spinner("Thinking..."):
                try:
                    res = requests.post(f"{API_BASE}/chat/note", json={"note_id": note["id"], "query": query})
                    if res.status_code == 200:
                        data = res.json()
                        response = data.get("response", "⚠️ No response.")
                        st.session_state[note_chat_key].append({"role": "assistant", "content": response, "timestamp": datetime.now()})
                    else:
                        st.session_state[note_chat_key].append({"role": "assistant", "content": f"❌ Error: {res.text}", "timestamp": datetime.now()})
                except requests.exceptions.RequestException:
                    st.session_state[note_chat_key].append({"role": "assistant", "content": "⚠️ Backend unreachable.", "timestamp": datetime.now()})
            st.rerun()

        st.markdown("---")
        

        st.markdown("</div>", unsafe_allow_html=True)





























# import streamlit as st
# from datetime import datetime
# from styles import page_header, apply_global_styles, success_message, error_message
# from components import init_session_state, get_note_by_id, update_note, delete_note, format_date, format_datetime

# apply_global_styles()
# init_session_state()

# if st.session_state.current_note_id is None:
#     st.warning("No note selected. Please select a note from the All Notes page.")
#     st.stop()

# note = get_note_by_id(st.session_state.current_note_id)

# if note is None:
#     st.error("Note not found")
#     st.stop()

# col1, col2 = st.columns([3, 1])

# with col1:
#     page_header(note['title'], f"Last modified: {format_date(note['updated_at'])}")

# with col2:
#     if st.button("← Back", use_container_width=True):
#         st.session_state.current_note_id = None
#         st.switch_page("pages/02_All_Notes.py")

# tab1, tab2, tab3 = st.tabs(["View", "Edit", "Attachments"])

# with tab1:
#     st.markdown(f"""
#     <div style="background-color: #ffffff; padding: 20px; ; line-height: 1.8;">
#         {note['content'].replace(chr(10), '<br>')}
#     </div>
#     """, unsafe_allow_html=True)

#     if note.get('instructions'):
#         st.markdown("### Special Instructions")
#         st.info(note['instructions'])

#     st.markdown("---")

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.markdown(f"""
#         <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #0066cc; text-align: center;">
#             <small style="color: #666666; display: block; margin-bottom: 8px;">Created</small>
#             <strong style="color: #0066cc;">{format_datetime(note['created_at'])}</strong>
#         </div>
#         """, unsafe_allow_html=True)

#     with col2:
#         st.markdown(f"""
#         <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #0066cc; text-align: center;">
#             <small style="color: #666666; display: block; margin-bottom: 8px;">Modified</small>
#             <strong style="color: #0066cc;">{format_date(note['updated_at'])}</strong>
#         </div>
#         """, unsafe_allow_html=True)

#     with col3:
#         st.markdown(f"""
#         <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #0066cc; text-align: center;">
#             <small style="color: #666666; display: block; margin-bottom: 8px;">Length</small>
#             <strong style="color: #0066cc;">{len(note['content'])} chars</strong>
#         </div>
#         """, unsafe_allow_html=True)

# with tab2:
#     st.markdown("### Edit Note")

#     edited_title = st.text_input("Title", value=note['title'])
#     edited_content = st.text_area("Content", value=note['content'], height=300)
#     edited_instructions = st.text_area("Instructions", value=note.get('instructions', ''), height=100)

#     col1, col2, col3 = st.columns([2, 1, 1])

#     with col1:
#         if st.button("💾 Save Changes", use_container_width=True):
#             update_note(
#                 note['id'],
#                 title=edited_title,
#                 content=edited_content,
#                 instructions=edited_instructions
#             )
#             success_message("Note updated successfully!")
#             st.rerun()

#     with col2:
#         if st.button("🔄 Discard", use_container_width=True):
#             st.rerun()

#     with col3:
#         if st.button("🗑️ Delete", use_container_width=True):
#             delete_note(note['id'])
#             st.success("Note deleted")
#             st.switch_page("pages/02_All_Notes.py")

# with tab3:
#     st.markdown("### Attachments")

#     if note.get('attachments'):
#         for attachment in note['attachments']:
#             st.markdown(f"""
#             <div class="card">
#                 <div style="display: flex; justify-content: space-between; align-items: center;">
#                     <div>
#                         <strong>📄 {attachment['name']}</strong>
#                         <br>
#                         <small style="color: #999999;">{attachment['size']} bytes</small>
#                     </div>
#                     <button style="padding: 8px 16px; background-color: #0066cc; color: white; border: none; border-radius: 4px; cursor: pointer;">Download</button>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)
#     else:
#         st.info("No attachments yet. Upload files from the Home page to attach them to notes.")

#     st.markdown("---")
#     st.markdown("### Add New Attachment")
#     new_attachment = st.file_uploader("Choose a file", key=f"attach_{note['id']}", label_visibility="collapsed")

#     if new_attachment:
#         if st.button("📎 Attach File"):
#             if 'attachments' not in note:
#                 note['attachments'] = []

#             note['attachments'].append({
#                 'name': new_attachment.name,
#                 'size': new_attachment.size,
#                 'type': new_attachment.type
#             })
#             update_note(note['id'], attachments=note['attachments'])
#             success_message(f"File '{new_attachment.name}' attached!")
#             st.rerun()

# st.markdown("---")

# st.markdown("""
# <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px;">
#     <p style="color: #666666; margin: 0; font-size: 0.9rem;">
#         <strong>Note ID:</strong> {0} |
#         <strong>Words:</strong> {1} |
#         <strong>Paragraphs:</strong> {2}
#     </p>
# </div>
# """.format(note['id'], len(note['content'].split()), len(note['content'].split('\n'))), unsafe_allow_html=True)
