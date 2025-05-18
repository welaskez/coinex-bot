from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base
from .mixins import CreatedAtMixin, UuidPkMixin


class User(CreatedAtMixin, UuidPkMixin, Base):
    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    wallet_address: Mapped[str | None] = mapped_column(unique=True)
