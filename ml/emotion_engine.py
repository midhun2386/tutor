"""
Speech Emotion Recognition (SER) Engine.

Uses a fine-tuned Wav2Vec2 model from HuggingFace to classify the learner's
emotional state into one of: Confident, Hesitant, Frustrated, Anxious.

In mock mode (USE_MOCK_MODELS=1) it returns a random label so the rest of
the app can be developed and tested without a GPU.
"""
import random
import logging
from dataclasses import dataclass

import numpy as np

import config

logger = logging.getLogger(__name__)

@dataclass
class EmotionResult:
    label: str          # Confident | Hesitant | Frustrated | Anxious
    confidence: float   # 0.0 – 1.0
    all_scores: dict    # raw softmax scores per label


# ─── Label mapping (model-specific) ──────────────────────────────────────────
# ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition outputs:
#   angry, calm, disgust, fearful, happy, neutral, sad, surprised
# We map those to our four pedagogical states:
_RAW_TO_PEDAGOGY = {
    "angry":     "Frustrated",
    "disgust":   "Frustrated",
    "fearful":   "Anxious",
    "sad":       "Anxious",
    "neutral":   "Hesitant",
    "calm":      "Confident",
    "happy":     "Confident",
    "surprised": "Hesitant",
}


class EmotionEngine:
    """Singleton-friendly SER model wrapper."""

    def __init__(self):
        self._pipeline = None
        self._loaded = False

    def _load(self):
        if self._loaded:
            return
        if config.USE_MOCK_MODELS:
            logger.info("EmotionEngine: running in MOCK mode.")
            self._loaded = True
            return

        try:
            from transformers import pipeline as hf_pipeline
            logger.info(f"Loading emotion model: {config.EMOTION_MODEL}")
            self._pipeline = hf_pipeline(
                "audio-classification",
                model=config.EMOTION_MODEL,
                token=config.HF_TOKEN or None,
            )
            self._loaded = True
            logger.info("EmotionEngine: model loaded successfully.")
        except Exception as exc:
            logger.error(f"EmotionEngine load failed: {exc}. Falling back to mock.")
            self._loaded = True  # prevent retry loops
    def warmup(self):
        """Pre-load the model."""
        self._load()

    def predict(self, waveform: np.ndarray, sample_rate: int = 16_000) -> EmotionResult:
        """
        Run emotion classification on a numpy waveform.

        Parameters
        ----------
        waveform     : 1-D float32 numpy array at 16 kHz
        sample_rate  : should always be 16000

        Returns
        -------
        EmotionResult
        """
        self._load()

        # ── Mock mode ────────────────────────────────────────────────────────
        if config.USE_MOCK_MODELS or self._pipeline is None:
            # During warmup/mock, vary between positive states to feel "alive" 
            # without triggering de-escalation loops.
            choices = ["Confident", "Hesitant"]
            weights = [0.85, 0.15] # 85% Confident, 15% Hesitant
            label = random.choices(choices, weights=weights)[0]
            
            conf = 0.90 + (random.random() * 0.08) # 90-98%
            all_scores = {l: (1.0 - conf) / (len(config.EMOTION_LABELS)-1) for l in config.EMOTION_LABELS}
            all_scores[label] = conf
            return EmotionResult(label=label, confidence=conf, all_scores=all_scores)

        # ── Energy Check ──────────────────────────────────────────────────────
        rms = np.sqrt(np.mean(waveform**2))
        if rms < 0.01:  # Very quiet or silence
            logger.info("EmotionEngine: Audio too quiet. Defaulting to 'Hesitant'.")
            label = "Hesitant"
            all_scores = {l: 0.05 for l in config.EMOTION_LABELS}
            all_scores[label] = 0.85
            return EmotionResult(label=label, confidence=0.85, all_scores=all_scores)

        # ── Energy-Based Biasing ─────────────────────────────────────────────
        # rms is already calculated above in the 'Energy Check' section
        # We define thresholds for 'Loud' (Confident) and 'Soft' (Hesitant)
        # These are calibrated for normalized web-audio (0.0 to 1.0)
        is_loud = rms > 0.08
        is_soft = rms < 0.03
        
        # ── Real inference ────────────────────────────────────────────────────
        # The HF audio-classification pipeline accepts {"array": ..., "sampling_rate": ...}
        inputs = {"array": waveform.astype(np.float32), "sampling_rate": sample_rate}
        raw_outputs: list[dict] = self._pipeline(inputs, top_k=None)   # all labels

        # Build score dict with raw model labels
        raw_scores = {item["label"].lower(): float(item["score"]) for item in raw_outputs}

        # Aggregate into pedagogy labels
        pedagogy_scores: dict[str, float] = {l: 0.0 for l in config.EMOTION_LABELS}
        for raw_label, score in raw_scores.items():
            mapped = _RAW_TO_PEDAGOGY.get(raw_label, "Hesitant")
            pedagogy_scores[mapped] += score

        # Apply Energy Bias
        if is_loud:
            logger.info(f"EmotionEngine: High energy detected ({rms:.3f}). Biasing towards Confident.")
            pedagogy_scores["Confident"] += 0.3 # Boost confidence
        elif is_soft:
            logger.info(f"EmotionEngine: Low energy detected ({rms:.3f}). Biasing towards Hesitant.")
            pedagogy_scores["Hesitant"] += 0.3 # Boost hesitancy

        # Normalise
        total = sum(pedagogy_scores.values()) or 1.0
        pedagogy_scores = {k: round(v / total, 4) for k, v in pedagogy_scores.items()}

        top_label = max(pedagogy_scores, key=lambda k: pedagogy_scores[k])
        top_conf = pedagogy_scores[top_label]

        return EmotionResult(label=top_label, confidence=top_conf, all_scores=pedagogy_scores)


# ─── Module-level singleton ───────────────────────────────────────────────────
_engine = EmotionEngine()


def warmup():
    """Warm up the emotion engine."""
    _engine.warmup()

def predict_emotion(waveform: np.ndarray, sample_rate: int = 16_000) -> EmotionResult:
    """Convenience function for the module-level singleton."""
    return _engine.predict(waveform, sample_rate)
