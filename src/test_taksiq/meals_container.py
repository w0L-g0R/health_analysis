from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import (
    Configuration,
    Object,
    Singleton,
)
from taskiq_aio_pika import AioPikaBroker


class MealsContainer(DeclarativeContainer):
    config = Configuration()

    repository = Object("Meals Repo")

    broker = Singleton(
        AioPikaBroker,
        url="amqp://guest:guest@127.0.0.1:5672",
        queue_name="meals_queue",
        exchange_name="meals_exchange",
    )
