"""
Lesson Page - The core interactive loop where pedagogical logic meets voice.
"""
import streamlit as st
import requests
import io
from config import API_BASE_URL
from streamlit_app.components.audio_recorder import render_audio_recorder
from streamlit_app.components.syllable_game import render_syllable_game
from streamlit_app.components.tts_component import render_voice_demo
from streamlit_app.utils import init_session_state

def get_new_lesson():
    if st.session_state.student_id is None:
        return
    payload = {
        "student_id": st.session_state.student_id,
        "language": st.session_state.language,
        "emotion": st.session_state.get('last_emotion', 'Confident'),
        "proficiency_level": st.session_state.get('proficiency_level', 'Beginner')
    }
    try:
        res = requests.post(f"{API_BASE_URL}/lessons/generate", json=payload, timeout=120)
        if res.status_code == 200:
            st.session_state.current_lesson = res.json()
            st.session_state.quiz_mode = False # Start in Teaching mode
            if 'current_build' in st.session_state:
                st.session_state.current_build = []
        else:
            st.error(f"Failed to fetch lesson. Server responded with: {res.status_code}")
            st.session_state.current_lesson = None
    except Exception as e:
        st.error(f"Could not connect to tutor backend: {e}")
        st.session_state.current_lesson = None

def run():
    init_session_state()
    st.markdown("<h1>📖 Lesson</h1>", unsafe_allow_html=True)
    
    if st.session_state.student_id is None:
        st.warning("Please go to Home and select a profile first.")
        return

    # Start Session if not already started
    if st.session_state.session_id is None:
        try:
            res = requests.post(f"{API_BASE_URL}/student/{st.session_state.student_id}/session/start", timeout=10)
            st.session_state.session_id = res.json()['session_id']
        except Exception as e:
            st.error(f"Failed to start session: {e}")

    # Fetch lesson if missing
    if st.session_state.current_lesson is None:
        get_new_lesson()

    lesson = st.session_state.get('current_lesson')
    if not lesson:
        st.error("📉 No lesson content found. This might happen if the backend is still starting up.")
        if st.button("🔄 Retry Fetching Lesson"):
            get_new_lesson()
            st.rerun()
        return

    # ── Render Lesson UI ──────────────────────────────────────────────────────
    st.markdown(
        f"""
        <div class="cinematic-card">
            <h2 style='font-size: 2.5rem; text-align: center; margin-bottom: 1rem;'>{lesson['lesson_text']}</h2>
            <p style='text-align: center; color: #C68642;'><i>Hint: {lesson['hint']}</i></p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Render the Voice Demo button below the text but inside the card-area
    render_voice_demo(lesson['lesson_text'], st.session_state.language)

    # ── Action Area ────────────────────────────────────────────────────────────
    
    # PHASE 1: TEACHING (Reading Aloud)
    if not st.session_state.quiz_mode:
        st.markdown("### 🎙️ Step 1: Read Aloud")
        st.info("Listen to the text above and try to repeat it into the microphone.")
        
        audio_bytes = render_audio_recorder()
        
        if audio_bytes:
            files = {'file': ('audio.wav', audio_bytes, 'audio/wav')}
            data = {
                'language': st.session_state.language, 
                'session_id': st.session_state.session_id,
                'expected_text': lesson['lesson_text']
            }
            
            with st.spinner("Analyzing your voice..."):
                try:
                    h_res = requests.get(f"{API_BASE_URL}/health", timeout=2)
                    models_ready = h_res.json().get("models_ready", False)

                    res = requests.post(f"{API_BASE_URL}/audio/analyze", files=files, data=data, timeout=60)
                    if res.status_code == 200:
                        analysis = res.json()
                        st.session_state.last_emotion = analysis['emotion_label']
                        st.session_state.last_transcript = analysis['transcript']
                        
                        if not models_ready:
                            st.warning("⚠️ Veena is still warming up her brain. You can skip to the quiz if you like!")
                            if st.button("Skip to Quiz 🧩"):
                                st.session_state.quiz_mode = True
                                st.rerun()

                        # ── ALWAYS Display Analysis Results ───────────────────────

                        if analysis.get('is_correct'):
                            st.balloons()
                            st.markdown("*✨ A sprinkle of digital stardust accompanies your choice! ✨*")
                        else:
                            st.markdown("*💡 Your selection has been highlighted with a vibrant, shimmering outline, ready for action! 💡*")

                        # Automatically speak the feedback
                        render_voice_demo(
                            analysis['creative_feedback'], 
                            st.session_state.language, 
                            autoplay=True,
                            label="🎧 Hear Veena's Feedback"
                        )

                        st.write(f"I heard: **{analysis['transcript']}**")
                        st.caption(f"Detected Emotion: **{analysis['emotion_label']}** ({analysis['confidence']:.1%})")
                        
                        # Progress Tracker
                        completed = st.session_state.get('lessons_completed', 0)
                        st.progress(min(completed / 3.0, 1.0), text=f"Progress: {completed}/3 lessons before Quiz!")

                        # ── Navigation Logic ──────────────────────────────────────
                        if completed >= 3:
                            if st.button("Great! Now Start Quiz 🧩"):
                                st.markdown("*🚀 ✨ Magic portal opening... preparing your challenge!*")
                                st.session_state.quiz_mode = True
                                st.rerun()
                        else:
                            if st.button("Get Next Practice Lesson ➡️"):
                                st.markdown("*✨ Transforming the lesson layout with a magical shimmer... ✨*")
                                # Increment lessons completed ONLY when clicking Next
                                st.session_state.lessons_completed = min(st.session_state.get('lessons_completed', 0) + 1, 3)
                                get_new_lesson()
                                st.rerun()
                    else:
                        st.error("Analysis failed.")
                except Exception as e:
                    st.error(f"Error communicating with backend: {e}")
                    if st.button("Skip to Quiz anyway 🧩"):
                        st.session_state.quiz_mode = True
                        st.rerun()

    # PHASE 2: QUIZ (Syllable Match)
    else:
        st.markdown("### 🧩 Step 2: The Syllable Quiz")
        st.info("Now, build the word by clicking the syllables in the correct order!")
        
        # We always use the syllables from the current lesson
        # CORRECTION: Fixed argument order (syllables, text)
        if render_syllable_game(lesson.get('syllables', []), lesson['lesson_text']):
            st.balloons()
            if st.button("Complete Lesson & Get Next ➡️"):
                st.session_state.last_emotion = "Confident"
                st.session_state.lessons_completed = 0 # Reset for next cycle
                get_new_lesson()
                st.rerun()
        
        if st.button("⬅️ Back to Reading"):
            st.session_state.quiz_mode = False
            st.rerun()

    if st.sidebar.button("End Session"):
        try:
            payload = {
                "session_id": st.session_state.session_id,
                "student_id": st.session_state.student_id,
                "average_emotion": st.session_state.get('last_emotion', 'Neutral')
            }
            requests.post(f"{API_BASE_URL}/student/session/end", json=payload, timeout=10)
            st.session_state.session_id = None
            st.session_state.student_id = None
            st.rerun()
        except Exception as e:
            st.error(f"Failed to end session: {e}")

if __name__ == "__main__":
    run()
