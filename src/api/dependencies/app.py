from logging.config import dictConfig

from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Container,
    Resource,
)
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from esdbclient import EventStoreDBClient

from api.dependencies.eventbus import EventBus
from api.dependencies.pools import Pools
from api.meals.infrastructure.repos.meals import Meals


class AppContainer(DeclarativeContainer):
    config = Configuration()

    logging = Resource(dictConfig, config=config.logging)

    eventbus_client = Resource(
        EventStoreDBClient,
        uri=config.dsn.eventstoredb.uri,
    )

    broker = Resource(
        RabbitmqBroker, url=config.dsn.rabbitmq.url
    )

    eventbus = Container(
        EventBus,
        config=config,
        client=eventbus_client,
    )

    pools = Container(Pools, config=config)

    meals = Container(Meals, pool=pools.timescale_db)
