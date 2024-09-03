from logging.config import dictConfig

from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Container,
    Resource,
)
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from dramatiq.middleware import AsyncIO
from esdbclient import EventStoreDBClient

from api.meals.container import MealsContainer
from dependencies.eventbus import EventBusContainer


class AppContainer(DeclarativeContainer):
    config = Configuration()

    logging = Resource(dictConfig, config=config.logging)

    eventbus_client = Resource(
        EventStoreDBClient,
        uri=config.dsn.eventstoredb.uri,
    )

    broker = Resource(
        RabbitmqBroker,
        # url=config.dsn.rabbitmq.url,
        host=config.dsn.rabbitmq.host,
        password=config.dsn.rabbitmq.password,
        user=config.dsn.rabbitmq.user,
        port=config.dsn.rabbitmq.port,
        middlewares=[
            AsyncIO(),
            # TimeLimit(),
            # Retries(),
            # Shutdown(),
        ],
    )

    # actor = Factory(
    #     Actor,
    #     fn=lambda x: x,
    #     actor_name="",
    #     queue_name="",
    #     broker=broker,
    #     priority=10,
    #     options={},
    # )

    eventbus = Resource(
        EventBusContainer,
        config=config,
        client=eventbus_client,
    )

    meals_container = Container(
        MealsContainer,
        # broker=broker,
        # actor=actor,
        config=config,
    )
