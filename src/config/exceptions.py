from enum import Enum


class EmptyValueErrorMessages(str, Enum):
    PORTS = "Empty value found in ports:"
    EVENTS = "Empty value found in events:"


class InvalidConfigurationError(ValueError):
    pass


class EmptyValueError(ValueError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
