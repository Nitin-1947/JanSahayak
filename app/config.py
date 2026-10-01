import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

APP_NAME = os.getenv("APP_NAME", "JanSahayak")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
LANGUAGE = os.getenv("LANGUAGE", "hi")
DEFAULT_STATE = os.getenv("DEFAULT_STATE", "Madhya Pradesh")
DATABASE_PATH = BASE_DIR / os.getenv("DATABASE_PATH", "data/app.db")

# Exotel Voicebot uses 8 kHz, mono, 16-bit PCM by default.
VOICE_SAMPLE_RATE = int(os.getenv("VOICE_SAMPLE_RATE", "8000"))
VOICE_CHANNELS = int(os.getenv("VOICE_CHANNELS", "1"))
VOICE_SAMPLE_WIDTH = 2
VOICE_CHUNK_MS = int(os.getenv("VOICE_CHUNK_MS", "100"))

# STT/VAD
STT_MODEL_DIR = BASE_DIR / os.getenv("STT_MODEL_DIR", "models/stt/vosk-model-small-hi-0.22")
STT_SAMPLE_RATE = int(os.getenv("STT_SAMPLE_RATE", "16000"))
VAD_RMS_THRESHOLD = float(os.getenv("VAD_RMS_THRESHOLD", "450"))
VAD_SILENCE_MS = int(os.getenv("VAD_SILENCE_MS", "800"))
VAD_MIN_SPEECH_MS = int(os.getenv("VAD_MIN_SPEECH_MS", "350"))

# TTS
TTS_MODEL_DIR = BASE_DIR / os.getenv("TTS_MODEL_DIR", "models/tts")
TTS_VOICE = os.getenv("TTS_VOICE", "hi_IN-pratham-medium")
TTS_USE_CUDA = os.getenv("TTS_USE_CUDA", "false").lower() == "true"

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
DATA_DIR = BASE_DIR / "data"
SCHEMES_DIR = DATA_DIR / "schemes"
KNOWLEDGE_DIR = DATA_DIR / "knowledge"
AUDIO_DIR = BASE_DIR / "audio"
INCOMING_AUDIO_DIR = AUDIO_DIR / "incoming"
PROCESSED_AUDIO_DIR = AUDIO_DIR / "processed"
OUTGOING_AUDIO_DIR = AUDIO_DIR / "outgoing"

def ensure_directories():
    for directory in [DATA_DIR, SCHEMES_DIR, KNOWLEDGE_DIR, INCOMING_AUDIO_DIR, PROCESSED_AUDIO_DIR, OUTGOING_AUDIO_DIR, STT_MODEL_DIR.parent, TTS_MODEL_DIR]:
        directory.mkdir(parents=True, exist_ok=True)
