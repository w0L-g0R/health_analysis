from dramatiq.brokers.rabbitmq import RabbitmqBroker

from dependency_injector.containers import (
    DeclarativeContainer,
)

from dependency_injector.providers import Factory, Aggregate, Object

from dependency_injector.providers import Dependency, Configuration

from api.meals.insert.event import MealInsertEvent
from api.meals.insert.handler import MealInsertEventHandler
from api.meals.repository import MealsRepository


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    broker = Dependency(instance_of=RabbitmqBroker)

    repository = Dependency(MealsRepository)

    meals_insert_event_class = Object(MealInsertEvent)

    meal_insert_handler = Factory(
        MealInsertEventHandler,
        config=config,
        broker=broker,
        event_class=meals_insert_event_class,
    )

    meals_event_handler = Aggregate(insert_meal=meal_insert_handler)
