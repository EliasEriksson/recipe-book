import litestar
from .controller import Controller
from . import routes


router = litestar.Router(
    path="/recipes/",
    tags=["recipes"],
    route_handlers=[
        Controller,
        routes.router,
    ],
)
