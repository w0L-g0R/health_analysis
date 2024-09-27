from src.config.field_validator import FieldValidator


class MealMutationResult:
    def to_message(self) -> str:
        raise NotImplementedError()


class SuccessfullyAddedMeal(FieldValidator, MealMutationResult):
    meal_id: str
