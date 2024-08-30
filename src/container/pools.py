from dependency_injector import providers
from dependency_injector.containers import (
    DeclarativeContainer,
)
from psycopg2.pool import SimpleConnectionPool


def init_timescale_db_pool(
    config: dict,
) -> None:
    print("config pool: ", config)
    pool = SimpleConnectionPool(
        minconn=1,  # Minimum number of connections in the pool
        maxconn=10,  # Maximum number of connections in the pool
        user=config.user,
        password=config.password,
        host=config.host,
        port=config.port,
        database=config.dbname,
    )
    yield pool
    pool.closeall()


class Pools(DeclarativeContainer):
    config = providers.Configuration()

    timescale_db_pool = providers.Factory(
        SimpleConnectionPool,
        config=config,
    )
