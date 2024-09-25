from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class MealDeleteEvent(BaseModel):
    meal_id: UUID = Field(default_factory=uuid4)
    user_id: UUID = Field(default_factory=uuid4)

    class Config:
        frozen = True
