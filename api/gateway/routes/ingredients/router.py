import litestar

from .controller import Controller

router = litestar.Router(
    path="/ingredients/",
    tags=["Ingredients"],
    route_handlers=[
        Controller,
    ],
)
