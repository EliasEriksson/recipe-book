from typing import *
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy import delete
from .. import models
from api import schemas


class Languages:
    _session: AsyncSession
    model: Type[models.Language]

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.model = models.Language

    async def list(self) -> Sequence[models.Language]:
        async with self._session.begin():
            query = select(self.model)
            result = await self._session.execute(query)
        return result.scalars().all()

    async def fetch_by_id(self, id: UUID) -> models.Language | None:
        async with self._session.begin():
            query = select(self.model).where(models.Language.id == id)
            result = await self._session.execute(query)
        return result.scalars().one_or_none()

    async def create(self, language: models.language.CreateProtocol) -> models.Language:
        async with self._session.begin():
            result = self.model.create(language)
            self._session.add(result)
        return result

    async def update(
        self, id: UUID, language: schemas.language.LanguageProtocol
    ) -> models.Language:
        result = await self.fetch_by_id(id)
        async with self._session.begin():
            result.update(language)
        return result

    async def delete_by_id(self, id: UUID) -> bool:
        async with self._session.begin():
            query = delete(self.model).where(self.model.id == id)
            result = await self._session.execute(query)
        return cast(int, result.rowcount) > 0
