from enum import Enum


class EmptyValueErrorMessages(str, Enum):
    STREAMS = "Empty value found in ports:"
    QUEUES = "Empty value found in queues:"
    EXCHANGES = "Empty value found in exchanges:"
    EVENTS = "Empty value found in events:"
    DATABASES = "Empty value found in databases:"


class InvalidConfigurationError(ValueError):
    pass


class EmptyValueError(ValueError):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
