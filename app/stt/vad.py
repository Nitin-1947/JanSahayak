import math
import struct

from app.config import VAD_RMS_THRESHOLD


class VoiceActivityDetector:
    """Simple energy VAD suitable for a first PSTN prototype."""

    def __init__(self, threshold: float = VAD_RMS_THRESHOLD):
        self.threshold = threshold

    def is_speech(self, pcm16: bytes) -> bool:
        if not pcm16:
            return False
        count = len(pcm16) // 2
        if count == 0:
            return False
        samples = struct.unpack(f"<{count}h", pcm16[: count * 2])
        rms = math.sqrt(sum(s * s for s in samples) / count)
        return rms >= self.threshold
