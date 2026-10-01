from app.memory.database import (
    initialize_database
)


def test_database():

    initialize_database()

    assert True