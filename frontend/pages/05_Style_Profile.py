import streamlit as st
import requests
import pandas as pd
from styles import page_header, apply_global_styles, success_message
from components import init_session_state
import json

apply_global_styles()
init_session_state()

st.set_page_config(
    layout="wide",
)

API_BASE = "http://localhost:8000"

page_header("🎨 Style Profile", "Personalize your All Notes experience")




            
# Fetch profiles from backend 
try:
    res = requests.get(f"{API_BASE}/style_profiles/")
    if res.status_code == 200:
        style_profiles = res.json()
    else:
        st.error("❌ Failed to fetch style profiles from backend.")
        st.stop()
except requests.exceptions.RequestException:
    st.error("⚠️ Backend not reachable.")
    st.stop()

if not style_profiles:
    st.warning("No style profiles found in database.")
    st.stop()

# Only show first profile for now (assuming single active profile)
profile = style_profiles[0]


# # Flatten nested keys (only top-level important keys)
# important_keys = [
#     "profile_id",
#     "name",
#     "user_persona",
#     "description",
#     "custom_instruction",
#     "tone",
#     "detail",
#     "abstraction",
#     "formatting",
#     "structure",
#     "language",
#     "stylistic_devices",
# ]

# # Extract a readable list of rows
# editable_rows = []
# for key in important_keys:
#     val = profile.get(key, "")
#     if isinstance(val, dict):
#         val = str(val)  # show nested dict as string
#     editable_rows.append({"Key": key, "Value": val})

# # Convert to DataFrame for display
# df = pd.DataFrame(editable_rows)

# st.markdown("### 📝 Edit Style Profile")
# st.markdown("""
# Press enter after modifying each cell to register the change.
# """)

# # Editable table (requires Streamlit >= 1.22)
# edited_df = st.data_editor(
#     df,
#     use_container_width=True,
#     num_rows="fixed",
#     hide_index=True,
#     key="style_editor",
# )

# # Save button 
# if st.button("💾 Save Changes", use_container_width=True, type="primary"):
#     # Apply user edits back into JSON
#     updated_profile = profile.copy()
#     for _, row in edited_df.iterrows():
#         key, value = row["Key"], row["Value"]
#         # Try to reparse dict-like strings safely
#         if key in important_keys:
#             if key in profile and isinstance(profile[key], dict):
#                 try:
#                     updated_profile[key] = eval(value)  # from string back to dict
#                 except Exception:
#                     updated_profile[key] = value
#             else:
#                 updated_profile[key] = value

#     # Wrap in list (since backend expects list of profiles)
#     updated_profiles = [updated_profile]

#     # Send PUT request to backend
#     try:
#         res = requests.put(f"{API_BASE}/style_profiles/", json=updated_profiles)
#         if res.status_code == 200:
#             success_message("✅ Style profile updated successfully!")
#         else:
#             st.error(f"❌ Failed to update profile: {res.text}")
#     except requests.exceptions.RequestException:
#         st.error("⚠️ Backend not reachable while saving changes.")

st.markdown("### 🧩 Basic Info")
profile["profile_id"] = st.text_input("Profile ID", value=profile.get("profile_id", ""))
profile["name"] = st.text_input("Profile Name", value=profile.get("name", ""))
profile["user_persona"] = st.text_input("User Persona", value=profile.get("user_persona", ""))
profile["description"] = st.text_area("Description", value=profile.get("description", ""), height=80)
profile["custom_instruction"] = st.text_area(
    "Custom Instruction",
    value=profile.get("custom_instruction", ""),
    height=80
)

st.markdown("---")

# ---------------------------------------------------------------------
# 🎨 Tone
# ---------------------------------------------------------------------
st.subheader("🎨 Tone")
tone = profile.get("tone", {})
col1, col2 = st.columns(2)
with col1:
    tone["formality"] = st.selectbox("Formality", ["very_formal", "formal", "neutral", "conversational", "friendly", "playful"], index=2 if tone.get("formality") == "neutral" else 0)
with col2:
    tone["voice"] = st.selectbox("Voice", ["active", "passive"], index=0 if tone.get("voice") == "active" else 1)
profile["tone"] = tone

# ---------------------------------------------------------------------
# 📚 Detail
# ---------------------------------------------------------------------
st.subheader("📚 Detail")
detail = profile.get("detail", {})
col1, col2 = st.columns(2)
with col1:
    detail["complexity_level"] = st.selectbox("Complexity Level", ["minimal", "low", "medium", "high", "exhaustive"], index=2)
with col2:
    detail["explain_example"] = st.selectbox("Explain Example", ["low_detail", "medium_detail", "high_detail"], index=1)
