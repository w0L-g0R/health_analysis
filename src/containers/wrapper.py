from dependency_injector import resources

from src.adapters.spi.events.event_store_db.client import EventStoreDbClient


class EventStoreDbClientWrapper(resources.Resource):

    def init(
        self, uri: str, stream_name: str, subscribe_from_end: bool
    ) -> EventStoreDbClient:
        return EventStoreDbClient(
            uri=uri,
            stream_name=stream_name,
            subscribe_from_end=subscribe_from_end,
        )

    def shutdown(self, resource: EventStoreDbClient) -> None:
        resource.shutdown()
