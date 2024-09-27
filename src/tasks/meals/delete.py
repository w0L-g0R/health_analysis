from typing import Callable


from src.adapters.spi.persistence.time_scale_db.queries.meals import MealDeleteQuery
from src.config.field_validator import FieldValidator
from src.domain.events.meals.delete import MealDeleteEvent
from src.domain.models.meals.insert import MealInsertModel
from src.ports.spi.tasks.meals.delete import TaskDelete
from src.ports.spi.persistence.repository import Repository


class MealDeleteTask(TaskDelete, FieldValidator):

    repository: Repository
    model: Callable[..., MealInsertModel]
    event: Callable[..., MealDeleteEvent]
    query: MealDeleteQuery

    async def delete(self, incoming_event_data: bytes):
        decoded_event = incoming_event_data.decode("utf-8")

        validated_event = self.event.model_validate(decoded_event)

        entity = self.model(
            meal_id=validated_event.meal_id,
            user_id=validated_event.user_id,
        )

        query_args = entity.model_dump().values()

        await self.repository.delete(tuple(query_args))
