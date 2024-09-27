from pydantic import BaseModel, ConfigDict


class FieldValidator(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
