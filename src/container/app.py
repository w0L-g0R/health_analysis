from logging.config import dictConfig

from dependency_injector import providers
from dependency_injector.containers import (
    DeclarativeContainer,
)

from container.pools import Pools

LOGGING_DICT = {
    "version": 1,
    "formatters": {
        "formatter": {
            "format": "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "formatter",
            "stream": "ext://sys.stderr",
        }
    },
    "root": {"level": "DEBUG", "handlers": ["console"]},
}


class AppContainer(DeclarativeContainer):
    config = providers.Configuration()

    logging = providers.Resource(
        dictConfig, config=config.logging
    )

    # core = providers.Container(Core, config=config)
    pools = providers.Container(Pools, config=config)


# class MealsRepository:
#     def __init__(self, pool: SimpleConnectionPool):
#         self.pool = pool
#         if pool:
#             print("Connection pool created successfully")

#     # def insert(self):


# class MealsContainer(DeclarativeContainer):
#     pool = providers.Dependency(
#         instance_of=SimpleConnectionPool
#     )

#     repository = providers.Singleton(
#         MealsRepository, pool=pool
#     )

#     # core = providers.Container(Core, config=config)

#     pools = providers.Container(Pools, config=config)

#     pass
