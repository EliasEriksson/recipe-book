import asyncio
from pathlib import Path

import click
import uvicorn

from api.configuration import Configuration
from api.configuration.environment.types import Environment

from ..database import Database
from .options import configuration_options

cli = click.Group("api")


@cli.command()
@configuration_options
def start(**environment: Environment) -> None:
    configuration = Configuration(cli=environment)
    print("Starting in mode:", configuration.mode)
    if not asyncio.run(Database(configuration).ready()):
        raise Exception(
            "Database models does not match database tables. Make a migration."
        )
    uvicorn.run(
        f"{Path(__file__).parent.parent.name}.gateway:gateway",
        port=configuration.api.port,
        log_level="info",
        reload=configuration.mode == "dev",
        proxy_headers=True,
    )
