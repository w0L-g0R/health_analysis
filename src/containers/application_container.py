from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Configuration,
    Container,
    Resource,
)

from src.containers.meals_container import MealsContainer

# from src.adapters.spi.events.event_store_db.subscription import EventStoreDbSubscription
from src.containers.resource_management import (
    init_and_shutdown_event_client,
    init_and_shutdown_time_scale_db_connection,
)


class ApplicationContainer(DeclarativeContainer):
    config = Configuration()

    event_client = Resource(
        init_and_shutdown_event_client,
        uri=config.connections.eventstoredb,
    )

    meal_events_subscription = Resource(
        event_client.provided.subscribe_to_stream,
        stream_name=config.subscriptions.meals.stream,
        subscribe_from_end=config.subscriptions.meals.from_end,
    )

    meals_connection_pool = Resource(
        init_and_shutdown_time_scale_db_connection,
        connection_string=config.connections.timescaledb,
        database=config.databases.meals,
    )

    meals_container = Container(
        MealsContainer,
        connection_string=config.connections.timescaledb,
        database=config.databases.meals,
    )
