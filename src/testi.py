import dramatiq
from dependency_injector.wiring import Provide, inject
from dramatiq.middleware import Middleware

from dependencies.app import HealthHandler
from new_main import napp
from testi2 import NAppContainer


class DependencyInjectionMiddleware(Middleware):
    def before_worker_boot(self, broker, worker):
        # Initialize and wire the container for this worker
        # napp.init_resources()
        napp.wire(modules=[__name__])
        print("DI middle")


@dramatiq.actor
@inject
def process(
    event_data: str,
    health_handler: HealthHandler = Provide[
        NAppContainer.health_container.health_handler
    ],
):
    print("__loader__: ", __loader__)

    # health_handler.print_meal(event_data)
    # assert type(health_handler) is HealthHandler, "Fail"

    print(f"\nHEALTH HANDLER: {type(health_handler)}")
