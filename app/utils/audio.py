def validate_audio_file(
    path: str
):

    return path.lower().endswith(
        (
            ".wav",
            ".mp3",
            ".flac",
            ".ogg"
        )
    )