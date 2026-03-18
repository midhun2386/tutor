"""
Pydantic schemas for FastAPI request/response validation.
"""
from __future__ import annotations
from pydantic import BaseModel, Field


# ─── Audio ────────────────────────────────────────────────────────────────────

class EmotionResponse(BaseModel):
    emotion_label: str
    confidence: float
    all_scores: dict[str, float]
    transcript: str
    is_correct: bool = False
    creative_feedback: str = ""
    language: str


# ─── Lesson ───────────────────────────────────────────────────────────────────

class LessonRequest(BaseModel):
    student_id: int
    language: str = "tamil"
    emotion: str = "Confident"
    mastery_level: int = Field(default=3, ge=0, le=10)
    proficiency_level: str = "Beginner"
    excluded_texts: list[str] = []


class LessonResponse(BaseModel):
    lesson_text: str
    hint: str
    exercise_type: str
    syllables: list[str] = []
    target_word: str = ""
    phoneme: str = ""


# ─── Student ──────────────────────────────────────────────────────────────────

class StudentCreate(BaseModel):
    name: str
    language: str = "tamil"
    proficiency_level: str = "Beginner"


class StudentOut(BaseModel):
    id: int
    name: str
    language: str
    proficiency_level: str

    class Config:
        from_attributes = True


class PhonemeProgressOut(BaseModel):
    phoneme: str
    mastery_score: float
    attempt_count: int
    error_count: int

    class Config:
        from_attributes = True


class StudentDetailOut(StudentOut):
    phoneme_progress: list[PhonemeProgressOut] = []


class PhonemeUpdateRequest(BaseModel):
    phoneme: str
    correct: bool


# ─── Session ──────────────────────────────────────────────────────────────────

class SessionStartResponse(BaseModel):
    session_id: int
    student_id: int


class SessionEndRequest(BaseModel):
    session_id: int
    student_id: int
    average_emotion: str = "Confident"
