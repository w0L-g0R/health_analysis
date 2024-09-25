from uuid import UUID

from pydantic import BaseModel, Field

class MealInsertModel(BaseModel):
    meal_id: UUID
    user_id: UUID
    meal_name: str = Field(min_length=3)
    calories: float = Field(gt=0)
    
    class Config:
        frozen = True