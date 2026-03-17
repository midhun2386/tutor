"""
Main Streamlit Entry Point.
Injects CSS and handles navigation.
"""
import streamlit as st
import os
from streamlit_app.utils import init_session_state

# Page Config
st.set_page_config(
    page_title="Vernacular AI Tutor",
    page_icon="📖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
with open(css_path, "r") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Session State Initialization
init_session_state()

# Sidebar Branding
st.sidebar.markdown(
    """
    <h1 style='color: #2D1B00;'>Veena</h1>
    <p style='color: #C68642; font-style: italic;'>Your Vernacular Literacy Tutor</p>
    <div class='film-strip-divider'></div>
    """, 
    unsafe_allow_html=True
)

st.sidebar.info("Select a page above to begin.")

# Navigation logic is handled by Streamlit's multipage structure in the 'pages/' directory.
# This file serves as the landing or global state handler.
if st.session_state.student_id is None:
    st.title("Welcome to Vernacular")
    st.markdown(
        """
        <div class="cinematic-card">
            <h2>Ready to learn?</h2>
            <p>Please go to the <b>Home</b> page to select your profile or register.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    st.success(f"Learning as: **{st.session_state.student_name}** ({st.session_state.language.capitalize()})")
