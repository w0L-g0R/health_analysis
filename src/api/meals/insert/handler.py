from dramatiq import Actor
from dramatiq.brokers.rabbitmq import RabbitmqBroker
from esdbclient import RecordedEvent

from api.meals.insert.event import MealInsertEvent
from api.meals.insert.query import MealInsertQuery
from api.meals.repository import MealsRepository


class MealInsertEventHandler:
    def __init__(
        self,
        config: dict,
        broker: RabbitmqBroker,
        actor: Actor,
        event_class: type[MealInsertEvent],
        repository: MealsRepository,
        sql_statement: MealInsertQuery,
    ):
        self.event_class = event_class
        self.repository = repository
        self.sql_statement = sql_statement

        actor.fn = self.handle
        actor.actor_name = MealInsertEventHandler.__name__
        actor.queue_name = config["queues"]["meals"]["insert"]

        broker.declare_actor(actor)
        print("broker.get_declared_actors(): ", broker.get_declared_actors())

        pass

    async def handle(self, event: RecordedEvent):
        data = self.event_class.model_validate_json(event.data)

        self.repository.execute(
            self.sql_statement(
                time=data.time,
                meal_id=data.meal_id,
                user_id=data.user_id,
                meal_name=data.meal_name,
                calories=data.meal_name,
            )
        )
