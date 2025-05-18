from typing import Generic, Type, TypeVar
from uuid import UUID

from core.models import Base
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T", bound=Base)

S = TypeVar("S", bound=BaseModel)


class BaseCRUD(Generic[T]):
    model: Type[T]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, schema: S) -> T:
        model = self.model(**schema.model_dump())

        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)

        return model

    async def get_by_id(self, model_id: UUID | str) -> T:
        return await self.session.get(self.model, model_id)

    async def get_all(self) -> list[T]:
        return list(await self.session.scalars(select(self.model)))

    async def update(self, model: T, schema: S) -> T:
        for k, v in schema.model_dump(exclude_unset=True).items():
            setattr(model, k, v)

        await self.session.commit()
        await self.session.refresh(model)

        return model

    async def delete(self, model: T) -> None:
        await self.session.delete(model)
        await self.session.commit()
