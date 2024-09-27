from abc import ABC


class Queries(ABC):

    @staticmethod
    def add() -> str:
        raise NotImplementedError()

    @staticmethod
    def delete() -> str:
        raise NotImplementedError()

    @staticmethod
    def update() -> str:
        raise NotImplementedError()
