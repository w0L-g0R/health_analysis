from typing import Generator

from dependency_injector import providers
from dependency_injector.containers import (
    DeclarativeContainer,
)
from psycopg2.pool import SimpleConnectionPool


def init_timescale_db_pool(
    config: dict,
) -> Generator:
    pool = SimpleConnectionPool(
        minconn=1,
        maxconn=10,
        user=config["user"],
        password=config["password"],
        host=config["host"],
        port=config["port"],
        database=config["dbname"],
    )
    yield pool
    pool.closeall()


class Pools(DeclarativeContainer):
    config = providers.Configuration()

    timescale_db_pool = providers.Factory(
        init_timescale_db_pool,
        config=config.dsn.timescaledb,
    )
