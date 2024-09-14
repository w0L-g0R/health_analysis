import logging
import asyncpg
from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Resource,
    Singleton,
)
from taskiq_aio_pika import AioPikaBroker

from dependencies.database import (
    TimeScaleDatabase,
    init_async_timescale_db_connection,
)


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    connection = Resource(
        init_async_timescale_db_connection,
        config=config.dsn.timescaledb,
    )

    database = Resource(
        TimeScaleDatabase,
        connection=connection,
    )

    broker = Resource(
        AioPikaBroker, url=config.dsn.rabbitmq.url
    )
