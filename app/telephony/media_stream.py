class MediaStream:
    def receive_audio(self):
        raise NotImplementedError

    def send_audio(self, audio):
        raise NotImplementedError