profile["detail"] = detail

# ---------------------------------------------------------------------
# 🧠 Abstraction
# ---------------------------------------------------------------------
st.subheader("🧠 Abstraction")
abstraction = profile.get("abstraction", {})
col1, col2, col3 = st.columns(3)
with col1:
    abstraction["complexity_level"] = st.selectbox("Complexity Level", ["beginner", "intermediate", "expert"], index=1)
with col2:
    abstraction["math_verbose"] = st.selectbox("Math Verbosity", ["sparse", "medium", "verbose"], index=0)
with col3:
    abstraction["include_glossary_of_terms"] = st.checkbox("Include Glossary", value=abstraction.get("include_glossary_of_terms", False))
profile["abstraction"] = abstraction

# ---------------------------------------------------------------------
# 🧾 Formatting
# ---------------------------------------------------------------------
st.subheader("🧾 Formatting")
fmt = profile.get("formatting", {})
col1, col2, col3 = st.columns(3)
with col1:
    fmt["use_bullets"] = st.checkbox("Use Bullets", value=fmt.get("use_bullets", False))
    fmt["use_numbered_lists"] = st.checkbox("Numbered Lists", value=fmt.get("use_numbered_lists", False))
with col2:
    fmt["use_headings"] = st.checkbox("Use Headings", value=fmt.get("use_headings", True))
    fmt["heading_style"] = st.selectbox("Heading Style", ["#", "##", "###", "bold", "underline"], index=0)
with col3:
    fmt["paragraph_length"] = st.selectbox("Paragraph Length", ["short", "medium", "long"], index=1)
    fmt["prefer_tables_for_data"] = st.checkbox("Prefer Tables", value=fmt.get("prefer_tables_for_data", False))
fmt["max_bullet_length_words"] = st.number_input("Max Bullet Length (words)", min_value=5, max_value=100, value=fmt.get("max_bullet_length_words", 25))
profile["formatting"] = fmt

# ---------------------------------------------------------------------
# 🏗️ Structure
# ---------------------------------------------------------------------
st.subheader("🏗️ Structure")
structure = profile.get("structure", {})
col1, col2, col3 = st.columns(3)
with col1:
    structure["include_title"] = st.checkbox("Include Title", value=structure.get("include_title", True))
    structure["include_summary_at_top"] = st.checkbox("Include Summary", value=structure.get("include_summary_at_top", True))
with col2:
    structure["include_examples_section"] = st.checkbox("Include Examples Section", value=structure.get("include_examples_section", True))
    structure["include_actions_or_todos_at_end"] = st.checkbox("Include To-Do Section", value=structure.get("include_actions_or_todos_at_end", False))
with col3:
    if(structure['section_order']):
        structure["section_order"] = st.text_area("Section Order (comma-separated)", value=", ".join(structure.get("section_order", [])))
profile["structure"] = structure

# ---------------------------------------------------------------------
# 🗣️ Language
# ---------------------------------------------------------------------
st.subheader("🗣️ Language")
language = profile.get("language", {})
col1, col2 = st.columns(2)
with col1:
    language["language"] = st.text_input("Language", value=language.get("language", "English"))
with col2:
    language["avoid_jargon"] = st.checkbox("Avoid Jargon", value=language.get("avoid_jargon", False))
profile["language"] = language

# ---------------------------------------------------------------------
# ✨ Stylistic Devices
# ---------------------------------------------------------------------
st.subheader("✨ Stylistic Devices")
style_dev = profile.get("stylistic_devices", {})
col1, col2, col3 = st.columns(3)
with col1:
    style_dev["use_examples"] = st.checkbox("Use Examples", value=style_dev.get("use_examples", True))
    style_dev["use_metaphors"] = st.checkbox("Use Metaphors", value=style_dev.get("use_metaphors", True))
with col2:
    style_dev["use_analogies"] = st.checkbox("Use Analogies", value=style_dev.get("use_analogies", True))
    style_dev["use_acronyms_expanded_first"] = st.checkbox("Expand Acronyms First", value=style_dev.get("use_acronyms_expanded_first", False))
with col3:
    style_dev["highlight_definitions"] = st.selectbox("Highlight Definitions", ["none", "bold", "italics", "quotes"], index=1)
profile["stylistic_devices"] = style_dev

# ---------------------------------------------------------------------
# 💾 Save to backend
# ---------------------------------------------------------------------
st.markdown("---")
if st.button("💾 Save Profile", use_container_width=True, type="primary"):
    try:
        updated_profiles = [profile]
        res = requests.put(f"{API_BASE}/style_profiles/", json=updated_profiles)
        if res.status_code == 200:
            success_message("✅ Style profile updated successfully!")
        else:
            st.error(f"❌ Failed to update profile: {res.text}")
    except requests.exceptions.RequestException:
        st.error("⚠️ Backend not reachable while saving changes.")


