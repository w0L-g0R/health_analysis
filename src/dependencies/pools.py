import logging

from asyncpg import Pool
from psycopg2.pool import ThreadedConnectionPool


def init_timescale_db_pool(
    config: dict, database: str
) -> Pool:
    try:
        pool = ThreadedConnectionPool(
            minconn=1,
            maxconn=10,
            user=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"],
            database=database,
        )

        logging.info(f"Timescale DB pool created: {id(pool)}")
        return pool

    except Exception as e:
        logging.error(
            f"Error initializing connection pool: {e}"
        )
        raise
