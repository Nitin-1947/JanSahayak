from app.memory.database import get_connection


def save_message(
    user_id: str,
    role: str,
    message: str
):

    connection = get_connection()

    connection.execute(
        """
        INSERT INTO conversations
        (
            user_id,
            role,
            message
        )
        VALUES (?, ?, ?)
        """,
        (
            user_id,
            role,
            message
        )
    )

    connection.commit()
    connection.close()


def get_recent_messages(
    user_id: str,
    limit: int = 10
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT role, message
        FROM conversations
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """,
        (
            user_id,
            limit
        )
    )

    rows = cursor.fetchall()

    connection.close()

    rows.reverse()

    return [
        {
            "role": row["role"],
            "content": row["message"]
        }
        for row in rows
    ]