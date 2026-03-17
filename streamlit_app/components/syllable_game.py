"""
Syllable Game Component - Interactive drag-and-drop-ish syllable matching.
Uses columns and session state to track progress.
"""
import streamlit as st
import random

def render_syllable_game(syllables: list[str], target_word: str):
    """
    Renders a 'syllable-builder' game where the student clicks
    syllables to reconstruct the word.
    """
    if 'current_build' not in st.session_state:
        st.session_state.current_build = []
    
    # We use a set of syllables to render buttons
    cols = st.columns(len(syllables))
    for i, syl in enumerate(syllables):
        if cols[i].button(syl, key=f"syl_{i}_{syl}", use_container_width=True):
            # Magical Effect on Click
            effects = [
                "*✨ A shimmering path of syllables appears! ✨*",
                "*⚡ A bolt of learning energy! ⚡*",
                "*🌟 Your choice sparkles with wisdom! 🌟*",
                "*🌈 A rainbow of sounds! 🌈*",
                "*🎈 Your selection floats up with a magical pop! 🎈*",
                "*💎 A diamond-sharp pronunciation! 💎*"
            ]
            st.markdown(random.choice(effects))
            
            st.session_state.current_build.append(syl)
            st.rerun()
            
    current_word = "".join(st.session_state.current_build).strip().lower()
    target_clean = target_word.strip().lower()
    
    st.write(f"**Current Progress:** `{current_word if st.session_state.current_build else '...'}`")
    
    if st.button("Reset Game 🔄"):
        st.session_state.current_build = []
        st.rerun()
        
    if current_word == target_clean:
        st.success(f"🎉 **Perfect!** You built the word: **{target_word}**")
        st.balloons()
        st.info("You've mastered this word! Click 'Next Lesson' below to continue.")
        return True
    elif len(current_word) >= len(target_clean) and current_word != target_clean:
        st.error(f"Almost! It looks like '{current_word}' isn't quite right. Reset and try again!")
        # Don't auto-reset immediately to let user see their mistake
        
    return False
