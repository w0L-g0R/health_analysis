from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Meal(BaseModel):
    meal_id: UUID = Field(default_factory=uuid4, frozen=True)
    user_id: UUID = Field(default_factory=uuid4, frozen=True)
    meal_name: str = Field(min_length=3, frozen=True)
    calories: float = Field(gt=0, frozen=True)
