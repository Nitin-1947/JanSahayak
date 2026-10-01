from pathlib import Path
import io
import wave

import numpy as np

from app.config import TTS_MODEL_DIR, TTS_VOICE, TTS_USE_CUDA, VOICE_SAMPLE_RATE


class TextToSpeech:
    """Hindi Piper TTS. Returns raw 8 kHz s16le mono PCM for Exotel."""

    def __init__(self, model_dir: Path = TTS_MODEL_DIR, voice: str = TTS_VOICE):
        try:
            from piper import PiperVoice
        except ImportError as exc:
            raise RuntimeError("Install piper-tts before starting the voice server.") from exc

        model_path = Path(model_dir) / f"{voice}.onnx"
        if not model_path.exists():
            raise FileNotFoundError(
                f"Piper Hindi voice not found: {model_path}. "
                "Run scripts\download_voice_models.py first."
            )

        self.voice = PiperVoice.load(str(model_path), use_cuda=TTS_USE_CUDA)

    def synthesize_wav(self, text: str) -> bytes:
        output = io.BytesIO()
        with wave.open(output, "wb") as wav_file:
            self.voice.synthesize_wav(text, wav_file)
        return output.getvalue()

    def synthesize_pcm(self, text: str) -> bytes:
        wav_bytes = self.synthesize_wav(text)
        with wave.open(io.BytesIO(wav_bytes), "rb") as wav_file:
            src_rate = wav_file.getframerate()
            channels = wav_file.getnchannels()
            width = wav_file.getsampwidth()
            frames = wav_file.readframes(wav_file.getnframes())

        if channels != 1 or width != 2:
            raise ValueError("Piper output must be 16-bit mono PCM.")

        audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32)
        if src_rate != VOICE_SAMPLE_RATE:
            target_len = max(1, round(len(audio) * VOICE_SAMPLE_RATE / src_rate))
            x_old = np.linspace(0.0, 1.0, num=len(audio), endpoint=False)
            x_new = np.linspace(0.0, 1.0, num=target_len, endpoint=False)
            audio = np.interp(x_new, x_old, audio)

        audio = np.clip(audio, -32768, 32767).astype(np.int16)
        return audio.tobytes()
