from logging.config import dictConfig

from dependencies.database import TimeScaleDatabase, init_async_timescale_db_pool
from dependencies.eventbus import EventBusContainer
from dependencies.meals import MealsContainer
from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import Configuration, Container, Resource, Singleton
from esdbclient import EventStoreDBClient
from taskiq_aio_pika import AioPikaBroker


class AppContainer(DeclarativeContainer):
    config = Configuration()

    logging = Resource(dictConfig, config=config.logging)

    # eventbus_client = Resource(
    #     EventStoreDBClient,
    #     uri=config.dsn.eventstoredb.uri,
    # )

    # eventbus = Resource(
    #     EventBusContainer,
    #     config=config,
    #     client=eventbus_client,
    # )

    pool = Resource(init_async_timescale_db_pool, config=config.dsn.timescaledb)

    database = Resource(TimeScaleDatabase, pool=pool)

    # meals_broker = Resource(AioPikaBroker, url=config.dsn.rabbitmq.url)

    meals_container = Container(
        MealsContainer,
        database=database,
        config=config,
    )
