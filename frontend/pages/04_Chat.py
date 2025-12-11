import streamlit as st
import requests
from datetime import datetime
from styles import page_header, apply_global_styles
from components import init_session_state, add_chat_message, clear_chat_history, format_date

# Apply UI style and initialize session
apply_global_styles()
init_session_state()

st.set_page_config(
    layout="wide",
)

API_BASE = "http://localhost:8000"

# ---------- HEADER ----------
st.markdown("""
    <div style="text-align: center;">
        <h1>💬 Chat Assistant</h1>
        <p style="color: #666;">Ask anything about your notes or explore them intelligently</p>
    </div>d=
""", unsafe_allow_html=True)

# ---------- MODE SELECTOR ----------
st.markdown("---")
mode = st.radio("Choose Chat Mode", ["Chat with All Notes 🌍", "Chat with a Specific Note 📘"])

note_id = None
if mode == "Chat with a Specific Note 📘":
    note_id = st.number_input("Enter Note ID to chat with:", min_value=1, step=1)

# ---------- CHAT HISTORY DISPLAY ----------
chat_container = st.container()

with chat_container:
    if not st.session_state.chat_history:
        st.markdown("""
        <div style="text-align: center; padding: 40px 20px; color: #999999;">
            <div style="font-size: 2.5rem; margin-bottom: 10px;">💭</div>
            <p><strong>No messages yet</strong></p>
            <p style="font-size: 0.9rem;">Start a conversation by typing below!</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-end; margin-bottom: 12px;">
                    <div style="background-color: #0066cc; color: white; padding: 12px 16px; border-radius: 12px; max-width: 70%; border-bottom-right-radius: 2px; word-wrap: break-word;">
                        <p style="margin: 0; line-height: 1.5;">{message['content']}</p>
                        <small style="opacity: 0.8; display: block; margin-top: 4px; text-align: right;">{format_date(message['timestamp'])}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; justify-content: flex-start; margin-bottom: 12px;">
                    <div style="background-color: #f0f0f0; color: #333333; padding: 12px 16px; border-radius: 12px; max-width: 70%; border-bottom-left-radius: 2px; word-wrap: break-word;">
                        <p style="margin: 0; line-height: 1.5;">{message['content']}</p>
                        <small style="opacity: 0.7; display: block; margin-top: 4px;">{format_date(message['timestamp'])}</small>
                    </div>
                </div>
                """, unsafe_allow_html=True)

# ---------- MESSAGE INPUT ----------
st.markdown("---")
st.markdown("### Send a Message")

col1, col2 = st.columns([4, 1])

with col1:
    user_message = st.text_input(
        "Your message",
        placeholder="Ask me anything about your notes...",
        label_visibility="collapsed"
    )

with col2:
    send_button = st.button("Send", use_container_width=True)

# ---------- BACKEND CHAT REQUEST ----------
if send_button and user_message:
    add_chat_message("user", user_message)

    with st.spinner("Thinking... 🧠"):
        try:
            if mode == "Chat with All Notes 🌍":
                res = requests.post(f"{API_BASE}/chat/global", json={"query": user_message})
            else:
                res = requests.post(f"{API_BASE}/chat/note", json={"note_id": note_id, "query": user_message})

            if res.status_code == 200:
                data = res.json()
                response = data.get("response", "⚠️ No response received from backend.")
                add_chat_message("assistant", response)
            else:
                add_chat_message("assistant", f"❌ Error: {res.text}")
        except requests.exceptions.RequestException:
            add_chat_message("assistant", "⚠️ Could not reach backend.")

    st.rerun()

# ---------- FOOTER WITH QUICK SUGGESTIONS ----------
st.markdown("---")
st.markdown("""
<div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 30px;">
    <h4 style="margin-top: 0; color: #0066cc;">Suggested Questions</h4>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
        <button onclick="alert('Summarize my notes')" style="padding: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; text-align: left;">
            <strong>Summarize my notes</strong><br><small>- Get a quick overview</small>
        </button>
        <button onclick="alert('Organize by topic')" style="padding: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; text-align: left;">
            <strong>Organize by topic</strong><br><small>- Auto-categorize content</small>
        </button>
        <button onclick="alert('Find related notes')" style="padding: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; text-align: left;">
            <strong>Find related notes</strong><br><small>- Discover connections</small>
        </button>
        <button onclick="alert('Generate report')" style="padding: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; text-align: left;">
            <strong>Generate report</strong><br><small>- Create summary document</small>
        </button>
    </div>
</div>
""", unsafe_allow_html=True)



























# import streamlit as st
# from datetime import datetime
# from styles import page_header, apply_global_styles
# from components import init_session_state, add_chat_message, clear_chat_history, format_date

# apply_global_styles()
# init_session_state()

# # page_header("Chat Assistant", "Ask questions and get insights about your notes")
# st.markdown("""
#     <div style="text-align: center;">
#         <h1>Chat Assistant</h1>
#     </div>
# """, unsafe_allow_html=True)



