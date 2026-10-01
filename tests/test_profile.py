from app.profile.profile_extractor import (
    ProfileExtractor
)


def test_profile_extraction():

    extractor = ProfileExtractor()

    result = extractor.extract_basic(
        "मैं 35 साल का किसान हूँ"
    )

    assert result["age"] == 35
    assert result["farmer"] is True