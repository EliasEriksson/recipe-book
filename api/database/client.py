from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import AsyncSessionTransaction
from .operations import Languages
from .operations import Recipes


class Client:
    _session: AsyncSession
    languages: Languages
    recipes: Recipes

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.languages = Languages(session)
        self.recipes = Recipes(session, self.languages)

    async def refresh(self, *args, **kwargs):
        await self._session.refresh(*args, **kwargs)

    def transaction(self) -> AsyncSessionTransaction:
        return self._session.begin()
