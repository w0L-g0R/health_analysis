from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class DeleteMealEvent(BaseModel):
    meal_id: UUID = Field(default_factory=uuid4, frozen=True)
    user_id: UUID = Field(default_factory=uuid4, frozen=True)