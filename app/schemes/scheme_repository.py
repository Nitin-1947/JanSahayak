import json
from pathlib import Path

from app.schemes.scheme_model import (
    Scheme,
    SchemeEligibility
)


class SchemeRepository:

    def __init__(self, directory: Path):
        self.directory = directory

    def load_all(self) -> list[Scheme]:

        schemes = []

        for file in self.directory.rglob("*.json"):

            try:

                with open(
                    file,
                    "r",
                    encoding="utf-8"
                ) as f:

                    data = json.load(f)

                if isinstance(data, list):
                    records = data
                else:
                    records = [data]

                for item in records:
                    schemes.append(
                        self._convert(item)
                    )

            except Exception as exc:
                print(
                    f"Could not load {file}: {exc}"
                )

        return schemes

    def _convert(
        self,
        data: dict
    ) -> Scheme:

        eligibility_data = data.get(
            "eligibility",
            {}
        )

        eligibility = SchemeEligibility(
            age_min=eligibility_data.get(
                "age_min"
            ),
            age_max=eligibility_data.get(
                "age_max"
            ),
            genders=eligibility_data.get(
                "genders",
                []
            ),
            occupations=eligibility_data.get(
                "occupations",
                []
            ),
            income_max=eligibility_data.get(
                "income_max"
            ),
            income_min=eligibility_data.get(
                "income_min"
            ),
            categories=eligibility_data.get(
                "categories",
                []
            ),
            residence_types=eligibility_data.get(
                "residence_types",
                []
            ),
            disability_required=eligibility_data.get(
                "disability_required"
            ),
            farmer_required=eligibility_data.get(
                "farmer_required"
            ),
            student_required=eligibility_data.get(
                "student_required"
            ),
            marital_statuses=eligibility_data.get(
                "marital_statuses",
                []
            ),
        )

        return Scheme(
            scheme_id=data["scheme_id"],
            name=data["name"],
            level=data["level"],
            state=data.get("state"),
            department=data.get("department"),
            description=data.get(
                "description",
                ""
            ),
            benefits=data.get(
                "benefits",
                []
            ),
            eligibility=eligibility,
            documents=data.get(
                "documents",
                []
            ),
            application_steps=data.get(
                "application_steps",
                []
            ),
            application_url=data.get(
                "application_url"
            ),
            official_source_url=data.get(
                "official_source_url"
            ),
            last_verified=data.get(
                "last_verified"
            )
        )