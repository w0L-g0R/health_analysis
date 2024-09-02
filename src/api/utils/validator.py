import json
from typing import Type
from pydantic import BaseModel, ValidationError


class Validator:
    def validate(self, data: json, model: Type) -> Type:
        """
        Validate the provided data against the given Pydantic model.

        :param data: The data to be validated (as a dictionary).
        :param model: The Pydantic model to validate against.
        :return: An instance of the validated model.
        :raises ValidationError: If validation fails.
        """
        try:
            validated_data = model.model_validate_json(data)
            return validated_data

        except ValidationError as e:
            print(f"Validation failed: {e}")
            raise
