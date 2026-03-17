"""
CRUD helpers for all database models.
"""
import datetime
from sqlalchemy.orm import Session
from database import models
from pedagogy.student_model import update_mastery_probability


# ─── Student ──────────────────────────────────────────────────────────────────

def create_student(db: Session, name: str, language: str = "tamil", proficiency_level: str = "Beginner") -> models.Student:
    student = models.Student(name=name, language=language, proficiency_level=proficiency_level)
    db.add(student)
    db.commit()
    db.refresh(student)
    return student


def get_student(db: Session, student_id: int) -> models.Student | None:
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def get_all_students(db: Session) -> list[models.Student]:
    return db.query(models.Student).all()


# ─── Session ──────────────────────────────────────────────────────────────────

def start_session(db: Session, student_id: int) -> models.SessionLog:
    session = models.SessionLog(student_id=student_id)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def end_session(db: Session, session_id: int, average_emotion: str) -> models.SessionLog | None:
    session = db.query(models.SessionLog).filter(models.SessionLog.id == session_id).first()
    if session:
        session.ended_at = datetime.datetime.utcnow()
        session.average_emotion = average_emotion
        db.commit()
        db.refresh(session)
    return session


# ─── Emotion Event ────────────────────────────────────────────────────────────

def log_emotion_event(
    db: Session,
    session_id: int,
    emotion_label: str,
    confidence: float,
    transcript: str | None = None,
) -> models.EmotionEvent:
    event = models.EmotionEvent(
        session_id=session_id,
        emotion_label=emotion_label,
        confidence=confidence,
        transcript=transcript,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


# ─── Phoneme Progress ─────────────────────────────────────────────────────────

def upsert_phoneme_progress(
    db: Session,
    student_id: int,
    phoneme: str,
    correct: bool,
) -> models.PhonemeProgress:
    record = (
        db.query(models.PhonemeProgress)
        .filter(
            models.PhonemeProgress.student_id == student_id,
            models.PhonemeProgress.phoneme == phoneme,
        )
        .first()
    )
    if record is None:
        record = models.PhonemeProgress(student_id=student_id, phoneme=phoneme)
        db.add(record)

    record.attempt_count += 1
    if not correct:
        record.error_count += 1
    
    # Use Bayesian Knowledge Tracing (BKT) for better mastery estimation
    record.mastery_score = update_mastery_probability(
        current_p=record.mastery_score,
        correct=correct
    )
    
    record.last_seen = datetime.datetime.utcnow()
    db.commit()
    db.refresh(record)
    return record


def get_phoneme_progress(db: Session, student_id: int) -> list[models.PhonemeProgress]:
    return (
        db.query(models.PhonemeProgress)
        .filter(models.PhonemeProgress.student_id == student_id)
        .all()
    )
