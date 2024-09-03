from datetime import datetime, timezone
from dramatiq import Actor, Message, actor
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from esdbclient import RecordedEvent

from api.meals.insert.event import MealInsertEvent
from api.meals.insert.query import MealInsertQuery
from api.meals.repository import MealsRepository


@actor(queue_name="meals")
def _process(event_data):
    print("event_data: ", event_data)
    # _ = self.event_class.model_validate(event_data)

    # statement, args = self.query.insert_meal(
    #     time=datetime.now(timezone.utc),
    #     meal_id=_.meal_id,
    #     user_id=_.user_id,
    #     meal_name=_.meal_name,
    #     calories=_.calories,
    # )


class MealInsertEventHandler:
    def __init__(
        self,
        config: dict,
        broker: RabbitmqBroker,
        actor: Actor,
        event_class: type[MealInsertEvent],
        repository: MealsRepository,
        query: MealInsertQuery,
    ):
        self.event_class = event_class
        self.repository = repository
        self.query = query

        # actor.fn = self.process
        # actor.actor_name = MealInsertEventHandler.__name__
        # actor.queue_name = config["queues"]["meals"]["insert"]

        # broker.declare_actor(actor)

    def process(self, event_data):
        _process.send(event_data)

        # await self.repository.execute(statement, args)
