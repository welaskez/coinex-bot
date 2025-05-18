from typing import Generic, Type, TypeVar
from uuid import UUID

from core.models import Base
from crud.base import BaseCRUD
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=Base)

S = TypeVar("S", bound=BaseModel)


class BaseService(Generic[T]):
    def __init__(self, session: AsyncSession, crud_class: Type[BaseCRUD[T]]) -> None:
        self.session = session
        self.crud = crud_class(session)

    async def create(self, schema: S) -> T:
        return await self.crud.create(schema)

    async def get_by_id(self, model_id: UUID | str) -> T | None:
        return await self.crud.get_by_id(model_id)

    async def get_all(self) -> list[T]:
        return await self.crud.get_all()

    async def update(self, model: T, schema: S) -> T:
        return await self.crud.update(model, schema)

    async def delete(self, model: T) -> None:
        await self.crud.delete(model)
