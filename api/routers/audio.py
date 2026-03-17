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
from pedagogy import emotion_responder

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/audio", tags=["Audio"])

def is_pronunciation_correct(transcript: str, expected: str) -> bool:
    """Simple fuzzy check for pronunciation accuracy."""
    import re
    def clean(s):
        return re.sub(r'[^\w\s]', '', s.lower()).strip()
    
    t_clean = clean(transcript)
    e_clean = clean(expected)
    
    if not e_clean: return True
    if e_clean in t_clean: return True
    
    # Overlap check for sentences
    t_words = set(t_clean.split())
    e_words = set(e_clean.split())
    if not e_words: return True
    
    overlap = len(t_words.intersection(e_words))
    # If more than 50% of words match, we call it 'correct' for a beginner
    return (overlap / len(e_words)) >= 0.5

@router.post("/analyze", response_model=EmotionResponse)
async def analyze_audio(
    file: UploadFile = File(..., description="WAV/audio file from the learner's mic"),
    language: str = Form(default="tamil"),
    expected_text: str = Form(default=""),
    session_id: int = Form(default=0),
    db: Session = Depends(get_db),
):
    """
    1. Load & preprocess audio bytes.
    2. Run emotion classification (with loudness bias).
    3. Run Whisper STT transcription.
    4. Check correctness & get creative feedback.
    5. Log to DB & return.
    """
    audio_bytes = await file.read()

    # ── Preprocess ──────────────────────────────────────────────────────────
    features = await anyio.to_thread.run_sync(audio_preprocessor.preprocess, audio_bytes)
    waveform = features["waveform"]
    sr = features["sample_rate"]
 
    # ── Emotion classification ───────────────────────────────────────────────
    emo_result = await anyio.to_thread.run_sync(emotion_engine.predict_emotion, waveform, sr)
    logger.info(f"Emotion: {emo_result.label} ({emo_result.confidence:.2f})")
 
    # ── STT transcription ────────────────────────────────────────────────────
    transcript_result = await anyio.to_thread.run_sync(stt_engine.transcribe, audio_bytes, language, expected_text)
    transcript = transcript_result.text
    logger.info(f"Transcript: {transcript[:60]}...")

    # ── Correctness & Feedback ───────────────────────────────────────────────
    is_correct = is_pronunciation_correct(transcript, expected_text)
    creative_feedback = emotion_responder.get_creative_feedback(language, is_correct)

    # ── Log to DB ────────────────────────────────────────────────────────────
    if session_id > 0:
        try:
            crud.log_emotion_event(
                db,
                session_id=session_id,
                emotion_label=emo_result.label,
                confidence=emo_result.confidence,
                transcript=transcript,
            )
        except Exception as exc:
            logger.warning(f"DB log failed: {exc}")

    return EmotionResponse(
        emotion_label=emo_result.label,
        confidence=emo_result.confidence,
        all_scores=emo_result.all_scores,
        transcript=transcript,
        is_correct=is_correct,
        creative_feedback=creative_feedback,
        language=transcript_result.language,
    )
