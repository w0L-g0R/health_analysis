import logging
from asyncpg import Pool, create_pool


async def init_async_timescale_db_pool(config: dict, database: str) -> Pool:
    try:
        pool = await create_pool(
            user=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"],
            database=database,
        )

        logging.info(f"Timescale DB pool created: {id(pool)}")
        return pool

    except Exception as e:
        logging.error(f"Error initializing connection pool: {e}")
        raise
