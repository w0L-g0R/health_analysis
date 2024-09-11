from logging.config import dictConfig

from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Container,
    Resource,
    Singleton,
)
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from esdbclient import EventStoreDBClient

# from api.health.container import HealthContainer
from api.meals.container import MealsContainer
from dependencies.eventbus import EventBusContainer

# from api.health.handler import HealthHandler


class HealthHandler:
    def __init__(self):
        self.name = "Hein"

    def print_meal(self, event_data):
        return event_data


class HealthContainer(DeclarativeContainer):
    health_handler = Singleton(HealthHandler)


class AppContainer(DeclarativeContainer):
    config = Configuration()

    logging = Resource(dictConfig, config=config.logging)

    eventbus_client = Resource(
        EventStoreDBClient,
        uri=config.dsn.eventstoredb.uri,
    )

    broker = Resource(
        RabbitmqBroker, url=config.dsn.rabbitmq.url
    )
    eventbus = Resource(
        EventBusContainer,
        config=config,
        client=eventbus_client,
    )

    meals_container = Container(
        MealsContainer,
        config=config,
    )

    health_container = Container(HealthContainer)
