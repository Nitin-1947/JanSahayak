from pathlib import Path
import shutil
import subprocess
import sys
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
STT_DIR = ROOT / "models" / "stt"
TTS_DIR = ROOT / "models" / "tts"
STT_MODEL = "vosk-model-small-hi-0.22"
STT_URL = "https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip"
TTS_VOICE = "hi_IN-pratham-medium"


def download_stt():
    target = STT_DIR / STT_MODEL
    if target.exists():
        print(f"STT model already exists: {target}")
        return
    STT_DIR.mkdir(parents=True, exist_ok=True)
    archive = STT_DIR / f"{STT_MODEL}.zip"
    print("Downloading Hindi Vosk STT model...")
    urllib.request.urlretrieve(STT_URL, archive)
    print("Extracting STT model...")
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(STT_DIR)
    archive.unlink(missing_ok=True)


def download_tts():
    TTS_DIR.mkdir(parents=True, exist_ok=True)
    model = TTS_DIR / f"{TTS_VOICE}.onnx"
    config = TTS_DIR / f"{TTS_VOICE}.onnx.json"
    if model.exists() and config.exists():
        print(f"TTS voice already exists: {model}")
        return
    print("Downloading Hindi Piper TTS voice...")
    subprocess.run(
        [sys.executable, "-m", "piper.download_voices", "--data-dir", str(TTS_DIR), TTS_VOICE],
        cwd=ROOT,
        check=True,
    )


if __name__ == "__main__":
    download_stt()
    download_tts()
    print("\nVoice models are ready.")
