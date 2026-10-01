def detect_language(text: str) -> str:

    hindi_chars = 0
    latin_chars = 0

    for char in text:

        if "\u0900" <= char <= "\u097F":
            hindi_chars += 1

        elif char.isalpha():
            latin_chars += 1

    if hindi_chars > latin_chars:
        return "hi"

    if latin_chars > 0:
        return "hinglish"

    return "unknown"