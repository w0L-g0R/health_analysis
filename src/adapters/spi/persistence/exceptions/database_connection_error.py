from typing import Any
from functools import wraps


class DatabaseStartConnectionError(Exception):
    def __init__(self, connection_string: str, database: str):
        self.message = f"""Error initializing database connection:
            Connection string: {connection_string}
            Database: {database}"""
        super().__init__(self.message)


def handle_start_connection_error(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except Exception as error:
            raise DatabaseStartConnectionError(
                connection_string=args[0], database=args[1]
            ) from error

    return wrapper


class DatabaseQueryError(Exception):
    def __init__(
        self, connection: str, database: str, query: str, args=tuple[Any, ...]
    ):
        self.message = f"""Error executing: 
                Query: {query}  
                Args: {list(*args)}:
                Connection: {connection}
                Database: {database}"""
        super().__init__(self.message)


def handle_query_error(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except Exception as error:
            raise DatabaseQueryError(
                connection=str(self._connection),
                database=self._database,
                query=getattr(self, f"_{func.__name__}_query"),
                args=args,
            ) from error

    return wrapper


class DatabaseCloseConnectionError(Exception):
    def __init__(self, connection: str, database: str):
        self.message = f"""Error closing database connection: 
                Connection: {connection}
                Database: {database}"""
        super().__init__(self.message)


def handle_close_connection_error(func):
    @wraps(func)
    async def wrapper(self, *args, **kwargs):
        try:
            return await func(self, *args, **kwargs)
        except Exception as error:
            raise DatabaseCloseConnectionError(
                connection=str(self._connection),
                database=self._database,
            ) from error

    return wrapper
