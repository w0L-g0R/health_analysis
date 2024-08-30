from logging import basicConfig
from logging.config import dictConfig
from pathlib import Path

import toml
from dependency_injector import providers
from dependency_injector.containers import (
    DeclarativeContainer,
)

from logger import get_logging_config_from


class Core(DeclarativeContainer):
    config_file = Path(__file__).parents[1] / "config.toml"

    config = providers.Configuration()

    logging = providers.Resource(
        basicConfig,
    )

    @classmethod
    def get_config_dict_from_toml_file(cls):
        with open(cls.config_file, "r") as file:
            data = toml.load(file)
            return data

    @classmethod
    def setup(cls):
        toml_data = cls.get_config_dict_from_toml_file()

        cls.config.from_dict(toml_data)

        cls.logging = providers.Resource(
            dictConfig,
            config=get_logging_config_from(toml_data),
        )

        print("cls.config: ", cls.config.databases)
