import random

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import (
    Callable,
    Configuration,
    Dict,
    Object,
    Resource,
    Singleton,
)

# from src.adapters.api.tasks.taskiq.add_meals.add_meal_task import AddMealTask

# from src.adapters.api.tasks.taskiq.add_meals.add_meal_task import (
#     AddMealTask,
#     add_meal_task,
# )
# from src.adapters.api.tasks.taskiq.meal_tasks import MealTasks
from src.database.time_scale_db.meals.meals_queries import MealsQueries
from src.containers.resource_management import (
    init_and_shutdown_time_asyncpg_connection_pool,
)

# from src.adapters.spi.events.event_store_db.subscription import EventStoreDbSubscription
from src.database.time_scale_db.meals.meals_repository import (
    MealsRepository,
)
from src.events.meals.add_meal_event import AddMealEvent
from src.models.meals.meal_model import Meal

# from src.ports.api.tasks.meals.meal_tasks import MealTasks


class MealsContainer(DeclarativeContainer):
    config = Configuration()
    number = Callable(random.randint, a=1, b=10)

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

    validators = Dict(AddMealEvent=Object(AddMealEvent))

    model = Object(Meal)
