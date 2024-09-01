import asyncio
import logging
from pprint import pformat
from signal import SIGINT, SIGTERM, signal

from dependency_injector.wiring import Provide, inject

from api.dependencies.app import AppContainer
from api.dependencies.eventbus import EventBus
from api.meals.infrastructure.repos.meals import Meals
from config import CONFIG

logging.config.dictConfig(CONFIG["logging"])
logger = logging.getLogger(__name__)

STOP_EVENT = asyncio.Event()
FORMATTED_CONFIG = pformat(CONFIG, indent=4)


async def handle_events(subscription, handler_name) -> None:
    logging.info(
        f"Started listening to subscription: {id(subscription)}"
    )

    while not STOP_EVENT.is_set():
        try:
            for event in subscription:
                logging.info(
                    f"Received event from {id(subscription)}:\n{pformat(event, indent=2)}"
                )
            # Prevent CPU overuse
            await asyncio.sleep(0.1)

        except Exception as e:
            logging.error(f"Error while handling events: {e}")
            await asyncio.sleep(0.1)


@inject
async def main(
    eventbus: EventBus = Provide[AppContainer.eventbus],
    meals: Meals = Provide[AppContainer.meals],
):
    logging.info("Started async main()")

    event_bus_client = eventbus.client()

    logging.info(
        "Resolved event bus client: %i", id(event_bus_client)
    )

    meals_subscription = eventbus.subscription.meals()

    logging.info(
        f"Resolved meals events subscription: {id(meals_subscription)} for {meals_subscription._stream_name}"
    )

    health_subscription = eventbus.subscription.health()

    logging.info(
        f"Resolved health events subscription: {id(health_subscription)} for {health_subscription._stream_name}"
    )

    meals.repository()
    meals_event_handler = "handler"

    try:
        logging.info("Start handling incoming events")

        await asyncio.gather(
            handle_events(
                meals_subscription, meals_event_handler
            ),
            handle_events(
                health_subscription, meals_event_handler
            ),
        )

    except KeyboardInterrupt:
        logging.error("Application interrupted by keyboard.")

    except Exception as e:
        logging.error(f"Error in main loop: {e}")

    finally:
        STOP_EVENT.set()

        logging.info(
            f"Stopped asyncio event {id(STOP_EVENT)}: {STOP_EVENT.is_set()}"
        )
        await asyncio.sleep(0.25)

        event_bus_client.close()

        logging.info(
            f"Closed event bus client {id(event_bus_client)}: {event_bus_client.is_closed}"
        )

        meals.repository().close()


def start():
    logger.info(
        f"\nStarting setup with config:\n{FORMATTED_CONFIG}\n"
    )

    app = AppContainer(config=CONFIG)
    app.init_resources()
    app.wire(modules=[__name__])
    app.check_dependencies()

    logging.info(f"AppContainer set up: {id(app)}")

    # Set up signals that stops the event loop in case of a container/pod shutdown
    sigint_handler = signal(
        SIGINT, lambda x: STOP_EVENT.set()
    )
    sigterm_handler = signal(
        SIGTERM, lambda x: STOP_EVENT.set()
    )

    logging.info(
        f"Shutdown signals for container shutdowns set up: {id(sigint_handler)}, {id(sigterm_handler)}"
    )

    logging.info(
        f"Stopped asyncio event {id(STOP_EVENT)}: {STOP_EVENT.is_set()}"
    )

    asyncio.run(main())


if __name__ == "__main__":
    start()

# async def event_listener():
#     esdb_client = EventStoreDBClient(uri=EVENTSTORE)
#     meals_subscription = esdb_client.subscribe_to_stream(
#         stream_name="stream_one", from_end=True
#     )

#     while True:
#         for i, event in enumerate(meals_subscription):
#             data = event.data.decode("utf-8")
#             meal = Meal.model_validate_json(data)
#             print("type: ", event.type)

#             if event.type == "InsertMeal":
#                 MealsEventHandler.handle_insert_event()
#                 statement, args = MealMutations.insert_meal(
#                     meal=meal
#                 )

#                 MealTasks.insert_meal.send(
#                     statement=statement,
#                     args=args,
#                 )

#                 await asyncio.sleep(0.1)

#         print("-----------------------------> Committed \n")

#         print("-----------------------------> Committed \n")
