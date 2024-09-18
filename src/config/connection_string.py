from enum import Enum
from typing import Any, List, Optional, Self, Tuple, Union

from pydantic import (
    AmqpDsn,
    BaseModel,
    Field,
    PostgresDsn,
    computed_field,
    field_validator,
    model_validator,
    validator,
)
from pydantic_core import MultiHostUrl, PydanticCustomError


CONNECTION_STRING_MISSING_PARAMETER_ERROR = PydanticCustomError(
    "UriInArgsErro",
    'Argument "uri" gets set after model validation and shoud not be passed on init!',
)


class ConnectionStringTimescaleDb(BaseModel):
    user: str
    password: str
    host: str
    port: Union[int, str] = Field(coerce_numbers_to_str=True)
    uri: Optional[PostgresDsn] = Field(
        default=None, validate_default=False
    )

    @computed_field(return_type=str)
    @property
    def dns(self):
        return str(self.uri)

    @model_validator(mode="before")
    @classmethod
    def check_uri_omitted(cls, data: Any) -> Any:
        if isinstance(data, dict):
            assert (
                "uri" not in data
            ), CONNECTION_STRING_MISSING_PARAMETER_ERROR
        return data

    @model_validator(mode="after")
    def create_uri(self) -> Self:
        if (
            self.user is not None
            and self.password is not None
            and self.host is not None
            and self.port is not None
        ):
            self.uri = MultiHostUrl.build(
                scheme="postgres",
                username=self.user,
                password=self.password,
                host=self.host,
                port=int(self.port),
            )
        else:
            raise ValueError("passwords do not match")
        return self

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
