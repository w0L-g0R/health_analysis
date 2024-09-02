from dramatiq import Actor
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from esdbclient import RecordedEvent

from api.utils.validator import Validator


class MealInsertEventHandler:
    def __init__(self, config: dict, broker: RabbitmqBroker, validator: Validator):
        self.queue_name = config["queues"]["meals"]["insert"]

        actor = Actor(
            fn=self.handle,
            actor_name=MealInsertEventHandler.__name__,
            queue_name=self.queue_name,
            broker=broker,
            priority=10,
            options={},
        )

        broker.declare_actor(actor)

        pass

    def handle(self, event: RecordedEvent):
        # Encode
        event_data = event.data.decode("utf-8")

        print("event_data: ", event_data)

        # Validate
        # Map event data to SQL args
        # Pipeline
        ##  Insert via Repo
        ##  Send Notification via Kafka to Notification Service
        # print(f"Handling event in queue {self.queue_name}: {event}")
        return
