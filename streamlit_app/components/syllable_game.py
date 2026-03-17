"""
Syllable Game Component - Interactive drag-and-drop-ish syllable matching.
Uses columns and session state to track progress.
"""
import streamlit as st

def render_syllable_game(target_word: str, syllables: list[str]):
    """
    Renders a simple game where the user clicks syllables in the correct order.
    """
    st.write(f"### 🧩 Build the word: **{target_word}**")
    
    if 'current_build' not in st.session_state:
        st.session_state.current_build = []
    
    cols = st.columns(len(syllables))
    for i, syl in enumerate(syllables):
        if cols[i].button(syl, key=f"syl_{syl}_{i}"):
            st.session_state.current_build.append(syl)
            st.rerun()
            
    current_word = "".join(st.session_state.current_build)
    st.write(f"**Current Progress:** {current_word if current_word else '...'}")
    
    if st.button("Reset Game"):
        st.session_state.current_build = []
        st.rerun()
        
    if current_word == target_word:
        st.success("🎉 Well done! You built the word!")
        return True
    elif len(current_word) >= len(target_word) and current_word != target_word:
        st.error("Let's try again!")
        st.session_state.current_build = []
        
    return False
