import json
import re


class ProfileExtractor:

    PROFILE_FIELDS = {
        "name",
        "age",
        "gender",
        "state",
        "district",
        "residence_type",
        "occupation",
        "employment_status",
        "income",
        "social_category",
        "disability",
        "disability_percentage",
        "marital_status",
        "education",
        "student",
        "farmer",
        "family_size",
        "children_count",
        "minority_status",
    }

    def extract_basic(
        self,
        text: str
    ) -> dict:

        result = {}

        age_match = re.search(
            r"\b(\d{1,3})\s*(?:साल|वर्ष|years?|yrs?)\b",
            text,
            re.IGNORECASE
        )

        if age_match:
            result["age"] = int(
                age_match.group(1)
            )

        lower = text.lower()

        if (
            "महिला" in text
            or "female" in lower
            or "औरत" in text
        ):
            result["gender"] = "female"

        elif (
            "पुरुष" in text
            or "male" in lower
            or "आदमी" in text
        ):
            result["gender"] = "male"

        if "किसान" in text:
            result["farmer"] = True
            result["occupation"] = "farmer"

        if "छात्र" in text or "student" in lower:
            result["student"] = True
            result["occupation"] = "student"

        if "दिव्यांग" in text:
            result["disability"] = True

        return result