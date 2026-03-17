# Verbacular AI Tutor 📖

Python-native emotive vernacular AI tutor for foundational literacy.

## Setup

1.  **Clone or Copy** this directory.
2.  **Create a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\\Scripts\\activate
    ```
3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure Environment**:
    Copy `.env.example` to `.env` and add your `HF_TOKEN`.
    If you don't have a GPU or token, set `USE_MOCK_MODELS=1` in `config.py` or `.env`.

## Running the App

Run the unified starter script:
```bash
python run.py
```

- **Frontend**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

## Architecture
- **Frontend**: Streamlit (Retro-vintage aesthetic)
- **Backend**: FastAPI
- **Intelligence**: 
  - Wav2Vec2 (Emotion Detection)
  - Whisper (STT)
  - TinyLlama (Lesson Generation)
- **Database**: SQLite / SQLAlchemy
