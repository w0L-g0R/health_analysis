from logging.config import dictConfig

from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Container,
    Resource,
    Singleton,
)
from esdbclient import EventStoreDBClient

# from container.clients import EventBusClient
from container.eventbus import EventBus
from container.pools import Pools


class AppContainer(DeclarativeContainer):
    config = Configuration()

    logging = Resource(dictConfig, config=config.logging)

    # client = Container(EventBusClient, config=config)

    client = Singleton(
        EventStoreDBClient,
        uri=config.dsn.eventstoredb.uri,
    )

    eventbus = Container(
        EventBus,
        config=config,
        client=client,
    )

    pools = Container(Pools, config=config)

    # event_handler =


# class MealsRepository:
#     def __init__(self, pool: SimpleConnectionPool):
#         self.pool = pool
#         if pool:
#             print("Connection pool created successfully")

#     # def insert(self):


# class MealsContainer(DeclarativeContainer):
#     pool = Dependency(
#         instance_of=SimpleConnectionPool
#     )

#     repository = Singleton(
#         MealsRepository, pool=pool
#     )

#     # core = Container(Core, config=config)

#     pools = Container(Pools, config=config)

#     pass
#     pass
