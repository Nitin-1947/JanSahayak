import sqlite3

from app.config import (
    DATABASE_PATH,
    ensure_directories
)


def get_connection():

    ensure_directories()

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS citizen_profiles (

            user_id TEXT PRIMARY KEY,

            phone_number TEXT,

            name TEXT,

            age INTEGER,

            gender TEXT,

            state TEXT,

            district TEXT,

            residence_type TEXT,

            occupation TEXT,

            employment_status TEXT,

            income REAL,

            social_category TEXT,

            disability INTEGER,

            disability_percentage REAL,

            marital_status TEXT,

            education TEXT,

            student INTEGER,

            farmer INTEGER,

            family_size INTEGER,

            children_count INTEGER,

            minority_status INTEGER,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS conversations (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT,

            role TEXT,

            message TEXT,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS memories (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            user_id TEXT,

            memory_key TEXT,

            memory_value TEXT,

            created_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP,

            updated_at TIMESTAMP
                DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    connection.commit()

    connection.close()