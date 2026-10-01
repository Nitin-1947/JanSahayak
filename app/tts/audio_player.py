import sounddevice as sd
import soundfile as sf


class AudioPlayer:

    def play(
        self,
        audio_path: str
    ):

        data, sample_rate = sf.read(
            audio_path,
            dtype="float32"
        )

        sd.play(
            data,
            sample_rate
        )

        sd.wait()