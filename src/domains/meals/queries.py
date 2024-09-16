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

    # def create(self, from_event: InsertMealEvent) -> InsertMealQuery:
    #     return InsertMealQuery(
    #         time=datetime.now(tz=timezone.utc),
    #         meal_id=from_event.meal_id,
    #         user_id=from_event.user_id,
    #         meal_name=from_event.meal_name,
    #         calories=from_event.calories,
    #         table=self.table_name,
    #     )

    @property
    def statement(self) -> str:
        return """
            INSERT INTO meals (time, meal_id, user_id, meal_name, calories)
            VALUES ($1, $2, $3, $4, $5)
        """

    @property
    def args(self) -> tuple:
        return tuple(self.model_dump(exclude={"table", "statement"}).values())

    class Config:
        frozen = True
