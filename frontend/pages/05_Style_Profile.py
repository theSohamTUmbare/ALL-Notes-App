import streamlit as st
from styles import page_header, apply_global_styles, success_message
from components import init_session_state

apply_global_styles()
init_session_state()

page_header("Style Profile", "Personalize your All Notes experience")

st.markdown("""
<div style="background: linear-gradient(135deg, #f0f7ff 0%, #ffffff 100%); border-radius: 12px; padding: 15px; margin-bottom: 20px; border-left: 4px solid #0066cc;">
    <p style="color: #0066cc; font-size: 0.95rem; margin: 0;"><strong>⚙️ Settings:</strong> Customize your profile and preferences for the best experience.</p>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["👤 Profile", "🎨 Preferences", "🔔 Notifications"])

with tab1:
    st.markdown("### Profile Information")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 20px; border-radius: 8px; text-align: center; margin-bottom: 15px;">
            <div style="width: 100px; height: 100px; background: linear-gradient(135deg, #0066cc 0%, #004499 100%); border-radius: 50%; margin: 0 auto 10px; display: flex; align-items: center; justify-content: center;">
                <span style="font-size: 2.5rem;">👤</span>
            </div>
            <p style="margin: 0; color: #666666; font-size: 0.9rem;">Profile Photo</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Upload Photo", use_container_width=True):
            uploaded = st.file_uploader("Choose profile photo", type=['jpg', 'png'], label_visibility="collapsed")

    with col2:
        name = st.text_input(
            "Full Name",
            value=st.session_state.user_profile.get('name', ''),
            placeholder="Your full name"
        )

        email = st.text_input(
            "Email Address",
            value=st.session_state.user_profile.get('email', ''),
            placeholder="your.email@example.com"
        )

        bio = st.text_area(
            "Bio",
            placeholder="Tell us about yourself...",
            height=100
        )

    st.markdown("---")

    st.markdown("### Account Settings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="card">
            <h4 style="margin-top: 0; color: #0066cc;">🔐 Password</h4>
            <p style="color: #666666; font-size: 0.9rem; margin-bottom: 10px;">Change your password regularly to keep your account secure.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Change Password", use_container_width=True, key="change_pwd"):
            st.session_state.show_pwd_modal = True

    with col2:
        st.markdown("""
        <div class="card">
            <h4 style="margin-top: 0; color: #0066cc;">📱 Two-Factor Auth</h4>
            <p style="color: #666666; font-size: 0.9rem; margin-bottom: 10px;">Add an extra layer of security to your account.</p>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Enable 2FA", use_container_width=True):
            st.info("Two-factor authentication setup instructions would appear here.")

with tab2:
    st.markdown("### Display Settings")

    col1, col2 = st.columns(2)

    with col1:
        theme = st.selectbox(
            "Theme",
            ["Light", "Dark", "Auto"],
            index=0
        )

        font_size = st.selectbox(
            "Font Size",
            ["Small", "Normal", "Large"],
            index=1
        )

    with col2:
        density = st.selectbox(
            "Layout Density",
            ["Compact", "Comfortable", "Spacious"],
            index=1
        )

        language = st.selectbox(
            "Language",
            ["English", "Spanish", "French", "German"],
            index=0
        )

    st.markdown("---")

    st.markdown("### Note Display")

    col1, col2 = st.columns(2)

    with col1:
        notes_per_page = st.slider("Notes per page", 5, 50, 20)
        show_timestamps = st.checkbox("Show timestamps", value=True)

    with col2:
        sort_order = st.selectbox("Default sort", ["Recent", "Oldest", "A-Z"])
        highlight_search = st.checkbox("Highlight search results", value=True)

    st.markdown("---")

    st.markdown("### Export Settings")

    export_format = st.multiselect(
        "Preferred export formats",
        ["PDF", "Markdown", "Word", "Text", "JSON"],
        default=["PDF", "Markdown"]
    )

    auto_backup = st.checkbox("Automatic daily backups", value=True)

with tab3:
    st.markdown("### Notification Preferences")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        <div class="card">
            <h4 style="margin-top: 0; color: #0066cc;">📧 Email Notifications</h4>
            <p style="color: #666666; margin: 0; font-size: 0.9rem;">Receive updates about your notes and account activity.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        email_enabled = st.toggle("Enabled", value=True)

    if email_enabled:
        st.markdown("##### Email Notification Types")

        col1, col2 = st.columns(2)

        with col1:
            st.checkbox("✓ New message from assistant", value=True, key="notify_msg")
            st.checkbox("✓ Note reminders", value=True, key="notify_remind")
            st.checkbox("✓ Daily digest", value=False, key="notify_digest")

        with col2:
            st.checkbox("✓ Weekly summary", value=True, key="notify_weekly")
            st.checkbox("✓ Backup notifications", value=True, key="notify_backup")
            st.checkbox("✓ Account alerts", value=True, key="notify_alerts")

    st.markdown("---")

    st.markdown("""
    <div class="card">
        <h4 style="margin-top: 0; color: #0066cc;">🔔 In-App Notifications</h4>
        <p style="color: #666666; margin: 0; font-size: 0.9rem;">See updates while using the application.</p>
    </div>
    """, unsafe_allow_html=True)

    in_app_enabled = st.toggle("Enabled", value=True, key="inapp_toggle")

    if in_app_enabled:
        st.slider("Notification sound volume", 0, 100, 70)

st.markdown("---")

col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    if st.button("💾 Save All Changes", use_container_width=True):
        st.session_state.user_profile['name'] = name
        st.session_state.user_profile['email'] = email
        st.session_state.user_profile['theme'] = theme if 'theme' in locals() else 'light'
        success_message("All changes saved successfully!")

with col2:
    if st.button("🔄 Reset", use_container_width=True):
        st.rerun()

with col3:
    if st.button("⚠️ Delete Account", use_container_width=True):
        st.warning("Account deletion is permanent and cannot be undone. Please contact support.")

st.markdown("---")

st.markdown("""
<div style="background-color: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px;">
    <h4 style="margin-top: 0; color: #0066cc;">📚 Help & Support</h4>
    <ul style="color: #666666; margin: 10px 0; padding-left: 20px;">
        <li><a href="#" style="color: #0066cc; text-decoration: none;">View Documentation</a></li>
        <li><a href="#" style="color: #0066cc; text-decoration: none;">Contact Support</a></li>
        <li><a href="#" style="color: #0066cc; text-decoration: none;">Report a Bug</a></li>
        <li><a href="#" style="color: #0066cc; text-decoration: none;">Request a Feature</a></li>
    </ul>
    <p style="color: #999999; font-size: 0.85rem; margin: 10px 0 0 0;">
        <strong>App Version:</strong> 1.0.0 | <strong>Last Updated:</strong> Nov 2024
    </p>
</div>
""", unsafe_allow_html=True)
