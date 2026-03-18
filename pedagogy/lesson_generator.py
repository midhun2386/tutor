"""
Lesson Generator - Static curriculum seeds for the tutor.
This complements the LLM by providing high-quality, verified starter content.
"""

CURRICULUM = {
    "tamil": {
        "level_1": [
            {"text": "அம்மா", "phoneme": "ma", "type": "word", "target_word": "அம்மா", "syllables": ["அம்", "மா"]},
            {"text": "அப்பா", "phoneme": "pa", "type": "word", "target_word": "அப்பா", "syllables": ["அப்", "பா"]},
            {"text": "படம்", "phoneme": "da", "type": "word", "target_word": "படம்", "syllables": ["ப", "ட", "ம்"]},
            {"text": "பட்டம்", "phoneme": "tta", "type": "word", "target_word": "பட்டம்", "syllables": ["பட்", "டம்"]},
            {"text": "வாத்து", "phoneme": "thu", "type": "word", "target_word": "வாத்து", "syllables": ["வாத்", "து"]},
            {"text": "பழம்", "phoneme": "zha", "type": "word", "target_word": "பழம்", "syllables": ["ப", "ழம்"]},
            {"text": "மரம்", "phoneme": "ra", "type": "word", "target_word": "மரம்", "syllables": ["ம", "ரம்"]},
            {"text": "கடல்", "phoneme": "da", "type": "word", "target_word": "கடல்", "syllables": ["க", "டல்"]},
            {"text": "கல்", "phoneme": "ka", "type": "word", "target_word": "கல்", "syllables": ["க", "ல்"]},
            {"text": "பல்", "phoneme": "pa", "type": "word", "target_word": "பல்", "syllables": ["ப", "ல்"]},
            {"text": "கண்", "phoneme": "ka", "type": "word", "target_word": "கண்", "syllables": ["க", "ண்"]},
            {"text": "பெண்", "phoneme": "pe", "type": "word", "target_word": "பெண்", "syllables": ["பெ", "ண்"]},
            {"text": "மண்", "phoneme": "ma", "type": "word", "target_word": "மண்", "syllables": ["ம", "ண்"]},
            {"text": "நாய்", "phoneme": "naa", "type": "word", "target_word": "நாய்", "syllables": ["நா", "ய்"]},
            {"text": "பூனை", "phoneme": "nai", "type": "word", "target_word": "பூனை", "syllables": ["பூ", "னை"]}
        ],
        "level_2": [
            {"text": "அம்மா வந்தாள்.", "phoneme": "va", "type": "sentence", "target_word": "வந்தாள்", "syllables": ["வந்", "தாள்"]},
            {"text": "பந்து உருண்டது.", "phoneme": "ra", "type": "sentence", "target_word": "பந்து", "syllables": ["பந்", "து"]},
            {"text": "அப்பா கடைக்குச் சென்றார்.", "phoneme": "pa", "type": "sentence", "target_word": "கடைக்கு", "syllables": ["க", "டை", "க்", "கு"]},
            {"text": "பட்டம் வானில் பறந்தது.", "phoneme": "tta", "type": "sentence", "target_word": "பட்டம்", "syllables": ["பட்", "டம்"]},
            {"text": "கிளி பழம் தின்றது.", "phoneme": "ki", "type": "sentence", "target_word": "கிளி", "syllables": ["கி", "ளி"]},
            {"text": "மரம் உயரமாக உள்ளது.", "phoneme": "ma", "type": "sentence", "target_word": "மரம்", "syllables": ["ம", "ரம்"]},
            {"text": "நான் பள்ளிக்குச் செல்கிறேன்.", "phoneme": "pa", "type": "sentence", "target_word": "பள்ளிக்குச்", "syllables": ["பள்", "ளி", "க்", "கு", "ச்"]},
            {"text": "மீன் நீரில் நீந்துகிறது.", "phoneme": "mii", "type": "sentence", "target_word": "மீன்", "syllables": ["மீ", "ன்"]},
            {"text": "நிலவு அழகாக இருக்கிறது.", "phoneme": "ni", "type": "sentence", "target_word": "நிலவு", "syllables": ["நி", "ல", "வு"]},
            {"text": "காக்கை கரைகிறது.", "phoneme": "kaa", "type": "sentence", "target_word": "காக்கை", "syllables": ["காக்", "கை"]}
        ],
        "level_3": [
            {"text": "இரவில் நிலவு அழகாக இருக்கிறது. நட்சத்திரங்கள் மின்னுகின்றன.", "phoneme": "na", "type": "paragraph", "target_word": "நட்சத்திரங்கள்", "syllables": ["நட்", "சத்", "தி", "ரங்", "கள்"]},
            {"text": "கடற்கரையில் அலைகள் வீசுகின்றன. குழந்தைகள் விளையாடுகிறார்கள்.", "phoneme": "ku", "type": "paragraph", "target_word": "குழந்தைகள்", "syllables": ["கு", "ழந்", "தை", "கள்"]},
            {"text": "மழை பெய்கிறது. மயில் தோகை விரித்து அடுகிறது.", "phoneme": "ma", "type": "paragraph", "target_word": "மயில்", "syllables": ["ம", "யி", "ல்"]},
            {"text": "காட்டுக்கு ராஜா சிங்கம். அது குகையில் வாழ்கிறது.", "phoneme": "si", "type": "paragraph", "target_word": "சிங்கம்", "syllables": ["சிங்", "கம்"]},
            {"text": "நாம் தினமும் படிக்க வேண்டும். அறிவை வளர்க்க வேண்டும்.", "phoneme": "pa", "type": "paragraph", "target_word": "படிக்க", "syllables": ["ப", "டிக்", "க"]}
        ],
        "expert": [
            {"text": "தமிழர்களின் விருந்தோம்பல் உலகப் புகழ் பெற்றது.", "phoneme": "vi", "type": "conversational", "target_word": "விருந்தோம்பல்", "syllables": ["வி", "ருந்", "தோம்", "பல்"]},
            {"text": "கணினித் துறையில் பல புதிய மாற்றங்கள் நிகழ்ந்துள்ளன.", "phoneme": "ka", "type": "conversational", "target_word": "கணினித்", "syllables": ["க", "ணி", "னி", "த்"]}
        ]
    },
    "hindi": {
        "level_1": [
            {"text": "आम", "phoneme": "aa", "type": "word", "target_word": "आम", "syllables": ["आ", "म"]},
            {"text": "घर", "phoneme": "gha", "type": "word", "target_word": "घर", "syllables": ["घ", "र"]},
            {"text": "नमक", "phoneme": "na", "type": "word", "target_word": "नमक", "syllables": ["न", "म", "क"]},
            {"text": "कमल", "phoneme": "ka", "type": "word", "target_word": "कमल", "syllables": ["क", "म", "ल"]},
            {"text": "कलम", "phoneme": "la", "type": "word", "target_word": "कलम", "syllables": ["क", "ल", "म"]},
            {"text": "सड़क", "phoneme": "da", "type": "word", "target_word": "सड़क", "syllables": ["स", "ड़", "क"]},
            {"text": "जग", "phoneme": "ja", "type": "word", "target_word": "जग", "syllables": ["ज", "ग"]},
            {"text": "मटर", "phoneme": "ta", "type": "word", "target_word": "मटर", "syllables": ["म", "ट", "र"]},
            {"text": "पानी", "phoneme": "pa", "type": "word", "target_word": "पानी", "syllables": ["पा", "नी"]},
            {"text": "रोटी", "phoneme": "ro", "type": "word", "target_word": "रोटी", "syllables": ["रो", "टी"]},
            {"text": "कुर्ता", "phoneme": "ku", "type": "word", "target_word": "कुर्ता", "syllables": ["कुर्", "ता"]},
            {"text": "किताब", "phoneme": "ki", "type": "word", "target_word": "किताब", "syllables": ["कि", "ता", "ब"]},
            {"text": "कुर्सी", "phoneme": "ku", "type": "word", "target_word": "कुर्सी", "syllables": ["कुर्", "सी"]},
            {"text": "तारा", "phoneme": "ta", "type": "word", "target_word": "तारा", "syllables": ["ता", "रा"]},
            {"text": "फूल", "phoneme": "phu", "type": "word", "target_word": "फूल", "syllables": ["फू", "ल"]}
        ],
        "level_2": [
            {"text": "राम घर चल।", "phoneme": "cha", "type": "sentence", "target_word": "चल", "syllables": ["च", "ल"]},
            {"text": "आम मीठा है।", "phoneme": "ma", "type": "sentence", "target_word": "मीठा", "syllables": ["मी", "ठा"]},
            {"text": "कमल जल पर है।", "phoneme": "la", "type": "sentence", "target_word": "कमल", "syllables": ["क", "म", "ल"]},
            {"text": "राम फल चख।", "phoneme": "cha", "type": "sentence", "target_word": "फल", "syllables": ["फ", "ल"]},
            {"text": "सड़क पर मत चल।", "phoneme": "da", "type": "sentence", "target_word": "सड़क", "syllables": ["स", "ड़", "क"]},
            {"text": "मुझे पानी चाहिए।", "phoneme": "pa", "type": "sentence", "target_word": "पानी", "syllables": ["पा", "नी"]},
            {"text": "कलम से लिखो।", "phoneme": "li", "type": "sentence", "target_word": "लिखो", "syllables": ["लि", "खो"]},
            {"text": "कुर्सी पर बैठो।", "phoneme": "ku", "type": "sentence", "target_word": "कुर्सी", "syllables": ["कुर्", "सी"]},
            {"text": "किताब पढ़ो।", "phoneme": "ki", "type": "sentence", "target_word": "किताब", "syllables": ["कि", "ता", "ब"]},
            {"text": "आज मौसम अच्छा है।", "phoneme": "ma", "type": "sentence", "target_word": "मौसम", "syllables": ["मौ", "स", "म"]}
        ],
        "level_3": [
            {"text": "राम घर चल। घर चल कर फल चख। सड़क पर मत चल।", "phoneme": "cha", "type": "paragraph", "target_word": "सड़क", "syllables": ["स", "ड़", "क"]},
            {"text": "आज आसमान साफ है। सूरज चमक रहा है। चिड़िया गा रही हैं।", "phoneme": "cha", "type": "paragraph", "target_word": "चमक", "syllables": ["च", "म", "क"]},
            {"text": "मुझे किताब पढ़ना पसंद है। इससे ज्ञान बढ़ता है।", "phoneme": "gyan", "type": "paragraph", "target_word": "ज्ञान", "syllables": ["ज्ञा", "न"]},
            {"text": "हम कल दिल्ली जाएँगे। वहाँ लाल किला देखेंगे।", "phoneme": "di", "type": "paragraph", "target_word": "दिल्ली", "syllables": ["दि", "ल्", "ली"]},
            {"text": "स्वास्थ्य सबसे बड़ा धन है। इसलिए रोज व्यायाम करें।", "phoneme": "swa", "type": "paragraph", "target_word": "स्वास्थ्य", "syllables": ["स्वा", "स्थ", "्य"]}
        ],
        "expert": [
            {"text": "भारतीय संस्कृति में विविधता में एकता का उत्कृष्ट उदाहरण है।", "phoneme": "vi", "type": "conversational", "target_word": "विविधता", "syllables": ["वि", "वि", "ध", "ता"]},
            {"text": "प्रौद्योगिकी ने हमारे जीवन के हर पहलू को बदल दिया है।", "phoneme": "pra", "type": "conversational", "target_word": "प्रौद्योगिकी", "syllables": ["प्रौ", "द्यो", "गि", "की"]}
        ]
    },
    "english": {
        "level_1": [
            {"text": "Cat", "phoneme": "at", "type": "word", "target_word": "Cat", "syllables": ["c", "at"]},
            {"text": "Dog", "phoneme": "og", "type": "word", "target_word": "Dog", "syllables": ["d", "og"]},
            {"text": "Bat", "phoneme": "at", "type": "word", "target_word": "Bat", "syllables": ["b", "at"]},
            {"text": "Hat", "phoneme": "at", "type": "word", "target_word": "Hat", "syllables": ["h", "at"]},
            {"text": "Mat", "phoneme": "at", "type": "word", "target_word": "Mat", "syllables": ["m", "at"]},
            {"text": "Sun", "phoneme": "un", "type": "word", "target_word": "Sun", "syllables": ["s", "un"]},
            {"text": "Run", "phoneme": "un", "type": "word", "target_word": "Run", "syllables": ["r", "un"]},
            {"text": "Fun", "phoneme": "un", "type": "word", "target_word": "Fun", "syllables": ["f", "un"]},
            {"text": "Big", "phoneme": "ig", "type": "word", "target_word": "Big", "syllables": ["b", "ig"]},
            {"text": "Pig", "phoneme": "ig", "type": "word", "target_word": "Pig", "syllables": ["p", "ig"]},
            {"text": "Red", "phoneme": "ed", "type": "word", "target_word": "Red", "syllables": ["r", "ed"]},
            {"text": "Bed", "phoneme": "ed", "type": "word", "target_word": "Bed", "syllables": ["b", "ed"]},
            {"text": "Pen", "phoneme": "en", "type": "word", "target_word": "Pen", "syllables": ["p", "en"]},
            {"text": "Ten", "phoneme": "en", "type": "word", "target_word": "Ten", "syllables": ["t", "en"]},
            {"text": "Top", "phoneme": "op", "type": "word", "target_word": "Top", "syllables": ["t", "op"]}
        ],
        "level_2": [
            {"text": "The cat sat.", "phoneme": "sa", "type": "sentence", "target_word": "cat", "syllables": ["c", "at"]},
            {"text": "The dog ran.", "phoneme": "ra", "type": "sentence", "target_word": "dog", "syllables": ["d", "og"]},
            {"text": "The sun is hot.", "phoneme": "ho", "type": "sentence", "target_word": "hot", "syllables": ["h", "ot"]},
            {"text": "I like to run.", "phoneme": "ri", "type": "sentence", "target_word": "run", "syllables": ["r", "un"]},
            {"text": "It is fun to read.", "phoneme": "re", "type": "sentence", "target_word": "read", "syllables": ["r", "ead"]},
            {"text": "She has a red pen.", "phoneme": "ed", "type": "sentence", "target_word": "red", "syllables": ["r", "ed"]},
            {"text": "The big pig is pink.", "phoneme": "ig", "type": "sentence", "target_word": "pig", "syllables": ["p", "ig"]},
            {"text": "Go to bed now.", "phoneme": "ed", "type": "sentence", "target_word": "bed", "syllables": ["b", "ed"]},
            {"text": "I see ten birds.", "phoneme": "en", "type": "sentence", "target_word": "ten", "syllables": ["t", "en"]},
            {"text": "The top is spinning.", "phoneme": "op", "type": "sentence", "target_word": "top", "syllables": ["t", "op"]}
        ],
        "level_3": [
            {"text": "The sun is hot today. The cat sat on the mat.", "phoneme": "un", "type": "paragraph", "target_word": "mat", "syllables": ["m", "at"]},
            {"text": "I like to read books. Reading is a lot of fun. Books take you to new places.", "phoneme": "oo", "type": "paragraph", "target_word": "books", "syllables": ["b", "oo", "ks"]},
            {"text": "We went to the park. The dogs were running around. It was a beautiful day.", "phoneme": "ar", "type": "paragraph", "target_word": "park", "syllables": ["p", "ar", "k"]},
            {"text": "My family loves to cook. We make pizza on Fridays. It tastes amazing.", "phoneme": "pi", "type": "paragraph", "target_word": "pizza", "syllables": ["piz", "za"]},
            {"text": "The stars are bright tonight. I can see the moon clearly. Space is wonderful.", "phoneme": "ar", "type": "paragraph", "target_word": "stars", "syllables": ["s", "tar", "s"]}
        ],
        "expert": [
            {"text": "It's a bit of a bummer that it's raining.", "phoneme": "ch", "type": "conversational", "target_word": "raining", "syllables": ["rain", "ing"]},
            {"text": "Learning English is a piece of cake!", "phoneme": "ce", "type": "conversational", "target_word": "piece", "syllables": ["pi", "ece"]},
            {"text": "The intricate mechanisms of climate change are quite fascinating to study.", "phoneme": "in", "type": "conversational", "target_word": "intricate", "syllables": ["in", "tri", "cate"]},
            {"text": "I'm looking forward to expanding my vocabulary through consistent practice.", "phoneme": "vo", "type": "conversational", "target_word": "vocabulary", "syllables": ["vo", "cab", "u", "lar", "y"]}
        ]
    }
}

def get_seed_lesson(language: str, level: int = 1, proficiency: str = "Beginner", exclude: list[str] = [], mastered: list[str] = []) -> dict:
    lang_curriculum = CURRICULUM.get(language.lower(), CURRICULUM["english"])
    prof_map = {"beginner": "level_1", "intermediate": "level_2", "expert": "expert"}
    level_key = prof_map.get(proficiency.lower(), f"level_{min(level, 3)}")
    
    choices = lang_curriculum.get(level_key) or lang_curriculum.get("level_3") or lang_curriculum["level_1"]
    
    # Filter out excluded texts AND mastered phonemes
    filtered = [c for c in choices if c["text"] not in exclude and c.get("phoneme") not in mastered]
    
    # If everything is excluded (all mastered), prioritize non-excluded texts even if phoneme is mastered
    if not filtered:
        filtered = [c for c in choices if c["text"] not in exclude]
        
    # Final fallback - just pick from original choices
    final_pool = filtered if filtered else choices
    
    import random
    return random.choice(final_pool)
