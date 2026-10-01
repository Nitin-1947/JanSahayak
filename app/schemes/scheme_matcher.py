from app.profile.profile_model import CitizenProfile
from app.schemes.scheme_repository import (
    SchemeRepository
)
from app.schemes.eligibility_engine import (
    EligibilityEngine,
    EligibilityResult
)


class SchemeMatcher:

    def __init__(
        self,
        repository: SchemeRepository
    ):
        self.repository = repository
        self.engine = EligibilityEngine()

    def find_matches(
        self,
        profile: CitizenProfile
    ) -> list[EligibilityResult]:

        schemes = self.repository.load_all()

        results = []

        for scheme in schemes:

            result = self.engine.evaluate(
                profile,
                scheme
            )

            if result.status != "not_eligible":
                results.append(result)

        # Sort: eligible first, then possibly_eligible
        results.sort(
            key=lambda r: (
                0 if r.status == "eligible" else 1
            )
        )

        return results