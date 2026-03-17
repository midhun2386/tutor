"""
Student router — student CRUD, session management, and phoneme progress updates.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.schemas import (
    StudentCreate, StudentOut, StudentDetailOut,
    PhonemeProgressOut, PhonemeUpdateRequest,
    SessionStartResponse, SessionEndRequest,
)
from database.database import get_db
from database import crud

router = APIRouter(prefix="/student", tags=["Student"])


# ─── Students ─────────────────────────────────────────────────────────────────

@router.post("/", response_model=StudentOut, status_code=201)
def create_student(body: StudentCreate, db: Session = Depends(get_db)):
    student = crud.create_student(db, name=body.name, language=body.language)
    return student


@router.get("/", response_model=list[StudentOut])
def list_students(db: Session = Depends(get_db)):
    return crud.get_all_students(db)


@router.get("/{student_id}", response_model=StudentDetailOut)
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    progress = crud.get_phoneme_progress(db, student_id)
    return StudentDetailOut(
        id=student.id,
        name=student.name,
        language=student.language,
        phoneme_progress=[
            PhonemeProgressOut(
                phoneme=p.phoneme,
                mastery_score=round(p.mastery_score, 3),
                attempt_count=p.attempt_count,
                error_count=p.error_count,
            )
            for p in progress
        ],
    )


# ─── Phoneme Progress ─────────────────────────────────────────────────────────

@router.post("/{student_id}/progress", response_model=PhonemeProgressOut)
def update_progress(
    student_id: int,
    body: PhonemeUpdateRequest,
    db: Session = Depends(get_db),
):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    record = crud.upsert_phoneme_progress(db, student_id, body.phoneme, body.correct)
    return PhonemeProgressOut(
        phoneme=record.phoneme,
        mastery_score=round(record.mastery_score, 3),
        attempt_count=record.attempt_count,
        error_count=record.error_count,
    )


# ─── Sessions ─────────────────────────────────────────────────────────────────

@router.post("/{student_id}/session/start", response_model=SessionStartResponse)
def start_session(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    session = crud.start_session(db, student_id)
    return SessionStartResponse(session_id=session.id, student_id=student_id)


@router.post("/session/end")
def end_session(body: SessionEndRequest, db: Session = Depends(get_db)):
    crud.end_session(db, body.session_id, body.average_emotion)
    return {"status": "ok"}
