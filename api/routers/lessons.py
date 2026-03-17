"""
Lesson router — generates adaptive lessons based on student state + emotion.
POST /lessons/generate
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import anyio

from api.schemas import LessonRequest, LessonResponse
from database.database import get_db
from database import crud
from ml import llm_engine

router = APIRouter(prefix="/lessons", tags=["Lessons"])


@router.post("/generate", response_model=LessonResponse)
async def generate_lesson(req: LessonRequest, db: Session = Depends(get_db)):
    """
    Computes the student's current mastery level from the DB, then
    calls the LLM engine to generate a contextually appropriate lesson.
    """
    # Compute average mastery across all phonemes for this student
    progress_records = crud.get_phoneme_progress(db, req.student_id)
    if progress_records:
        avg_mastery = sum(r.mastery_score for r in progress_records) / len(progress_records)
        mastery_level = int(avg_mastery * 10)  # scale to 0-10
    else:
        mastery_level = req.mastery_level  # fallback from request

    # Offload heavy LLM generation to a thread pool
    # run_sync only takes positional args for the function. We use req.proficiency_level as a positional arg.
    lesson = await anyio.to_thread.run_sync(
        llm_engine.generate_lesson,
        req.language,
        req.emotion,
        mastery_level,
        req.proficiency_level
    )

    return LessonResponse(
        lesson_text=lesson.lesson_text,
        hint=lesson.hint,
        exercise_type=lesson.exercise_type,
        syllables=lesson.syllables,
    )
