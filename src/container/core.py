from logging.config import dictConfig

from dependency_injector import providers
from dependency_injector.containers import (
    DeclarativeContainer,
)


class Core(DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        dictConfig, config=config.logging
    )