# chat_container = st.container()

# with chat_container:
#     if not st.session_state.chat_history:
#         st.markdown("""
#         <div style="text-align: center; padding: 40px 20px; color: #999999;">
#             <div style="font-size: 2.5rem; margin-bottom: 10px;">💭</div>
#             <p><strong>No messages yet</strong></p>
#             <p style="font-size: 0.9rem;">Start a conversation by typing in the message box below</p>
#         </div>
#         """, unsafe_allow_html=True)
#     else:
#         for message in st.session_state.chat_history:
#             if message['role'] == 'user':
#                 st.markdown(f"""
#                 <div style="display: flex; justify-content: flex-end; margin-bottom: 12px;">
#                     <div style="background-color: #0066cc; color: white; padding: 12px 16px; border-radius: 12px; max-width: 70%; border-bottom-right-radius: 2px; word-wrap: break-word;">
#                         <p style="margin: 0; line-height: 1.5;">{message['content']}</p>
#                         <small style="opacity: 0.8; display: block; margin-top: 4px; text-align: right;">{format_date(message['timestamp'])}</small>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)
#             else:
#                 st.markdown(f"""
#                 <div style="display: flex; justify-content: flex-start; margin-bottom: 12px;">
#                     <div style="background-color: #f0f0f0; color: #333333; padding: 12px 16px; border-radius: 12px; max-width: 70%; border-bottom-left-radius: 2px; word-wrap: break-word;">
#                         <p style="margin: 0; line-height: 1.5;">{message['content']}</p>
#                         <small style="opacity: 0.7; display: block; margin-top: 4px;">{format_date(message['timestamp'])}</small>
#                     </div>
#                 </div>
#                 """, unsafe_allow_html=True)

# st.markdown("---")

# st.markdown("### Send a Message")

# col1, col2 = st.columns([4, 1])

# with col1:
#     user_message = st.text_input(
#         "Your message",
#         placeholder="Ask me anything about your notes...",
#         label_visibility="collapsed"
#     )

# with col2:
#     send_button = st.button("Send", use_container_width=True)

# if send_button and user_message:
#     add_chat_message("user", user_message)

#     response_messages = [
#         "That's a great question! Based on your notes, I can help you organize and find information more effectively.",
#         "I understand. Let me analyze your notes and provide insights on this topic.",
#         "Excellent point! Your notes contain relevant information that could help with this.",
#         "I'm here to help! Let me look through your notes and provide a comprehensive response.",
#         "That's an interesting query. Your notes have several references to this subject."
#     ]

#     import random
#     response = random.choice(response_messages)
#     add_chat_message("assistant", response)

#     st.rerun()

# st.markdown("---")

# st.markdown("""
# <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 30px;">
#     <h4 style="margin-top: 0; color: #0066cc;">Suggested Questions</h4>
#     <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
#         <button onclick="alert('Question 1')" style="padding: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; text-align: left; transition: all 0.3s ease;" onmouseover="this.style.borderColor='#0066cc'; this.style.boxShadow='0 2px 8px rgba(0,102,204,0.1)';" onmouseout="this.style.borderColor='#e0e0e0'; this.style.boxShadow='none';">
#             <strong style="color: #fffff0;">Summarize my notes</strong>
#             <br><small style="color: #ffffff;">- Get a quick overview</small>
#         </button>
#         <button onclick="alert('Question 2')" style="padding: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; text-align: left; transition: all 0.3s ease;" onmouseover="this.style.borderColor='#0066cc'; this.style.boxShadow='0 2px 8px rgba(0,102,204,0.1)';" onmouseout="this.style.borderColor='#e0e0e0'; this.style.boxShadow='none';">
#             <strong style="color: #fffff0;">Organize by topic</strong>
#             <br><small style="color: #ffffff;">- Auto-categorize content</small>
#         </button>
#         <button onclick="alert('Question 3')" style="padding: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; text-align: left; transition: all 0.3s ease;" onmouseover="this.style.borderColor='#0066cc'; this.style.boxShadow='0 2px 8px rgba(0,102,204,0.1)';" onmouseout="this.style.borderColor='#e0e0e0'; this.style.boxShadow='none';">
#             <strong style="color: #fffff0;">Find related notes</strong>
#             <br><small style="color: #ffffff;">- Discover connections</small>
#         </button>
#         <button onclick="alert('Question 4')" style="padding: 10px; background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 6px; cursor: pointer; text-align: left; transition: all 0.3s ease;" onmouseover="this.style.borderColor='#0066cc'; this.style.boxShadow='0 2px 8px rgba(0,102,204,0.1)';" onmouseout="this.style.borderColor='#e0e0e0'; this.style.boxShadow='none';">
#             <strong style="color: #fffff0;">Generate report</strong>
#             <br><small style="color: #ffffff;">- Create summary document</small>
#         </button>
#     </div>
# </div>
# """, unsafe_allow_html=True)


