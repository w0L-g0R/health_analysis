import logging
from dramatiq import Actor
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from esdbclient import RecordedEvent
from pydantic import ValidationError

from api.meals.insert.event import MealInsertEvent


class MealInsertEventHandler:
    def __init__(
        self,
        config: dict,
        broker: RabbitmqBroker,
        # timescale_db_record_factory: Provider[MealInsertModel],
        event_class: type[MealInsertEvent],
    ):
        self.event_class = event_class
        print("self.event_class: ", self.event_class)
        self.queue_name = config["queues"]["meals"]["insert"]

        # actor = Actor(
        #     fn=self.handle,
        #     actor_name=MealInsertEventHandler.__name__,
        #     queue_name=self.queue_name,
        #     broker=broker,
        #     priority=10,
        #     options={},
        # )

        # broker.declare_actor(actor)
        # print("broker.get_declared_actors(): ", broker.get_declared_actors())

        pass

    async def handle(self, event: RecordedEvent):
        # Validate & Deserialize
        event_data: MealInsertEvent = self.validate_and_deserialize_json_data(
            event_model=self.event_class, event=event
        )

        # event_data = event.data.decode("utf-8")
        print("event_data: ", event_data.calories)

        # Map event data to SQL args
        # Pipeline
        ##  Insert via Repo
        ##  Send Notification via Kafka to Notification Service
        # print(f"Handling event in queue {self.queue_name}: {event}")
        return

    def validate_and_deserialize_json_data(
        self, event_model: MealInsertEvent, event: RecordedEvent
    ) -> MealInsertEvent:
        try:
            return event_model.model_validate_json(event.data)

        except ValidationError as e:
            logging.error(f"Validation failed: {e}")
            raise
