from pathlib import Path
import sys
import wave

PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.tts.text_to_speech import TextToSpeech

OUTPUT_DIR = PROJECT_ROOT / "audio" / "outgoing"
OUTPUT_FILE = OUTPUT_DIR / "test_hindi.wav"

SAMPLE_RATE = 22050
CHANNELS = 1
SAMPLE_WIDTH = 2


def save_pcm_as_wav(pcm_data: bytes, output_file: Path):
    output_file.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with wave.open(str(output_file), "wb") as wav_file:
        wav_file.setnchannels(CHANNELS)
        wav_file.setsampwidth(SAMPLE_WIDTH)
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(pcm_data)


def main():
    print("JanSahayak Hindi TTS Test")
    print("-" * 40)

    text = (
        "नमस्ते! मैं जनसहायक हूँ। "
        "मैं आपकी सरकारी योजनाओं और नागरिक सेवाओं "
        "से जुड़ी जानकारी में सहायता कर सकता हूँ।"
    )

    print("Text:")
    print(text)
    print()

    print("Loading TTS model...")

    tts = TextToSpeech()

    print("TTS model loaded.")
    print()

    print("Generating Hindi speech...")

    pcm_data = tts.synthesize_pcm(text)

    if not pcm_data:
        raise RuntimeError("TTS returned empty audio.")

    print(f"Generated PCM audio: {len(pcm_data):,} bytes")

    save_pcm_as_wav(
        pcm_data,
        OUTPUT_FILE
    )

    print()
    print("TTS generation completed.")
    print(f"Audio file: {OUTPUT_FILE}")
    print()
    print("Audio format:")
    print("  Sample rate : 22050 Hz")
    print("  Channels    : Mono")
    print("  Bit depth   : 16-bit PCM")
    print("  Format      : WAV")


if __name__ == "__main__":
    main()
