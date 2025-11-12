import streamlit as st

def apply_global_styles():
    """Apply comprehensive custom styling to the entire app"""
    st.markdown("""
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    html, body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background-color: #ffffff;
        color: #1a1a1a;
    }

    /* Main container */
    .main {
        padding: 0;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e0e0e0;
    }

    [data-testid="stSidebarContent"] {
        padding: 20px;
    }

    /* Headers */
    h1 {
        color: #0066cc;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
    }

    h2 {
        color: #1a1a1a;
        font-size: 1.8rem;
        font-weight: 600;
        margin-bottom: 15px;
        margin-top: 20px;
    }

    h3 {
        color: #333333;
        font-size: 1.3rem;
        font-weight: 600;
        margin-bottom: 10px;
    }

    /* Text styling */
    body, p, label, div {
        line-height: 1.6;
    }

    /* Input fields */
    input, textarea, [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
        border: 1px solid #d0d0d0 !important;
        border-radius: 6px !important;
        padding: 10px 12px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }

    input:focus, textarea:focus {
        border-color: #0066cc !important;
        box-shadow: 0 0 0 3px rgba(0, 102, 204, 0.1) !important;
        outline: none !important;
    }

    /* Buttons */
    button {
        background-color: #0066cc !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
        letter-spacing: 0.5px !important;
    }

    button:hover {
        background-color: #0052a3 !important;
        box-shadow: 0 4px 12px rgba(0, 102, 204, 0.3) !important;
        transform: translateY(-2px) !important;
    }

    button:active {
        transform: translateY(0) !important;
    }

    /* Cards */
    .card {
        background-color: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }

    .card:hover {
        border-color: #0066cc;
        box-shadow: 0 6px 16px rgba(0, 102, 204, 0.15);
        transform: translateY(-2px);
    }

    /* Streamlit specific elements */
    [data-testid="stMetric"] {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        border-left: 4px solid #0066cc;
    }

    [data-testid="stExpanderHeader"] {
        background-color: #f8f9fa;
        border-radius: 6px;
        font-weight: 600;
    }

    [data-testid="stExpanderHeader"]:hover {
        background-color: #eff2f7;
    }

    /* Divider */
    hr {
        border: none;
        height: 1px;
        background-color: #e0e0e0;
        margin: 20px 0;
    }

    /* Error, warning, success messages */
    [data-testid="stAlert"] {
        border-radius: 6px;
        padding: 12px 16px;
        font-size: 0.95rem;
    }

    /* Smooth scrolling */
    html {
        scroll-behavior: smooth;
    }

    /* Selection styling */
    ::selection {
        background-color: rgba(0, 102, 204, 0.2);
        color: #1a1a1a;
    }

    /* Placeholder text */
    input::placeholder, textarea::placeholder {
        color: #999999;
        font-style: italic;
    }

    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }

    ::-webkit-scrollbar-track {
        background: #f8f9fa;
    }

    ::-webkit-scrollbar-thumb {
        background: #c0c0c0;
        border-radius: 4px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #0066cc;
    }
    </style>
    """, unsafe_allow_html=True)


def page_header(title, subtitle=""):
    """Display a professional page header"""
    st.markdown(f"""
    <div style="margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #e0e0e0;">
        <h1 style="margin: 0 0 10px 0;">{title}</h1>
        {f'<p style="color: #666666; font-size: 1.1rem; margin: 0;">{subtitle}</p>' if subtitle else ''}
    </div>
    """, unsafe_allow_html=True)


def note_card(title, preview, date, tags=None):
    """Display a styled note card"""
    tags_html = ""
    if tags:
        tags_html = " ".join([f'<span style="display: inline-block; background-color: #e8f4fd; color: #0066cc; padding: 4px 10px; border-radius: 16px; font-size: 0.85rem; margin-right: 5px; margin-bottom: 5px;">{tag}</span>' for tag in tags])

    st.markdown(f"""
    <div class="card" style="cursor: pointer;">
        <h3 style="margin: 0 0 8px 0; color: #0066cc;">{title}</h3>
        <p style="color: #666666; margin: 8px 0; font-size: 0.95rem; line-height: 1.5;">{preview}</p>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 12px;">
            <small style="color: #999999;">{date}</small>
            <div>{tags_html}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def stat_box(label, value, icon="📊"):
    """Display a styled statistic box"""
    st.markdown(f"""
    <div style="background-color: #f8f9fa; border-radius: 8px; padding: 20px; text-align: center; border-left: 4px solid #0066cc;">
        <div style="font-size: 2rem; margin-bottom: 8px;">{icon}</div>
        <div style="font-size: 1.5rem; font-weight: 700; color: #0066cc;">{value}</div>
        <div style="color: #666666; font-size: 0.95rem; margin-top: 5px;">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def divider():
    """Display a subtle divider"""
    st.markdown("<hr style='margin: 30px 0; border: none; height: 1px; background-color: #e0e0e0;'>", unsafe_allow_html=True)


def success_message(message):
    """Display a success message with styling"""
    st.markdown(f"""
    <div style="background-color: #f0f9ff; border-left: 4px solid #10b981; padding: 12px 16px; border-radius: 4px; color: #047857;">
        <strong>✓ {message}</strong>
    </div>
    """, unsafe_allow_html=True)


def error_message(message):
    """Display an error message with styling"""
    st.markdown(f"""
    <div style="background-color: #fef2f2; border-left: 4px solid #ef4444; padding: 12px 16px; border-radius: 4px; color: #991b1b;">
        <strong>✗ {message}</strong>
    </div>
    """, unsafe_allow_html=True)


def info_message(message):
    """Display an info message with styling"""
    st.markdown(f"""
    <div style="background-color: #f0f9ff; border-left: 4px solid #3b82f6; padding: 12px 16px; border-radius: 4px; color: #1e40af;">
        <strong>ℹ {message}</strong>
    </div>
    """, unsafe_allow_html=True)
