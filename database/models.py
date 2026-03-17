"""
SQLAlchemy models for the Vernacular AI Literacy Tutor.
Tables: Student, SessionLog, PhonemeProgress, EmotionEvent
"""
import datetime
from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    language = Column(String(40), default="tamil")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    sessions = relationship("SessionLog", back_populates="student", cascade="all, delete")
    phoneme_progress = relationship("PhonemeProgress", back_populates="student", cascade="all, delete")


class SessionLog(Base):
    __tablename__ = "session_logs"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)
    average_emotion = Column(String(40), nullable=True)
    notes = Column(Text, nullable=True)

    student = relationship("Student", back_populates="sessions")
    emotion_events = relationship("EmotionEvent", back_populates="session", cascade="all, delete")


class PhonemeProgress(Base):
    __tablename__ = "phoneme_progress"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    phoneme = Column(String(20), nullable=False)          # e.g. "ka", "pa", "aa"
    mastery_score = Column(Float, default=0.0)            # 0.0 – 1.0
    attempt_count = Column(Integer, default=0)
    error_count = Column(Integer, default=0)
    last_seen = Column(DateTime, default=datetime.datetime.utcnow)

    student = relationship("Student", back_populates="phoneme_progress")


class EmotionEvent(Base):
    __tablename__ = "emotion_events"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("session_logs.id"), nullable=False)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow)
    emotion_label = Column(String(40), nullable=False)    # Confident / Hesitant / Frustrated / Anxious
    confidence = Column(Float, default=0.0)
    transcript = Column(Text, nullable=True)

    session = relationship("SessionLog", back_populates="emotion_events")
