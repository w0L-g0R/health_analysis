from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Object,
    Singleton,
)

from api.meals.insert.event import MealInsertEvent
from api.meals.insert.handler import MealInsertEventHandler
from api.meals.queries import MealInsertCommand
from dependencies.database import MealsRepository
from dependencies.pools import init_timescale_db_pool


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    pool = Singleton(
        init_timescale_db_pool,
        config=config.dsn.timescaledb,
    )

    repository = Singleton(MealsRepository, pool=pool)

    # insert_event_handler = Singleton(
    #     MealInsertEventHandler,
    #     repository=repository,
    #     event_class=Object(MealInsertEvent),
    #     query=Object(MealInsertCommand),
    # )
