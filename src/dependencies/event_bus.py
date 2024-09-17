from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Singleton,
    Resource,
)

from src.adapters.clients import EventBusClient
from src.handlers.meals_handler import MealsHandler
from src.tasks.meal_tasks import MealsTasks


# def get_subscription(client, stream_name: str, from_end: bool) -> CatchupSubscription:
#     return client.subscribe_to_stream(stream_name=stream_name, from_end=from_end)


class EventBusContainer(DeclarativeContainer):
    config = Configuration()

    meals_handler = Resource(MealsHandler, tasks=MealsTasks)

    meal_events_client = Resource(
        EventBusClient,
        uri=config.dsn.eventstoredb.uri,
        handler=meals_handler,
        stream_name=config.subscriptions.meals.stream,
        from_end=config.subscriptions.meals.from_end,
    )

    # meals_subscription = Singleton(
    #     get_subscription,
    #     client=client,
    #     stream_name=config.subscriptions.meals.stream,
    #     from_end=config.subscriptions.meals.from_end,
    # )
