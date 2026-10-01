def clean_response(text: str) -> str:
    if not text:
        return "माफ कीजिए, मुझे कोई उत्तर नहीं मिला।"

    text = text.strip()

    return text