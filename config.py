"""
Central configuration for the Vernacular AI Literacy Tutor.
All settings are read from environment variables (with defaults).
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ─── Paths ────────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent

# ─── Database ─────────────────────────────────────────────────────────────────
DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'tutor.db'}")

# ─── API ──────────────────────────────────────────────────────────────────────
API_BASE_URL: str = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")
API_HOST: str = "127.0.0.1"
API_PORT: int = 8000

# ─── ML Models ────────────────────────────────────────────────────────────────
WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "small")
EMOTION_MODEL: str = os.getenv(
    "EMOTION_MODEL",
    "ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition",
)
LLM_MODEL: str = os.getenv("LLM_MODEL", "meta-llama/Llama-3.2-1B-Instruct")
HF_TOKEN: str | None = os.getenv("HF_TOKEN", None)

# ─── Feature Flags ────────────────────────────────────────────────────────────
USE_MOCK_MODELS: bool = os.getenv("USE_MOCK_MODELS", "0") == "1"

# ─── Default Language ─────────────────────────────────────────────────────────
DEFAULT_LANGUAGE: str = os.getenv("DEFAULT_LANGUAGE", "tamil")
SUPPORTED_LANGUAGES: list[str] = ["tamil", "hindi", "english"]

# ─── Emotion Labels ────────────────────────────────────────────────────────────
EMOTION_LABELS: list[str] = ["Confident", "Hesitant", "Frustrated", "Anxious"]

# ─── Pedagogical Thresholds ────────────────────────────────────────────────────
FRUSTRATION_THRESHOLD: float = 0.55   # confidence above this triggers de-escalation
MASTERY_THRESHOLD: float = 0.80       # phoneme mastery score to advance difficulty
