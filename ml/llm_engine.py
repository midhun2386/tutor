"""
LLM Engine — Adaptive lesson & feedback generation using Gemini.
"""
import logging
import random
import config
from pydantic import BaseModel, Field
from pedagogy.lesson_generator import get_seed_lesson
from google import genai
from google.genai import types

logger = logging.getLogger(__name__)

class LessonOutput(BaseModel):
    lesson_text: str = Field(description="1-2 sentences in the target language.")
    hint: str = Field(description="A helpful phonetic hint in English.")
    exercise_type: str = Field(description="Either 'reading' or 'syllable_match'.")
    syllables: list[str] = Field(default_factory=list, description="List of syllable strings if syllable_match.")
    target_word: str = Field(description="The specific vocabulary word focused on (required).")
    phoneme: str = Field(description="The core phoneme or letter sound being taught (required).")

_DE_ESCALATION_LESSONS = {
    "tamil": LessonOutput(
        lesson_text="இது கஷ்டமான வார்த்தை. நாம் சுலபமான ஒன்றை முயற்சிப்போம்!",
        hint="மெதுவாக படிக்கலாம். அவசரமே இல்லை 😊",
        exercise_type="syllable_match",
        syllables=["அம்", "மா", "அப்", "பா"],
        phoneme="ma",
        target_word="அம்மா"
    ),
    "hindi": LessonOutput(
        lesson_text="यह मुश्किल था। कोई बात नहीं, एक आसान शब्द आज़माते हैं!",
        hint="धीरे धीरे पढ़ो। कोई जल्दी नहीं है 😊",
        exercise_type="syllable_match",
        syllables=["माँ", "घर", "पा", "पा"],
        phoneme="ma",
        target_word="माँ"
    ),
    "english": LessonOutput(
        lesson_text="That was a tough one! Let's try something easier together.",
        hint="Take a breath. We'll go nice and slow 😊",
        exercise_type="syllable_match",
        syllables=["cat", "bat", "mat", "hat"],
        phoneme="at",
        target_word="cat"
    ),
}

_SYSTEM_PROMPT = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are AVA, a world-class English conversation tutor specializing in "home profile" contexts.
Your goal is to tailor your instruction based on the student's proficiency level: {proficiency_level}.

PEDAGOGICAL STRATEGY:
- BEGINNER: Focus on fundamental concepts. Use basic vocabulary (household items, greetings) and simple sentences.
- INTERMEDIATE: Focus on everyday sentence formation. Teach asking questions, making requests, and expressing opinions in a home setting.
- EXPERT: Focus on refining grammar, correct tense usage, and complex/nnuanced conversations. Encourage longer, descriptive sentences and extended dialogues.

STUDENT STATUS:
- Mastered Phonemes: {mastered_phonemes} (AVOID THESE)

TASK:
1. Generate ONE perfect reading exercise (1-2 sentences) tailored to the "{proficiency_level}" strategy.
2. Ensure the target phoneme is NOT in the mastered list.
3. Provide a helpful phonetic hint.
4. If the level is EXPERT, prioritize advanced grammar and varied sentence structures.

You must respond with valid JSON matching the provided schema.
"""

class LLMEngine:
    def __init__(self):
        self._client = None
        self._loaded = False
        self._is_loading = False

    def _load(self):
        if self._loaded or self._is_loading:
            return
            
        if config.USE_MOCK_MODELS:
            logger.info("LLMEngine: MOCK mode.")
            self._loaded = True
            return

        self._is_loading = True
        try:
            logger.info(f"Connecting to Gemini: {config.LLM_MODEL}")
            if not config.GEMINI_API_KEY:
                logger.error("GEMINI_API_KEY is not set in environment or config!")
                return
                
            self._client = genai.Client(api_key=config.GEMINI_API_KEY)
            self._loaded = True
            logger.info("Gemini Engine connected.")
        except Exception as exc:
            logger.error(f"Gemini connection failed: {exc}")
        finally:
            self._is_loading = False

    def warmup(self):
        self._load()

    def generate_lesson(self, language="tamil", emotion="Confident", mastery_level=3, proficiency_level="Beginner", excluded_texts=[], mastered_phonemes=[]) -> LessonOutput:
        from pedagogy.lesson_generator import get_seed_lesson

        # If model is not ready (still loading or failed), return curated seed instantly
        if not self._loaded:
            if not self._is_loading:
                self._load() 
            
            # CRITICAL: During warmup, provide a level-appropriate seed
            seed = get_seed_lesson(language, proficiency=proficiency_level, exclude=excluded_texts, mastered=mastered_phonemes)
            
            return LessonOutput(
                lesson_text=seed["text"],
                hint=seed.get("hint", f"Focus on: {seed['phoneme']}"),
                exercise_type=seed.get("type", "reading"),
                syllables=seed.get("syllables", []),
                target_word=seed.get("target_word", seed["text"]),
                phoneme=seed.get("phoneme", "")
            )

        # De-escalation shortcut for distressed states - ONLY IF MODELS ARE LOADED
        if emotion in ("Frustrated", "Anxious"):
            seed = get_seed_lesson(language, level=1, proficiency=proficiency_level, exclude=excluded_texts, mastered=mastered_phonemes)
            return LessonOutput(
                lesson_text=seed["text"],
                hint="Let's take it slow and easy.",
                exercise_type=seed.get("type", "reading"),
                syllables=seed.get("syllables", []),
                target_word=seed.get("target_word", seed["text"]),
                phoneme=seed.get("phoneme", "")
            )

        try:
            # Real LLM inference via Gemini
            prompt = _SYSTEM_PROMPT.format(
                language=language, 
                emotion=emotion, 
                mastery_level=mastery_level,
                proficiency_level=proficiency_level,
                mastered_phonemes=", ".join(mastered_phonemes) if mastered_phonemes else "None"
            )
            
            if not self._client:
                raise ValueError("Gemini client not initialized")
                
            response = self._client.models.generate_content(
                model=config.LLM_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=LessonOutput,
                    temperature=0.7,
                ),
            )
            
            # The SDK automatically parses the JSON text into the Pydantic object
            import json
            parsed = json.loads(response.text)
            
            return LessonOutput(
                lesson_text=parsed.get("lesson_text", ""),
                hint=parsed.get("hint", ""),
                exercise_type=parsed.get("exercise_type", "reading"),
                syllables=parsed.get("syllables", []),
                target_word=parsed.get("target_word", ""),
                phoneme=parsed.get("phoneme", "")
            )
            
        except Exception as exc:
            logger.warning(f"LLM error: {exc}")
        
        # Final fallback - use seed with proficiency if possible
        seed = get_seed_lesson(language, proficiency=proficiency_level, exclude=excluded_texts, mastered=mastered_phonemes)
        return LessonOutput(
            lesson_text=seed["text"], 
            hint="Try this one!", 
            exercise_type=seed.get("type", "reading"),
            syllables=seed.get("syllables", []),
            target_word=seed.get("target_word", seed["text"]),
            phoneme=seed.get("phoneme", "")
        )

_engine = LLMEngine()

def warmup(): _engine.warmup()
def generate_lesson(language="tamil", emotion="Confident", mastery_level=3, proficiency_level="Beginner", excluded_texts=[], mastered_phonemes=[]): 
    return _engine.generate_lesson(language, emotion, mastery_level, proficiency_level=proficiency_level, excluded_texts=excluded_texts, mastered_phonemes=mastered_phonemes)
