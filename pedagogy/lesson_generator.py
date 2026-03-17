"""
Lesson Generator - Static curriculum seeds for the tutor.
This complements the LLM by providing high-quality, verified starter content.
"""

CURRICULUM = {
    "tamil": {
        "level_1": [
            {"text": "அம்மா", "phoneme": "ma", "type": "word", "syllables": ["அம்", "மா"]},
            {"text": "அப்பா", "phoneme": "pa", "type": "word", "syllables": ["அப்", "பா"]},
            {"text": "படம்", "phoneme": "da", "type": "word", "syllables": ["ப", "ட", "ம்"]},
            {"text": "பட்டம்", "phoneme": "tta", "type": "word", "syllables": ["பட்", "டம்"]},
            {"text": "வாத்து", "phoneme": "thu", "type": "word", "syllables": ["வாத்", "து"]},
            {"text": "பழம்", "phoneme": "zha", "type": "word", "syllables": ["ப", "ழம்"]},
            {"text": "மரம்", "phoneme": "ra", "type": "word", "syllables": ["ம", "ரம்"]},
            {"text": "கடல்", "phoneme": "da", "type": "word", "syllables": ["க", "டல்"]}
        ],
        "level_2": [
            {"text": "அம்மா வந்தாள்.", "phoneme": "va", "type": "sentence"},
            {"text": "பந்து உருண்டது.", "phoneme": "ra", "type": "sentence"},
            {"text": "அப்பா கடைக்குச் சென்றார்.", "phoneme": "pa", "type": "sentence"},
            {"text": "பட்டம் வானில் பறந்தது.", "phoneme": "tta", "type": "sentence"},
            {"text": "கிளி பழம் தின்றது.", "phoneme": "ki", "type": "sentence"}
        ],
        "level_3": [
            {"text": "அம்மா கடைக்குச் சென்றார். அங்கு அழகான பட்டம் வாங்கினார். பட்டம் வானில் உயரமாகப் பறந்தது.", "phoneme": "tta", "type": "paragraph"}
        ]
    },
    "hindi": {
        "level_1": [
            {"text": "आम", "phoneme": "aa", "type": "word", "syllables": ["आ", "म"]},
            {"text": "घर", "phoneme": "gha", "type": "word", "syllables": ["घ", "र"]},
            {"text": "नमक", "phoneme": "na", "type": "word", "syllables": ["न", "म", "क"]},
            {"text": "कमल", "phoneme": "ka", "type": "word", "syllables": ["क", "म", "ल"]},
            {"text": "कलम", "phoneme": "la", "type": "word", "syllables": ["क", "ल", "म"]},
            {"text": "सड़क", "phoneme": "da", "type": "word", "syllables": ["स", "ड़", "क"]},
            {"text": "जग", "phoneme": "ja", "type": "word", "syllables": ["ज", "ग"]},
            {"text": "मटर", "phoneme": "ta", "type": "word", "syllables": ["म", "ट", "र"]}
        ],
        "level_2": [
            {"text": "राम घर चल।", "phoneme": "cha", "type": "sentence"},
            {"text": "आम मीठा है।", "phoneme": "ma", "type": "sentence"},
            {"text": "कमल जल पर है।", "phoneme": "la", "type": "sentence"},
            {"text": "राम फल चख।", "phoneme": "cha", "type": "sentence"},
            {"text": "सड़क पर मत चल।", "phoneme": "da", "type": "sentence"}
        ],
        "level_3": [
            {"text": "राम घर चल। घर चल कर फल चख। आम मीठा है। सड़क पर मत चल।", "phoneme": "cha", "type": "paragraph"}
        ]
    },
    "english": {
        "level_1": [
            {"text": "Cat", "phoneme": "at", "type": "word", "syllables": ["c", "at"]},
            {"text": "Dog", "phoneme": "og", "type": "word", "syllables": ["d", "og"]},
            {"text": "Bat", "phoneme": "at", "type": "word", "syllables": ["b", "at"]},
            {"text": "Hat", "phoneme": "at", "type": "word", "syllables": ["h", "at"]},
            {"text": "Mat", "phoneme": "at", "type": "word", "syllables": ["m", "at"]},
            {"text": "Sun", "phoneme": "un", "type": "word", "syllables": ["s", "un"]},
            {"text": "Run", "phoneme": "un", "type": "word", "syllables": ["r", "un"]},
            {"text": "Fun", "phoneme": "un", "type": "word", "syllables": ["f", "un"]}
        ],
        "level_2": [
            {"text": "The cat sat.", "phoneme": "sa", "type": "sentence"},
            {"text": "The dog ran.", "phoneme": "ra", "type": "sentence"},
            {"text": "The sun is hot.", "phoneme": "ho", "type": "sentence"},
            {"text": "I like to run.", "phoneme": "ri", "type": "sentence"},
            {"text": "It is fun to read.", "phoneme": "re", "type": "sentence"}
        ],
        "level_3": [
            {"text": "The sun is hot today. The cat sat on the mat. I like to run and have fun in the sun. Reading is fun.", "phoneme": "un", "type": "paragraph"}
        ],
        "expert": [
            {"text": "It's a bit of a bummer that it's raining, but we can just chill at home. If you're feeling under the weather, you should probably take it easy.", "phoneme": "ch", "type": "conversational"},
            {"text": "Learning English is a piece of cake once you get the hang of it! Had I known you were coming, I would have cooked extra.", "phoneme": "ce", "type": "conversational"}
        ]
    }
}

def get_seed_lesson(language: str, level: int = 1, proficiency: str = "Beginner") -> dict:
    lang_curriculum = CURRICULUM.get(language.lower(), CURRICULUM["english"])
    
    # Map proficiency to level key
    prof_map = {
        "beginner": "level_1",
        "intermediate": "level_2",
        "expert": "expert"
    }
    
    level_key = prof_map.get(proficiency.lower(), f"level_{min(level, 3)}")
    
    # Fallback cascade: level_N -> level_1
    choices = lang_curriculum.get(level_key)
    if not choices:
        # If expert not found for a language, try level_3
        choices = lang_curriculum.get("level_3") or lang_curriculum["level_1"]
        
    import random
    return random.choice(choices)
