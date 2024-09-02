from logging.config import dictConfig

from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Factory,
)

from dependency_injector.providers import Configuration, Container, Resource
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from esdbclient import EventStoreDBClient

from api.meals.bootstrap import MealsContainer
from api.meals.repository import MealsRepository
from dependencies.eventbus import EventBusContainer
from dependencies.pools import init_async_timescale_db_pool


class AppContainer(DeclarativeContainer):
    config = Configuration()

    logging = Resource(dictConfig, config=config.logging)

    eventbus_client = Resource(
        EventStoreDBClient,
        uri=config.dsn.eventstoredb.uri,
    )

    broker = Resource(RabbitmqBroker, url=config.dsn.rabbitmq.url)

    eventbus = Resource(
        EventBusContainer,
        config=config,
        client=eventbus_client,
    )

    timescale_db_pool = Factory(init_async_timescale_db_pool, config=config)

    meals_repository = Resource(MealsRepository, pool=timescale_db_pool)

    meals_container = Container(
        MealsContainer,
        broker=broker,
        repository=meals_repository,
        config=config,
    )
