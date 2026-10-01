from typing import Optional

from app.profile.profile_model import CitizenProfile
from app.memory.database import get_connection


class ProfileManager:

    def create_profile(
        self,
        user_id: str,
        phone_number: Optional[str] = None
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT OR IGNORE INTO citizen_profiles
            (
                user_id,
                phone_number
            )
            VALUES (?, ?)
            """,
            (
                user_id,
                phone_number
            )
        )

        connection.commit()
        connection.close()

    def update_profile(
        self,
        user_id: str,
        **fields
    ):

        allowed_fields = {
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

        fields = {
            key: value
            for key, value in fields.items()
            if key in allowed_fields
            and value is not None
        }

        if not fields:
            return

        connection = get_connection()

        cursor = connection.cursor()

        assignments = ", ".join(
            f"{key} = ?"
            for key in fields
        )

        values = list(fields.values())

        values.append(user_id)

        cursor.execute(
            f"""
            UPDATE citizen_profiles
            SET {assignments},
                updated_at = CURRENT_TIMESTAMP
            WHERE user_id = ?
            """,
            values
        )

        connection.commit()
        connection.close()

    def get_profile(
        self,
        user_id: str
    ) -> Optional[CitizenProfile]:

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT *
            FROM citizen_profiles
            WHERE user_id = ?
            """,
            (user_id,)
        )

        row = cursor.fetchone()

        connection.close()

        if not row:
            return None

        return CitizenProfile(
            user_id=row["user_id"],
            name=row["name"],
            age=row["age"],
            gender=row["gender"],
            state=row["state"],
            district=row["district"],
            residence_type=row["residence_type"],
            occupation=row["occupation"],
            employment_status=row["employment_status"],
            income=row["income"],
            social_category=row["social_category"],
            disability=(
                bool(row["disability"])
                if row["disability"] is not None
                else None
            ),
            disability_percentage=row[
                "disability_percentage"
            ],
            marital_status=row["marital_status"],
            education=row["education"],
            student=(
                bool(row["student"])
                if row["student"] is not None
                else None
            ),
            farmer=(
                bool(row["farmer"])
                if row["farmer"] is not None
                else None
            ),
            family_size=row["family_size"],
            children_count=row["children_count"],
            minority_status=(
                bool(row["minority_status"])
                if row["minority_status"] is not None
                else None
            ),
            phone_number=row["phone_number"],
        )

    def missing_fields(
        self,
        user_id: str
    ):

        profile = self.get_profile(user_id)

        if not profile:
            return []

        fields = [
            "age",
            "gender",
            "state",
            "district",
            "occupation",
            "income",
            "social_category",
            "disability",
            "residence_type",
        ]

        return [
            field
            for field in fields
            if getattr(profile, field) is None
        ]