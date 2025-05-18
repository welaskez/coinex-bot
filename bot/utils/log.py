import logging

from core.config import settings


def setup_logging(level: int) -> None:
    logging.basicConfig(
        level=level,
        format=settings.log.format,
        handlers=[logging.StreamHandler()],
    )
