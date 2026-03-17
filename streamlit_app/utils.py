import streamlit as st

def init_session_state():
    """
    Centralized session state initialization for a robust multi-page app.
    Call this at the top of every page script.
    """
    if 'student_id' not in st.session_state:
        st.session_state.student_id = None
    if 'student_name' not in st.session_state:
        st.session_state.student_name = ""
    if 'language' not in st.session_state:
        st.session_state.language = "tamil"
    if 'session_id' not in st.session_state:
        st.session_state.session_id = None
    if 'last_emotion' not in st.session_state:
        st.session_state.last_emotion = "Confident"
    if 'current_lesson' not in st.session_state:
        st.session_state.current_lesson = None
    if 'quiz_mode' not in st.session_state:
        st.session_state.quiz_mode = False
