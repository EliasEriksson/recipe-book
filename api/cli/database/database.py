import asyncio

import click
from alembic import command

from api.cli.options import configuration_options
from api.configuration import Configuration
from api.configuration.environment.types import Environment
from api.database import Database

from .seed import seed_database

cli = click.Group("database")


@cli.command()
@configuration_options
def delete(**environment: Environment) -> None:
    configuration = Configuration(cli=environment)
    message = (
        f"This operation will delete all tables related to this "
        f"application from the database '{configuration.database.name}'.\n"
        f"OBS! This operation is irreversible.\n"
        f"Are you sure you want to continue? (y/n): "
    )
    if input(message).lower() == "y":
        print("Proceeding...")
        database = Database(configuration)
        asyncio.run(database.delete())
        print("Database deleted.")
    else:
        print("Aborted.")


@cli.command()
@configuration_options
def ready(**environment: Environment) -> None:
    configuration = Configuration(cli=environment)
    if asyncio.run(Database(configuration).ready()):
        print(
            f"Tables in the database does reflect the database models! \033[32m✓\033[0m"
        )
    else:
        print(
            f"Tables in the database does not reflect the database models. \033[31m✗\033[0m"
        )


@cli.command()
@configuration_options
def seed(**environment: Environment) -> None:
    Configuration(cli=environment)
    asyncio.run(seed_database())


@cli.command()
@click.option("--message", "-m", type=str, help="Revision message", default=None)
@configuration_options
def revision(message: str | None, **environment: Environment) -> None:
    configuration = Configuration(cli=environment)
    command.revision(
        configuration.database.alembic,
        autogenerate=True,
        message=message,
    )


@cli.command()
@configuration_options
def migrate(**environment: Environment) -> None:
    configuration = Configuration(cli=environment)
    for content in configuration.database.migrations.iterdir():
        if content.is_file():
            break
    else:
        command.revision(
            configuration.database.alembic,
            "Initializing database.",
            autogenerate=True,
        )
    command.upgrade(configuration.database.alembic, "head")


@cli.command()
@click.argument("revision", type=str)
@configuration_options
def upgrade(revision: str, **environment: Environment) -> None:
    configuration = Configuration(cli=environment)
    command.upgrade(configuration.database.alembic, revision)


@cli.command()
@click.argument("revision", type=str, required=True)
@configuration_options
def downgrade(revision: str, **environment: Environment) -> None:
    configuration = Configuration(cli=environment)
    command.downgrade(configuration.database.alembic, revision)


@cli.command()
@configuration_options
def heads(**environment: Environment) -> None:
    configuration = Configuration(cli=environment)
    command.heads(configuration.database.alembic)


@cli.command()
@configuration_options
def check(**environment: Environment) -> None:
    configuration = Configuration(cli=environment)
    command.check(configuration.database.alembic)


@cli.command()
@configuration_options
def branches(**environment: Environment) -> None:
    configuration = Configuration(cli=environment)
    command.branches(configuration.database.alembic)


@cli.command()
@configuration_options
def current(**environment: Environment) -> None:
    configuration = Configuration(cli=environment)
    command.current(configuration.database.alembic)


@cli.command()
@configuration_options
def ensure_version(**environment: Environment) -> None:
    configuration = Configuration(cli=environment)
    command.ensure_version(configuration.database.alembic)


@cli.command()
@click.argument("revision", type=str, required=True)
@configuration_options
def show(revision: str, **environment: Environment) -> None:
    configuration = Configuration(cli=environment)
    command.show(configuration.database.alembic, revision)


@cli.command()
@click.argument("revision", type=str, required=True)
@configuration_options
def stamp(revision: str, **environment: Environment) -> None:
    configuration = Configuration(cli=environment)
    command.stamp(configuration.database.alembic, revision)
