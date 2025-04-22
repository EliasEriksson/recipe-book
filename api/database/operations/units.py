from datetime import datetime
from uuid import UUID

from sqlalchemy import delete, desc, func, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from api import schemas
from api.database.page_result import PageResult

from .. import models
from ..operator import Operator
from .languages import Languages


class Result:
    unit: models.Unit
    translation: models.UnitTranslation

    def __init__(self, unit: models.Unit, translation: models.UnitTranslation) -> None:
        self.unit = unit
        self.translation = translation

    @property
    def modified(self) -> datetime:
        return (
            self.unit.modified
            if self.unit.modified > self.translation.modified
            else self.translation.modified
        )


class Units:
    _session: AsyncSession
    _languages: Languages
    _operator: Operator

    def __init__(self, session: AsyncSession, languages: Languages) -> None:
        self._session = session
        self._operator = Operator(session)
        self._languages = languages

    def list(
        self,
        language_code: str | None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PageResult[Result]:
        pass

    async def fetch_by_id(self, id: UUID, language_id: UUID) -> Result:
        pass

    async def create(self, creatable: schemas.unit.CreateProtocol) -> Result:
        pass

    async def update(self, id: UUID, data: schemas.recipe.RecipeProtocol) -> Result:
        pass

    async def delete(self, id: UUID) -> bool:
        pass

    async def delete_translation(self, id: UUID, language_id: UUID) -> bool:
        pass
