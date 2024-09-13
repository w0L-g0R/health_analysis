from dependencies.database import TimeScaleDatabase
from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import Dict, Object, Singleton, Dependency
from taskiq_aio_pika import AioPikaBroker

# from api.meals.insert.event import MealInsertEvent
# from api.meals.insert.handler import MealInsertEventHandler
# from api.meals.queries import MealInsertCommand
# from dependencies.database import MealsRepository
# from dependencies.pools import init_timescale_db_pool


class MealsContainer(DeclarativeContainer):
    config = Dependency()
    database = Dependency(TimeScaleDatabase)
    # broker = Dependency(AioPikaBroker)

    # broker_dependencies = Dict({{"database": database}})

    #     repository = Singleton(MealsRepository, pool=pool)

    # database = Singleton(DB)


#     config = Configuration()


# insert_event_handler = Singleton(
#     MealInsertEventHandler,
#     repository=repository,
#     event_class=Object(MealInsertEvent),
#     query=Object(MealInsertCommand),
# )
