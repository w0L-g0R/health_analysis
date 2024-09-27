from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Configuration,
    Resource,
    Singleton,
)
from esdbclient import EventStoreDBClient
from esdbclient.common import AbstractCatchupSubscription

from src.adapters.spi.events.meal_events import MealEvents

# from src.adapters.spi.events.event_store_db.subscription import EventStoreDbSubscription
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
        MealsEventsHandler, subscription=meal_events_subscription.provided
    )

    meal_events = Singleton(
        MealEvents,
        add_meal=config.events.meals.add,
    )

    # meals_connection_pool = Resource(
    #     init_and_shutdown_time_asyncpg_connection_pool,
    #     connection_string=config.connections.timescaledb,
    #     database=config.databases.meals,
    # )

    # meals_container = Container(
    #     MealsContainer,
    #     # connection_string=config.connections.timescaledb,
    #     # database=config.databases.meals,
    #     connection_pool=meals_connection_pool.provided,
    #     events_subscription=meal_events_subscription,
    # )
