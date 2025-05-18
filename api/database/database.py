from sqlalchemy import text
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
            echo=True,
        )
        self._session_maker = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
        )

    # TODO this ready function should compare the models against the live database
    # async def ready(self) -> bool:
    #     script = alembic.script.ScriptDirectory.from_config(
    #         alembic.config.Config("alembic.ini")
    #     )
    #     async with self._engine.begin() as connection:
    #         revision = await connection.run_sync(
    #             lambda connection: alembic.runtime.migration.MigrationContext.configure(
    #                 connection
    #             ).get_current_revision()
    #         )
    #         return revision == script.get_current_head()

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
