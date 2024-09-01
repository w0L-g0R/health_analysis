from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Singleton,
)
from esdbclient import EventStoreDBClient


class EventBusClient(DeclarativeContainer):
    config = Configuration()

    client = Singleton(
        EventStoreDBClient,
        uri=config.dsn.eventstoredb.uri,
    )
