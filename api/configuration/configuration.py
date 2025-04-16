from __future__ import annotations
from typing import *
from functools import cached_property
from api.shared.singleton import Singleton
from .variables import Variables
from . import environment
from .exceptions import ConfigurationValueError
from . import api
from . import database
from . import email


class Configuration(Singleton):
    _environment: environment.Environment
    api: api.Configuration
    email: email.Configuration
    database: database.Configuration

    def __init__(
        self,
        *,
        cli: environment.types.Environment | None = None,
        file: environment.types.Environment | None = None,
    ) -> None:
        self._environment = environment.Environment(
            {
                **environment.Environment.clean(file or {}),
                **environment.Environment.clean(cli or {}),
            }
        )
        self._environment.write_missing(
            {
                Variables.mode: "dev",
            }
        )
        self.api = api.Configuration(self, self._environment)
        self.database = database.Configuration(self, self._environment)
        self.email = email.Configuration(self, self._environment)

    @cached_property
    def mode(self) -> Literal["prod", "dev", "test"]:
        result = self._environment.get_string(Variables.mode)
        if result not in ["dev", "prod", "test"]:
            raise ConfigurationValueError()
        return cast(Literal["dev", "prod", "test"], result)
