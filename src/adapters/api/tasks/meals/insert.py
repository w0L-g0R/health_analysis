from dataclasses import dataclass
from src.application.domain.meals.models.insert.event import MealInsertEvent
from src.application.domain.meals.models.insert.model import MealInsertModel
from src.application.domain.meals.models.insert.query import MealInsertQuery
from src.ports.spi.persistence.repository import Repository
from src.ports.use_cases.meals.delete_meal import MealDeleteUseCase
from src.ports.use_cases.meals.insert_meal import MealInsertUseCase

@dataclass
class MealInsertService(MealDeleteUseCase):
    repository: Repository
    model: MealInsertModel
    use_case: MealInsertUseCase
    event: MealInsertEvent
    query: MealInsertQuery


    async def insert_meal(self, incoming_event_data: bytes):
        decoded_event = incoming_event_data.decode("utf-8")

        validated_event = self.event.model_validate(decoded_event)

        entity = self.model(
            meal_id=validated_event.meal_id,
            user_id=validated_event.user_id,
            calories=validated_event.calories,
            meal_name=validated_event.meal_name,
        )
        
        query_args = entity.model_dump.values()

        await self.repository.insert(tuple(query_args))
