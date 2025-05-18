from core.models import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import BaseCRUD


class UserCRUD(BaseCRUD[User]):
    model = User

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session)

    async def get_by_tg_id(self, tg_id: int) -> User | None:
        return await self.session.scalar(select(User).where(User.tg_id == tg_id))
