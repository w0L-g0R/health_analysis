from enum import Enum
from typing import List, Optional, Tuple, Union

from pydantic import (
    AmqpDsn,
    BaseModel,
    Field,
    PostgresDsn,
    field_validator,
    model_validator,
    validator,
)
from pydantic_core import MultiHostUrl


class ConnectionStringMissingParameterError(ValueError):
    def __init__(self, missing_params: List[str], database: str):
        super().__init__(
            f"Missing following parameters of {database} connection string: {', '.join(missing_params)}"
        )


# class BaseConnectionString(BaseModel):
#     host: str
#     port: Union[int, str]

#     @staticmethod
#     def check_missing_params(values, params):
#         missing_params = [
#             param for param in params if param not in values or not values[param]
#         ]
#         return missing_params


class TimescaleDBCredentials(BaseModel):
    user: str
    password: str
    host: str
    port: Union[int, str]
    uri: PostgresDsn | None = Field(default=None, validate_default=False)

    # @property
    # def dsn(self):
    #     uri = MultiHostUrl(
    #         f"postgres://{self.user}:{self.password}@{self.host}:{self.port}"
    #     )
    #     return uri.__str__()

    @validator("uri", pre=True, always=True)
    def validate_uri(cls, value, values):
        # If the value is None, construct the DSN using the user inputs
        if value is None:
            dsn = f"postgres://{values['user']}:{values['password']}@{values['host']}:{values['port']}"
            # Pydantic will automatically validate if this is a correct PostgresDsn
            return dsn
        return value

    # @field_validator("dsn", mode="before")
    # def assemble_dsn(cls, v, values):
    #     return v or f"postgres://{values['user']}:{values['password']}@{values['host']}:{values['port']}"

    # @validator("dsn", pre=True, always=True)
    # def assemble_dsn(cls, v, values):
    #     return (
    #         v
    #         or f"postgres://{values['user']}:{values['password']}@{values['host']}:{values['port']}"
    #     )


# class TimescaleDBConnectionString(BaseModel):
#     uri: PostgresDsn

# @field_validator("uri")
# def validate_uri(self, v):
#     assert v.path and len(v.path) > 1, "database must be provided"


# class EventStoreDBConnectionString(BaseConnectionString):
#     query_params: Optional[List[Tuple[str, str]]] = Field(default=None)
#     uri: Optional[str] = Field(default=None)

#     @field_validator("uri")
#     @classmethod
#     def resolve(cls, values):
#         if not values.query_params:
#             raise ConnectionStringMissingParameterError(
#                 missing_params=["query_params"],
#                 database="eventstore_db",
#             )

#         tls_value = next(
#             (v for k, v in values.query_params if k == "tls"), "false"
#         ).lower()
#         connection_string = f"esdb://{values['host']}:{values['port']}?tls={tls_value}"

#         if tls_value == "true":
#             missing_params = cls.check_missing_params(
#                 values, ["user", "password", "host", "port"]
#             )
#             if not missing_params:
#                 connection_string = f"esdb://{values['user']}:{values['password']}@{values['host']}:{values['port']}?tls=true"
#         else:
#             missing_params = cls.check_missing_params(values, ["host", "port"])

#         if missing_params:
#             raise ConnectionStringMissingParameterError(
#                 missing_params=missing_params,
#                 database="eventstore_db",
#             )

#         return connection_string


# class RabbitMQConnectionString(BaseConnectionString):
#     user: Optional[str]
#     password: Optional[str]
#     uri: Optional[AmqpDsn] = Field(validate_default=True, default=None)

#     @field_validator("uri", mode="before")
#     @classmethod
#     def resolve(cls, values):
#         missing_params = cls.check_missing_params(
#             values, ["user", "password", "host", "port"]
#         )
#         if missing_params:
#             raise ConnectionStringMissingParameterError(
#                 missing_params=missing_params,
#                 database="rabbit_mq",
#             )
#         return f"amqp://{values['user']}:{values['password']}@{values['host']}:{values['port']}"
