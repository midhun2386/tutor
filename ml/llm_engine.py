"""
LLM Engine — Adaptive lesson & feedback generation using a local instruct model.
"""
import logging
import random
from dataclasses import dataclass, field
import config
from pedagogy.lesson_generator import get_seed_lesson

logger = logging.getLogger(__name__)

@dataclass
class LessonOutput:
    lesson_text: str
    hint: str
    exercise_type: str
    syllables: list[str] = field(default_factory=list)

_DE_ESCALATION_LESSONS = {
    "tamil": LessonOutput(
        lesson_text="இது கஷ்டமான வார்த்தை. நாம் சுலபமான ஒன்றை முயற்சிப்போம்!",
        hint="மெதுவாக படிக்கலாம். அவசரமே இல்லை 😊",
        exercise_type="syllable_match",
        syllables=["அம்", "மா", "அப்", "பா"],
    ),
    "hindi": LessonOutput(
        lesson_text="यह मुश्किल था। कोई बात नहीं, एक आसान शब्द आज़माते हैं!",
        hint="धीरे धीरे पढ़ो। कोई जल्दी नहीं है 😊",
        exercise_type="syllable_match",
        syllables=["माँ", "घर", "पा", "पा"],
    ),
    "english": LessonOutput(
        lesson_text="That was a tough one! Let's try something easier together.",
        hint="Take a breath. We'll go nice and slow 😊",
        exercise_type="syllable_match",
        syllables=["cat", "bat", "mat", "hat"],
    ),
}

_SYSTEM_PROMPT = """You are Veena, a warm and encouraging vernacular literacy tutor.
You help beginners learn to read in {language}.
The student's current emotion is: {emotion}.
Their mastery level is: {mastery_level}/10.
Generate ONE short reading exercise (1-2 sentences) with a helpful phonetic hint.
Respond ONLY with JSON:
{{"lesson_text": "...", "hint": "...", "exercise_type": "reading|syllable_match", "syllables": []}}
"""

class LLMEngine:
    def __init__(self):
        self._pipeline = None
        self._loaded = False
        self._is_loading = False # Prevent multiple threads from loading at once

    def _load(self):
        if self._loaded:
            return
        if self._is_loading:
            return # Let the background thread finish
            
        if config.USE_MOCK_MODELS:
            logger.info("LLMEngine: MOCK mode.")
            self._loaded = True
            return

        self._is_loading = True
        try:
            from transformers import pipeline as hf_pipeline
            import torch
            logger.info(f"Loading LLM: {config.LLM_MODEL}")
            
            # Optimized for CPU usage if no GPU is found
            device = 0 if torch.cuda.is_available() else -1
            
            self._pipeline = hf_pipeline(
                "text-generation",
                model=config.LLM_MODEL,
                device=device,
                max_new_tokens=128, # Shorter output for speed
                temperature=0.7,
                do_sample=True,
            )
            self._loaded = True
            logger.info("LLMEngine loaded.")
        except Exception as exc:
            logger.error(f"LLMEngine load failed: {exc}")
        finally:
            self._is_loading = False

    def warmup(self):
        self._load()

    def generate_lesson(self, language="tamil", emotion="Confident", mastery_level=3) -> LessonOutput:
        # If model is not ready (still loading or failed), return curated seed instantly
        if not self._loaded:
            if not self._is_loading:
                self._load() 
            
            # CRITICAL: During warmup, IGNORE de-escalation to avoid the [Together] loop
            # Provide a normal difficulty seed instead
            level = max(1, min(2, mastery_level // 4 + 1))
            seed = get_seed_lesson(language, level=level)
            return LessonOutput(
                lesson_text=seed["text"],
                hint=f"Let's focus on: {seed['phoneme']}",
                exercise_type="syllable_match" if seed["type"] == "word" else "reading",
                syllables=seed.get("syllables", []) if seed["type"] == "word" else []
            )

        # De-escalation shortcut for distressed states - ONLY IF MODELS ARE LOADED
        if emotion in ("Frustrated", "Anxious"):
            return _DE_ESCALATION_LESSONS.get(language, _DE_ESCALATION_LESSONS["english"])

        # Real LLM inference
        prompt = _SYSTEM_PROMPT.format(language=language, emotion=emotion, mastery_level=mastery_level)
        try:
            import json
            # No anyio here - we are already in a worker thread
            output_list = self._pipeline(prompt)
            output = output_list[0]["generated_text"]
            
            json_start = output.find("{")
            json_end = output.rfind("}") + 1
            if json_start != -1 and json_end > json_start:
                parsed = json.loads(output[json_start:json_end])
                return LessonOutput(
                    lesson_text=parsed.get("lesson_text", ""),
                    hint=parsed.get("hint", ""),
                    exercise_type=parsed.get("exercise_type", "reading"),
                    syllables=parsed.get("syllables", [])
                )
        except Exception as exc:
            logger.warning(f"LLM error: {exc}")
        
        # Final fallback
        seed = get_seed_lesson(language, level=1)
        return LessonOutput(lesson_text=seed["text"], hint="Try this one!", exercise_type="reading")

_engine = LLMEngine()

def warmup(): _engine.warmup()
def generate_lesson(l="tamil", e="Confident", m=3): return _engine.generate_lesson(l, e, m)
