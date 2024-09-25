class BrokerError(Exception):
    """Base class for all broker-related exceptions."""

    pass


class BrokerStartupError(BrokerError):
    """Raised when there is an error during broker startup."""

    pass


class BrokerRuntimeError(BrokerError):
    """Raised when a runtime error occurs in the broker."""

    pass


class BrokerShutdownError(BrokerError):
    """Raised when there is an error during broker shutdown."""

    pass


class InvalidExchangeNameError(Exception):
    def __init__(self, message="Exchange_name must not be None or empty"):
        self.message = message
        super().__init__(self.message)
