import sounddevice as sd
import soundfile as sf

from app.config import (
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS
)


class Microphone:

    def record(
        self,
        output_path: str,
        seconds: int = 5
    ):

        print(
            "Recording..."
        )

        audio = sd.rec(
            int(
                seconds
                * AUDIO_SAMPLE_RATE
            ),
            samplerate=AUDIO_SAMPLE_RATE,
            channels=AUDIO_CHANNELS,
            dtype="float32"
        )

        sd.wait()

        sf.write(
            output_path,
            audio,
            AUDIO_SAMPLE_RATE
        )

        print(
            "Recording saved."
        )