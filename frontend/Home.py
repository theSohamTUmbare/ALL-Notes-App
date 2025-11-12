import streamlit as st
from styles import apply_global_styles
from components import init_session_state

st.set_page_config(
    page_title="All Notes",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_global_styles()
init_session_state()

# st.markdown("""
# <style>
#     [data-testid="stSidebarNav"] {
#         background-color: #f8f9fa;
#     }
# </style>
# """, unsafe_allow_html=True)

# st.sidebar.markdown("""
# <div style="padding: 20px 0; border-bottom: 1px solid #e0e0e0; margin-bottom: 20px;">
#     <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 5px;">
#         <div style="font-size: 2rem;">📝</div>
#         <div>
#             <h1 style="margin: 0; font-size: 1.5rem; color: #0066cc;">All Notes</h1>
#             <p style="margin: 0; font-size: 0.8rem; color: #999999;">Professional Note Manager</p>
#         </div>
#     </div>
# </div>
# """, unsafe_allow_html=True)

# st.sidebar.markdown("### Navigation")

# pages = {
#     "🏠 Home": "pages/01_Home.py",
#     "📋 All Notes": "pages/02_All_Notes.py",
#     "💬 Chat": "pages/04_Chat.py",
#     "⚙️ Style Profile": "pages/05_Style_Profile.py",
# }

# for page_name, page_path in pages.items():
#     if st.sidebar.button(page_name, use_container_width=True, key=f"nav_{page_name}"):
#         st.switch_page(page_path)

# st.sidebar.markdown("---")

# st.sidebar.markdown("""
# <div style="background-color: #f0f7ff; padding: 15px; border-radius: 8px; border-left: 4px solid #0066cc;">
#     <p style="margin: 0 0 10px 0; color: #0066cc; font-weight: 600;">📊 Quick Stats</p>
#     <div style="font-size: 1.8rem; font-weight: 700; color: #0066cc; margin: 8px 0;">""" + str(len(st.session_state.notes)) + """</div>
#     <p style="margin: 0; color: #666666; font-size: 0.9rem;">Total Notes</p>
# </div>
# """, unsafe_allow_html=True)

# st.sidebar.markdown("---")

# st.sidebar.markdown("""
# <div style="color: #999999; font-size: 0.85rem; text-align: center; padding-top: 20px;">
#     <p style="margin: 5px 0;"><strong>All Notes v1.0</strong></p>
#     <p style="margin: 5px 0;">Professional Note Manager</p>
#     <p style="margin: 5px 0; border-top: 1px solid #e0e0e0; padding-top: 10px;">
#         <a href="#" style="color: #0066cc; text-decoration: none;">Privacy</a> •
#         <a href="#" style="color: #0066cc; text-decoration: none;">Terms</a> •
#         <a href="#" style="color: #0066cc; text-decoration: none;">Support</a>
#     </p>
# </div>
# """, unsafe_allow_html=True)

# st.markdown("""
# <div style="text-align: center; padding: 60px 20px;">
#     <div style="font-size: 4rem; margin-bottom: 15px; animation: bounce 2s infinite;">📝</div>
#     <h1 style="color: #0066cc; font-size: 2.5rem; margin: 10px 0;">Welcome to All Notes</h1>
#     <p style="color: #666666; font-size: 1.2rem; margin: 10px 0;">Your professional note management solution</p>

#     <div style="margin-top: 30px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px; max-width: 600px; margin-left: auto; margin-right: auto;">
#         <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #0066cc;">
#             <div style="font-size: 2rem; margin-bottom: 10px;">✨</div>
#             <h3 style="margin: 0 0 5px 0; color: #0066cc;">Easy Creation</h3>
#             <p style="margin: 0; color: #666666; font-size: 0.9rem;">Create and organize notes in seconds</p>
#         </div>
#         <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #0066cc;">
#             <div style="font-size: 2rem; margin-bottom: 10px;">🔍</div>
#             <h3 style="margin: 0 0 5px 0; color: #0066cc;">Fast Search</h3>
#             <p style="margin: 0; color: #666666; font-size: 0.9rem;">Find any note instantly with powerful search</p>
#         </div>
#         <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #0066cc;">
#             <div style="font-size: 2rem; margin-bottom: 10px;">💬</div>
#             <h3 style="margin: 0 0 5px 0; color: #0066cc;">Smart Chat</h3>
#             <p style="margin: 0; color: #666666; font-size: 0.9rem;">Chat with AI about your notes</p>
#         </div>
#         <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #0066cc;">
#             <div style="font-size: 2rem; margin-bottom: 10px;">📊</div>
#             <h3 style="margin: 0 0 5px 0; color: #0066cc;">Insights</h3>
#             <p style="margin: 0; color: #666666; font-size: 0.9rem;">Get insights and analytics on your notes</p>
#         </div>
#     </div>
# </div>

# <style>
#     @keyframes bounce {
#         0%, 100% { transform: translateY(0); }
#         50% { transform: translateY(-10px); }
#     }
# </style>
# """, unsafe_allow_html=True)

# st.markdown("---")

# st.markdown("""
# <div style="background: linear-gradient(135deg, #0066cc 0%, #004499 100%); color: white; padding: 40px 20px; border-radius: 12px; text-align: center; margin: 30px 0;">
#     <h2 style="color: white; margin: 0 0 10px 0;">Ready to get started?</h2>
#     <p style="color: rgba(255,255,255,0.9); margin: 0 0 20px 0; font-size: 1.1rem;">Create your first note or browse existing ones</p>
# </div>
# """, unsafe_allow_html=True)


import streamlit as st
from datetime import datetime
from styles import page_header, apply_global_styles, success_message, error_message
from components import init_session_state, create_note

apply_global_styles()
init_session_state()

# page_header("What will you note today?", "Create and organize your notes effortlessly")
st.markdown("""
    <div style="text-align: center;">
        <h1>What will you note today?</h1>
        <p style="font-size: 18px; color: gray;">Create and organize your notes effortlessly</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%); border-radius: 12px; padding: 20px; margin-bottom: 30px; border-left: 4px solid #0066cc;">
    <p style="color: #0066cc; font-size: 1.1rem; margin: 0;"><strong>✨ Pro Tip:</strong> Add clear titles and detailed notes for better organization and search.</p>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Note Content")
    note_title = st.text_input(
        "Title",
        placeholder="Enter a meaningful title for your note",
        label_visibility="collapsed"
    )

    note_content = st.text_area(
        "Content",
        placeholder="Write your thoughts, ideas, or information here... You can write as much as you need.",
        height=250,
        label_visibility="collapsed"
    )

with col2:
    st.markdown("### Additional Info")

    st.markdown("""
    <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 15px;">
        <p style="font-size: 0.9rem; color: #666666; margin: 0 0 10px 0;"><strong>Character Count:</strong></p>
        <p style="font-size: 1.5rem; color: #0066cc; margin: 0; font-weight: 700;">
    """ + str(len(note_content)) + """
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("### Instructions (Optional)")
instructions = st.text_area(
    "Add special instructions or tags",
    placeholder="e.g., 'Format as markdown' or 'Important - Follow up needed'",
    height=40,
    label_visibility="collapsed"
)

st.markdown("### Attachments (Optional)")
uploaded_file = st.file_uploader(
    "Upload files to attach to this note",
    key="note_attachment",
    label_visibility="collapsed"
)

st.markdown("---")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    if st.button("Create Note", use_container_width=True, key="create_btn"):
        if not note_title.strip():
            error_message("Please enter a title for your note")
        elif not note_content.strip():
            error_message("Please enter some content for your note")
        else:
            attachments = []
            if uploaded_file:
                attachments.append({
                    'name': uploaded_file.name,
                    'size': uploaded_file.size,
                    'type': uploaded_file.type
                })

            note_id = create_note(
                title=note_title,
                content=note_content,
                instructions=instructions,
                attachments=attachments
            )

            success_message(f"Note created successfully! #notes/v{note_id}")
            st.balloons()

            st.session_state.note_title = ""
            st.session_state.note_content = ""
            st.session_state.instructions = ""

with col2:
    if st.button("Draft", use_container_width=True):
        st.info("Draft saved to session")

with col3:
    if st.button("Reset", use_container_width=True):
        st.rerun()

st.markdown("---")

st.markdown("""
<div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 30px;">
    <h3 style="margin-top: 0; color: #0066cc;">💡 How to Use All Notes</h3>
    <ul style="color: #666666; line-height: 1.8;">
        <li><strong>Create:</strong> Write your note with a clear title and provide detailed content</li>
        <li><strong>Organize:</strong> Add instructions to customize your notes</li>
        <li><strong>Find:</strong> Use the search feature to quickly locate any note</li>
        <li><strong>Chat:</strong> Ask questions about your notes using the chat feature</li>
        <li><strong>Export:</strong> Download your notes in various formats</li>
    </ul>
</div>
""", unsafe_allow_html=True)
