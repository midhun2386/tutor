"""
FastAPI application entry-point.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import threading

from database.database import init_db
from api.routers import audio, lessons, student
from ml import emotion_engine, stt_engine, llm_engine

logging.basicConfig(level=logging.INFO, format="%(levelname)s | %(name)s | %(message)s")

app = FastAPI(
    title="Vernacular AI Literacy Tutor API",
    description="Backend for emotion-aware adaptive literacy tutoring.",
    version="1.0.0",
)

MODELS_READY = False

# Allow Streamlit (localhost:8501) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(audio.router)
app.include_router(lessons.router)
app.include_router(student.router)

def warmup_models():
    global MODELS_READY
    logging.info("Warming up ML engines in background...")
    try:
        emotion_engine.warmup()
        stt_engine.warmup()
        llm_engine.warmup()
        MODELS_READY = True
        logging.info("All ML engines ready.")
    except Exception as e:
        logging.error(f"Warmup failed: {e}")

@app.on_event("startup")
def on_startup():
    init_db()
    logging.info("Database initialised.")
    # Start warmup in a separate thread so the server can start immediately
    threading.Thread(target=warmup_models, daemon=True).start()

@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "ok" if MODELS_READY else "loading",
        "service": "Vernacular AI Literacy Tutor API",
        "models_ready": MODELS_READY
    }

@app.get("/", tags=["Health"])
def root():
    return {"message": "Vernacular AI Tutor API is running"}
