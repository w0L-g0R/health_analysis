from api.meals.insert.query import MealInsertQuery
from dramatiq import Actor
from dramatiq.brokers.rabbitmq import RabbitmqBroker

from dependency_injector.containers import (
    DeclarativeContainer,
)

from dependency_injector.providers import Factory, Object, Singleton

from dependency_injector.providers import Dependency, Configuration

from api.meals.insert.event import MealInsertEvent
from api.meals.insert.handler import MealInsertEventHandler
from api.meals.repository import MealsRepository


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    broker = Dependency(instance_of=RabbitmqBroker)

    repository = Dependency(MealsRepository)

    actor = Factory(
        Actor,
        fn=lambda x: x,
        actor_name="",
        queue_name="",
        broker=broker,
        priority=10,
        options={},
    )

    insert_event_handler = Singleton(
        MealInsertEventHandler,
        config=config,
        broker=broker,
        repository=repository,
        actor=actor,
        event_class=Object(MealInsertEvent),
        sql_statement=Object(MealInsertQuery),
    )
