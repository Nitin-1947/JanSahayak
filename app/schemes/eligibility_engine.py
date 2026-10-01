from app.profile.profile_model import CitizenProfile
from app.schemes.scheme_model import Scheme


class EligibilityResult:

    def __init__(
        self,
        scheme: Scheme,
        status: str,
        reasons: list[str],
        missing: list[str]
    ):
        self.scheme = scheme
        self.status = status
        self.reasons = reasons
        self.missing = missing


class EligibilityEngine:

    def evaluate(
        self,
        profile: CitizenProfile,
        scheme: Scheme
    ) -> EligibilityResult:

        rules = scheme.eligibility

        reasons = []
        missing = []

        # Age
        if rules.age_min is not None:

            if profile.age is None:
                missing.append("age")

            elif profile.age < rules.age_min:
                return EligibilityResult(
                    scheme,
                    "not_eligible",
                    [
                        f"Minimum age is {rules.age_min}"
                    ],
                    []
                )

        if rules.age_max is not None:

            if profile.age is None:
                missing.append("age")

            elif profile.age > rules.age_max:
                return EligibilityResult(
                    scheme,
                    "not_eligible",
                    [
                        f"Maximum age is {rules.age_max}"
                    ],
                    []
                )

        # Gender
        if rules.genders:

            if profile.gender is None:
                missing.append("gender")

            elif (
                "all" not in rules.genders
                and profile.gender not in rules.genders
            ):
                return EligibilityResult(
                    scheme,
                    "not_eligible",
                    ["Gender criteria do not match"],
                    []
                )

        # Occupation
        if rules.occupations:

            if profile.occupation is None:
                missing.append("occupation")

            elif profile.occupation not in rules.occupations:
                return EligibilityResult(
                    scheme,
                    "not_eligible",
                    ["Occupation criteria do not match"],
                    []
                )

        # Income
        if rules.income_max is not None:

            if profile.income is None:
                missing.append("income")

            elif profile.income > rules.income_max:
                return EligibilityResult(
                    scheme,
                    "not_eligible",
                    ["Income is above the scheme limit"],
                    []
                )

        # Social category
        if rules.categories:

            if profile.social_category is None:
                missing.append("social_category")

            elif profile.social_category not in rules.categories:
                return EligibilityResult(
                    scheme,
                    "not_eligible",
                    ["Social category does not match"],
                    []
                )

        # Residence
        if rules.residence_types:

            if profile.residence_type is None:
                missing.append("residence_type")

            elif profile.residence_type not in rules.residence_types:
                return EligibilityResult(
                    scheme,
                    "not_eligible",
                    ["Residence criteria do not match"],
                    []
                )

        # Disability
        if rules.disability_required is not None:

            if profile.disability is None:
                missing.append("disability")

            elif (
                profile.disability
                != rules.disability_required
            ):
                return EligibilityResult(
                    scheme,
                    "not_eligible",
                    ["Disability criteria do not match"],
                    []
                )

        # Farmer
        if rules.farmer_required is not None:

            if profile.farmer is None:
                missing.append("farmer")

            elif profile.farmer != rules.farmer_required:
                return EligibilityResult(
                    scheme,
                    "not_eligible",
                    ["Farmer criteria do not match"],
                    []
                )

        # Student
        if rules.student_required is not None:

            if profile.student is None:
                missing.append("student")

            elif profile.student != rules.student_required:
                return EligibilityResult(
                    scheme,
                    "not_eligible",
                    ["Student criteria do not match"],
                    []
                )

        if missing:

            return EligibilityResult(
                scheme,
                "possibly_eligible",
                reasons,
                missing
            )

        return EligibilityResult(
            scheme,
            "eligible",
            [
                "All available eligibility rules matched"
            ],
            []
        )