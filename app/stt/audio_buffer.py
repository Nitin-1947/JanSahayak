class AudioBuffer:
    def __init__(self):
        self.chunks: list[bytes] = []

    def add(self, chunk: bytes):
        self.chunks.append(chunk)

    def clear(self):
        self.chunks.clear()

    def get(self) -> bytes:
        return b"".join(self.chunks)

    def __len__(self):
        return sum(len(c) for c in self.chunks)
