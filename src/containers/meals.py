from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import Configuration, Resource, Dict, Factory, Object

from src.adapters.spi.persistence.time_scale_db.queries.meals import MealsQueries
from src.adapters.spi.persistence.time_scale_db.repository import TimeScaleDbRepository


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    repository = Resource(
        TimeScaleDbRepository,
        user=config.dns.timescaledb.user,
        password=config.dns.timescaledb.password,
        host=config.dns.timescaledb.host,
        port=config.dns.timescaledb.port,
        database=config.databases.meals,
        queries=MealsQueries,
    )

    event_client = Resource(
        EventStoreDbClient,
        uri=config.dns.eventstoredb.uri,
        stream_name=config.subscriptions.meals.stream,
        subscribe_from_end=config.subscriptions.meals.from_end,
    )

    event_subscription = Resource(EventSubscription)

    task_insert = Factory(
        MealInsertTask,
        repository=repository,
        event=MealInsertEvent,
        model=Object(MealInsertModel),
    )

    task_delete = Factory(
        MealDeleteService,
        repository=repository,
        event=MealDeleteEvent,
        model=Object(MealDeleteModel),
    )

    event_handler = Factory(
        MealsEventsHandler,
        meal_insert_use_case=service_insert,
        meal_delete_use_case=service_delete,
        meal_insert_event_type_name=config.events.meals.insert,
        meal_delete_event_type_name=config.events.meals.insert,
    )

    tasks = Dict(
        {
            MealsService.insert_meal.__name__: MealsService.insert_meal,
        }
    )

    broker = Resource(
        TaskiqBroker,
        url=config.dsn.rabbitmq.url,
        type="meals_broker",
        tasks=tasks,
        exchange_name=config.exchanges.meals,
        queue_name=config.queues.meals,
    )
