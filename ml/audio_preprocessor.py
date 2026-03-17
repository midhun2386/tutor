"""
Audio Preprocessor — Librosa-based feature extraction from raw audio bytes.

Converts WAV/audio bytes → numpy arrays of acoustic features used by both
the Emotion Engine (mel-spectrograms) and as a diagnostic layer.
"""
import io
import numpy as np
import librosa


# ─── Constants ────────────────────────────────────────────────────────────────
TARGET_SR = 16_000   # Wav2Vec2 & Whisper both expect 16 kHz mono
N_MELS = 64
HOP_LENGTH = 512
N_FFT = 1024


def load_audio(audio_bytes: bytes) -> tuple[np.ndarray, int]:
    """
    Load raw audio bytes into a mono, resampled numpy array.

    Parameters
    ----------
    audio_bytes : bytes
        Raw audio file content (WAV, OGG, MP3, etc.)

    Returns
    -------
    (waveform, sample_rate)
    """
    buf = io.BytesIO(audio_bytes)
    waveform, sr = librosa.load(buf, sr=TARGET_SR, mono=True)
    return waveform, sr


def extract_mel_spectrogram(waveform: np.ndarray, sr: int = TARGET_SR) -> np.ndarray:
    """Return a (n_mels, time) log-mel spectrogram array."""
    mel = librosa.feature.melspectrogram(
        y=waveform, sr=sr, n_mels=N_MELS, hop_length=HOP_LENGTH, n_fft=N_FFT
    )
    log_mel = librosa.power_to_db(mel, ref=np.max)
    return log_mel


def extract_mfcc(waveform: np.ndarray, sr: int = TARGET_SR, n_mfcc: int = 40) -> np.ndarray:
    """Return (n_mfcc, time) MFCC matrix."""
    return librosa.feature.mfcc(y=waveform, sr=sr, n_mfcc=n_mfcc)


def extract_pitch_features(waveform: np.ndarray, sr: int = TARGET_SR) -> dict:
    """
    Extract pitch (F0) statistics useful for detecting vocal tremors and anxiety.

    Returns dict with: mean_pitch, std_pitch, pitch_range
    """
    pitches, magnitudes = librosa.piptrack(y=waveform, sr=sr)
    # Only keep frames with significant energy
    pitch_vals = pitches[magnitudes > np.median(magnitudes)]
    pitch_vals = pitch_vals[pitch_vals > 0]

    if len(pitch_vals) == 0:
        return {"mean_pitch": 0.0, "std_pitch": 0.0, "pitch_range": 0.0}

    return {
        "mean_pitch": float(np.mean(pitch_vals)),
        "std_pitch": float(np.std(pitch_vals)),
        "pitch_range": float(np.max(pitch_vals) - np.min(pitch_vals)),
    }


def extract_pause_features(waveform: np.ndarray, sr: int = TARGET_SR) -> dict:
    """
    Detect silent pauses — a strong marker of hesitation and frustration.

    Returns dict with: pause_count, total_pause_duration_s
    """
    # Use top_db=20 to mark silence
    intervals = librosa.effects.split(waveform, top_db=20)
    total_duration = len(waveform) / sr
    speech_duration = sum((end - start) / sr for start, end in intervals)
    pause_duration = total_duration - speech_duration
    pause_count = max(0, len(intervals) - 1)

    return {
        "pause_count": pause_count,
        "total_pause_duration_s": round(pause_duration, 3),
    }


def preprocess(audio_bytes: bytes) -> dict:
    """
    Full preprocessing pipeline — returns a dict with waveform + features.
    This is the entry-point used by the emotion engine.
    """
    waveform, sr = load_audio(audio_bytes)
    return {
        "waveform": waveform,
        "sample_rate": sr,
        "mel_spectrogram": extract_mel_spectrogram(waveform, sr),
        "mfcc": extract_mfcc(waveform, sr),
        "pitch": extract_pitch_features(waveform, sr),
        "pauses": extract_pause_features(waveform, sr),
    }
