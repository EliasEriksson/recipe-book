import litestar
from .controller import Controller
from . import routes


router = litestar.Router(
    path="/recipes/",
    route_handlers=[
        Controller,
        routes.router,
    ],
)
