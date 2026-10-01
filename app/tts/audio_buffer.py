class AudioBuffer:
    def __init__(self):
        self.audio = b""

    def set(self, audio: bytes):
        self.audio = audio

    def get(self) -> bytes:
        return self.audio

    def clear(self):
        self.audio = b""
