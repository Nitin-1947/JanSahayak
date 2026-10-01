from app.profile.profile_model import CitizenProfile
from app.schemes.scheme_model import (
    Scheme,
    SchemeEligibility
)
from app.schemes.eligibility_engine import (
    EligibilityEngine
)


def test_age_eligibility():

    profile = CitizenProfile(
        user_id="test",
        age=25
    )

    scheme = Scheme(
        scheme_id="test",
        name="Test Scheme",
        level="central",
        state=None,
        department="Test",
        description="Test",
        benefits=[],
        eligibility=SchemeEligibility(
            age_min=18,
            age_max=60
        ),
        documents=[],
        application_steps=[],
        application_url=None,
        official_source_url=None,
        last_verified=None
    )

    result = EligibilityEngine().evaluate(
        profile,
        scheme
    )

    assert result.status == "eligible"