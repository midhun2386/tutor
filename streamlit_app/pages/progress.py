"""
Progress Page - Visualizing the learner's journey.
"""
import streamlit as st
import requests
import pandas as pd
from config import API_BASE_URL
from streamlit_app.utils import init_session_state

def run():
    init_session_state()
    st.markdown("<h1>📊 Progress</h1>", unsafe_allow_html=True)

    if st.session_state.student_id is None:
        st.warning("Please select a profile first.")
        return

    try:
        res = requests.get(f"{API_BASE_URL}/student/{st.session_state.student_id}")
        if res.status_code == 200:
            data = res.json()
            st.subheader(f"Overview for {data['name']}")
            
            progress = data.get('phoneme_progress', [])
            if progress:
                df = pd.DataFrame(progress)
                
                # Chart 1: Mastery Scores
                st.write("### 🏆 Mastery level per Sound")
                st.bar_chart(df.set_index('phoneme')['mastery_score'])
                
                # Table: Details
                st.write("### 📝 Detailed Statistics")
                st.table(df[['phoneme', 'attempt_count', 'error_count', 'mastery_score']])
            else:
                st.info("No practice data yet. Start a lesson to see progress!")
        else:
            st.error("Could not fetch progress data.")
    except Exception as e:
        st.error(f"Backend unreachable: {e}")

if __name__ == "__main__":
    run()
