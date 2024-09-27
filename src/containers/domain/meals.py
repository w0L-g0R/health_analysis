from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Callable,
    Configuration,
    Factory,
    Object,
    Resource,
)

from src.tasks.meals.insert import MealInsertQuery, MealInsertTask

# from src.adapters.spi.events.event_store_db.subscription import EventStoreDbSubscription
from src.adapters.spi.persistence.time_scale_db.repository import TimeScaleDbRepository
from src.containers.utils.resource_management import (
    init_and_shutdown_event_client,
    init_and_shutdown_time_scale_db_connection,
)
from src.domain.events.meals.insert import MealInsertEvent
from src.domain.models.meals.insert import MealInsertModel


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    event_client = Resource(
        init_and_shutdown_event_client,
        uri=config.connections.eventstoredb,
    )
    #
    event_subscription = Resource(
        event_client.provided.subscribe_to_stream,
        stream_name=config.subscriptions.meals.stream,
        subscribe_from_end=config.subscriptions.meals.from_end,
    )

    connection = Resource(
        init_and_shutdown_time_scale_db_connection,
        connection_string=config.connections.timescaledb,
        database=config.databases.meals,
    )

    repository = Resource(
        TimeScaleDbRepository,
        connection=connection,
    )

    task_insert = Factory(
        MealInsertTask,
        repository=repository.provided,
        event=Callable[MealInsertEvent],
        model=Callable[MealInsertModel],
        query=Object(MealInsertQuery),
    )
    #
    # task_delete = Factory(
    #     MealDeleteTask,
    #     repository=repository.provided,
    #     event=Callable[MealDeleteEvent],
    #     model=Callable[MealDeleteModel],
    #     query=Object(MealDeleteQuery),
    # )
    #
    # event_handler = Resource(
    #     MealsEventsHandler,
    #     meal_insert_task=task_insert,
    #     meal_delete_task=task_delete,
    #     meal_insert_event_type_name=config.events.meals.insert,
    #     meal_delete_event_type_name=config.events.meals.insert,
    # )
    #
    # tasks = Dict(
    #     {
    #         MealInsertTask.__name__: MealInsertTask,
    #         MealDeleteTask.__name__: MealDeleteTask,
    #     }
    # )
    #
    # broker = Resource(
    #     TaskiqBroker,
    #     url=config.connections.rabbitmq.uri,
    #     name="meals_broker",
    #     tasks=tasks,
    #     exchange_name=config.exchanges.meals,
    #     queue_name=config.queues.meals,
    # )
