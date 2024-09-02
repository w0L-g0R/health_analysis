from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class Meal(BaseModel):
    time: datetime
    meal_id: UUID
    user_id: UUID
    meal_name: str = Field(min_length=3)
    calories: float = Field(gt=0, frozen=True)

    # @property
    # # def args(self) -> MealInsertArgs:
    # def args(self):
    #     return (
    #         datetime.now(timezone.utc).isoformat(),
    #         str(self.meal_id),
    #         str(self.user_id),
    #         str(self.meal_name),
    #         str(self.calories),
    #     )
