import litestar

from .controller import Controller

router = litestar.Router(
    path="/ingredients/",
    tags=["RecipeIngredients"],
    route_handlers=[
        Controller,
    ],
)
