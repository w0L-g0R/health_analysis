from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Resource,
    Object,
    Dict,
    Factory,
)
from domain.meals.events import (
    DeleteMealEvent,
    InsertMealEvent,
    MealEvents,
)
from domain.meals.queries import MealQueries, InsertMealQuery
from taskiq_aio_pika import AioPikaBroker

from dependencies.infrastructure.database import (
    TimeScaleDatabase,
)


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    database = Resource(
        TimeScaleDatabase,
        config=config.dsn.timescaledb,
    )

    broker = Resource(
        AioPikaBroker, url=config.dsn.rabbitmq.url
    )

    events = Dict(
        {
            MealEvents.INSERT: Object(InsertMealEvent),
            MealEvents.DELETE: Object(DeleteMealEvent),
        }
    )

    queries = Dict(
        {
            MealQueries.INSERT: Factory(InsertMealQuery),
        }
    )
