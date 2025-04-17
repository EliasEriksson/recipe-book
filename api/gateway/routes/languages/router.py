import litestar
from .controller import Controller


router = litestar.Router(
    path="/languages/",
    tags=["languages"],
    route_handlers=[
        Controller,
    ],
)
