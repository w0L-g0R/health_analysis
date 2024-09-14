from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Singleton,
    Resource,
)
from esdbclient import CatchupSubscription, EventStoreDBClient


def get_subscription(
    client, stream_name: str, from_end: bool
) -> CatchupSubscription:
    return client.subscribe_to_stream(
        stream_name=stream_name, from_end=from_end
    )


class EventBusContainer(DeclarativeContainer):
    config = Configuration()

    client = Resource(
        EventStoreDBClient,
        uri=config.dsn.eventstoredb.uri,
    )

    meals_subscription = Singleton(
        get_subscription,
        client=client,
        stream_name=config.subscriptions.meals.stream,
        from_end=config.subscriptions.meals.from_end,
    )

    # health_subscription = Singleton(
    #     subscription_factory,
    #     client=client,
    #     stream_name=config.subscriptions.health.stream,
    #     from_end=config.subscriptions.health.from_end,
    # )
