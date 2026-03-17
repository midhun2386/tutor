"""
Audio router — receives raw audio, returns emotion + transcript.
POST /audio/analyze
"""
import logging
from fastapi import APIRouter, UploadFile, File, Form, Depends
import anyio
from sqlalchemy.orm import Session

from api.schemas import EmotionResponse
from database.database import get_db
from database import crud
from ml import audio_preprocessor, emotion_engine, stt_engine

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/audio", tags=["Audio"])


@router.post("/analyze", response_model=EmotionResponse)
async def analyze_audio(
    file: UploadFile = File(..., description="WAV/audio file from the learner's mic"),
    language: str = Form(default="tamil"),
    session_id: int = Form(default=0),
    db: Session = Depends(get_db),
):
    """
    1. Load & preprocess audio bytes (librosa).
    2. Run Wav2Vec2 emotion classification.
    3. Run Whisper STT transcription.
    4. Log the emotion event to the DB (if session_id > 0).
    5. Return EmotionResponse.
    """
    audio_bytes = await file.read()

    # ── Preprocess ──────────────────────────────────────────────────────────
    # Offload CPU-heavy librosa/preprocessing to a threadpool
    features = await anyio.to_thread.run_sync(audio_preprocessor.preprocess, audio_bytes)
    waveform = features["waveform"]
    sr = features["sample_rate"]
 
    # ── Emotion classification ───────────────────────────────────────────────
    # Offload Wav2Vec2 inference
    emo_result = await anyio.to_thread.run_sync(emotion_engine.predict_emotion, waveform, sr)
    logger.info(f"Emotion: {emo_result.label} ({emo_result.confidence:.2f})")
 
    # ── STT transcription ────────────────────────────────────────────────────
    # Offload Whisper inference (heavy)
    transcript_result = await anyio.to_thread.run_sync(stt_engine.transcribe, audio_bytes, language)
    logger.info(f"Transcript: {transcript_result.text[:60]}...")

    # ── Log to DB ────────────────────────────────────────────────────────────
    if session_id > 0:
        try:
            crud.log_emotion_event(
                db,
                session_id=session_id,
                emotion_label=emo_result.label,
                confidence=emo_result.confidence,
                transcript=transcript_result.text,
            )
        except Exception as exc:
            logger.warning(f"DB log failed: {exc}")

    return EmotionResponse(
        emotion_label=emo_result.label,
        confidence=emo_result.confidence,
        all_scores=emo_result.all_scores,
        transcript=transcript_result.text,
        language=transcript_result.language,
    )
