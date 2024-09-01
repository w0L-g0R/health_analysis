from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Aggregate,
    Configuration,
    Dependency,
    Factory,
)
from esdbclient import EventStoreDBClient


class EventBus(DeclarativeContainer):
    config = Configuration()

    client = Dependency(instance_of=EventStoreDBClient)

    def subscription_factory(client, stream_name, from_end):
        return client.subscribe_to_stream(
            stream_name=stream_name, from_end=from_end
        )

    meals_subscription = Factory(
        subscription_factory,
        client=client,
        stream_name=config.subscriptions.meals.stream,
        from_end=config.subscriptions.meals.from_end,
    )

    health_subscription = Factory(
        subscription_factory,
        client=client,
        stream_name=config.subscriptions.health.stream,
        from_end=config.subscriptions.health.from_end,
    )

    subscription = Aggregate(
        health=health_subscription, meals=meals_subscription
    )
