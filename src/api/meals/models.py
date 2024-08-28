from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Meal(BaseModel):
    time: datetime = Field(frozen=True)
    meal_id: UUID = Field(frozen=True)
    user_id: UUID = Field(frozen=True)
    meal_name: str = Field(min_length=3, frozen=True)
    calories: float = Field(gt=0, frozen=True)

    # @property
    # def args(self, meal: Meal) -> InsertMealReturn:
    #     return (
    #         datetime.now(timezone.utc).isoformat(),
    #         str(meal.meal_id),
    #         str(meal.user_id),
    #         str(meal.meal_name),
    #         str(meal.calories),
    #     )
