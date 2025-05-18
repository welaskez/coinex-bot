__all__ = ("publish_usdt_rub_price",)

import logging
import sys

from core.config import settings

from .post_rate import publish_usdt_rub_price

if sys.argv[0] == "worker":
    logging.basicConfig(level=settings.log.level, format=settings.log.format)
