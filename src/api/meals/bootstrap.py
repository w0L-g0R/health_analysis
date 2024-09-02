from dramatiq.brokers.rabbitmq import RabbitmqBroker

from dependency_injector.containers import (
    DeclarativeContainer,
)

from dependency_injector.providers import Factory, Aggregate, Object

from dependency_injector.providers import Dependency, Singleton, Configuration
from psycopg2.pool import SimpleConnectionPool

from api.meals.insert.event import MealInsertEvent
from api.meals.insert.handler import MealInsertEventHandler
from api.meals.repository import MealsRepository
from api.utils.validator import Validator


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    pool = Dependency(instance_of=SimpleConnectionPool)

    broker = Dependency(instance_of=RabbitmqBroker)

    repository = Singleton(MealsRepository, pool=pool)

    meals_insert_event_class = Object(MealInsertEvent)

    meal_insert_handler = Factory(
        MealInsertEventHandler,
        config=config,
        broker=broker,
        event_class=meals_insert_event_class,
    )

    meals_event_handler = Aggregate(insert_meal=meal_insert_handler)
