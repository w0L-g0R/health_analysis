from collections.abc import Awaitable
from pprint import pformat

from asyncpg import connect, Connection
from dependency_injector.resources import AsyncResource


class TimeScaleDbConnection(AsyncResource):

    async def init(
        self, connection_string: str, database: str
    ) -> Awaitable[Connection]:
        return await connect(dsn="/".join([connection_string, database]))

    async def shutdown(self, connection) -> None:
        await connection.close()
