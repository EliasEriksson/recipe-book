import litestar

from . import ingredients, languages, recipes, units

router = litestar.Router(
    path="/",
    route_handlers=[
        recipes.router,
        units.router,
        languages.router,
        ingredients.router,
    ],
)
