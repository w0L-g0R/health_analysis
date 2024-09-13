from logging.config import dictConfig

from dependencies.eventbus import EventBusContainer
from dependencies.meals import MealsContainer
from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Container,
    Resource,
)
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from esdbclient import EventStoreDBClient


class AppContainer(DeclarativeContainer):
    config = Configuration()

    logging = Resource(dictConfig, config=config.logging)

    # eventbus_client = Resource(
    #     EventStoreDBClient,
    #     uri=config.dsn.eventstoredb.uri,
    # )

    meals_broker = Resource(RabbitmqBroker, url=config.dsn.rabbitmq.url)

    # eventbus = Resource(
    #     EventBusContainer,
    #     config=config,
    #     client=eventbus_client,
    # )

    # meals_container = Container(
    #     MealsContainer,
    #     config=config,
    # )
