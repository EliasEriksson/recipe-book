import litestar

from .controller import Controller

router = litestar.Router(
    path="/languages/",
    tags=["Languages"],
    route_handlers=[
        Controller,
    ],
)
