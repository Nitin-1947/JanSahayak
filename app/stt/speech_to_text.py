import json
from pathlib import Path

from app.config import STT_MODEL_DIR, STT_SAMPLE_RATE


class SpeechToText:
    """Streaming Hindi STT using the lightweight Vosk Hindi model."""

    def __init__(self, model_dir: Path = STT_MODEL_DIR):
        try:
            from vosk import Model, KaldiRecognizer
        except ImportError as exc:
            raise RuntimeError("Install vosk before starting the voice server.") from exc

        if not Path(model_dir).exists():
            raise FileNotFoundError(
                f"Hindi STT model not found: {model_dir}. "
                "Run scripts\download_voice_models.py first."
            )

        self._KaldiRecognizer = KaldiRecognizer
        self.model = Model(str(model_dir))
        self.recognizer = self._new_recognizer()

    def _new_recognizer(self):
        return self._KaldiRecognizer(self.model, STT_SAMPLE_RATE)

    def accept_audio(self, pcm16_16k: bytes) -> bool:
        return self.recognizer.AcceptWaveform(pcm16_16k)

    def partial_text(self) -> str:
        try:
            data = json.loads(self.recognizer.PartialResult())
            return data.get("partial", "").strip()
        except Exception:
            return ""

    def final_text(self) -> str:
        try:
            data = json.loads(self.recognizer.FinalResult())
            return data.get("text", "").strip()
        finally:
            self.recognizer = self._new_recognizer()
