"""
Lesson Generator - Static curriculum seeds for the tutor.
This complements the LLM by providing high-quality, verified starter content.
"""

CURRICULUM = {
    "tamil": {
        "level_1": [
            {"text": "அம்மா", "phoneme": "ma", "type": "word", "syllables": ["அம்", "மா"]},
            {"text": "அப்பா", "phoneme": "pa", "type": "word", "syllables": ["அப்", "பா"]},
            {"text": "படம்", "phoneme": "da", "type": "word", "syllables": ["ப", "ட", "ம்"]}
        ],
        "level_2": [
            {"text": "அம்மா வந்தாள்.", "phoneme": "va", "type": "sentence"},
            {"text": "பந்து உருண்டது.", "phoneme": "ra", "type": "sentence"}
        ]
    },
    "hindi": {
        "level_1": [
            {"text": "आम", "phoneme": "aa", "type": "word", "syllables": ["आ", "म"]},
            {"text": "घर", "phoneme": "gha", "type": "word", "syllables": ["घ", "र"]},
            {"text": "नमक", "phoneme": "na", "type": "word", "syllables": ["न", "म", "क"]}
        ],
        "level_2": [
            {"text": "राम घर चल।", "phoneme": "cha", "type": "sentence"},
            {"text": "आम मीठा है।", "phoneme": "ma", "type": "sentence"}
        ]
    },
    "english": {
        "level_1": [
            {"text": "Cat", "phoneme": "at", "type": "word", "syllables": ["c", "at"]},
            {"text": "Dog", "phoneme": "og", "type": "word", "syllables": ["d", "og"]},
            {"text": "Bat", "phoneme": "at", "type": "word", "syllables": ["b", "at"]}
        ],
        "level_2": [
            {"text": "The cat sat.", "phoneme": "sa", "type": "sentence"},
            {"text": "The dog ran.", "phoneme": "ra", "type": "sentence"}
        ]
    }
}

def get_seed_lesson(language: str, level: int = 1) -> dict:
    lang_curriculum = CURRICULUM.get(language.lower(), CURRICULUM["english"])
    level_key = f"level_{level}"
    import random
    return random.choice(lang_curriculum.get(level_key, lang_curriculum["level_1"]))
