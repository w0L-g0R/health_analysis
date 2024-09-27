from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Callable,
    Configuration,
    Object,
    Resource,
    Singleton,
)
from zope.event import subscribers

from src.adapters.api.tasks.taskiq.add_meals.add_meal_task import (
    AddMealTask,
    add_meal_task,
)
from src.adapters.api.tasks.taskiq.meal_tasks import MealTasks
from src.adapters.spi.events.meal_events import MealEvents
from src.adapters.spi.persistence.time_scale_db.meals.meals_queries import MealsQueries
from src.containers.resource_management import (
    init_and_shutdown_time_asyncpg_connection_pool,
)

# from src.adapters.spi.events.event_store_db.subscription import EventStoreDbSubscription
from src.adapters.spi.persistence.time_scale_db.meals.meals_repository import (
    MealsRepository,
)
from src.events.meals.add_meal_event import AddMealEvent
from src.models.meals.meal_model import Meal

# from src.ports.api.tasks.meals.meal_tasks import MealTasks


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    connection_pool = Resource(
        init_and_shutdown_time_asyncpg_connection_pool,
        connection_string=config.connections.timescaledb,
        database=config.databases.meals,
    )

    repository = Resource(
        MealsRepository,
        connection_pool=connection_pool.provided,
        queries=Singleton(MealsQueries),
    )

    meal_tasks = Singleton(
        MealTasks,
        add_meal=Singleton(
            AddMealTask,
            name=config.events.meals.add,
            repository=repository.provided,
            model=Callable[Meal],
            event=Callable[AddMealEvent],
        ),
    )

    # add_meal_task = Factory(
    #     AddMealTask,
    #     _repository=repository.provided,
    #     _dto=Callable[AddMealDto],
    #     _model=Callable[Meal],
    # )
    #
    # remove_meal_task = Factory(
    #     RemoveMealTask,
    #     _repository=repository.provided,
    #     _dto=Callable[RemoveMealDto],
    # )
    #


#
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
