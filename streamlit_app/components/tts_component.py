"""
TTS Component - Uses the Browser's native SpeechSynthesis API to provide pronunciation demos.
Low-latency and zero-cost approach for multilingual teaching.
"""
import streamlit as st
import streamlit.components.v1 as components

def render_voice_demo(text: str, language: str, autoplay: bool = False, label: str = "🎧 Listen to Veena"):
    """
    Renders a button that, when clicked, uses the browser's voice to speak the text.
    If autoplay is True, it attempts to speak immediately on load.
    """
    # Map project languages to browser locales
    lang_map = {
        "tamil": "ta-IN",
        "hindi": "hi-IN",
        "english": "en-US"
    }
    locale = lang_map.get(language.lower(), "en-US")

    # JavaScript to trigger Web Speech API
    js_code = f"""
    <script>
    function speak() {{
        const msg = new SpeechSynthesisUtterance({repr(text)});
        msg.lang = '{locale}';
        msg.rate = 0.9; 
        window.speechSynthesis.speak(msg);
    }}
    
    // Attempt autoplay if requested
    if ({'true' if autoplay else 'false'}) {{
        // Timeout to ensure browser is ready
        setTimeout(speak, 500);
    }}
    </script>
    <button onclick="speak()" style="
        background-color: #C68642; 
        color: white; 
        border: none; 
        padding: 8px 16px; 
        border-radius: 20px; 
        cursor: pointer;
        font-family: inherit;
        font-size: 0.9rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        transition: transform 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
        {label}
    </button>
    """
    
    components.html(js_code, height=45)
