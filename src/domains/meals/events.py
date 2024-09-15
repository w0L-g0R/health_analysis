from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class InsertMealEvent(BaseModel):
    meal_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    meal_name: str = Field(min_length=3)
    calories: float = Field(gt=0)

    class Config:
        frozen = True


class DeleteMealEvent(BaseModel):
    meal_id: UUID = Field(default_factory=uuid4, frozen=True)
    user_id: UUID = Field(default_factory=uuid4, frozen=True)

    class Config:
        frozen = True


class MealEvents(Enum):
    INSERT = InsertMealEvent.__name__
    DELETE = DeleteMealEvent.__name__
