SENSITIVE_FIELDS = {
    "aadhaar_number",
    "otp",
    "pin",
    "password",
    "bank_password",
    "cvv"
}


def is_sensitive_field(
    field: str
):

    return (
        field.lower()
        in SENSITIVE_FIELDS
    )