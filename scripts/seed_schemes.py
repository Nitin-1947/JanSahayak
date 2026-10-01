from app.config import ensure_directories
from app.schemes.scheme_repository import (
    SchemeRepository
)
from app.config import SCHEMES_DIR


def main():

    ensure_directories()

    repository = SchemeRepository(
        SCHEMES_DIR
    )

    schemes = repository.load_all()

    print(
        f"Loaded {len(schemes)} schemes."
    )


if __name__ == "__main__":
    main()