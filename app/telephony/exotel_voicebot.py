import asyncio
import base64
import json
import logging
import time
from typing import Optional

import numpy as np

from app.config import (
    VOICE_SAMPLE_RATE,
    VOICE_CHUNK_MS,
    STT_SAMPLE_RATE,
    VAD_SILENCE_MS,
    VAD_MIN_SPEECH_MS,
)
from app.stt.speech_to_text import SpeechToText
from app.stt.vad import VoiceActivityDetector
from app.tts.text_to_speech import TextToSpeech

logger = logging.getLogger("jansahayak-exotel")


def upsample_8k_to_16k(pcm8: bytes) -> bytes:
    if not pcm8:
        return b""
    samples = np.frombuffer(pcm8, dtype=np.int16).astype(np.float32)
    if len(samples) < 2:
        return pcm8
    x_old = np.arange(len(samples), dtype=np.float32)
    x_new = np.linspace(0, len(samples) - 1, len(samples) * 2, dtype=np.float32)
    out = np.interp(x_new, x_old, samples)
    return np.clip(out, -32768, 32767).astype(np.int16).tobytes()


class ExotelVoicebotSession:
    def __init__(self, websocket, manager):
        self.websocket = websocket
        self.manager = manager
        self.stream_sid: Optional[str] = None
        self.user_id: Optional[str] = None
        self.stt = SpeechToText()
        self.tts = TextToSpeech()
        self.vad = VoiceActivityDetector()
        self.speech_ms = 0
        self.silence_ms = 0
        self.turn_audio = bytearray()
        self.processing = False

    async def send_pcm(self, pcm: bytes):
        if not self.stream_sid or not pcm:
            return
        chunk_bytes = int(VOICE_SAMPLE_RATE * VOICE_CHUNK_MS / 1000) * 2
        chunk_bytes = max(3200, chunk_bytes)
        chunk_bytes -= chunk_bytes % 320
        for offset in range(0, len(pcm), chunk_bytes):
            chunk = pcm[offset: offset + chunk_bytes]
            if len(chunk) < 320:
                chunk += b"\x00" * (320 - len(chunk))
            payload = base64.b64encode(chunk).decode("ascii")
            await self.websocket.send_text(json.dumps({
                "event": "media",
                "stream_sid": self.stream_sid,
                "media": {"payload": payload},
            }))
            await asyncio.sleep(len(chunk) / 2 / VOICE_SAMPLE_RATE)

    async def say(self, text: str):
        logger.info("AI: %s", text)
        pcm = await asyncio.to_thread(self.tts.synthesize_pcm, text)
        await self.send_pcm(pcm)

    async def handle_media(self, payload: str):
        try:
            pcm8 = base64.b64decode(payload)
        except Exception:
            logger.warning("Invalid media payload")
            return

        chunk_ms = max(20, int(len(pcm8) / 2 / VOICE_SAMPLE_RATE * 1000))
        is_speech = self.vad.is_speech(pcm8)
        pcm16 = upsample_8k_to_16k(pcm8)
        self.stt.accept_audio(pcm16)

        if is_speech:
            self.speech_ms += chunk_ms
            self.silence_ms = 0
            self.turn_audio.extend(pcm8)
        elif self.speech_ms:
            self.silence_ms += chunk_ms
            self.turn_audio.extend(pcm8)

        if (
            not self.processing
            and self.speech_ms >= VAD_MIN_SPEECH_MS
            and self.silence_ms >= VAD_SILENCE_MS
        ):
            self.processing = True
            audio_seen = bytes(self.turn_audio)
            self.turn_audio.clear()
            self.speech_ms = 0
            self.silence_ms = 0
            try:
                text = self.stt.final_text()
                if text:
                    logger.info("Caller: %s", text)
                    response = await asyncio.to_thread(
                        self.manager.process, self.user_id, text
                    )
                    await self.say(response)
                else:
                    logger.info("No speech recognized")
            except Exception:
                logger.exception("Turn processing failed")
                await self.say("माफ कीजिए, अभी मुझे आपकी बात समझने में दिक्कत हुई। कृपया दोबारा बोलिए।")
            finally:
                self.processing = False

    async def run(self):
        await self.websocket.accept()
        logger.info("Exotel WebSocket connected")

        try:
            while True:
                message = await self.websocket.receive_text()
                data = json.loads(message)
                event = data.get("event")

                if event == "connected":
                    logger.info("Exotel connection established")

                elif event == "start":
                    start = data.get("start", {})
                    self.stream_sid = start.get("stream_sid") or data.get("stream_sid")
                    caller = (
                        start.get("custom_parameters", {}).get("phone_number")
                        or start.get("phone_number")
                    )
                    self.user_id = await asyncio.to_thread(
                        self.manager.create_user, caller
                    )
                    await self.say(
                        "नमस्ते! मैं जनसहायक हूँ। मैं सरकारी योजनाओं और नागरिक सेवाओं की जानकारी में आपकी मदद कर सकता हूँ। आप हिंदी या हिंग्लिश में बोल सकते हैं।"
                    )

                elif event == "media":
                    await self.handle_media(
                        data.get("media", {}).get("payload", "")
                    )

                elif event == "dtmf":
                    logger.info("DTMF: %s", data.get("dtmf"))

                elif event == "stop":
                    logger.info("Exotel stream stopped")
                    break

                elif event == "clear":
                    logger.info("Exotel requested audio clear")

        except Exception:
            logger.exception("Voicebot WebSocket error")
        finally:
            logger.info("Voice session ended")
