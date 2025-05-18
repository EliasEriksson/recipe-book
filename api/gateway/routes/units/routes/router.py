import litestar

router = litestar.Router(
    path="/{unit_id:uuid}/",
    route_handlers=[],
)