st.markdown("### 🧩 Learn Your Writing Style")
st.markdown("""
Provide your notes (text or file). The system will analyze your writing and suggest a personalized style profile.
""")

# --- Inputs ---
col1, col2 = st.columns(2)
with col1:
    user_text = st.text_area("✏️ Paste your text here", height=200, placeholder="Type or paste your notes...")
with col2:
    user_file = st.file_uploader("📄 Or upload a file (PDF/Text)", type=["pdf", "txt"])


# --- Button to send data ---
if st.button("🚀 Learn Style from Notes", use_container_width=True, type="primary"):
    if not user_text and not user_file:
        st.warning("⚠️ Please provide text or upload a file first.")
        st.stop()

    with st.spinner("Analyzing your writing style..."):
        try:
            files = {}
            data = {
                "current_profile": json.dumps(profile)  # ✅ serialize dict to JSON string
            }
            if user_text:
                data["user_text"] = user_text
            if user_file:
                files = {"file": user_file}

            res = requests.post(f"{API_BASE}/pipeline/learn", data=data, files=files)
            print(res.text)
            
            if res.status_code == 200:
                st.success("✅ New style profile generated successfully!")
                new_profile = res.json()
                st.json(new_profile)
            else:
                st.error(f"❌ Style learning failed: {res.text}")
        except requests.exceptions.RequestException:
            st.error("⚠️ Backend not reachable during style learning.")
            


# st.markdown("""
# <div style="background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%); border-radius: 12px; padding: 15px; margin-bottom: 20px; border-left: 4px solid #0066cc;">
#     <p style="color: #0066cc; font-size: 0.95rem; margin: 0;"><strong>⚙️ Settings:</strong> Customize your profile and preferences for the best experience.</p>
# </div>
# """, unsafe_allow_html=True)















# tab1, tab2, tab3 = st.tabs(["👤 Profile", "🎨 Preferences", "🔔 Notifications"])

# with tab1:
#     st.markdown("### Profile Information")

#     col1, col2 = st.columns([1, 2])

#     with col1:
#         st.markdown("""
#         <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 15px;">
#             <div style="width: 100px; height: 100px; background: linear-gradient(135deg, #0066cc 0%, #004499 100%); border-radius: 50%; margin: 0 auto 10px; display: flex; align-items: center; justify-content: center;">
#                 <span style="font-size: 2.5rem;">👤</span>
#             </div>
#             <p style="margin: 0; color: #666666; font-size: 0.9rem;">Profile Photo</p>
#         </div>
#         """, unsafe_allow_html=True)

#         if st.button("Upload Photo", use_container_width=True):
#             uploaded = st.file_uploader("Choose profile photo", type=['jpg', 'png'], label_visibility="collapsed")

#     with col2:
#         name = st.text_input(
#             "Full Name",
#             value=st.session_state.user_profile.get('name', ''),
#             placeholder="Your full name"
#         )

#         email = st.text_input(
#             "Email Address",
#             value=st.session_state.user_profile.get('email', ''),
#             placeholder="your.email@example.com"
#         )

#         bio = st.text_area(
#             "Bio",
#             placeholder="Tell us about yourself...",
#             height=100
#         )

#     st.markdown("---")

#     st.markdown("### Account Settings")

#     col1, col2 = st.columns(2)

#     with col1:
#         st.markdown("""
#         <div class="card">
#             <h4 style="margin-top: 0; color: #0066cc;">🔐 Password</h4>
#             <p style="color: #666666; font-size: 0.9rem; margin-bottom: 10px;">Change your password regularly to keep your account secure.</p>
#         </div>
#         """, unsafe_allow_html=True)

#         if st.button("Change Password", use_container_width=True, key="change_pwd"):
#             st.session_state.show_pwd_modal = True

#     with col2:
#         st.markdown("""
#         <div class="card">
#             <h4 style="margin-top: 0; color: #0066cc;">📱 Two-Factor Auth</h4>
#             <p style="color: #666666; font-size: 0.9rem; margin-bottom: 10px;">Add an extra layer of security to your account.</p>
#         </div>
#         """, unsafe_allow_html=True)

#         if st.button("Enable 2FA", use_container_width=True):
#             st.info("Two-factor authentication setup instructions would appear here.")

# with tab2:
#     st.markdown("### Display Settings")

#     col1, col2 = st.columns(2)

