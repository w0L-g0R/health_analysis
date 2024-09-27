from asyncpg import connect, create_pool
from esdbclient import EventStoreDBClient


async def init_and_shutdown_time_asyncpg_connection_pool(**kwargs):
    dsn = "/".join(list(kwargs.values()))
    resource = await create_pool(dsn=dsn)
    yield resource
    await resource.close()


def init_and_shutdown_event_store_db_client(**kwargs):
    print("kwargs: ", kwargs)
    resource = EventStoreDBClient(**kwargs)
    yield resource
    resource.close()
