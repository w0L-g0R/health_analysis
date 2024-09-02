from datetime import datetime, timezone
from uuid import UUID

from pydantic import BaseModel, Field


class MealInsertModel(BaseModel):
    time: datetime = Field(default_factory=datetime.now(timezone.utc))
    meal_id: UUID
    user_id: UUID
    meal_name: str = Field(min_length=3)
    calories: float = Field(gt=0)

    class Config:
        frozen = True

    @property
    def args(self):
        return (
            self.time,
            self.meal_id,
            self.user_id,
            self.meal_name,
            self.calories,
        )
