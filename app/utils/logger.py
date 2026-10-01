import logging
from app.config import LOG_LEVEL


def get_logger(name: str):
    logger = logging.getLogger(name)

    if not logger.handlers:
        handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.setLevel(
            getattr(logging, LOG_LEVEL.upper(), logging.INFO)
        )

    return logger