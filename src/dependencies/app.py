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
from esdbclient import EventStoreDBClient

from api.meals.bootstrap import MealsContainer
from api.utils.validator import Validator
from dependencies.eventbus import EventBusContainer
from dependencies.pools import PoolsContainer


class AppContainer(DeclarativeContainer):
    config = Configuration()

    logging = Resource(dictConfig, config=config.logging)

    validator = Resource(Validator)

    eventbus_client = Resource(
        EventStoreDBClient,
        uri=config.dsn.eventstoredb.uri,
    )

    broker = Resource(RabbitmqBroker, url=config.dsn.rabbitmq.url)

    eventbus = Container(
        EventBusContainer,
        config=config,
        client=eventbus_client,
    )

    pools = Container(PoolsContainer, config=config)

    meals = Container(
        MealsContainer,
        broker=broker,
        pool=pools.timescale_db,
        config=config,
        validator=validator,
    )
