"""
Speech-to-Text (STT) Engine — Whisper-based vernacular transcription.

Supports regional dialects and code-switching (e.g., Tanglish).
Falls back to a deterministic mock transcript in USE_MOCK_MODELS mode.
"""
import io
import logging
import tempfile
import os
from dataclasses import dataclass

import config

logger = logging.getLogger(__name__)


@dataclass
class TranscriptResult:
    text: str
    language: str
    segments: list[dict]    # word-level timing (from Whisper)


class STTEngine:
    """Singleton Whisper STT wrapper."""

    def __init__(self):
        self._model = None
        self._loaded = False

    def _load(self):
        if self._loaded:
            return
        if config.USE_MOCK_MODELS:
            logger.info("STTEngine: running in MOCK mode.")
            self._loaded = True
            return
        try:
            import whisper
            logger.info(f"Loading Whisper model: {config.WHISPER_MODEL}")
            self._model = whisper.load_model(config.WHISPER_MODEL)
            self._loaded = True
            logger.info("STTEngine: model loaded successfully.")
        except Exception as exc:
            logger.error(f"STTEngine load failed: {exc}. Falling back to mock.")
            self._loaded = True
    def warmup(self):
        """Pre-load the model."""
        self._load()

    def transcribe(self, audio_bytes: bytes, language_hint: str = "ta") -> TranscriptResult:
        """
        Transcribe raw audio bytes.

        Parameters
        ----------
        audio_bytes   : WAV or any audio file bytes
        language_hint : ISO-639-1 code ("ta"=Tamil, "hi"=Hindi, "en"=English)

        Returns
        -------
        TranscriptResult
        """
        self._load()

        # ── Mock mode ─────────────────────────────────────────────────────────
        if config.USE_MOCK_MODELS or self._model is None:
            mock_texts = {
                "ta": "AI இன்னும் தயாராகிக்கொண்டிருக்கிறது... சிறிது நேரத்தில் மீண்டும் முயலவும்.", 
                "hi": "AI अभी तैयार हो रहा है... कृपया कुछ सेकंड में पुनः प्रयास करें।",
                "en": "[AI Warming Up] Please wait a few seconds and try recording again.",
            }
            text = mock_texts.get(language_hint, mock_texts["en"])
            return TranscriptResult(text=text, language=language_hint, segments=[])

        # ── Real inference ─────────────────────────────────────────────────────
        # Whisper needs a file path, so write bytes to a temp file
        tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp_path = tmp.name
        try:
            tmp.write(audio_bytes)
            tmp.close()  # Close the file handle so Whisper can open it on Windows

            result = self._model.transcribe(
                tmp_path,
                language=language_hint,
                task="transcribe",
                word_timestamps=True,
            )
        finally:
            # On Windows, deletion might fail if process still holds a handle
            try:
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
            except Exception as e:
                logger.warning(f"Failed to delete temp file {tmp_path}: {e}")

        segments = [
            {
                "start": s.get("start", 0),
                "end": s.get("end", 0),
                "text": s.get("text", ""),
            }
            for s in result.get("segments", [])
        ]
        return TranscriptResult(
            text=result.get("text", "").strip(),
            language=result.get("language", language_hint),
            segments=segments,
        )


# ─── Module-level singleton ───────────────────────────────────────────────────
_engine = STTEngine()

LANG_CODE_MAP = {
    "tamil":   "ta",
    "hindi":   "hi",
    "english": "en",
}


def warmup():
    """Warm up the STT engine."""
    _engine.warmup()

def transcribe(audio_bytes: bytes, language: str = "tamil") -> TranscriptResult:
    """Convenience wrapper; accepts full language name or ISO code."""
    lang_code = LANG_CODE_MAP.get(language.lower(), language)
    return _engine.transcribe(audio_bytes, lang_code)
