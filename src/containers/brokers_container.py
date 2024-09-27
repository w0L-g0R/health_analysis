from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Resource
from taskiq_aio_pika import AioPikaBroker


class BrokersContainer(DeclarativeContainer):
    config = Configuration()

    meals_broker = Resource(
        AioPikaBroker,
        url=config.connections.rabbitmq,
        queue_name=config.queues.meals,
    )

    health_broker = Resource(
        AioPikaBroker,
        url=config.connections.rabbitmq,
        queue_name=config.queues.health,
    )
