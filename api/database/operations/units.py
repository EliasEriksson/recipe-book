from datetime import datetime
from typing import *
from uuid import UUID

from sqlalchemy import ColumnElement, delete, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import QueryableAttribute, aliased, selectinload

from api import schemas
from api.database.page_result import PageResult

from .. import models
from ..operator import Operator


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


# noinspection DuplicatedCode
class Units:
    _session: AsyncSession
    _operator: Operator

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._operator = Operator(session)

    async def list(
        self,
        language_code: str | None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> PageResult[Result]:
        if language_code is None:
            translation = aliased(
                models.UnitTranslation,
                select(
                    models.UnitTranslation,
                    func.min(models.UnitTranslation.created),
                )
                .distinct(models.UnitTranslation.unit_id)
                .group_by(
                    models.UnitTranslation.unit_id,
                    models.UnitTranslation.language_id,
                )
                .subquery("translation"),
                flat=True,
            )
            query = (
                select(translation, models.Unit)
                .order_by(desc(cast(ColumnElement, translation.created)))
                .options(selectinload(cast(QueryableAttribute, translation.unit)))
            )
        else:
            query = (
                select(models.UnitTranslation)
                .join(models.Language)
                .where(models.Language.code == language_code)
                .order_by(desc(models.UnitTranslation.created))
                .options(selectinload(models.UnitTranslation.unit))
            )
        query = query.join(models.Unit)
        return await self._operator.list(
            query,
            lambda result: Result(result.unit, result),
            limit,
            offset,
        )

    async def fetch_by_id(self, id: UUID, language_id: UUID) -> Result:
        query = (
            select(models.UnitTranslation)
            .where(models.UnitTranslation.unit_id == id)
            .where(models.UnitTranslation.language_id == language_id)
            .join(models.Unit)
            .options(selectinload(models.UnitTranslation.unit))
        )
        return await self._operator.fetch(
            query, lambda result: Result(result.unit, result)
        )

    async def create(self, data: schemas.unit.CreateProtocol) -> Result:
        unit = models.Unit.create(data)
        async with self._session.begin():
            self._session.add(unit)
            await self._session.flush()
            translation = models.UnitTranslation.create(unit, data)
            self._session.add(translation)
        return Result(unit, translation)

    async def update(self, id: UUID, data: schemas.unit.UnitProtocol) -> Result:
        query = (
            select(models.Unit)
            .join(models.UnitTranslation)
            .where(models.Unit.id == id)
            .options(selectinload(models.Unit.translations))
        )
        async with self._session.begin():
            unit = await self._operator.execute_scalars_first(self._session, query)
            for translation in unit.translations:
                if translation.language_id == data.language_id:
                    translation.update(data)
                    break
            else:
                translation = models.UnitTranslation.create(unit, data)
                self._session.add(translation)
                unit.translations.append(translation)
            unit.update(data)
        return Result(unit, translation)

    async def delete(self, id: UUID) -> bool:
        query = delete(models.Unit).where(models.Unit.id == id)
        return await self._operator.delete(query)

    async def delete_translation(self, id: UUID, language_id: UUID) -> bool:
        query = (
            delete(models.UnitTranslation)
            .where(models.UnitTranslation.unit_id == id)
            .where(models.UnitTranslation.language_id == language_id)
        )
        return await self._operator.delete(query)
