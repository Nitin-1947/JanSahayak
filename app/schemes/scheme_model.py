from dataclasses import dataclass, field
from typing import Optional


@dataclass
class SchemeEligibility:

    age_min: Optional[int] = None
    age_max: Optional[int] = None

    genders: list[str] = field(
        default_factory=list
    )

    occupations: list[str] = field(
        default_factory=list
    )

    income_max: Optional[float] = None

    income_min: Optional[float] = None

    categories: list[str] = field(
        default_factory=list
    )

    residence_types: list[str] = field(
        default_factory=list
    )

    disability_required: Optional[bool] = None

    farmer_required: Optional[bool] = None

    student_required: Optional[bool] = None

    marital_statuses: list[str] = field(
        default_factory=list
    )


@dataclass
class Scheme:

    scheme_id: str

    name: str

    level: str

    state: Optional[str]

    department: Optional[str]

    description: str

    benefits: list[str]

    eligibility: SchemeEligibility

    documents: list[str]

    application_steps: list[str]

    application_url: Optional[str]

    official_source_url: Optional[str]

    last_verified: Optional[str]