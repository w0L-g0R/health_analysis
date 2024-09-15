from datetime import datetime
from enum import Enum
from uuid import UUID

from pydantic import BaseModel, Field


from datetime import timezone


class InsertMealQuery(BaseModel):
    time: datetime
    meal_id: UUID
    user_id: UUID
    table: str
    meal_name: str = Field(min_length=3)
    calories: float = Field(gt=0)

    @property
    def statement(self) -> str:
        return """
            INSERT INTO meals (time, meal_id, user_id, meal_name, calories)
            VALUES ($1, $2, $3, $4, $5)
        """

    @property
    def args(self) -> tuple:
        return tuple(
            self.model_dump(
                exclude={"table", "statement"}
            ).values()
        )

    class Config:
        frozen = True
