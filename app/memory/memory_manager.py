from app.memory.database import get_connection


class MemoryManager:

    def save(
        self,
        user_id: str,
        key: str,
        value: str
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT id
            FROM memories
            WHERE user_id = ?
            AND memory_key = ?
            """,
            (
                user_id,
                key
            )
        )

        existing = cursor.fetchone()

        if existing:

            cursor.execute(
                """
                UPDATE memories
                SET memory_value = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    value,
                    existing["id"]
                )
            )

        else:

            cursor.execute(
                """
                INSERT INTO memories
                (
                    user_id,
                    memory_key,
                    memory_value
                )
                VALUES (?, ?, ?)
                """,
                (
                    user_id,
                    key,
                    value
                )
            )

        connection.commit()
        connection.close()

    def get_all(
        self,
        user_id: str
    ):

        connection = get_connection()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT memory_key, memory_value
            FROM memories
            WHERE user_id = ?
            """,
            (user_id,)
        )

        rows = cursor.fetchall()

        connection.close()

        return {
            row["memory_key"]:
                row["memory_value"]
            for row in rows
        }

    def delete(
        self,
        user_id: str,
        key: str
    ):

        connection = get_connection()

        connection.execute(
            """
            DELETE FROM memories
            WHERE user_id = ?
            AND memory_key = ?
            """,
            (
                user_id,
                key
            )
        )

        connection.commit()
        connection.close()