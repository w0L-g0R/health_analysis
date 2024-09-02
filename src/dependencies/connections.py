import logging
from asyncpg import Pool, create_pool


async def init_async_timescale_db_pool(
    config: dict,
) -> Pool:
    try:
        pool = await create_pool(dsn=config["dsn"]["timescaledb"]["dsn"])

        logging.info(f"Timescale DB pool created: {id(pool)}")
        return pool

    except Exception as e:
        logging.error(f"Error initializing connection pool: {e}")
        raise
