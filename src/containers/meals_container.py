from asyncpg import Pool
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Callable,
    Configuration,
    Dependency,
    Factory,
    Resource,
    Singleton,
)
from esdbclient import CatchupSubscription

from src.adapters.api.eventstore.meal_events_handler import MealsEventsHandler
from src.containers.resource_management import (
    init_and_shutdown_time_asyncpg_connection_pool,
)
from src.domain.models.meals.meal_model import Meal
from src.ports.api.use_cases.meals.add_meal.add_meal_dto import AddMealDto
from src.ports.api.use_cases.meals.remove_meal.remove_meal_dto import RemoveMealDto
from src.ports.api.use_cases.meals.remove_meal.remove_meal_use_case import (
    RemoveMealUseCase,
)
from src.tasks.meals.add_meal_task import AddMealTask

# from src.adapters.spi.events.event_store_db.subscription import EventStoreDbSubscription
from src.adapters.spi.persistence.meals.meals_repository import MealsRepository
from src.tasks.meals.remove_meal_task import RemoveMealTask


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    meals_connection_pool = Resource(
        init_and_shutdown_time_asyncpg_connection_pool,
        connection_string=config.connections.timescaledb,
        database=config.databases.meals,
    )
    repository = Singleton(
        MealsRepository,
        _connection_pool=meals_connection_pool.provided,
    )

    add_meal_task = Factory(
        AddMealTask,
        _repository=repository.provided,
        _dto=Callable[AddMealDto],
        _model=Callable[Meal],
    )

    remove_meal_task = Factory(
        RemoveMealTask,
        _repository=repository.provided,
        _dto=Callable[RemoveMealDto],
    )

    event_handler = Resource(
        MealsEventsHandler,
        add_meal_use_case=add_meal_task,
        remove_meal_use_case=RemoveMealUseCase,
        add_meal_event_type=config.events.meal.add,
        remove_meal_event_type=config.events.meal.remove,
    )

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
