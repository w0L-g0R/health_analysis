from datetime import date
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel

# class Department(Enum):
#     HR = "HR"
#     SALES = "SALES"
#     IT = "IT"
#     ENGINEERING = "ENGINEERING"

class Meal(BaseModel):
    meal_id: UUID
    user_id: UUID
    meal_name: str
    calories: float