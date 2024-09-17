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


from src.adapters.brokers import TaskiqBroker
from src.adapters.databases import TimeScaleDb
from src.dependencies.meals.factories import InsertMealQueryFactory, MealQueryFactory
from src.domains.meals.events import DeleteMealEvent, InsertMealEvent, MealEvents
from src.tasks.meal_tasks import MealTaskPath, MealsTasks


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    database = Resource(
        TimeScaleDb,
        config=config.dsn.timescaledb,
    )

    tasks = Dict(
        {
            MealTaskPath.INSERT.value: MealsTasks.insert_meal,
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
        TaskiqBroker,
        url=config.dsn.rabbitmq.url,
        name="meals_broker",
        tasks=tasks,
        database=database.provided,
        events=events,
        query_factories=query_factories,
    )
