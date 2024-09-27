from typing import Callable

from pydantic import validate_call

from src.adapters.spi.persistence.health.queries.meals import MealDeleteQuery
from src.config.field_validator import FieldValidator
from src._LEGACY.meal_repository import Repository


class RemoveMealTask(
    FieldValidator,
    RemoveMealUseCase,
):

    repository: Repository
    model: Callable[..., MealModel]
    event: Callable[..., RemoveMealDto]
    query: MealDeleteQuery

    @validate_call
    async def delete(self, incoming_event_data: bytes):
        decoded_event = incoming_event_data.decode("utf-8")

        validated_event = self.event.model_validate(decoded_event)

        entity = self.model(
            meal_id=validated_event.meal_id,
            user_id=validated_event.user_id,
        )

        query_args = entity.model_dump().values()

        await self.repository.delete(tuple(query_args))
