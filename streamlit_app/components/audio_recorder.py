"""
Audio Recorder Component - Wrapper for audio-recorder-streamlit.
"""
import streamlit as st
from audio_recorder_streamlit import audio_recorder

def render_audio_recorder():
    """Renders the microphone button and returns audio bytes if recorded."""
    st.write("### 🎤 Read Aloud")
    audio_bytes = audio_recorder(
        text="Click to start/stop recording",
        recording_color="#FF4B4B",
        neutral_color="#C68642",
        icon_size="2x",
    )
    return audio_bytes
