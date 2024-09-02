import logging

from asyncpg import Pool, create_pool
from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Factory,
)


async def init_async_timescale_db_pool(
    config: dict,
) -> Pool:
    try:
        pool = await create_pool(dsn=config["dsn"])

        logging.info(f"Timescale DB pool created: {id(pool)}")
        return pool

    except Exception as e:
        logging.error(f"Error initializing connection pool: {e}")
        raise


class PoolsContainer(DeclarativeContainer):
    config = Configuration()

    timescale_db = Factory(
        init_async_timescale_db_pool,
        config=config.dsn.timescaledb,
    )
