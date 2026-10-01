from dataclasses import dataclass
from typing import Optional


@dataclass
class CitizenProfile:

    user_id: str

    name: Optional[str] = None

    age: Optional[int] = None

    gender: Optional[str] = None

    state: Optional[str] = None

    district: Optional[str] = None

    residence_type: Optional[str] = None

    occupation: Optional[str] = None

    employment_status: Optional[str] = None

    income: Optional[float] = None

    social_category: Optional[str] = None

    disability: Optional[bool] = None

    disability_percentage: Optional[float] = None

    marital_status: Optional[str] = None

    education: Optional[str] = None

    student: Optional[bool] = None

    farmer: Optional[bool] = None

    family_size: Optional[int] = None

    children_count: Optional[int] = None

    minority_status: Optional[bool] = None

    phone_number: Optional[str] = None