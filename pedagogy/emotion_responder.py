"""
Emotion Responder - Maps emotional states to specific pedagogical protocols.
Provides the 'voice' and 'behavior' of the tutor during stress or success.
"""

def get_emotional_response(emotion: str, language: str = "tamil") -> dict:
    """
    Returns a response object with UI visual hints and voice message templates
    based on the student's detected emotion.
    """
    protocols = {
        "Frustrated": {
            "tamil": {
                "message": "பரவாயில்லை, நாம் மெதுவாகப் படிப்போம். மூச்சை இழுத்து விடுங்கள்.",
                "ui_color": "#FF8C00", # Warm Orange
                "action": "DE_ESCALATE",
                "vibe": "calming"
            },
            "hindi": {
                "message": "कोई बात नहीं, हम धीरे-धीरे पढ़ेंगे। एक गहरी साँस लें।",
                "ui_color": "#FF8C00",
                "action": "DE_ESCALATE",
                "vibe": "calming"
            },
            "english": {
                "message": "It's okay, let's go slower. Take a deep breath.",
                "ui_color": "#FF8C00",
                "action": "DE_ESCALATE",
                "vibe": "calming"
            }
        },
        "Anxious": {
            "tamil": {
                "message": "நீங்கள் நன்றாக செய்கிறீர்கள்! பயப்பட வேண்டாம்.",
                "ui_color": "#FFD700", # Gold
                "action": "ENCOURAGE",
                "vibe": "supportive"
            },
            "hindi": {
                "message": "आप बहुत अच्छा कर रहे हैं! घबराओ मत।",
                "ui_color": "#FFD700",
                "action": "ENCOURAGE",
                "vibe": "supportive"
            },
            "english": {
                "message": "You're doing great! No need to worry.",
                "ui_color": "#FFD700",
                "action": "ENCOURAGE",
                "vibe": "supportive"
            }
        },
        "Hesitant": {
            "tamil": {
                "message": "முயற்சி செய்து பாருங்கள், உங்களால் முடியும்!",
                "ui_color": "#ADD8E6", # Light Blue
                "action": "HINT",
                "vibe": "patient"
            },
            "hindi": {
                "message": "कोशिश करो, तुम कर सकते हो!",
                "ui_color": "#ADD8E6",
                "action": "HINT",
                "vibe": "patient"
            },
            "english": {
                "message": "Give it a try, you can do it!",
                "ui_color": "#ADD8E6",
                "action": "HINT",
                "vibe": "patient"
            }
        },
        "Confident": {
            "tamil": {
                "message": "சிறப்பு! அடுத்ததை முயற்சிப்போம்.",
                "ui_color": "#90EE90", # Light Green
                "action": "ADVANCE",
                "vibe": "celebratory"
            },
            "hindi": {
                "message": "बहुत बढ़िया! चलिए अगला प्रयास करते हैं।",
                "ui_color": "#90EE90",
                "action": "ADVANCE",
                "vibe": "celebratory"
            },
            "english": {
                "message": "Excellent! Let's try the next one.",
                "ui_color": "#90EE90",
                "action": "ADVANCE",
                "vibe": "celebratory"
            }
        }
    }

    # Fallback to English if language not found
    lang_responses = protocols.get(emotion, protocols["Hesitant"])
    return lang_responses.get(language.lower(), lang_responses["english"])
