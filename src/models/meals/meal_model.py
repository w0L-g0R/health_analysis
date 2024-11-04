from typing import Any, Dict, Optional
from uuid import UUID
from pydantic import Field
from src.config.field_validator import FieldValidator


class Meal(FieldValidator):
    meal_id: UUID
    user_id: UUID
    meal_data: Optional[str] = Field(default=None)

    class Config:
        frozen = True
