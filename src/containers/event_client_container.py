from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Configuration,
    Resource,
)
from esdbclient import EventStoreDBClient
from esdbclient.common import AbstractCatchupSubscription
from src.containers.resource_management import (
    init_and_shutdown_event_store_db_client,
)
from src.handlers.meal_events_handler import MealsEventsHandler


def init_subscription(
    client: EventStoreDBClient, stream_name: str, from_end: bool
) -> AbstractCatchupSubscription:
    return client.subscribe_to_stream(stream_name=stream_name, from_end=from_end)


class EventClientContainer(DeclarativeContainer):
    config = Configuration()

    events_client = Resource(
        init_and_shutdown_event_store_db_client,
        uri=config.connections.eventstoredb,
    )

    meal_events_subscription = Resource(
        init_subscription,
        client=events_client.provided,
        stream_name=config.streams.meals,
        from_end=config.streams.from_end.meals,
    )

    meal_events_handler = Resource(
        MealsEventsHandler,
        subscription=meal_events_subscription.provided,
        add_meal_event=config.events.meals.add,
    )
