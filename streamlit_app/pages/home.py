"""
Home Page - Student registration/selection.
"""
import streamlit as st
import requests
import os
from config import API_BASE_URL
from streamlit_app.utils import init_session_state

def run():
    init_session_state()
    st.markdown("<h1>🏠 Home</h1>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="cinematic-card">
            <h3>Who is learning today?</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    # 0. Check Backend Health
    try:
        health_res = requests.get(f"{API_BASE_URL}/health", timeout=2)
        health_data = health_res.json()
        if health_data.get("status") == "loading":
            st.warning("🧠 Veena is warming up her brain (ML models)... This may take a minute.")
            st.info("You can still view the app, but some features might be slow.")
    except Exception:
        st.error("🛑 Backend not reachable. Please start the app using `python run.py`.")
        return

    # 1. Fetch Existing Students
    try:
        response = requests.get(f"{API_BASE_URL}/student/")
        students = response.json() if response.status_code == 200 else []
    except Exception as e:
        students = []
        st.sidebar.error(f"Sync error: {e}")

    if students:
        student_names = {s['name']: s for s in students}
        selected_name = st.selectbox("Select Profile", ["--"] + list(student_names.keys()))
        
        if selected_name != "--":
            s_data = student_names[selected_name]
            if st.button("Continue to Lessons"):
                st.session_state.student_id = s_data['id']
                st.session_state.student_name = s_data['name']
                st.session_state.language = s_data['language']
                st.rerun()

    st.divider()

    # 2. Register New Student
    st.subheader("New Learner?")
    with st.form("registration_form", clear_on_submit=True):
        new_name = st.text_input("Name", help="Enter your first name")
        new_lang = st.selectbox("Language", ["tamil", "hindi", "english"])
        submitted = st.form_submit_button("Register & Start")
        
        if submitted:
            if new_name:
                payload = {"name": new_name, "language": new_lang}
                try:
                    res = requests.post(f"{API_BASE_URL}/student/", json=payload, timeout=10)
                    if res.status_code == 201:
                        s_data = res.json()
                        st.session_state.student_id = s_data['id']
                        st.session_state.student_name = s_data['name']
                        st.session_state.language = s_data['language']
                        st.success("Registered!")
                        st.rerun()
                    else:
                        st.error("Registration failed.")
                except Exception as e:
                    st.error(f"Backend unreachable: {e}")
            else:
                st.warning("Please enter a name.")

if __name__ == "__main__":
    run()
