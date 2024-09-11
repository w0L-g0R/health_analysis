from dependency_injector.containers import (
    DeclarativeContainer,
)
from dependency_injector.providers import Container, Singleton
from dramatiq.middleware import Middleware


class DependencyInjectionMiddleware(Middleware):
    def before_worker_boot(self, broker, worker):
        # Initialize and wire the container for this worker
        app = NAppContainer()
        app.init_resources()
        app.wire(modules=[__name__])


class HealthHandler:
    def __init__(self):
        self.name = "Hein"

    def print_meal(self, event_data):
        return print("\n___print_meal:", event_data)


class HealthContainer(DeclarativeContainer):
    health_handler = Singleton(HealthHandler)


class NAppContainer(DeclarativeContainer):
    health_container = Container(HealthContainer)
