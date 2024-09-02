from datetime import datetime
import logging
from typing import Any, Dict
from dramatiq import Actor
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from esdbclient import RecordedEvent
from pydantic import ValidationError

from api.meals.insert.event import MealInsertEvent
from api.meals.insert.query import MealInsertQuery
from api.meals.repository import MealsRepository


class MealInsertEventHandler:
    def __init__(
        self,
        config: dict,
        broker: RabbitmqBroker,
        event_class: type[MealInsertEvent],
        repository: MealsRepository,
        query_factory: MealInsertQuery,
    ):
        self.event_class = event_class
        self.queue_name = config["queues"]["meals"]["insert"]
        self.repository = repository
        self.query_factory = query_factory

        actor = Actor(
            fn=self.handle,
            actor_name=MealInsertEventHandler.__name__,
            queue_name=self.queue_name,
            broker=broker,
            priority=10,
            options={},
        )

        broker.declare_actor(actor)
        print("broker.get_declared_actors(): ", broker.get_declared_actors())

        pass

    async def handle(self, event: RecordedEvent):
        data = self.event_model.model_validate_json(event.data)

        query, args = self.query_factory(
            time=data.time,
            meal_id=data.meal_id,
            user_id=data.user_id,
            meal_name=data.meal_name,
            calories=data.meal_name,
        )

        self.repository.execute(query, args)

        # Map event data to SQL args
        # Pipeline
        ##  Insert via Repo
        ##  Send Notification via Kafka to Notification Service
        # print(f"Handling event in queue {self.queue_name}: {event}")

        return
