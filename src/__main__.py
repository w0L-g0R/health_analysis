import asyncio
import logging
from pprint import pformat
from signal import SIGINT, SIGTERM, signal

from api.meals.insert.handler import MealInsertEventHandler
from api.meals.repository import MealsRepository
from dependency_injector.wiring import Provide, inject
import dramatiq

from config import CONFIG
from dependencies.app import AppContainer
from dependencies.eventbus import EventBusContainer
from esdbclient import CatchupSubscription


logging.config.dictConfig(CONFIG["logging"])
logger = logging.getLogger(__name__)

STOP_EVENT = asyncio.Event()
FORMATTED_CONFIG = pformat(CONFIG, indent=4)


@inject
async def handle_events(
    subscription: CatchupSubscription,
    insert_event_handler: MealInsertEventHandler = Provide[
        AppContainer.meals_container.insert_event_handler
    ],
):
    logging.info(f"Started listening to subscription: {id(subscription)}")

    while not STOP_EVENT.is_set():
        try:
            for event in subscription:
                logging.info(
                    f"Received event from subscription {id(subscription)}:\n{pformat(event, indent=2)}"
                )

                match event.type:
                    case "MealInsert":
                        await insert_event_handler.handle(event)
                    case _:
                        print("No matching type")

            # Prevent CPU overuse
            await asyncio.sleep(0.1)

        except Exception as e:
            logging.error(f"Error while handling events:\n{e}")
            raise e
            await asyncio.sleep(0.1)


@inject
async def shutdown(
    eventbus_client: EventBusContainer = Provide[AppContainer.eventbus_client],
    meals_repository: MealsRepository = Provide[AppContainer.meals_repository],
):
    STOP_EVENT.set()

    logging.info(f"Stopped asyncio event {id(STOP_EVENT)}: {STOP_EVENT.is_set()}")
    await asyncio.sleep(0.25)

    eventbus_client.close()

    logging.info(
        f"Closed event bus client {id(eventbus_client)}: {eventbus_client._is_closed}"
    )

    await meals_repository.close()


@inject
async def start_event_subscriptons(
    eventbus=Provide[AppContainer.eventbus],
):
    try:
        logging.info("Start handling incoming events")

        await asyncio.gather(
            handle_events(eventbus.meals_subscription()),
            # handle_events(health_subscription, meals_event_handler),
        )

    except Exception as e:
        logging.error(f"Error in main loop: {e}")

    finally:
        await shutdown()


if __name__ == "__main__":
    logger.info(f"\nStarting setup with config:\n{FORMATTED_CONFIG}\n")
    logger.info(f"Stopped asyncio event {id(STOP_EVENT)}: {STOP_EVENT.is_set()}")

    app = AppContainer(config=CONFIG)
    app.init_resources()
    app.wire(modules=[__name__])
    app.check_dependencies()

    logging.info(f"AppContainer set up: {id(app)}")

    # Set up signals that stops the event loop in case of a container/pod shutdown
    sigint_handler = signal(SIGINT, lambda x: STOP_EVENT.set())
    sigterm_handler = signal(SIGTERM, lambda x: STOP_EVENT.set())

    logging.info(
        f"Shutdown signals for container shutdowns set up: {id(sigint_handler)}, {id(sigterm_handler)}"
    )

    dramatiq.set_broker(app.broker())

    logging.info(f"Broker set up: {dramatiq.get_broker()}")

    try:
        asyncio.run(start_event_subscriptons())

    except KeyboardInterrupt:
        logging.error("Application interrupted by keyboard.")
