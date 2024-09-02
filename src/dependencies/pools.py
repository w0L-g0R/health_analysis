import logging

from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Factory,
)
from psycopg2.pool import SimpleConnectionPool


def init_timescale_db_pool(
    config: dict,
) -> SimpleConnectionPool:
    try:
        pool = SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            user=config["user"],
            password=config["password"],
            host=config["host"],
            port=config["port"],
            database=config["dbname"],
        )
        logging.info(f"Timescale DB pool created: {id(pool)}")
        return pool
    except Exception as e:
        logging.error(f"Error initializing connection pool: {e}")
        raise


class PoolsContainer(DeclarativeContainer):
    config = Configuration()

    timescale_db = Factory(
        init_timescale_db_pool,
        config=config.dsn.timescaledb,
    )
