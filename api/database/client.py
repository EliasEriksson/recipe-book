from sqlalchemy.ext.asyncio import AsyncSession, AsyncSessionTransaction

from .operations import Ingredients, Languages, Recipes, Units


class Client:
    _session: AsyncSession
    languages: Languages
    recipes: Recipes
    units: Units
    ingredients: Ingredients

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self.languages = Languages(session)
        self.recipes = Recipes(session)
        self.units = Units(session)
        self.ingredients = Ingredients(session)

    async def refresh(self, *args, **kwargs):
        await self._session.refresh(*args, **kwargs)

    def transaction(self) -> AsyncSessionTransaction:
        return self._session.begin()
