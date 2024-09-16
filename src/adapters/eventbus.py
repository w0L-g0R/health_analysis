import logging
from pprint import pformat
from esdbclient import EventStoreDBClient

from src.abstractions.handler import EventHandler
from src.config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


class EventBus(EventStoreDBClient):
    def __init__(self, uri: str, stream: str, from_end: bool, handler: EventHandler):
        super().__init__(uri)
        self.stream = stream
        self.from_end = from_end
        self.handler = handler

    async def listen_to_subscription_events(self, broker):
        subscription = self.subscribe_to_stream(self.stream)

        try:
            for event in subscription:
                logger.info(
                    f"Received event from subscription {id(subscription)}:\n{pformat(event, indent=2)}"
                )

                await self.handler.handle(event)

                match event.type:
                    case "MealInsert":
                        # await insert_event_handler.validate_and_serialize(event)
                        # insert_event_handler.process(event.data.decode("utf-8"))
                        # process_insert_meal_event.send(
                        #     event.data.decode("utf-8"),
                        # )
                        pass
                        # process(event.data.decode("utf-8"))
                    case _:
                        print("No matching type")

            # Prevent CPU overuse
            # await asyncio.sleep(0.1)

        except Exception as e:
            logger.error(f"Error in handle_events:{e}")
            raise e

        finally:
            if subscription:
                subscription.stop()
