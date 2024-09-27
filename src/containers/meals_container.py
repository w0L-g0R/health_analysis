from asyncpg import Pool
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Callable,
    Configuration,
    Dependency,
    Factory,
    Object,
    Resource,
    Singleton,
)
from esdbclient import CatchupSubscription

from src.domain.models.meals.meal_model import Meal
from src.ports.api.use_cases.meals.add_meal.add_meal import AddMealDto
from src.tasks.meals.add_meal_task import AddMealTask

# from src.adapters.spi.events.event_store_db.subscription import EventStoreDbSubscription
from src.adapters.spi.persistence.meals.meals_repository import MealsRepository
from src.containers.resource_management import (
    init_and_shutdown_event_client,
    init_and_shutdown_time_scale_db_connection,
)


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    event_client = Resource(
        init_and_shutdown_event_client,
        uri=config.connections.eventstoredb,
    )
    #
    event_subscription = Dependency(
        CatchupSubscription,
    )

    connection_pool = Dependency(Pool)

    repository = Singleton(
        MealsRepository,
        _connection_pool=connection_pool,
    )

    add_meal_task = Factory(
        AddMealTask,
        _repository=repository.provided,
        _dto=Callable[AddMealDto],
        _model=Callable[Meal],
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
