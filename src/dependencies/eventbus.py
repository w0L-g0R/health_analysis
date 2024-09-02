from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Singleton,
    Configuration,
    Dependency,
)
from esdbclient import CatchupSubscription, EventStoreDBClient


class EventBusContainer(DeclarativeContainer):
    config = Configuration()

    client = Dependency(instance_of=EventStoreDBClient)

    def subscription_factory(
        client, stream_name: str, from_end: bool
    ) -> CatchupSubscription:
        return client.subscribe_to_stream(stream_name=stream_name, from_end=from_end)

    meals_subscription = Singleton(
        subscription_factory,
        client=client,
        stream_name=config.subscriptions.meals.stream,
        from_end=config.subscriptions.meals.from_end,
    )

    health_subscription = Singleton(
        subscription_factory,
        client=client,
        stream_name=config.subscriptions.health.stream,
        from_end=config.subscriptions.health.from_end,
    )

    # subscription = Aggregate(health=health_subscription, meals=meals_subscription)
