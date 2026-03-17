import random

_CREATIVE_FEEDBACK = {
    "correct": {
        "tamil": [
            "அற்புதம்! மிகச் சரியாகச் சொன்னீர்கள்! 🌟",
            "அருமை! உங்கள் உச்சரிப்பு மிகத் தெளிவாக உள்ளது. 👏",
            "வாழ்த்துக்கள்! நீங்கள் மிக வேகமாக கற்றுக் கொள்கிறீர்கள். 🚀",
            "சிறப்பு! இதே வேகத்தில் தொடருவோம்! ✨"
        ],
        "hindi": [
            "अद्भुत! आपने बिल्कुल सही कहा! 🌟",
            "बहुत बढ़िया! आपका उच्चारण बहुत स्पष्ट है। 👏",
            "बधाई हो! आप बहुत तेजी से सीख रहे हैं। 🚀",
            "शानदार! इसी तरह जारी रखें! ✨"
        ],
        "english": [
            "Amazing! You said that perfectly! 🌟",
            "Great job! Your pronunciation is very clear. 👏",
            "Congratulations! You're learning so fast. 🚀",
            "Excellent! Let's keep this momentum going! ✨"
        ]
    },
    "incorrect": {
        "tamil": [
            "கிட்டத்தட்ட நெருங்கிவிட்டீர்கள்! மீண்டும் ஒருமுறை முயற்சிப்போம். 💪",
            "பரவாயில்லை, முயற்சி செய்வதுதான் முக்கியம். மீண்டும் சொல்லுங்கள். 😊",
            "மெதுவாக முயற்சி செய்யுங்கள், உங்களால் முடியும்! 💡",
            "குறைந்தபட்சம் நீங்கள் முயற்சி செய்தீர்கள், அதுவே பெரிய விஷயம்! 🌈"
        ],
        "hindi": [
            "लगभग पहुँच गए! एक बार फिर कोशिश करते हैं। 💪",
            "कोई बात नहीं, कोशिश करना महत्वपूर्ण है। फिर से कहें। 😊",
            "धीरे-धीरे कोशिश करें, आप कर सकते हैं! 💡",
            "कम से कम आपने कोशिश की, यही बड़ी बात है! 🌈"
        ],
        "english": [
            "Almost there! Let's try it one more time. 💪",
            "It's okay, trying is what matters. Say it again. 😊",
            "Take it slow, I know you can do it! 💡",
            "At least you gave it a shot, that's the spirit! 🌈"
        ]
    }
}

def get_creative_feedback(language: str = "english", is_correct: bool = True) -> str:
    """Returns a random creative feedback string in the target language."""
    category = "correct" if is_correct else "incorrect"
    lang_key = language.lower() if language.lower() in ["tamil", "hindi"] else "english"
    
    options = _CREATIVE_FEEDBACK[category].get(lang_key, _CREATIVE_FEEDBACK[category]["english"])
    return random.choice(options)

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
