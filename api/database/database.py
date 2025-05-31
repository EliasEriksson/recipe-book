import asyncio

from alembic.autogenerate import compare_metadata
from alembic.migration import MigrationContext
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from api.configuration import Configuration

from . import models
from .client import Client


class Database:
    _configuration: Configuration
    _engine: AsyncEngine
    _session_maker: async_sessionmaker[AsyncSession]
    _session: AsyncSession | None

    def __init__(self, configuration: Configuration | None = None) -> None:
        self._configuration = (
            configuration if configuration is not None else Configuration()
        )
        self._engine = create_async_engine(
            self._configuration.database.url,
            # echo=True,
        )
        self._session_maker = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
        )

    async def ready(self) -> bool:
        engine = await asyncio.to_thread(
            lambda: create_engine(self._configuration.database.url)
        )
        connection = await asyncio.to_thread(lambda: engine.connect())
        context = await asyncio.to_thread(
            lambda: MigrationContext.configure(connection)
        )
        diffs = await asyncio.to_thread(
            lambda: compare_metadata(context, models.base.Base.metadata)
        )
        return len(diffs) == 0

    async def delete(self) -> None:
        async with self._engine.begin() as connection:
            await connection.run_sync(models.base.Base.metadata.drop_all)
            drop_alembic = text(f"DROP TABLE IF EXISTS alembic_version;")
            await connection.execute(drop_alembic)

        migrations = self._configuration.database.migrations
        if migrations.exists():
            for content in migrations.iterdir():
                if content.is_file():
                    content.unlink()

    async def __aenter__(self) -> Client:
        self._session = await self._session_maker(bind=self._engine).__aenter__()
        return Client(self._session)

    async def __aexit__(self, *args, **kwargs) -> None:
        if self._session:
            await self._session.__aexit__(*args, **kwargs)

    async def dispose(self) -> None:
        await self._engine.dispose()
