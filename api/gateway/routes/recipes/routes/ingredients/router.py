import litestar
from .controller import Controller

router = litestar.Router(
    path="/ingredients/",
    route_handlers=[
        Controller,
    ],
)
