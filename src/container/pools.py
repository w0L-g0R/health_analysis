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
        config=config.databases.timescale,
    )

    # timescale_db_pool = providers.Factory(
    #     SimpleConnectionPool,
    #     minconn=1,  # Minimum number of connections in the pool
    #     maxconn=10,  # Maximum number of connections in the pool
    #     user=config.databases.timescale.user,
    #     password=config.databases.timescale.password,
    #     host=config.databases.timescale.host,
    #     port=config.databases.timescale.port,
    #     database=config.databases.timescale.dbname,
    # )
