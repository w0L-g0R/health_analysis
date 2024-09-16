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
from taskiq_aio_pika import AioPikaBroker


from src.adapters.broker import Broker
from src.adapters.database import Database
from src.dependencies.meals.factories import InsertMealQueryFactory, MealQueryFactory
from src.domains.meals.events import DeleteMealEvent, InsertMealEvent, MealEvents
from src.tasks.meal_tasks import MealTasks, insert_meal


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    database = Resource(
        Database,
        config=config.dsn.timescaledb,
    )

    tasks = Dict(
        {
            MealTasks.INSERT.value: insert_meal,
        }
    )

    events = Dict(
        {
            MealEvents.INSERT: Object(InsertMealEvent),
            MealEvents.DELETE: Object(DeleteMealEvent),
        }
    )

    query_factories = Dict(
        {
            MealQueryFactory.INSERT: Factory(
                InsertMealQueryFactory,
                table_name=config.dsn.timescaledb.tables.meals,
            )
        }
    )

    broker = Resource(
        Broker,
        url=config.dsn.rabbitmq.url,
        tasks=tasks,
        database=database.provided,
        events=events,
        query_factories=query_factories,
    )
