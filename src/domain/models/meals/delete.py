from uuid import UUID
from pydantic import BaseModel

class MealDeleteModel(BaseModel):
    meal_id: UUID
    user_id: UUID

    class Config:
        frozen = True