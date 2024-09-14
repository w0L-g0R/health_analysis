import asyncio
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

from config import CONFIG_DICT
from dependencies.database import (
    TimeScaleDatabase,
    init_async_timescale_db_connection,
)


async def init_async_timescale_db_connection(config: dict):
    try:
        connection = await asyncpg.connect(
            user=config["user"],
            password=config["password"],
            database=config["database"],
            host=config["host"],
            port=config["port"],
        )

        logging.info(
            f"Timescale DB connection created: {id(connection)}"
        )
        return connection

    except Exception as e:
        logging.error(f"Error initializing connection: {e}")
        raise


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


async def main():
    c = MealsContainer()
    c.config.from_dict(CONFIG_DICT)
    # conn = await c.connection()

    # Initialize resources
    await c.init_resources()
    database = await c.database()
    broker = c.broker()

    return broker


# Use asyncio.run to run the async function
broker = asyncio.run(main())
print("conn: ", broker)
