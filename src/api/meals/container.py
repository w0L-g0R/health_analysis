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
from api.meals.insert.query import MealInsertQuery
from api.meals.repository import MealsRepository
from dependencies.connections import (
    init_async_timescale_db_pool,
)


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    # broker = Dependency(instance_of=RabbitmqBroker)

    # actor = Dependency(instance_of=Actor)

    pool = Singleton(
        init_async_timescale_db_pool,
        config=config.dsn.timescaledb,
        database=config.databases.meals,
    )

    repository = Singleton(MealsRepository, pool=pool)

    insert_event_handler = Singleton(
        MealInsertEventHandler,
        # config=config,
        # broker=broker,
        repository=repository,
        # actor=actor,
        event_class=Object(MealInsertEvent),
        query=Object(MealInsertQuery),
    )
