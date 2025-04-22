import subprocess
import sys

import click

from api.configuration import Configuration
from api.configuration.environment.types import Environment
from api.configuration.variables import Variables

from . import api, database, ui
from .options import configuration_options

cli = click.Group()
cli.add_command(api.cli)
cli.add_command(ui.cli)
cli.add_command(database.cli)


@cli.command()
@configuration_options
def test(**environment: Environment):
    configuration = Configuration(
        cli={
            **{
                variable: value
                for variable, value in environment.items()
                if value is not None
            },
            Variables.mode: "test",
        },
    )
    print("Starting in mode:", configuration.mode)
    return_code = subprocess.call(["pytest", "--asyncio-mode", "auto", "api/tests"])
    sys.exit(return_code)
