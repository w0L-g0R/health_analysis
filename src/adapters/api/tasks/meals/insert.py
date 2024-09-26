from typing import Callable

from src.adapters.spi.persistence.time_scale_db.queries.meals import MealInsertQuery
from src.domain.events.meals.insert import MealInsertEvent
from src.domain.models.meals.insert import MealInsertModel
from src.ports.api.tasks.meals.insert import TaskInsert
from src.ports.spi.persistence.repository import Repository


class MealInsertTask(TaskInsert):
    repository: Repository
    model: Callable[..., MealInsertModel]
    event: Callable[..., MealInsertEvent]
    query: MealInsertQuery

    async def insert(self, incoming_event_data: bytes):
        decoded_event = incoming_event_data.decode("utf-8")

        validated_event = self.event.model_validate(decoded_event)

        entity = self.model(
            meal_id=validated_event.meal_id,
            user_id=validated_event.user_id,
            calories=validated_event.calories,
            meal_name=validated_event.meal_name,
        )

        query_args = entity.model_dump().values()

        await self.repository.insert(tuple(query_args))