#     with col1:
#         theme = st.selectbox(
#             "Theme",
#             ["Light", "Dark", "Auto"],
#             index=0
#         )

#         font_size = st.selectbox(
#             "Font Size",
#             ["Small", "Normal", "Large"],
#             index=1
#         )

#     with col2:
#         density = st.selectbox(
#             "Layout Density",
#             ["Compact", "Comfortable", "Spacious"],
#             index=1
#         )

#         language = st.selectbox(
#             "Language",
#             ["English", "Spanish", "French", "German"],
#             index=0
#         )

#     st.markdown("---")

#     st.markdown("### Note Display")

#     col1, col2 = st.columns(2)

#     with col1:
#         notes_per_page = st.slider("Notes per page", 5, 50, 20)
#         show_timestamps = st.checkbox("Show timestamps", value=True)

#     with col2:
#         sort_order = st.selectbox("Default sort", ["Recent", "Oldest", "A-Z"])
#         highlight_search = st.checkbox("Highlight search results", value=True)

#     st.markdown("---")

#     st.markdown("### Export Settings")

#     export_format = st.multiselect(
#         "Preferred export formats",
#         ["PDF", "Markdown", "Word", "Text", "JSON"],
#         default=["PDF", "Markdown"]
#     )

#     auto_backup = st.checkbox("Automatic daily backups", value=True)

# with tab3:
#     st.markdown("### Notification Preferences")

#     col1, col2 = st.columns([2, 1])

#     with col1:
#         st.markdown("""
#         <div class="card">
#             <h4 style="margin-top: 0; color: #0066cc;">📧 Email Notifications</h4>
#             <p style="color: #666666; margin: 0; font-size: 0.9rem;">Receive updates about your notes and account activity.</p>
#         </div>
#         """, unsafe_allow_html=True)

#     with col2:
#         email_enabled = st.toggle("Enabled", value=True)

#     if email_enabled:
#         st.markdown("##### Email Notification Types")

#         col1, col2 = st.columns(2)

#         with col1:
#             st.checkbox("✓ New message from assistant", value=True, key="notify_msg")
#             st.checkbox("✓ Note reminders", value=True, key="notify_remind")
#             st.checkbox("✓ Daily digest", value=False, key="notify_digest")

#         with col2:
#             st.checkbox("✓ Weekly summary", value=True, key="notify_weekly")
#             st.checkbox("✓ Backup notifications", value=True, key="notify_backup")
#             st.checkbox("✓ Account alerts", value=True, key="notify_alerts")

#     st.markdown("---")

#     st.markdown("""
#     <div class="card">
#         <h4 style="margin-top: 0; color: #0066cc;">🔔 In-App Notifications</h4>
#         <p style="color: #666666; margin: 0; font-size: 0.9rem;">See updates while using the application.</p>
#     </div>
#     """, unsafe_allow_html=True)

#     in_app_enabled = st.toggle("Enabled", value=True, key="inapp_toggle")

#     if in_app_enabled:
#         st.slider("Notification sound volume", 0, 100, 70)

# st.markdown("---")

# col1, col2, col3 = st.columns([2, 1, 1])

# with col1:
#     if st.button("💾 Save All Changes", use_container_width=True):
#         st.session_state.user_profile['name'] = name
#         st.session_state.user_profile['email'] = email
#         st.session_state.user_profile['theme'] = theme if 'theme' in locals() else 'light'
#         success_message("All changes saved successfully!")

# with col2:
#     if st.button("🔄 Reset", use_container_width=True):
#         st.rerun()

# with col3:
#     if st.button("⚠️ Delete Account", use_container_width=True):
#         st.warning("Account deletion is permanent and cannot be undone. Please contact support.")

# st.markdown("---")

# st.markdown("""
# <div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px;">
#     <h4 style="margin-top: 0; color: #0066cc;">📚 Help & Support</h4>
#     <ul style="color: #666666; margin: 10px 0; padding-left: 20px;">
#         <li><a href="#" style="color: #0066cc; text-decoration: none;">View Documentation</a></li>
#         <li><a href="#" style="color: #0066cc; text-decoration: none;">Contact Support</a></li>
#         <li><a href="#" style="color: #0066cc; text-decoration: none;">Report a Bug</a></li>
#         <li><a href="#" style="color: #0066cc; text-decoration: none;">Request a Feature</a></li>
#     </ul>
#     <p style="color: #999999; font-size: 0.85rem; margin: 10px 0 0 0;">
#         <strong>App Version:</strong> 1.0.0 | <strong>Last Updated:</strong> Nov 2024
#     </p>
# </div>
# """, unsafe_allow_html=True)
