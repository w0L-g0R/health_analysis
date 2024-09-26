from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Callable,
    Configuration,
    Dict,
    Factory,
    Object,
    Resource,
)

from src.adapters.api.tasks.meals.delete import MealDeleteTask
from src.adapters.api.tasks.meals.insert import MealInsertQuery, MealInsertTask
from src.adapters.spi.events.event_store_db.client import EventStoreDbClient
from src.adapters.spi.messages.taskiq.broker import TaskiqBroker
from src.adapters.spi.persistence.time_scale_db.connection import TimeScaleDbConnection
from src.adapters.spi.persistence.time_scale_db.queries.meals import MealDeleteQuery
from src.adapters.spi.persistence.time_scale_db.repository import TimeScaleDbRepository
from src.containers.wrapper import EventStoreDbClientWrapper
from src.domain.events.meals.delete import MealDeleteEvent
from src.domain.events.meals.insert import MealInsertEvent
from src.domain.models.meals.delete import MealDeleteModel
from src.domain.models.meals.insert import MealInsertModel
from src.handler.meals import MealsEventsHandler
from src.ports.spi.events.subscription import EventSubscription


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    connection = Resource(
        TimeScaleDbConnection,
        connection_string=config.connections.timescaledb,
        database=config.databases.meals,
    )

    repository = Resource(
        TimeScaleDbRepository,
        connection=connection,
    )

    event_client = Resource(
        EventStoreDbClientWrapper,
        uri=config.connections.eventstoredb,
        stream_name=config.subscriptions.meals.stream,
        subscribe_from_end=config.subscriptions.meals.from_end,
    )
    #
    # event_subscription = Resource(EventSubscription)
    #
    # task_insert = Factory(
    #     MealInsertTask,
    #     repository=repository.provided,
    #     event=Callable[MealInsertEvent],
    #     model=Callable[MealInsertModel],
    #     query=Object(MealInsertQuery),
    # )
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
