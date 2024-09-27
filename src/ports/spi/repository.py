from abc import ABC


class Repository(ABC):

    async def add(self, data: str):
        raise NotImplementedError()

    async def delete(self, data: str):
        raise NotImplementedError()

    async def update(self, data: str):
        raise NotImplementedError()

    # async def get(self, data: str):
    #     raise NotImplementedError()
