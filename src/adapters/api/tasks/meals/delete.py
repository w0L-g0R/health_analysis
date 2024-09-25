from src.application.domain.meals.models.delete.event import MealDeleteEvent
from src.application.domain.meals.models.delete.model import MealDeleteModel
from src.application.domain.meals.models.delete.query import MealDeleteQuery
from src.ports.spi.persistence.repository import Repository
from src.ports.api.tasks.meals.delete import TaskDelete


class MealDeleteTask(TaskDelete):
    repository: Repository
    model: MealDeleteModel
    event: MealDeleteEvent
    query: MealDeleteQuery

    async def delete(self, incoming_event_data: bytes):
        decoded_event = incoming_event_data.decode("utf-8")

        validated_event = self.event.model_validate(decoded_event)

        entity = self.model(
            meal_id=validated_event.meal_id,
            user_id=validated_event.user_id,
        )

        query_args = entity.model_dump.values()

        await self.repository.delete(tuple(query_args))
