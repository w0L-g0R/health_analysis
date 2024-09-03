from logging.config import dictConfig

from dependencies.connections import init_async_timescale_db_pool
from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import Singleton, Factory

from dependency_injector.providers import Configuration, Container, Resource
from dramatiq import Actor
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from esdbclient import EventStoreDBClient

from api.meals.bootstrap import MealsContainer
from api.meals.repository import MealsRepository
from dependencies.eventbus import EventBusContainer


class AppContainer(DeclarativeContainer):
    config = Configuration()

    logging = Resource(dictConfig, config=config.logging)

    eventbus_client = Resource(
        EventStoreDBClient,
        uri=config.dsn.eventstoredb.uri,
    )

    broker = Resource(RabbitmqBroker, url=config.dsn.rabbitmq.url)

    actor = Factory(
        Actor,
        fn=lambda x: x,
        actor_name="",
        queue_name="",
        broker=broker,
        priority=10,
        options={},
    )

    eventbus = Resource(
        EventBusContainer,
        config=config,
        client=eventbus_client,
    )

    meals_container = Container(
        MealsContainer,
        broker=broker,
        actor=actor,
        config=config,
    )
